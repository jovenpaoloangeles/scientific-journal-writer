from pydantic import BaseModel, Field
from typing import List, Dict, Any
from ..citation_editor.models import CitedContent

class ValidationResult(BaseModel):
    """Model for content validation results."""
    is_valid: bool = Field(..., description="Whether the content passed validation")
    issues: List[str] = Field(default_factory=list, description="List of validation issues")
    warnings: List[str] = Field(default_factory=list, description="List of validation warnings")

class PublishedContent(BaseModel):
    """Model for the final published content."""
    original_content: CitedContent = Field(..., description="The original cited content")
    formatted_content: Dict[str, Any] = Field(..., description="Content formatted for output")
    metadata: Dict[str, Any] = Field(..., description="Content metadata")
    validation: ValidationResult = Field(..., description="Validation results")
    
    class Config:
        """Pydantic model configuration."""
        json_schema_extra = {
            "example": {
                "original_content": {
                    "content": "Content with citations...",
                    "citations": [
                        {
                            "text": "Example citation",
                            "reason": "Support for claim",
                            "location": "paragraph 1",
                            "suggested_source_type": "journal"
                        }
                    ]
                },
                "formatted_content": {
                    "section": "Introduction",
                    "content": "Formatted content...",
                    "citations": ["citation1", "citation2"],
                    "word_count": 500
                },
                "metadata": {
                    "author": "AI Writer",
                    "timestamp": "2024-01-20T12:00:00Z",
                    "version": "1.0.0",
                    "section_type": "Introduction"
                },
                "validation": {
                    "is_valid": True,
                    "issues": [],
                    "warnings": ["Consider adding more examples"]
                }
            }
        } 