"""Validated input and output contracts for one-issue triage."""
from typing import Literal
from pydantic import BaseModel, ConfigDict, Field

class Issue(BaseModel):
    # Discard GitHub metadata and gold labels.
    model_config = ConfigDict(strict=True)
    repo: str = Field(min_length=1, max_length=200)
    number: int = Field(gt=0)
    title: str = Field(min_length=1, max_length=2000)
    body: str | None = Field(default=None, max_length=50000)

class Assessment(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)
    issue_type: Literal["bug", "enhancement", "documentation", "question", "meta", "unknown"]
    component: str | None = Field(max_length=100)
    severity: Literal["low", "medium", "high", "critical", "unknown"]
    has_reproduction_steps: bool | None
    summary: str = Field(min_length=1, max_length=500)
    uncertainty: str = Field(min_length=1, max_length=500)

class TriageRecord(Assessment):
    repo: str
    number: int
