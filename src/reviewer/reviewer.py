from typing import List, Dict
from openai import OpenAI
from .models import ReviewedContent, ReviewScore, ReviewCriteria
from .. import config
from ..utils.cost_tracker import cost_tracker
import re

def extract_score(score_text: str) -> float:
    """Extract numeric score from score text."""
    # Try to find X/10 pattern first
    score_match = re.search(r'(\d+)/10', score_text)
    if score_match:
        return float(score_match.group(1))
    
    # Try to find just the number
    score_match = re.search(r'(\d+(?:\.\d+)?)', score_text)
    if score_match:
        return float(score_match.group(1))
    
    return 0.0

def review_content(content: str, api_key: str) -> ReviewedContent:
    """
    Review content for quality and academic standards.
    
    Args:
        content: Content to review
        api_key: OpenAI API key
        
    Returns:
        ReviewedContent: Reviewed content with scores and feedback
    """
    client = OpenAI(api_key=api_key)
    
    prompt = f"""Review this academic text for quality. Score each criterion from 1-10 (where 10 is excellent) and provide specific feedback.

Text to review:

{content}

Evaluate these criteria:

1. Clarity (Score 1-10)
- Clear and concise writing
- Well-explained concepts
- Appropriate use of technical terms
- Minimal ambiguity
Score guidelines:
- 8-10: Excellent clarity, concepts are explained exceptionally well
- 6-7: Good clarity, most concepts are well explained
- 4-5: Average clarity, some concepts need better explanation
- 1-3: Poor clarity, significant improvement needed

2. Coherence (Score 1-10)
- Logical flow between ideas
- Smooth transitions between paragraphs
- Clear connections between concepts
- Consistent argument development
Score guidelines:
- 8-10: Excellent flow and connections between ideas
- 6-7: Good flow with minor transition issues
- 4-5: Average flow, some disconnected ideas
- 1-3: Poor flow, major coherence issues

3. Academic Style (Score 1-10)
- Formal and professional tone
- Appropriate vocabulary
- Objective presentation
- Scholarly language
Score guidelines:
- 8-10: Excellent academic style and professionalism
- 6-7: Good academic style with minor issues
- 4-5: Average style, needs more formality
- 1-3: Poor style, significant improvement needed

4. Content Quality (Score 1-10)
- Thorough coverage of topic
- Accurate information
- Depth of analysis
- Balanced presentation
Score guidelines:
- 8-10: Excellent depth and accuracy
- 6-7: Good coverage with minor gaps
- 4-5: Average depth, needs more detail
- 1-3: Poor coverage, major improvements needed

5. Structure (Score 1-10)
- Well-organized paragraphs
- Clear introduction and conclusion
- Appropriate section lengths
- Logical progression
Score guidelines:
- 8-10: Excellent organization and structure
- 6-7: Good structure with minor issues
- 4-5: Average structure, needs improvement
- 1-3: Poor structure, major reorganization needed

For each criterion:
1. Provide a score from 1-10 (10 being excellent)
2. Give specific examples from the text
3. Suggest improvements if needed

Provide output in this exact format:

SCORES:
Clarity: [X]/10 | Feedback: [specific feedback with examples]
Coherence: [X]/10 | Feedback: [specific feedback with examples]
Academic Style: [X]/10 | Feedback: [specific feedback with examples]
Content Quality: [X]/10 | Feedback: [specific feedback with examples]
Structure: [X]/10 | Feedback: [specific feedback with examples]

OVERALL FEEDBACK:
[Comprehensive feedback about strengths and specific areas for improvement]

Note: Replace [X] with a numeric score between 1 and 10. Consider the score guidelines carefully when assigning scores. For academic papers of this quality, scores should typically be in the 6-10 range unless there are significant issues."""

    response = client.chat.completions.create(
        messages=[
            {"role": "system", "content": "You are an expert academic reviewer with extensive experience in evaluating scientific papers. Evaluate the text thoroughly and provide detailed, constructive feedback. Be specific in your scoring and justify your ratings with examples from the text. Use the provided scoring guidelines to ensure consistent and fair evaluation. For academic papers of this quality, scores should typically be in the 6-10 range unless there are significant issues."},
            {"role": "user", "content": prompt}
        ],
        model=config.MODEL_NAME,
        temperature=config.TEMPERATURE,
        max_tokens=config.MAX_TOKENS
    )
    
    # Track costs
    cost_tracker.add_call(
        model=config.MODEL_NAME,
        input_tokens=response.usage.prompt_tokens,
        output_tokens=response.usage.completion_tokens,
        operation="review_content"
    )
    
    # Parse response
    response_text = response.choices[0].message.content
    sections = response_text.split("\n\n")
    
    # Initialize scores and feedback
    scores = {}
    overall_feedback = ""
    
    for section in sections:
        if section.startswith("SCORES:"):
            scores_text = section.replace("SCORES:", "").strip()
            for score_line in scores_text.split("\n"):
                if ":" not in score_line or "|" not in score_line:
                    continue
                    
                try:
                    # Split into criterion and rest
                    criterion, rest = score_line.split(":", 1)
                    criterion = criterion.strip()
                    
                    # Split rest into score and feedback
                    score_part, feedback_part = rest.split("|", 1)
                    
                    # Extract score using helper function
                    score = extract_score(score_part)
                    
                    # Extract feedback
                    feedback = feedback_part.replace("Feedback:", "").strip()
                    
                    # Convert criterion name to enum format
                    criterion_key = criterion.upper().replace(" ", "_")
                    if criterion_key in ReviewCriteria.__members__:
                        scores[criterion_key] = ReviewScore(
                            criterion=ReviewCriteria[criterion_key],
                            score=score,
                            feedback=feedback
                        )
                except (ValueError, KeyError, AttributeError) as e:
                    print(f"Warning: Could not parse score for {criterion}: {e}")
                    continue
                    
        elif section.startswith("OVERALL FEEDBACK:"):
            overall_feedback = section.replace("OVERALL FEEDBACK:", "").strip()
    
    # Ensure we have all criteria with default scores
    for criterion in ReviewCriteria:
        if criterion.name not in scores:
            scores[criterion.name] = ReviewScore(
                criterion=criterion,
                score=6.0,  # Default to 6.0 for missing scores
                feedback="No specific feedback provided for this criterion"
            )
    
    # Calculate total score (average of all scores)
    total_score = sum(score.score for score in scores.values()) / len(scores) if scores else 6.0
    
    return ReviewedContent(
        content=content,
        scores=list(scores.values()),
        total_score=total_score,
        overall_feedback=overall_feedback or "No overall feedback provided"
    ) 