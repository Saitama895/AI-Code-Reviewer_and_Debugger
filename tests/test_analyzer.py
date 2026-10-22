import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
import ast
from code_reviewer.result import evaluate_constant
from code_reviewer.analyser import analyze_python

def test_valid_python():
    result = analyze_python("x = 10")

    assert result.status == "success"
    assert result.findings == []
    assert result.errors == []

def test_empty_source():
    result = analyze_python("   ")

    assert result.status == "failed"
    assert len(result.errors) == 1


def test_syntax_error():
    result = analyze_python("def hello(:\n    pass")

    assert result.status == "partial"
    assert len(result.errors) == 1
    assert result.errors[0].line_number == 1

def test_detects_division_by_zero():
    result = analyze_python("x = 10 / 0")

    assert len(result.findings) == 1
    assert result.findings[0].line_number == 1
    assert "ast" in result.findings[0].sources


def test_ignores_nonzero_denominator():
    result = analyze_python("x = 10 / 2")

    assert result.findings == []


def test_ignores_variable_denominator():
    result = analyze_python("x = 10 / divisor")

    assert result.findings == []


def test_detects_multiple_occurrences():
    source = "x = 10 / 0\ny = 5 / 0"
    result = analyze_python(source)

    assert len(result.findings) == 2
    assert [f.line_number for f in result.findings] == [1, 2]


def test_ignores_boolean_denominator():
    result = analyze_python("x = 10 / False")

    assert result.findings == []

def test_division_by_zero_in_subtraction():
    result = analyze_python("x = 10 / (1 - 1)")
    assert result.status == "success"
    assert len(result.findings) == 1


def test_nonzero_multiplication_denominator():
    result = analyze_python("x = 10 / (2 * 3)")
    assert len(result.findings) == 0


def test_division_by_zero_in_subtraction_with_same_values():
    result = analyze_python("x = 10 / (5 - 5)")
    assert len(result.findings) == 1


def test_nested_division_by_zero_does_not_crash():
    result = analyze_python("x = 10 / (1 / 0)")
    assert result.status == "success"
    assert len(result.findings) >= 1


@pytest.mark.parametrize(
    "expression, expected",
    [
        ("-0", 0),
        ("-(2 - 2)", 0),
        ("+0", 0),
        ("-5", -5),
        ("-denominator", None),
    ],
)
def test_evaluate_unary_expressions(expression, expected):
    node = ast.parse(expression, mode="eval").body

    assert evaluate_constant(node) == expected