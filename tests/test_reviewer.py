import pytest
from unittest.mock import patch, MagicMock
from src.reviewer import ContentReviewer, review_content
from src.reviewer.models import SectionScore, ReviewResult

def test_section_score():
    """Test section score calculation."""
    score = SectionScore(
        relevance=9.0,
        clarity=8.0,
        structure=7.0,
        flow=6.0
    )
    weighted_score = score.calculate_weighted_score()
    expected_score = 9.0 * 0.4 + 8.0 * 0.3 + 7.0 * 0.2 + 6.0 * 0.1
    assert weighted_score == pytest.approx(expected_score)

def test_section_score_validation():
    """Test section score validation."""
    with pytest.raises(ValueError):
        SectionScore(
            relevance=11.0,  # Invalid score > 10
            clarity=8.0,
            structure=7.0,
            flow=6.0
        )

def test_review_result():
    """Test review result creation."""
    score = SectionScore(
        relevance=9.0,
        clarity=8.0,
        structure=7.0,
        flow=6.0
    )
    result = ReviewResult(
        content="Test content",
        scores=score,
        feedback=["Good", "Needs work"],
        total_score=8.0
    )
    assert result.content == "Test content"
    assert len(result.feedback) == 2
    assert result.total_score == 8.0

@patch('dspy.ChainOfThought')
def test_content_review(mock_chain, sample_input_data):
    """Test content review with mocked DSPY."""
    # Create a mock reviewer that returns the response
    mock_reviewer = MagicMock()
    mock_reviewer.return_value = {
        'relevance': 8.0,
        'clarity': 7.0,
        'structure': 6.0,
        'flow': 5.0,
        'feedback': ["Good point"]
    }

    # Set up the chain mock
    mock_instance = MagicMock()
    mock_instance.return_value = mock_reviewer
    mock_chain.return_value = mock_instance

    reviewer = ContentReviewer()
    result = reviewer.review_version(
        content="Test content",
        input_data=sample_input_data
    )

    assert isinstance(result, ReviewResult)
    assert result.content == "Test content"
    assert result.scores.relevance == 8.0
    assert result.scores.clarity == 7.0
    assert result.scores.structure == 6.0
    assert result.scores.flow == 5.0
    assert result.feedback == ["Good point"]
    assert result.total_score == 6.5

@patch('src.reviewer.reviewer.ContentReviewer')
def test_review_content_convenience(mock_reviewer_class, sample_input_data):
    """Test the convenience function for content review."""
    mock_reviewer = MagicMock()
    mock_reviewer.review_versions.return_value = [
        ReviewResult(
            content="Content 1",
            scores=SectionScore(relevance=8.0, clarity=7.0, structure=6.0, flow=5.0),
            feedback=["Good"],
            total_score=7.0
        )
    ]
    mock_reviewer_class.return_value = mock_reviewer
    
    results = review_content(["Content 1"], sample_input_data)
    assert len(results) == 1
    assert isinstance(results[0], ReviewResult)
    assert mock_reviewer.review_versions.called 