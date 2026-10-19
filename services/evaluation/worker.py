"""Evaluation worker (FR-19, design §19, §38).

Reads jobs off the durable queue and runs them. Runs in-process here because the
whole deployment is one machine (claude.md "Deployment — LOCAL ONLY"); nothing
about it assumes that, so moving it to its own process is a matter of running
`run_worker` from a separate entry point.

Alongside draining the queue it runs a **reconciliation sweep**. The job row is
written to Postgres and the queue message is published separately, which means
the two can disagree — a Redis restart between them would otherwise strand a
session in EVALUATING forever. The sweep re-enqueues anything the queue has
lost, which makes the durable row the authority and the queue merely the fast
path.
"""

import asyncio
import logging
import socket
import uuid
from datetime import timedelta

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from services.common.db import SessionFactory
from services.common.timeutil import as_utc, utcnow
from services.evaluation import queue, service
from services.evaluation import repository as repo
from services.evaluation.models import EvaluationJob
from services.llm import QuotaExhausted
from services.session import repository as session_repo
from services.session.state import EvaluationState, SessionState, transition_evaluation

logger = logging.getLogger(__name__)

WORKER_INTERVAL_SECONDS = 5.0
# How long a job may sit QUEUED before the sweep assumes its queue message was
# lost and republishes it.
STALE_JOB_SECONDS = 120.0
# A job the worker runs again by itself (held up by the model allowance, or cut
# off by a restart) tries this many times in all, then stays FAILED with its
# message: a cap that never frees is a configuration fault, not bad luck.
MAX_AUTOMATIC_ATTEMPTS = 20
# A job in one of these states when the worker starts was cut off by a restart:
# one process runs the one worker, so nothing else can be writing it.
IN_PROGRESS = (
    EvaluationState.PREPARING,
    EvaluationState.RUNNING,
    EvaluationState.WAITING_FOR_AGENT,
    EvaluationState.AGGREGATING,
    EvaluationState.REPORT_GENERATING,
)

CONSUMER_NAME = f"{socket.gethostname()}-{uuid.uuid4().hex[:8]}"


async def sweep(session: AsyncSession) -> int:
    """Create jobs for ended sessions and re-enqueue stale ones."""
    created = 0

    for gd in await session_repo.list_sessions_in_state(session, SessionState.ENDED):
        await service.request_evaluation(session, gd)
        created += 1

    cutoff = utcnow().timestamp() - STALE_JOB_SECONDS
    result = await session.execute(
        select(EvaluationJob).where(EvaluationJob.state == str(EvaluationState.QUEUED))
    )
    for job in result.scalars():
        if as_utc(job.queued_at).timestamp() > cutoff:
            continue
        gd = await session_repo.get_session_by_id(session, job.session_id)
        if gd is None:
            continue
        participants = await session_repo.list_active_participants(session, gd.id)
        await queue.enqueue(
            service.to_contract(job, gd.topic, [p.candidate_label for p in participants])
        )
        logger.info("re-enqueued stale evaluation job", extra={"job_id": str(job.id)})

    # Jobs held up by the model allowance, once it is due back: queued again, and
    # each attempt that finds it still spent fails fast and waits again.
    result = await session.execute(
        select(EvaluationJob).where(
            EvaluationJob.state == str(EvaluationState.FAILED),
            EvaluationJob.retry_after.is_not(None),
        )
    )
    for job in result.scalars():
        if as_utc(job.retry_after) > utcnow() or job.attempts >= MAX_AUTOMATIC_ATTEMPTS:
            continue
        gd = await session_repo.get_session_by_id(session, job.session_id)
        if gd is None:
            continue
        job.state = str(transition_evaluation(EvaluationState.FAILED, EvaluationState.QUEUED))
        job.retry_after = None
        job.queued_at = utcnow()
        await session.flush()
        participants = await session_repo.list_active_participants(session, gd.id)
        await queue.enqueue(
            service.to_contract(job, gd.topic, [p.candidate_label for p in participants])
        )
        logger.info("evaluation job runs again: allowance due back", extra={"job_id": str(job.id)})

    return created


async def _run_queued(session: AsyncSession, queued: queue.QueuedJob) -> bool:
    """Run one dequeued job. Returns True on success."""
    job = await repo.get_job_for_version(
        session, uuid.UUID(queued.job.session_id), queued.job.evaluation_version
    )
    if job is None:
        logger.warning(
            "queue referenced an unknown job",
            extra={"session_id": queued.job.session_id, "version": queued.job.evaluation_version},
        )
        return True  # Nothing to do; ack it rather than retrying forever.

    if EvaluationState(job.state) is EvaluationState.COMPLETED:
        # Redelivery of an already-finished job (design §39): ack and move on.
        return True

    return await _run_job(session, job)


