import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from pydantic import ValidationError

from code_reviewer.schemas import Finding


def make_finding(**overrides):
    data = {
        "title": "Division by zero",
        "severity": "medium",
        "confidence": "high",
        "line_number": 2,
        "explanation": "The denominator may be zero.",
        "impact": "The function may raise ZeroDivisionError.",
        "suggested_fix": "Check the denominator before division.",
        "sources": {"llm"},
        "status": "likely",
    }
    data.update(overrides)
    return Finding(**data)


def test_valid_finding():
    finding = make_finding()
    assert finding.title == "Division by zero"


def test_invalid_severity():
    with pytest.raises(ValidationError):
        make_finding(severity="extreme")


def test_none_line_number():
    finding = make_finding(line_number=None)
    assert finding.line_number is None


def test_zero_line_number():
    with pytest.raises(ValidationError):
        make_finding(line_number=0)


def test_missing_sources():
    with pytest.raises(ValidationError):
        Finding(
            title="Division by zero",
            severity="medium",
            confidence="high",
            line_number=2,
            explanation="The denominator may be zero.",
            impact="The function may raise ZeroDivisionError.",
            suggested_fix=None,
            status="likely",
        )
