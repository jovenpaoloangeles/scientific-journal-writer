"""Models for content review."""
from typing import List
from enum import Enum
from pydantic import BaseModel

class ReviewCriteria(str, Enum):
    """Enumeration of review criteria."""
    CLARITY = "Clarity"
    COHERENCE = "Coherence"
    ACADEMIC_STYLE = "Academic Style"
    CONTENT_QUALITY = "Content Quality"
    STRUCTURE = "Structure"

class ReviewScore(BaseModel):
    """Model for a single review score."""
    criterion: ReviewCriteria
    score: int
    feedback: str

class ReviewedContent(BaseModel):
    """Model for reviewed content."""
    content: str
    scores: List[ReviewScore]
    total_score: float
    overall_feedback: str 