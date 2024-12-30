"""Models for version selection."""
from typing import List
from pydantic import BaseModel

class SelectedContent(BaseModel):
    """Model for selected content version."""
    content: str
    score: float
    selection_reason: str 