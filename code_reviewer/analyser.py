import ast
from code_reviewer.result import ReviewResult, ReviewError

def analyze_python(source: str) -> ReviewResult:

    if not source.strip():
        return ReviewResult(
            status="failed",
            errors=[ReviewError(message="Python source cannot be empty")],
        )

    try:
        ast.parse(source)
    except SyntaxError as exc:
        return ReviewResult(
            status="partial",
            errors=[
                ReviewError(
                    message=exc.msg,
                    line_number=exc.lineno,
                )
            ],
        )

    return ReviewResult(status="success")