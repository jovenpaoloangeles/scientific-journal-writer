"""Models for revision agent."""
from typing import List
from pydantic import BaseModel

class RevisionChange(BaseModel):
    """Model for a single revision change."""
    type: str
    location: str
    change: str

class RevisedContent(BaseModel):
    """Model for revised content."""
    original_content: str
    revised_content: str
    revision_changes: List[RevisionChange]
    revision_summary: str 