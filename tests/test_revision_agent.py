import pytest
from unittest.mock import patch, MagicMock
from src.revision_agent import RevisionAgent, revise_content
from src.revision_agent.models import RevisionChange, RevisedContent

def test_revision_change_creation():
    """Test creating a RevisionChange instance."""
    change = RevisionChange(
        type="grammar",
        location="paragraph 1",
        change="Fixed verb tense"
    )
    assert isinstance(change, RevisionChange)
    assert change.type == "grammar"
    assert change.location == "paragraph 1"
    assert change.change == "Fixed verb tense"

def test_revised_content_creation(sample_content):
    """Test creating a RevisedContent instance."""
    revised = RevisedContent(
        original_content=sample_content,
        revised_content="Improved content",
        changes=[
            RevisionChange(
                type="grammar",
                location="p1",
                change="Fixed verb tense"
            )
        ],
        revision_summary="Made grammatical improvements"
    )
    assert isinstance(revised, RevisedContent)
    assert revised.original_content == sample_content
    assert revised.revised_content == "Improved content"
    assert len(revised.changes) == 1
    assert revised.revision_summary == "Made grammatical improvements"

@patch('openai.OpenAI')
def test_revision_agent(mock_openai, sample_content):
    """Test revision agent with mocked OpenAI."""
    # Mock OpenAI response
    mock_completion = MagicMock()
    mock_completion.choices = [
        MagicMock(
            message=MagicMock(
                content="""
                REVISED CONTENT:
                This is the improved content with better grammar and clarity.

                CHANGES:
                1. Grammar - paragraph 1: Fixed verb tense
                2. Clarity - paragraph 2: Improved sentence structure

                SUMMARY:
                Made grammatical improvements and enhanced clarity
                """
            )
        )
    ]
    mock_client = MagicMock()
    mock_client.chat.completions.create.return_value = mock_completion
    mock_openai.return_value = mock_client

    # Create agent and run test
    agent = RevisionAgent(api_key="mock_key")
    result = agent.revise_content(sample_content)

    assert isinstance(result, RevisedContent)
    assert "improved content" in result.revised_content.lower()
    assert len(result.changes) == 2
    assert "Made grammatical improvements" in result.revision_summary

@patch('src.revision_agent.agent.RevisionAgent')
def test_revise_content_convenience(mock_agent_class, sample_content):
    """Test the convenience function for revising content."""
    mock_agent = MagicMock()
    mock_agent.revise_content.return_value = RevisedContent(
        original_content=sample_content,
        revised_content="Improved content",
        changes=[
            RevisionChange(
                type="grammar",
                location="p1",
                change="Fixed verb tense"
            )
        ],
        revision_summary="Test summary"
    )
    mock_agent_class.return_value = mock_agent

    result = revise_content(sample_content, api_key="mock_key")

    assert isinstance(result, RevisedContent)
    assert result.revised_content == "Improved content"
    assert len(result.changes) == 1
    assert result.revision_summary == "Test summary" 