"""Models for content generation."""
from typing import Dict, Any
from pydantic import BaseModel

class GeneratedContent(BaseModel):
    """Model for generated content."""
    content: str
    section: str
    word_limit: int
    generation_params: Dict[str, Any]
    
    def __str__(self) -> str:
        """Return a string representation of the content."""
        return self.content 