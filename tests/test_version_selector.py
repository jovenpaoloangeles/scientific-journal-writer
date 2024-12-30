import pytest
from unittest.mock import patch, MagicMock
from src.version_selector import VersionSelector, select_best_version
from src.version_selector.models import SelectedVersion
from src.reviewer.models import ReviewResult, SectionScore

def test_selected_version_creation(sample_review_result):
    """Test creating a SelectedVersion instance."""
    selected = SelectedVersion(
        selected_content=sample_review_result,
        comparison_summary=["Version 1 better"],
        selection_reason="Highest score",
        improvement_suggestions=["Add examples"]
    )
    assert selected.selected_content == sample_review_result
    assert len(selected.comparison_summary) == 1
    assert len(selected.improvement_suggestions) == 1

@patch('dspy.ChainOfThought')
def test_version_comparison(mock_chain):
    """Test version comparison with mocked DSPY."""
    # Create a mock comparator that returns the response
    mock_comparator = MagicMock()
    mock_comparator.return_value = {
        'comparison_summary': ["Version 1 better"],
        'selection_reason': "Best score",
        'improvements': ["Add examples"]
    }

    # Set up the chain mock
    mock_instance = MagicMock()
    mock_instance.return_value = mock_comparator
    mock_chain.return_value = mock_instance

    selector = VersionSelector()
    versions = [
        ReviewResult(
            content="Content 1",
            scores=SectionScore(relevance=8.0, clarity=7.0, structure=6.0, flow=5.0),
            feedback=["Good"],
            total_score=7.0
        ),
        ReviewResult(
            content="Content 2",
            scores=SectionScore(relevance=9.0, clarity=8.0, structure=7.0, flow=6.0),
            feedback=["Better"],
            total_score=8.0
        )
    ]

    result = selector.select_version(versions)

    assert isinstance(result, SelectedVersion)
    assert result.selected_content == versions[1]
    assert result.comparison_summary == ["Version 1 better"]
    assert result.selection_reason == "Best score"
    assert result.improvement_suggestions == ["Add examples"]

def test_version_selector_empty_list():
    """Test version selector with empty list."""
    selector = VersionSelector()
    with pytest.raises(ValueError):
        selector.select_version([])

@patch('src.version_selector.selector.VersionSelector')
def test_select_best_version_convenience(mock_selector_class, sample_review_result):
    """Test the convenience function for version selection."""
    mock_selector = MagicMock()
    mock_selector.select_version.return_value = SelectedVersion(
        selected_content=sample_review_result,
        comparison_summary=["Test comparison"],
        selection_reason="Test reason",
        improvement_suggestions=["Test suggestion"]
    )
    mock_selector_class.return_value = mock_selector
    
    result = select_best_version([sample_review_result])
    assert isinstance(result, SelectedVersion)
    assert mock_selector.select_version.called 