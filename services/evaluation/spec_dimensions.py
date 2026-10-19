"""The six contribution measures M14's spec names, counted in code (FR-14.15).

Novelty, uptake, floor dynamics, entry skill, listening and closure, each 0-10.
They sit beside the evaluator agents' own dimensions rather than replacing them,
and they are proxies, not judgements of quality: each says in `basis` exactly what
was counted, so a student can see where a number came from and a reviewer can
challenge it. Nothing here calls a model.
"""

import re
from collections.abc import Sequence

from services.common.contracts import CandidateMetrics

_CLOSURE = re.compile(
    r"\b(to sum up|to summari[sz]e|in summary|in conclusion|to conclude|so overall|"
    r"overall,|the way forward|where we agree|what we agree|we can all agree|"
    r"my closing|to wrap up)\b",
    re.IGNORECASE,
)
_WORD = re.compile(r"[a-z']{4,}")
# A line whose content words are this largely already said by someone is a repeat.
_REPEAT_SHARE = 0.6


def _ten(value: float) -> float:
    return round(max(0.0, min(1.0, value)) * 10, 1)


def _words(text: str) -> set[str]:
    return set(_WORD.findall((text or "").lower()))


def _novelty(label: str, segments: Sequence) -> tuple[float, str]:
    seen: set[str] = set()
    own = fresh = 0
    for segment in sorted(segments, key=lambda s: s.start):
        words = _words(segment.text)
        if segment.candidate_id == label and words:
            own += 1
            if len(words & seen) / len(words) < _REPEAT_SHARE:
                fresh += 1
        seen |= words
    if own == 0:
        return 0.0, "no contributions to judge"
    return _ten(fresh / own), f"{fresh} of {own} contributions added points nobody had made"


def spec_dimensions(
    label: str,
    metrics: CandidateMetrics,
    moments: Sequence[dict],
    segments: Sequence,
) -> dict[str, dict]:
    """Per measure: `{"score": 0-10, "basis": what was counted}`."""
    if metrics.turns == 0:
        return {}
    turns = metrics.turns

    uptake = (
        metrics.responses + metrics.arguments_supported + metrics.arguments_challenged
    ) / turns
    listening_hits = metrics.responses + metrics.questions
    # Listening also rewards not talking over people.
    listening = min(1.0, listening_hits / turns) * (1.0 - min(1.0, metrics.interruptions / turns))
    interrupt_rate = min(1.0, metrics.interruptions / turns)
    # Floor dynamics: an even-ish share and no cutting in. 1/3 to 1/2 is read as healthy.
    share_penalty = max(0.0, metrics.participation_ratio - 0.5) * 2
    floor = 1.0 - min(1.0, 0.6 * interrupt_rate + 0.4 * share_penalty)

    if moments:
        taken = sum(1 for m in moments if not m.get("missed"))
        entry = taken / len(moments)
        entry_basis = f"{taken} of {len(moments)} invitations by name were taken within seconds"
    else:
        entry, entry_basis = 1.0, "nobody turned to them by name, so nothing was missed"

    own_text = [s.text for s in segments if s.candidate_id == label]
    closed = sum(1 for text in own_text if _CLOSURE.search(text or ""))
    closure = 1.0 if closed else 0.0  # one real summing-up is the full mark

    novelty, novelty_basis = _novelty(label, segments)
    return {
        "novelty": {"score": novelty, "basis": novelty_basis},
        "uptake": {
            "score": _ten(uptake),
            "basis": f"{metrics.responses} replies, {metrics.arguments_supported} supports and "
            f"{metrics.arguments_challenged} challenges over {turns} turns",
        },
        "floor_dynamics": {
            "score": _ten(floor),
            "basis": f"{metrics.participation_ratio:.0%} of the floor, "
            f"{metrics.interruptions} interruptions over {turns} turns",
        },
        "entry_skill": {"score": _ten(entry), "basis": entry_basis},
        "listening": {
            "score": _ten(listening),
            "basis": f"{metrics.responses} replies and {metrics.questions} questions, "
            f"{metrics.interruptions} interruptions over {turns} turns",
        },
        "closure": {
            "score": _ten(closure),
            "basis": f"{closed} contribution{'s' if closed != 1 else ''} summed the discussion up",
        },
    }
