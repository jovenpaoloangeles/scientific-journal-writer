"""Models for citation editor."""
from typing import List
from pydantic import BaseModel
from src.revision_agent.models import RevisionChange

class Citation(BaseModel):
    """Model for a single citation."""
    text: str
    source: str
    location: str
    reason: str

class CitedContent(BaseModel):
    """Model for content with citations."""
    original_content: str
    cited_content: str
    citations: List[Citation]
    citation_changes: List[RevisionChange]
    citation_summary: str 