async def _run_job(session: AsyncSession, job: EvaluationJob) -> bool:
    """Run one job, recording a failure on a fresh session. True on success."""
    # Read before any rollback: a rollback expires the row, and touching an expired
    # attribute afterwards triggers a lazy load that async SQLAlchemy cannot do.
    job_id = job.id
    try:
        await service.run_job(session, job)
        await session.commit()
        return True
    except QuotaExhausted as exc:
        # Not a fault: the model allowance is spent. The job runs again when it is
        # back, and the student reads why their report is waiting.
        await session.rollback()
        async with SessionFactory() as fresh:
            failed = await repo.get_job(fresh, job_id)
            if failed is not None:
                await service.fail_job(
                    fresh,
                    failed,
                    "Today's AI allowance is used up, so your report is waiting. It will "
                    f"be written by itself in about {exc.minutes} min — this page updates.",
                    retry_after=utcnow() + timedelta(seconds=exc.retry_in),
                )
                await fresh.commit()
        logger.warning(
            "evaluation waits for model allowance",
            extra={"job_id": str(job_id), "retry_in": round(exc.retry_in)},
        )
        return False
    except Exception as exc:
        await session.rollback()
        async with SessionFactory() as fresh:
            failed = await repo.get_job(fresh, job_id)
            if failed is not None:
                await service.fail_job(fresh, failed, str(exc))
                await fresh.commit()
        logger.exception("evaluation job raised", extra={"job_id": str(job_id)})
        return False


async def drain(factory: async_sessionmaker[AsyncSession], *, block_ms: int = 1000) -> int:
    """Process whatever is currently on the queue. Returns jobs completed."""
    try:
        jobs = await queue.read(CONSUMER_NAME, count=1, block_ms=block_ms)
        jobs.extend(await queue.claim_stalled(CONSUMER_NAME))
    except Exception as exc:
        logger.debug("evaluation queue unavailable", extra={"error": str(exc)})
        return await drain_from_database(factory)

    completed = 0
    for queued in jobs:
        async with factory() as session:
            ok = await _run_queued(session, queued)
        if ok:
            await queue.ack(queued.message_id)
            completed += 1
        else:
            await queue.retry(queued, "worker run failed")
    return completed


async def drain_from_database(factory: async_sessionmaker[AsyncSession]) -> int:
    """Fallback when Redis is unreachable: run QUEUED jobs straight from the DB.

    The job row is the authority and the queue only the fast path (see the
    module docstring), so a missing queue degrades latency, never correctness.
    This is what lets the platform run with no Redis at all.

    ponytail: one worker, no claim/lock. Two workers without Redis could both
    pick the same job; the (session_id, evaluation_version) constraint keeps
    the result single, but it would be computed twice.
    """
    async with factory() as session:
        result = await session.execute(
            select(EvaluationJob.id).where(EvaluationJob.state == str(EvaluationState.QUEUED))
        )
        job_ids = list(result.scalars())

    completed = 0
    for job_id in job_ids:
        async with factory() as session:
            job = await repo.get_job(session, job_id)
            if job is None or EvaluationState(job.state) is not EvaluationState.QUEUED:
                continue
            if await _run_job(session, job):
                completed += 1
    return completed


async def recover_interrupted(factory: async_sessionmaker[AsyncSession]) -> int:
    """Jobs a restart cut off mid-report run again rather than stay RUNNING forever.

    Found on Day 5 (19 Oct): the server restarted during an evaluation and the
    report page said "analysing" for good. Each is failed with a sentence the
    student reads, due now, and the next sweep queues it again.
    """
    async with factory() as session:
        result = await session.execute(
            select(EvaluationJob).where(EvaluationJob.state.in_([str(s) for s in IN_PROGRESS]))
        )
        jobs = list(result.scalars())
        for job in jobs:
            await service.fail_job(
                session,
                job,
                "The server restarted while your report was being written. It is being "
                "written again now — this page updates.",
                retry_after=utcnow(),
            )
            logger.warning("evaluation job cut off by a restart", extra={"job_id": str(job.id)})
        await session.commit()
    return len(jobs)


async def run_worker(
    factory: async_sessionmaker[AsyncSession] | None = None,
    *,
    interval: float = WORKER_INTERVAL_SECONDS,
) -> None:
    """Long-running worker loop, started by the app lifespan."""
    factory = factory or SessionFactory
    logger.info("evaluation worker started", extra={"consumer": CONSUMER_NAME})
    try:
        await recover_interrupted(factory)
    except Exception as exc:
        logger.warning("could not recover interrupted jobs", extra={"error": str(exc)})
    while True:
        try:
            async with factory() as session:
                await sweep(session)
                await session.commit()
            await drain(factory)
        except asyncio.CancelledError:
            logger.info("evaluation worker stopped")
            raise
        except Exception as exc:
            logger.warning("evaluation worker tick failed", extra={"error": str(exc)})
        await asyncio.sleep(interval)
