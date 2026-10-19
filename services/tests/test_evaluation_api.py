"""Evaluation and report HTTP endpoints (FR-20, FR-30 – FR-32).

The pipeline itself is covered in `test_evaluation_pipeline.py`; this covers the
API surface over it — serialization, access control, and the states a client can
observe. The response shapes are tested because a working pipeline behind a
broken response model is still a broken feature.
"""

import uuid

import pytest
from httpx import AsyncClient

from services.session import repository as session_repo
from services.session import service as session_service
from services.session.models import Participant
from services.session.state import ParticipantState
from services.speech.service import persist_segment

SCRIPT = [
    ("A", 0, 25, "Regulation of generative AI is overdue and the cost of inaction is high."),
    ("B", 26, 40, "I disagree, that assumes regulators can move faster than the technology."),
    ("A", 41, 70, "B, that is fair, but who bears the cost of waiting?"),
    ("C", 72, 78, "Could we separate model training from deployment?"),
]


@pytest.fixture
async def evaluated(
    session_factory, client: AsyncClient, gd_session, host_auth, candidate_auth, second_candidate
):
    """A session run to COMPLETED, driven through the HTTP API."""
    session_id = uuid.UUID(gd_session["id"])
    for header in (candidate_auth, second_candidate):
        await client.post("/api/v1/lobbies/join", json={"code": gd_session["code"]}, headers=header)
        await client.post(
            f"/api/v1/lobbies/{session_id}/ready", json={"ready": True}, headers=header
        )
    await client.post(f"/api/v1/sessions/{session_id}/start", headers=host_auth)

    async with session_factory() as db:
        gd = await session_repo.get_session_by_id(db, session_id)
        await session_repo.add_participant(
            db,
            Participant(
                session_id=gd.id,
                user_id=gd.host_id,
                candidate_label="C",
                display_name="Third Candidate",
                state=str(ParticipantState.ACTIVE),
                is_ready=True,
            ),
        )
        for label, start, end, text in SCRIPT:
            await session_service.record_speech(db, gd, label, float(start), float(end))
            await persist_segment(db, gd.id, label, float(start), float(end), text, 0.92)
        await db.commit()

    ended = await client.post(f"/api/v1/sessions/{session_id}/end", headers=host_auth)
    assert ended.status_code == 200, ended.text
    return gd_session


async def test_evaluate_endpoint_returns_a_usable_status(client: AsyncClient, evaluated, host_auth):
    """Regression: the row's primary key is `id`, the wire field is `job_id`."""
    response = await client.post(
        f"/api/v1/sessions/{evaluated['id']}/evaluate?run_now=true", headers=host_auth
    )
    assert response.status_code == 200, response.text
    body = response.json()

    assert uuid.UUID(body["job_id"])
    assert body["session_id"] == evaluated["id"]
    assert body["state"] == "COMPLETED"
    assert body["evaluation_version"] == 1
    assert body["selected_agents"]
    # Design §40: the reproducibility triple is visible to the client.
    assert body["rubric_version"] and body["prompt_version"] and body["agent_version"]
    assert body["error"] is None


async def test_status_endpoint_matches_the_evaluate_response(
    client: AsyncClient, evaluated, host_auth
):
    created = await client.post(
        f"/api/v1/sessions/{evaluated['id']}/evaluate?run_now=true", headers=host_auth
    )
    fetched = await client.get(f"/api/v1/sessions/{evaluated['id']}/evaluation", headers=host_auth)
    assert fetched.status_code == 200, fetched.text
    assert fetched.json()["job_id"] == created.json()["job_id"]


async def test_status_is_404_before_any_evaluation(
    client: AsyncClient, gd_session, host_auth, candidate_auth
):
    await client.post(
        "/api/v1/lobbies/join", json={"code": gd_session["code"]}, headers=candidate_auth
    )
    response = await client.get(
        f"/api/v1/sessions/{gd_session['id']}/evaluation", headers=host_auth
    )
    assert response.status_code == 404


