import pytest
from src.input_handler import ContentInput

def test_content_input_creation():
    """Test creating a ContentInput instance."""
    input_data = ContentInput(
        section="Introduction",
        keypoints=["Point 1", "Point 2"],
        word_limit=500
    )
    assert input_data.section == "Introduction"
    assert len(input_data.keypoints) == 2
    assert input_data.word_limit == 500

def test_content_input_validation():
    """Test ContentInput validation."""
    with pytest.raises(ValueError):
        ContentInput(
            section="Introduction",
            keypoints=["Point 1"],
            word_limit=-100  # Invalid word limit
        )

def test_content_input_to_dict(sample_input_data):
    """Test converting ContentInput to dictionary."""
    data_dict = sample_input_data.to_dict()
    assert isinstance(data_dict, dict)
    assert "section" in data_dict
    assert "keypoints" in data_dict
    assert "word_limit" in data_dict

def test_content_input_from_dict():
    """Test creating ContentInput from dictionary."""
    data_dict = {
        "section": "Methodology",
        "keypoints": ["Method 1", "Method 2"],
        "word_limit": 300
    }
    input_data = ContentInput.from_dict(data_dict)
    assert input_data.section == "Methodology"
    assert len(input_data.keypoints) == 2
    assert input_data.word_limit == 300 