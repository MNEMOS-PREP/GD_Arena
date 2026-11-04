"""The punctuation a model gets wrong in an evaluator's JSON, and the one thing the repair must never do."""

import json

import pytest

from services.llm import json_repair
from services.llm.openai_provider import _parse_json


def test_valid_json_is_left_alone():
    text = '{"a": "He said \\"hi\\"", "b": [1, 2, 3]}'
    assert json_repair.repair(text) == text
    assert json_repair.loads(text) == json.loads(text)


def test_an_unescaped_quote_inside_a_string_is_escaped():
    text = '{"quote": "A said "that is fair" and left", "score": 7}'
    assert json_repair.loads(text) == {"quote": 'A said "that is fair" and left', "score": 7}


def test_a_missing_comma_between_keys_is_added():
    text = '{"a": "x" "b": "y"}'
    assert json_repair.loads(text) == {"a": "x", "b": "y"}


def test_a_missing_comma_between_array_items_is_added():
    assert json_repair.loads('{"items": ["one" "two" "three"]}') == {"items": ["one", "two", "three"]}


def test_a_missing_comma_between_objects_in_an_array_is_added():
    assert json_repair.loads('{"e": [{"t": "a"} {"t": "b"}]}') == {"e": [{"t": "a"}, {"t": "b"}]}


def test_a_trailing_comma_is_dropped():
    assert json_repair.loads('{"a": [1, 2,], "b": "x",}') == {"a": [1, 2], "b": "x"}


def test_the_evaluator_shape_with_quoted_evidence_survives():
    text = (
        '{"dimension": "behaviour", "score": 8, "evidence": [{"timestamp": "00:26", '
        '"quote": "I said "evidence" matters", "note": "clear"} {"timestamp": "01:12", "quote": "ok", "note": "short"}]}'
    )
    data = json_repair.loads(text)
    assert data["score"] == 8
    assert [e["timestamp"] for e in data["evidence"]] == ["00:26", "01:12"]
    assert data["evidence"][0]["quote"] == 'I said "evidence" matters'


def test_text_that_is_not_json_still_fails():
    with pytest.raises(json.JSONDecodeError):
        json_repair.loads("this is prose, not a verdict")


def test_the_provider_parser_uses_it_and_still_strips_a_fence():
    assert _parse_json('Here you go: {"a": "x" "b": "y"} done') == {"a": "x", "b": "y"}
