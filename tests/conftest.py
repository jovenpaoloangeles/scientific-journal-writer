import pytest
from typing import List, Dict
from src.input_handler.content_input import ContentInput
from src.reviewer.models import ReviewResult, SectionScore
from src.version_selector.models import SelectedVersion
from src.revision_agent.models import RevisedContent
from src.citation_editor.models import CitedContent, Citation
from src.revision_agent.models import RevisionChange

@pytest.fixture
def sample_input_data() -> ContentInput:
    """Fixture for sample input data."""
    return ContentInput(
        section="Introduction",
        keypoints=["First key point", "Second key point"],
        word_limit=500
    )

@pytest.fixture
def sample_review_result(sample_input_data) -> ReviewResult:
    """Fixture for sample review result."""
    return ReviewResult(
        content="Sample content for review",
        scores=SectionScore(
            relevance=8.5,
            clarity=7.5,
            structure=8.0,
            flow=7.0
        ),
        feedback=["Good point 1", "Could improve point 2"],
        total_score=7.8
    )

@pytest.fixture
def sample_selected_version(sample_review_result) -> SelectedVersion:
    """Fixture for sample selected version."""
    return SelectedVersion(
        selected_content=sample_review_result,
        comparison_summary=["Version 1 was better in clarity"],
        selection_reason="Best overall score",
        improvement_suggestions=["Add more examples"]
    )

@pytest.fixture
def sample_revised_content(sample_selected_version) -> RevisedContent:
    """Fixture for sample revised content."""
    return RevisedContent(
        original_content=sample_selected_version,
        revised_content="Improved content with examples",
        revision_changes=[
            {
                "type": "addition",
                "location": "paragraph 2",
                "change": "Added examples"
            }
        ],
        revision_summary="Added examples for clarity"
    )

@pytest.fixture
def sample_cited_content(sample_revised_content) -> CitedContent:
    """Fixture for sample cited content."""
    return CitedContent(
        original_content=sample_revised_content,
        cited_content="Content with [citation1] and [citation2]",
        citations=[
            Citation(
                text="First citation",
                source="Journal A",
                location="paragraph 1"
            ),
            Citation(
                text="Second citation",
                source="Book B",
                location="paragraph 2"
            )
        ],
        citation_changes=[
            RevisionChange(
                type="citation",
                location="paragraph 1",
                change="Added citation 1"
            ),
            RevisionChange(
                type="citation",
                location="paragraph 2",
                change="Added citation 2"
            )
        ],
        citation_summary="Added citations for claims and methods"
    ) 