from pydantic import BaseModel, Field
from typing import Literal, Optional, Annotated

class Finding(BaseModel):
    title : str = Field(min_length=1, description="short description for the code")
    severity : Literal["low", "medium", "high", "critical"] = Field(..., description="It tells about how severe the bug is hence can be put on priority bases accordingly.")
    confidence : Literal["low", "medium", "high"] = Field(..., description="The llm generated confidence for bug finding")
    line_number : int | None = Field(ge = 1, description="showcasing the line at which an error occured", default=None)
    explanation : str = Field(min_length=1, description="Explanation of the bug")
    impact : str = Field(min_length=1, description="it tells what could break or go wrong")
    suggested_fix : str | None = Field(..., description="Proposed fix or None if no safe fix is known")
    sources : set[Literal["ruff", "bandit", "llm", "ast"]]
    status : Literal["confirmed", "likely", "needs_review", "unsupported"]