async def test_only_the_host_can_trigger_an_evaluation(
    client: AsyncClient, evaluated, candidate_auth
):
    response = await client.post(
        f"/api/v1/sessions/{evaluated['id']}/evaluate", headers=candidate_auth
    )
    assert response.status_code == 403


async def test_scores_endpoint_is_host_only(
    client: AsyncClient, evaluated, host_auth, candidate_auth
):
    await client.post(
        f"/api/v1/sessions/{evaluated['id']}/evaluate?run_now=true", headers=host_auth
    )

    allowed = await client.get(f"/api/v1/sessions/{evaluated['id']}/scores", headers=host_auth)
    assert allowed.status_code == 200
    assert len(allowed.json()) == 3
    for score in allowed.json():
        assert 0 <= score["overall"] <= 100
        assert score["weights"]

    refused = await client.get(f"/api/v1/sessions/{evaluated['id']}/scores", headers=candidate_auth)
    assert refused.status_code == 403


async def test_a_candidate_reads_their_own_report(
    client: AsyncClient, evaluated, host_auth, candidate_auth
):
    """FR-30."""
    await client.post(
        f"/api/v1/sessions/{evaluated['id']}/evaluate?run_now=true", headers=host_auth
    )
    response = await client.get(
        f"/api/v1/sessions/{evaluated['id']}/report", headers=candidate_auth
    )

    assert response.status_code == 200, response.text
    body = response.json()["body"]
    assert body["candidate_label"] == "A"
    assert body["dimensions"]
    assert body["metrics"]["speaking_seconds"] > 0
    assert body["feedback"]


async def test_a_candidate_cannot_read_another_candidates_report(
    client: AsyncClient, evaluated, host_auth, candidate_auth
):
    """NFR-07 privacy."""
    await client.post(
        f"/api/v1/sessions/{evaluated['id']}/evaluate?run_now=true", headers=host_auth
    )
    response = await client.get(
        f"/api/v1/sessions/{evaluated['id']}/report/B", headers=candidate_auth
    )
    assert response.status_code == 403


async def test_the_host_can_read_any_candidates_report(client: AsyncClient, evaluated, host_auth):
    await client.post(
        f"/api/v1/sessions/{evaluated['id']}/evaluate?run_now=true", headers=host_auth
    )
    response = await client.get(f"/api/v1/sessions/{evaluated['id']}/report/B", headers=host_auth)
    assert response.status_code == 200
    assert response.json()["body"]["candidate_label"] == "B"


async def test_the_group_report_is_host_only(
    client: AsyncClient, evaluated, host_auth, candidate_auth
):
    """Design §34 — it names who dominated and who did not speak."""
    await client.post(
        f"/api/v1/sessions/{evaluated['id']}/evaluate?run_now=true", headers=host_auth
    )

    allowed = await client.get(
        f"/api/v1/sessions/{evaluated['id']}/report/group", headers=host_auth
    )
    assert allowed.status_code == 200
    body = allowed.json()["body"]
    assert body["discussion_quality"] in {"high", "moderate", "low"}
    assert "participation" in body

    refused = await client.get(
        f"/api/v1/sessions/{evaluated['id']}/report/group", headers=candidate_auth
    )
    assert refused.status_code == 403


async def test_history_reflects_a_completed_session(
    client: AsyncClient, evaluated, host_auth, candidate_auth
):
    """FR-31."""
    await client.post(
        f"/api/v1/sessions/{evaluated['id']}/evaluate?run_now=true", headers=host_auth
    )
    response = await client.get("/api/v1/me/history", headers=candidate_auth)

    assert response.status_code == 200, response.text
    body = response.json()
    assert body["sessions_completed"] == 1
    assert body["average_overall"] is not None
    assert body["trend"]
    assert body["entries"][0]["session_id"] == evaluated["id"]


