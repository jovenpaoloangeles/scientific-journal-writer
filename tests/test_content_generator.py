import pytest
from unittest.mock import patch, MagicMock
from src.content_generator import ContentGenerator, generate_content
from src.content_generator.config import ContentConfig

def test_config():
    """Test configuration."""
    config = ContentConfig.get_default_config()
    assert "model" in config
    assert "temperature" in config
    assert "max_tokens" in config

def test_prompt_template():
    """Test prompt template generation."""
    template = ContentConfig.get_prompt_template("Introduction")
    assert "Write an academic introduction" in template
    assert "{keypoints}" in template
    assert "{word_limit}" in template

def test_prompt_template_fallback():
    """Test prompt template fallback for unknown section."""
    template = ContentConfig.get_prompt_template("UnknownSection")
    assert "Write an academic section" in template
    assert "Follow academic writing style" in template

@patch('openai.OpenAI')
def test_content_generation(mock_openai):
    """Test content generation with mocked OpenAI."""
    # Mock OpenAI response
    mock_completion = MagicMock()
    mock_completion.choices = [MagicMock(message=MagicMock(content="Generated content"))]
    mock_client = MagicMock()
    mock_client.chat.completions.create.return_value = mock_completion
    mock_openai.return_value = mock_client

    generator = ContentGenerator()
    versions = generator.generate_versions(
        input_data=MagicMock(
            section="Introduction",
            keypoints=["Point 1"],
            word_limit=500
        ),
        num_versions=1
    )

    assert len(versions) == 1
    assert isinstance(versions[0], str)
    assert versions[0] == "Generated content"

@patch('src.content_generator.generator.ContentGenerator')
def test_generate_content_convenience(mock_generator_class):
    """Test the convenience function for content generation."""
    mock_generator = MagicMock()
    mock_generator.generate_versions.return_value = ["Content 1", "Content 2"]
    mock_generator_class.return_value = mock_generator
    
    result = generate_content(MagicMock())
    assert len(result) == 2
    assert mock_generator.generate_versions.called 