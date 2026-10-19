"""Discourse graph with typed edges between contributions (M14 FR-14.14).

The metrics engine already builds who-answered-whom between *speakers*. This
builds the finer graph the spec asks for: one node per contribution, and an edge
from each contribution to the one it responds to, typed by how it responds.

Edge types, decided in code from adjacency and wording (no model, so the same
transcript always gives the same graph):

* ``answer``    - replies to a contribution that asked a question
* ``challenge`` - pushes back ("I disagree", "however", "the problem with")
* ``support``   - backs it ("I agree", "building on", "good point")
* ``extend``    - follows on from it, within the response window, without either
* ``new``       - no edge target: opens a point nobody was answering

The typing is wording-based and says so; it is a reading aid for the group
report, not a verdict on the discussion.
"""

from __future__ import annotations

import re
from collections import Counter
from collections.abc import Sequence

from services.metrics.engine import (
    _CHALLENGE_RE,
    _SUPPORT_RE,
    RESPONSE_WINDOW_SECONDS,
    _addressed_target,
)

EDGE_TYPES = ("answer", "challenge", "support", "extend", "new")


def build_discourse_graph(segments: Sequence, candidates: set[str] | None = None) -> dict:
    """Nodes, typed edges and a per-type count for the whole transcript."""
    ordered = sorted(segments, key=lambda s: s.start)
    labels = candidates or {s.candidate_id for s in ordered}
    nodes: list[dict] = []
    edges: list[dict] = []
    for index, segment in enumerate(ordered):
        text = segment.text or ""
        nodes.append(
            {
                "id": index,
                "speaker": segment.candidate_id,
                "start": round(float(segment.start), 2),
                "text": text,
            }
        )
        target = _target(ordered, index, labels)
        if target is None:
            edges.append({"source": index, "target": None, "type": "new"})
            continue
        edges.append(
            {
                "source": index,
                "target": target,
                "type": _edge_type(text, ordered[target].text or ""),
            }
        )
    counts = Counter(edge["type"] for edge in edges)
    return {
        "nodes": nodes,
        "edges": edges,
        "counts": {kind: counts.get(kind, 0) for kind in EDGE_TYPES},
    }


def _target(ordered: Sequence, index: int, labels: set[str]) -> int | None:
    """The contribution this one answers: the one it names, else the last other speaker's."""
    segment = ordered[index]
    addressed = _addressed_target(segment.text or "", labels - {segment.candidate_id})
    for back in range(index - 1, -1, -1):
        earlier = ordered[back]
        if earlier.candidate_id == segment.candidate_id:
            continue
        if addressed and earlier.candidate_id == addressed:
            return back
        if not addressed:
            gap = segment.start - earlier.end
            return back if gap <= RESPONSE_WINDOW_SECONDS else None
    return None


def _edge_type(text: str, target_text: str) -> str:
    if _CHALLENGE_RE.search(text):
        return "challenge"
    if _SUPPORT_RE.search(text):
        return "support"
    if re.search(r"\?", target_text):
        return "answer"
    return "extend"