async def test_history_is_empty_for_a_new_candidate(client: AsyncClient, candidate_auth):
    response = await client.get("/api/v1/me/history", headers=candidate_auth)
    assert response.status_code == 200
    assert response.json() == {
        "sessions_completed": 0,
        "average_overall": None,
        "trend": {},
        "entries": [],
    }


async def test_metrics_endpoint_reports_the_deterministic_numbers(
    client: AsyncClient, evaluated, host_auth
):
    """FR-18 over HTTP."""
    response = await client.get(f"/api/v1/sessions/{evaluated['id']}/metrics", headers=host_auth)
    assert response.status_code == 200, response.text
    body = response.json()

    assert body["total_speaking_seconds"] > 0
    assert set(body["candidates"]) == {"A", "B", "C"}
    total = sum(c["participation_ratio"] for c in body["candidates"].values())
    assert total == pytest.approx(1.0, abs=0.01)
    # A spoke most in the script.
    assert "A" in body["dominant"]


async def test_evaluating_an_already_completed_session_is_idempotent(
    client: AsyncClient, evaluated, host_auth
):
    """The background worker and this endpoint race by design (design §39).

    Whichever arrives second must return the existing result, not fail on
    COMPLETED -> PREPARING. Caught live, where a worker is actually running.
    """
    first = await client.post(
        f"/api/v1/sessions/{evaluated['id']}/evaluate?run_now=true", headers=host_auth
    )
    assert first.status_code == 200, first.text
    assert first.json()["state"] == "COMPLETED"

    second = await client.post(
        f"/api/v1/sessions/{evaluated['id']}/evaluate?run_now=true", headers=host_auth
    )
    assert second.status_code == 200, second.text
    assert second.json()["job_id"] == first.json()["job_id"]
    assert second.json()["evaluation_version"] == 1


async def test_the_report_carries_a_synthesis_narrative(
    client: AsyncClient, evaluated, host_auth, candidate_auth
):
    """Design §20 Final Evaluator: narrative plus the tool calls behind it."""
    await client.post(
        f"/api/v1/sessions/{evaluated['id']}/evaluate?run_now=true", headers=host_auth
    )
    response = await client.get(
        f"/api/v1/sessions/{evaluated['id']}/report", headers=candidate_auth
    )

    synthesis = response.json()["body"]["synthesis"]
    assert synthesis["error"] is None
    assert synthesis["summary"]
    # The narrative was written by a model that read the score through a tool.
    assert [call["tool"] for call in synthesis["tool_calls"]] == [
        "compute_final_score",
        "score_if",
    ]
    # And it has nowhere to put a score of its own.
    assert "overall_score" not in synthesis


async def test_a_report_held_up_by_the_model_allowance_waits_then_runs_by_itself(
    session_factory, client: AsyncClient, evaluated, host_auth, monkeypatch
):
    """Day 5: at Groq's daily cap every agent failed and the report never came.

    The job now says why, in words a student reads, and the worker runs it again
    once the allowance is due back.
    """
    from datetime import timedelta

    from services.common.timeutil import utcnow
    from services.evaluation import queue, worker
    from services.evaluation import repository as eval_repo
    from services.evaluation import service as eval_service
    from services.llm import set_llm_provider
    from services.llm.stub_provider import StubLLM

    sid = evaluated["id"]
    url = f"/api/v1/sessions/{sid}/evaluation"
    await client.post(f"/api/v1/sessions/{sid}/evaluate", headers=host_auth)

    async def unreachable(*args, **kwargs):
        raise ConnectionError("redis is not running")

    monkeypatch.setattr(queue, "read", unreachable)
    monkeypatch.setattr(worker, "SessionFactory", session_factory)
    monkeypatch.setattr(eval_service, "allowance_back_in", lambda: 600.0)
    set_llm_provider(StubLLM(fail=True))
    try:
        assert await worker.drain(session_factory) == 0
        status = (await client.get(url, headers=host_auth)).json()
        assert status["state"] == "FAILED" and status["retry_after"]
        assert "allowance" in status["error"] and "about 10 min" in status["error"]

        async with session_factory() as db:  # not due yet: left alone
            await worker.sweep(db)
            await db.commit()
        assert (await client.get(url, headers=host_auth)).json()["state"] == "FAILED"

        async with session_factory() as db:  # due: queued again, and it runs
            job = await eval_repo.latest_job(db, uuid.UUID(sid))
            job.retry_after = utcnow() - timedelta(seconds=1)
            await db.commit()
        set_llm_provider(StubLLM())
        monkeypatch.setattr(eval_service, "allowance_back_in", lambda: None)
        async with session_factory() as db:
            await worker.sweep(db)
            await db.commit()
        assert await worker.drain(session_factory) == 1
        status = (await client.get(url, headers=host_auth)).json()
        assert status["state"] == "COMPLETED" and status["retry_after"] is None
    finally:
        set_llm_provider(StubLLM())


