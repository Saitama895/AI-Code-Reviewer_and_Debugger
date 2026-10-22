import ast
from code_reviewer.result import ReviewResult, ReviewError, find_division_by_zero

def analyze_python(source: str) -> ReviewResult:

    if not source.strip():
        return ReviewResult(
            status="failed",
            errors=[ReviewError(message="Python source cannot be empty")],
        )

    try:
        tree = ast.parse(source)
    except SyntaxError as exc:
        return ReviewResult(
            status="partial",
            errors=[
                ReviewError(
                    message=exc.msg or "Invalid Python syntax.",
                    line_number=exc.lineno,
                )
            ],
        )

    findings = find_division_by_zero(tree)

    return ReviewResult(
        status="success",
        findings=findings
    )   