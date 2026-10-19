"""The six measures M14's spec names, counted in code (FR-14.15)."""

from services.common.contracts import CandidateMetrics, TranscriptSegment
from services.evaluation.aggregator import AggregatedScore
from services.evaluation.report import build_candidate_report, entry_moments
from services.evaluation.spec_dimensions import spec_dimensions


def _seg(label, start, end, text):
    return TranscriptSegment(
        session_id="s", candidate_id=label, start=start, end=end, text=text, confidence=0.9
    )


def _metrics(**kw):
    base = dict(
        session_id="s",
        candidate_id="A",
        speaking_seconds=30,
        participation_ratio=0.3,
        turns=3,
        interruptions=0,
        responses=2,
        questions=1,
        arguments_supported=1,
        arguments_challenged=0,
    )
    return CandidateMetrics(**{**base, **kw})


SEGMENTS = [
    _seg("P1", 0, 8, "Internships favour students with contacts in large cities."),
    _seg(
        "A", 9, 15, "Contacts matter, but unpaid placements also exclude poorer families entirely."
    ),
    _seg("P2", 16, 22, "Asha, do you think colleges should pay stipends?"),
    _seg("A", 23, 30, "Stipends would help, so the funding question decides it."),
    _seg("A", 80, 90, "To sum up, we agree access matters and funding is the open question."),
]


def test_all_six_measures_come_with_a_score_and_a_basis():
    metrics = _metrics()
    moments = entry_moments(SEGMENTS, "A", "Asha Rao", {"P1": "Arjun", "P2": "Bhavana"})
    result = spec_dimensions("A", metrics, moments, SEGMENTS)
    assert set(result) == {
        "novelty",
        "uptake",
        "floor_dynamics",
        "entry_skill",
        "listening",
        "closure",
    }
    for entry in result.values():
        assert 0.0 <= entry["score"] <= 10.0
        assert entry["basis"]
    assert result["closure"]["score"] == 10.0
    assert result["entry_skill"]["score"] == 10.0  # Bhavana's question was answered at once


def test_interrupting_and_ignoring_people_lowers_listening_and_floor_dynamics():
    polite = spec_dimensions("A", _metrics(), [], SEGMENTS)
    rude = spec_dimensions(
        "A",
        _metrics(interruptions=3, responses=0, questions=0, participation_ratio=0.8),
        [],
        SEGMENTS,
    )
    assert rude["listening"]["score"] < polite["listening"]["score"]
    assert rude["floor_dynamics"]["score"] < polite["floor_dynamics"]["score"]


def test_a_repeated_point_is_not_novel():
    repeat = [
        _seg("P1", 0, 5, "Internships favour students with contacts in large cities."),
        _seg("A", 6, 10, "Internships favour students with contacts in large cities."),
    ]
    assert spec_dimensions("A", _metrics(turns=1), [], repeat)["novelty"]["score"] == 0.0


def test_a_silent_candidate_has_nothing_to_measure():
    assert spec_dimensions("A", _metrics(turns=0), [], SEGMENTS) == {}


def test_the_candidate_report_carries_them():
    score = AggregatedScore(
        candidate_label="A",
        overall=60.0,
        dimensions={"communication": 6.0},
        weights={"communication": 1.0},
        confidence=0.7,
        needs_human_review=False,
    )
    report = build_candidate_report("A", "Asha Rao", score, [], _metrics(), segments=SEGMENTS)
    assert "listening" in report.to_dict()["spec_dimensions"]


def test_a_hindi_contribution_is_measured_like_an_english_one():
    """Day 5 review: the same point scored novelty 10 in English and 0 in Hindi."""
    opener = _seg("P1", 0, 5, "Should colleges make internships mandatory?")
    english = [opener, _seg("A", 6, 12, "Experience teaches what lectures cannot, so yes.")]
    hindi = [opener, _seg("A", 6, 12, "मुझे लगता है कि अनुभव वह सिखाता है जो कक्षा नहीं सिखाती")]
    in_english = spec_dimensions("A", _metrics(turns=1), [], english)["novelty"]
    in_hindi = spec_dimensions("A", _metrics(turns=1), [], hindi)["novelty"]
    assert in_hindi["score"] == in_english["score"] == 10.0
    assert in_hindi["basis"] != "no contributions to judge"


def test_entry_skill_is_not_measured_when_nobody_invited_them():
    """Day 5 review: never being invited used to score a full 10."""
    entry = spec_dimensions("A", _metrics(), [], SEGMENTS)["entry_skill"]
    assert entry["score"] is None and "not measured" in entry["basis"]


def test_a_late_turn_that_pulls_others_together_is_closure_in_any_language():
    """Closure is what a contribution does, not only an English phrase."""
    talk = [
        _seg("P1", 0, 10, "Stipends decide whether poorer students can take internships at all."),
        _seg("P2", 11, 20, "Colleges should vet companies first, or it is free labour."),
        _seg("A", 21, 28, "I think that is fair."),
        _seg("A", 70, 80, "So stipends for poorer students, and colleges vet companies first."),
    ]
    result = spec_dimensions("A", _metrics(), [], talk)["closure"]
    assert result["score"] == 10.0 and "drawing on others" in result["basis"]
    early_only = talk[:3]
    assert spec_dimensions("A", _metrics(), [], early_only)["closure"]["score"] == 0.0
