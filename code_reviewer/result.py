from pydantic import BaseModel, Field
from typing import Literal
import ast
from code_reviewer.schemas import Finding

class ReviewError(BaseModel):
    message : str
    line_number : int | None = None

class ReviewResult(BaseModel):
    status : Literal["success", "partial", "failed"]
    findings : list[Finding] = Field(default_factory=list)
    errors : list[ReviewError] = Field(default_factory=list)


def find_division_by_zero(tree: ast.AST) -> list[Finding]:
    findings = []

    for node in ast.walk(tree):
        if not isinstance(node, ast.BinOp):
            continue

        if not isinstance(node.op, ast.Div):
            continue

        finding = evaluate_constant(node.right)

        if finding == 0:
            findings.append(
                Finding(              
                    title="Division by zero",
                    severity="medium",
                    confidence="high",
                    line_number=node.lineno,
                    explanation=(
                        "The division operation uses the integer literal zero "
                        "as its denominator."
                    ),
                    impact="Executing this expression raises ZeroDivisionError.",
                    suggested_fix=(
                        "Validate the denominator before performing the division."
                    ),
                    sources={"ast"},  # Replace with a static-rule source.
                    status="confirmed",  
                )
            )

    return findings

def evaluate_constant(node):

    # Case 1: Integer constants, excluding booleans
    if isinstance(node, ast.Constant):
        if type(node.value) is int:
            return node.value
        return None
    elif isinstance(node, ast.UnaryOp):
        value = evaluate_constant(node.operand)
        if value is None:
            return None
        
        if isinstance(node.op, ast.USub):
            return -1 * value
        elif isinstance(node.op, ast.UAdd):
            return value
        
        return None

    # Case 2: Binary arithmetic expressions
    if isinstance(node, ast.BinOp):
        left = evaluate_constant(node.left)
        right = evaluate_constant(node.right)

        # Cannot evaluate if either operand is unknown
        if left is None or right is None:
            return None
        
        if isinstance(node.op, ast.Add):
            return left + right 
        
        elif isinstance(node.op, ast.Sub):
            return left - right  
        
        elif isinstance(node.op, ast.Mult):
            return left * right  
        
        elif isinstance(node.op, ast.Div):
            if right == 0:
                return None
            return left / right   
        
    # Unsupported Expression
    return None