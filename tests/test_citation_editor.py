import pytest
from unittest.mock import patch, MagicMock
from src.citation_editor import CitationEditor, add_citations
from src.citation_editor.models import Citation, CitedContent
from src.revision_agent.models import RevisionChange

def test_citation_creation():
    """Test creating a Citation instance."""
    citation = Citation(
        text="Test statement",
        source="Journal A",
        location="paragraph 1"
    )
    assert isinstance(citation, Citation)
    assert citation.text == "Test statement"
    assert citation.source == "Journal A"
    assert citation.location == "paragraph 1"

def test_cited_content_creation(sample_revised_content):
    """Test creating a CitedContent instance."""
    cited = CitedContent(
        original_content=sample_revised_content,
        cited_content="Content with [citation]",
        citations=[
            Citation(
                text="Test citation",
                source="Journal A",
                location="p1"
            )
        ],
        citation_changes=[
            RevisionChange(
                type="citation",
                location="p1",
                change="Added citation"
            )
        ],
        citation_summary="Added citations"
    )
    assert isinstance(cited, CitedContent)
    assert cited.original_content == sample_revised_content
    assert cited.cited_content == "Content with [citation]"
    assert len(cited.citations) == 1
    assert len(cited.citation_changes) == 1
    assert cited.citation_summary == "Added citations"

@patch('openai.OpenAI')
def test_citation_editor(mock_openai, sample_revised_content):
    """Test citation editor with mocked OpenAI."""
    # Mock OpenAI response
    mock_completion = MagicMock()
    mock_completion.choices = [
        MagicMock(
            message=MagicMock(
                content="""
                CITED CONTENT:
                Content with [citation1] and [citation2]

                CITATIONS:
                1. First statement: Journal A - paragraph 1
                2. Second statement: Book B - paragraph 2

                SUMMARY:
                Added citations for key claims
                """
            )
        )
    ]
    mock_client = MagicMock()
    mock_client.chat.completions.create.return_value = mock_completion
    mock_openai.return_value = mock_client

    # Create editor and run test
    editor = CitationEditor(api_key="mock_key")
    result = editor.add_citations(sample_revised_content)

    assert isinstance(result, CitedContent)
    assert "Content with [citation1] and [citation2]" in result.cited_content
    assert len(result.citations) == 2
    assert len(result.citation_changes) == 2
    assert "Added citations for key claims" in result.citation_summary

@patch('src.citation_editor.editor.CitationEditor')
def test_add_citations_convenience(mock_editor_class, sample_revised_content):
    """Test the convenience function for adding citations."""
    mock_editor = MagicMock()
    mock_editor.add_citations.return_value = CitedContent(
        original_content=sample_revised_content,
        cited_content="Content with [citation]",
        citations=[
            Citation(
                text="Test",
                source="Journal A",
                location="p1"
            )
        ],
        citation_changes=[
            RevisionChange(
                type="citation",
                location="p1",
                change="Added citation"
            )
        ],
        citation_summary="Test summary"
    )
    mock_editor_class.return_value = mock_editor

    result = add_citations(sample_revised_content, api_key="mock_key")

    assert isinstance(result, CitedContent)
    assert result.cited_content == "Content with [citation]"
    assert len(result.citations) == 1
    assert len(result.citation_changes) == 1
    assert result.citation_summary == "Test summary" 