async def test_a_report_a_restart_cut_off_is_written_again_not_left_running(
    session_factory, client: AsyncClient, evaluated, host_auth, monkeypatch
):
    """Day 5: a restart mid-evaluation left the job RUNNING and the page "analysing"."""
    from services.evaluation import queue, worker
    from services.evaluation import repository as eval_repo
    from services.session.state import EvaluationState

    sid = evaluated["id"]
    url = f"/api/v1/sessions/{sid}/evaluation"
    await client.post(f"/api/v1/sessions/{sid}/evaluate", headers=host_auth)
    async with session_factory() as db:  # the process died here, mid-report
        job = await eval_repo.latest_job(db, uuid.UUID(sid))
        job.state = str(EvaluationState.RUNNING)
        await db.commit()

    assert await worker.recover_interrupted(session_factory) == 1
    status = (await client.get(url, headers=host_auth)).json()
    assert status["state"] == "FAILED" and "restarted" in status["error"]

    async def unreachable(*args, **kwargs):
        raise ConnectionError("redis is not running")

    monkeypatch.setattr(queue, "read", unreachable)
    async with session_factory() as db:
        await worker.sweep(db)
        await db.commit()
    assert await worker.drain(session_factory) == 1
    assert (await client.get(url, headers=host_auth)).json()["state"] == "COMPLETED"


async def test_any_other_total_failure_is_not_retried_by_itself(
    session_factory, client: AsyncClient, evaluated, host_auth, monkeypatch
):
    from services.evaluation import queue, worker
    from services.llm import set_llm_provider
    from services.llm.stub_provider import StubLLM

    sid = evaluated["id"]
    await client.post(f"/api/v1/sessions/{sid}/evaluate", headers=host_auth)

    async def unreachable(*args, **kwargs):
        raise ConnectionError("redis is not running")

    monkeypatch.setattr(queue, "read", unreachable)
    monkeypatch.setattr(worker, "SessionFactory", session_factory)
    set_llm_provider(StubLLM(fail=True))
    try:
        assert await worker.drain(session_factory) == 0
    finally:
        set_llm_provider(StubLLM())
    status = (await client.get(f"/api/v1/sessions/{sid}/evaluation", headers=host_auth)).json()
    assert status["state"] == "FAILED" and status["retry_after"] is None


async def test_without_redis_the_worker_runs_queued_jobs_from_the_database(
    session_factory, client: AsyncClient, evaluated, host_auth, monkeypatch
):
    """No-Docker mode: the queue is unreachable, the job row is still the
    authority, so the worker must evaluate it straight from the database."""
    from services.evaluation import queue, worker

    queued = await client.post(f"/api/v1/sessions/{evaluated['id']}/evaluate", headers=host_auth)
    assert queued.json()["state"] == "QUEUED"

    async def unreachable(*args, **kwargs):
        raise ConnectionError("redis is not running")

    monkeypatch.setattr(queue, "read", unreachable)
    assert await worker.drain(session_factory) == 1

    status = await client.get(f"/api/v1/sessions/{evaluated['id']}/evaluation", headers=host_auth)
    assert status.json()["state"] == "COMPLETED"
