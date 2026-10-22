from pydantic import BaseModel, Field
from typing import Literal

from code_reviewer.schemas import Finding

class ReviewError(BaseModel):
    message : str
    line_number : int | None = None

class ReviewResult(BaseModel):
    status : Literal["success", "partial", "failed"]
    findings : list[Finding] = Field(default_factory=list)
    errors : list[ReviewError] = Field(default_factory=list)

