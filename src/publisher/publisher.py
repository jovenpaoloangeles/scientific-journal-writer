from typing import Dict, List, Any
from datetime import datetime
import json
import re

from ..citation_editor.models import CitedContent
from .models import PublishedContent, ValidationResult
from .. import config

class ContentPublisher:
    """Content publisher for final output formatting and validation."""
    
    def __init__(self):
        """Initialize the content publisher."""
        self.validators = [
            self._validate_word_count,
            self._validate_citations,
            self._validate_structure,
            self._validate_metadata
        ]
    
    def _validate_word_count(self, content: CitedContent) -> List[str]:
        """Validate the word count of the content."""
        issues = []
        target_count = 1000  # Default word limit if not specified
        actual_count = self._calculate_word_count(content.cited_content)
        
        # Allow 10% margin above and require at least 85% of target
        if actual_count > target_count * 1.1:
            issues.append(f"Content exceeds word limit: {actual_count} words vs {target_count} limit")
        elif actual_count < target_count * 0.85:
            issues.append(f"Content is too short: {actual_count} words vs {target_count} target")
        return issues
    
    def _validate_citations(self, content: CitedContent) -> List[str]:
        """Validate citation formatting and placement."""
        issues = []
        citation_count = len(content.citations)
        if citation_count == 0:
            issues.append("No citations found in the content")
        
        # Check citation format
        citation_pattern = r'\[.*?\]'
        if not all('[' in cite.text and ']' in cite.text for cite in content.citations):
            issues.append("Some citations are not properly formatted")
        
        return issues
    
    def _validate_structure(self, content: CitedContent) -> List[str]:
        """Validate the structure of the content."""
        issues = []
        
        # Basic structure checks
        if not content.cited_content.strip():
            issues.append("Content is empty")
        if not content.citations:
            issues.append("No citations found")
        
        return issues
    
    def _validate_metadata(self, metadata: Dict) -> List[str]:
        """Validate metadata completeness."""
        required_fields = ["author", "timestamp", "version"]
        issues = []
        
        for field in required_fields:
            if field not in metadata:
                issues.append(f"Missing required metadata field: {field}")
        
        return issues
    
    def format_content(self, content: CitedContent) -> Dict[str, Any]:
        """Format the content for output."""
        metadata = self.create_metadata(content)
        
        # Use the cited content if available, otherwise use original content
        final_content = content.cited_content if content.cited_content else content.original_content
        
        # Calculate word count properly
        word_count = self._calculate_word_count(final_content)
        
        return {
            "section": "Introduction",  # Default section type
            "content": final_content,
            "citations": [citation.model_dump() for citation in content.citations],
            "word_count": word_count,
            "metadata": metadata
        }
    
    def create_metadata(self, content: CitedContent) -> Dict[str, Any]:
        """Create metadata for the content."""
        # Use the cited content if available, otherwise use original content
        final_content = content.cited_content if content.cited_content else content.original_content
        
        # Calculate word count properly
        word_count = self._calculate_word_count(final_content)
        
        return {
            "section_type": "Introduction",  # Default section type
            "word_count": word_count,
            "citation_count": len(content.citations),
            "timestamp": datetime.now().isoformat(),
            "author": "AI Content Generator",
            "version": "1.0.0",
            "generation_info": {
                "model": config.MODEL_NAME,
                "temperature": config.TEMPERATURE
            }
        }
    
    def _calculate_word_count(self, text: str) -> int:
        """Calculate word count properly by handling various edge cases."""
        if not text:
            return 0
            
        # Remove Word Count markers
        text = re.sub(r'\*\*Word Count:.*?\*\*', '', text)
        text = re.sub(r'\[Word count:.*?\]', '', text)
        text = re.sub(r'Word Count:.*?\n', '', text)
        text = re.sub(r'\(\d+ words\)', '', text)
        
        # Replace line breaks and special characters with spaces
        text = re.sub(r'[\n\r\t]', ' ', text)
        
        # Remove special characters except hyphens between words and apostrophes
        text = re.sub(r'[^\w\s\'-]', ' ', text)
        
        # Replace multiple spaces with a single space and trim
        text = re.sub(r'\s+', ' ', text).strip()
        
        # Handle hyphenated words and contractions
        text = re.sub(r'(?<=[a-zA-Z])-(?=[a-zA-Z])', ' ', text)  # Split hyphenated words
        text = re.sub(r'\'s\b', '', text)  # Remove possessive 's
        text = re.sub(r'\'t\b', ' not', text)  # Expand contractions
        text = re.sub(r'\'re\b', ' are', text)
        text = re.sub(r'\'ve\b', ' have', text)
        text = re.sub(r'\'m\b', ' am', text)
        text = re.sub(r'\'ll\b', ' will', text)
        text = re.sub(r'\'d\b', ' would', text)
        
        # Split into words and count non-empty words
        words = [word for word in text.split() if word.strip() and any(c.isalnum() for c in word)]
        
        return len(words)
    
    def validate_content(self, content: CitedContent, metadata: Dict) -> ValidationResult:
        """Run all validation checks."""
        all_issues = []
        warnings = []
        
        # Calculate word count before validation
        word_count = self._calculate_word_count(content.cited_content if content.cited_content else content.original_content)
        
        # Run all validators
        for validator in self.validators:
            if validator == self._validate_metadata:
                issues = validator(metadata)
            else:
                issues = validator(content)
            all_issues.extend(issues)
        
        # Add warnings for potential improvements
        if len(content.citations) < 3:
            warnings.append("Consider adding more citations for better academic rigor")
        
        # Add word count warning if needed
        target_count = 1000  # Default word limit
        if word_count < target_count * 0.7:
            warnings.append(f"Content is shorter than target: {word_count} words vs {target_count} target")
        elif word_count > target_count * 1.1:
            warnings.append(f"Content is longer than target: {word_count} words vs {target_count} target")
        
        return ValidationResult(
            is_valid=len(all_issues) == 0,
            issues=all_issues,
            warnings=warnings
        )
    
    def publish(self, content: CitedContent) -> PublishedContent:
        """
        Publish the content with formatting and validation.
        
        Args:
            content: The cited content to publish
            
        Returns:
            PublishedContent: The formatted and validated content
        """
        # Format content
        formatted_content = self.format_content(content)
        
        # Create metadata
        metadata = self.create_metadata(content)
        
        # Validate
        validation_result = self.validate_content(content, metadata)
        
        return PublishedContent(
            original_content=content,
            formatted_content=formatted_content,
            metadata=metadata,
            validation=validation_result
        )

def publish_content(content: CitedContent) -> PublishedContent:
    """
    Convenience function to publish content.
    
    Args:
        content: The cited content to publish
        
    Returns:
        PublishedContent: The published content
    """
    publisher = ContentPublisher()
    return publisher.publish(content) 