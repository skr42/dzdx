from pydantic import BaseModel, Field
from typing import Literal

class CommentRequest(BaseModel):
    comment: str


class AnalysisResult(BaseModel):
    label: Literal["toxic", "non-toxic"]

    score: float = Field(..., ge=0.0, le=1.0)

class CommentResponse(BaseModel):
    allowed: bool
    analysis: AnalysisResult
