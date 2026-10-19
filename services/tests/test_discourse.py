"""The discourse graph: typed edges between contributions (M14 FR-14.14)."""

from services.common.contracts import TranscriptSegment
from services.metrics.discourse import EDGE_TYPES, build_discourse_graph


def _seg(label, start, end, text):
    return TranscriptSegment(
        session_id="s", candidate_id=label, start=start, end=end, text=text, confidence=0.9
    )


SEGMENTS = [
    _seg("P1", 0, 6, "Should internships be paid? I think they must be."),
    _seg("A", 7, 12, "However, small firms cannot afford that."),
    _seg("P2", 13, 18, "I agree with Asha, building on that, cost is the limit."),
    _seg("P1", 19, 24, "What would a fair stipend look like?"),
    _seg("A", 25, 30, "Perhaps tied to the firm's size."),
    _seg("P2", 200, 205, "Separately, remote placements are a new topic."),
]


def test_every_contribution_gets_one_typed_edge():
    graph = build_discourse_graph(SEGMENTS)
    assert len(graph["nodes"]) == len(graph["edges"]) == len(SEGMENTS)
    assert {e["type"] for e in graph["edges"]} <= set(EDGE_TYPES)


def test_edges_are_typed_by_how_they_respond():
    types = [e["type"] for e in build_discourse_graph(SEGMENTS)["edges"]]
    assert types == ["new", "challenge", "support", "extend", "answer", "new"]


def test_a_reply_after_a_long_silence_opens_a_new_point():
    graph = build_discourse_graph(SEGMENTS)
    assert graph["edges"][-1] == {"source": 5, "target": None, "type": "new"}
    assert graph["counts"]["new"] == 2


def test_the_graph_is_reproducible():
    assert build_discourse_graph(SEGMENTS) == build_discourse_graph(SEGMENTS)
