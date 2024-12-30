from typing import List
from pydantic import BaseModel, Field

class ContentInput(BaseModel):
    """
    Model for handling article section input data.
    """
    section: str = Field(..., description="Section of the article (e.g., Introduction, Methodology)")
    keypoints: List[str] = Field(..., description="List of key points to be expanded")
    word_limit: int = Field(..., gt=0, description="Word limit for the expanded content")

    def to_dict(self) -> dict:
        """Convert the input data to a dictionary format."""
        return {
            "section": self.section,
            "keypoints": self.keypoints,
            "word_limit": self.word_limit
        }

    @classmethod
    def from_dict(cls, data: dict) -> "ContentInput":
        """Create a ContentInput instance from a dictionary."""
        return cls(**data) 