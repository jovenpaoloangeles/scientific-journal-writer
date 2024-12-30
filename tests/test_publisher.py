import pytest
from datetime import datetime
from src.publisher import ContentPublisher, publish_content
from src.publisher.models import ValidationResult, PublishedContent

def test_validation_result():
    """Test creating a ValidationResult instance."""
    validation = ValidationResult(
        is_valid=True,
        issues=[],
        warnings=["Consider adding more examples"]
    )
    assert validation.is_valid
    assert len(validation.issues) == 0
    assert len(validation.warnings) == 1

def test_published_content_creation(sample_cited_content):
    """Test creating a PublishedContent instance."""
    published = PublishedContent(
        original_content=sample_cited_content,
        formatted_content={
            "section": "Introduction",
            "content": "Test content",
            "citations": []
        },
        metadata={
            "author": "Test",
            "timestamp": datetime.utcnow().isoformat(),
            "version": "1.0"
        },
        validation=ValidationResult(
            is_valid=True,
            issues=[],
            warnings=[]
        )
    )
    assert published.original_content == sample_cited_content
    assert "section" in published.formatted_content
    assert "author" in published.metadata
    assert published.validation.is_valid

def test_word_count_validation(sample_cited_content):
    """Test word count validation."""
    publisher = ContentPublisher()
    issues = publisher._validate_word_count(sample_cited_content)
    assert isinstance(issues, list)

def test_citation_validation(sample_cited_content):
    """Test citation validation."""
    publisher = ContentPublisher()
    issues = publisher._validate_citations(sample_cited_content)
    assert isinstance(issues, list)

def test_structure_validation(sample_cited_content):
    """Test content structure validation."""
    publisher = ContentPublisher()
    issues = publisher._validate_structure(sample_cited_content)
    assert isinstance(issues, list)

def test_metadata_validation():
    """Test metadata validation."""
    publisher = ContentPublisher()
    metadata = {
        "author": "Test",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0",
        "section_type": "Introduction"
    }
    issues = publisher._validate_metadata(metadata)
    assert len(issues) == 0

    # Test with missing field
    incomplete_metadata = {"author": "Test"}
    issues = publisher._validate_metadata(incomplete_metadata)
    assert len(issues) > 0

def test_content_formatting(sample_cited_content):
    """Test content formatting."""
    publisher = ContentPublisher()
    formatted = publisher.format_content(sample_cited_content)
    assert isinstance(formatted, dict)
    assert "section" in formatted
    assert "content" in formatted
    assert "citations" in formatted
    assert "word_count" in formatted

def test_metadata_creation(sample_cited_content):
    """Test metadata creation."""
    publisher = ContentPublisher()
    metadata = publisher.create_metadata(sample_cited_content)
    assert isinstance(metadata, dict)
    assert "author" in metadata
    assert "timestamp" in metadata
    assert "version" in metadata
    assert "section_type" in metadata
    assert "generation_info" in metadata

def test_content_publishing(sample_cited_content):
    """Test the complete publishing process."""
    publisher = ContentPublisher()
    result = publisher.publish(sample_cited_content)
    assert isinstance(result, PublishedContent)
    assert result.validation.is_valid is not None

def test_publish_content_convenience(sample_cited_content):
    """Test the convenience function for publishing."""
    result = publish_content(sample_cited_content)
    assert isinstance(result, PublishedContent)
    assert result.validation.is_valid is not None 