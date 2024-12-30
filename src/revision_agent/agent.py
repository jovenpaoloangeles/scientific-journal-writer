from typing import List, Dict
from openai import OpenAI
from .models import RevisionChange, RevisedContent
from .. import config
from ..utils.cost_tracker import cost_tracker
import re

def revise_content(content: str, api_key: str) -> RevisedContent:
    """
    Revise the content for clarity, coherence, and academic style.
    
    Args:
        content: Content to revise
        api_key: OpenAI API key
        
    Returns:
        RevisedContent: Revised content with changes
    """
    client = OpenAI(api_key=api_key)
    
    # Calculate original word count
    word_count = len(re.findall(r'\b\w+\b', content))
    
    prompt = f"""Review and revise this academic text for clarity, coherence, and academic style.
Make specific improvements to enhance:
1. Clarity - Clear writing and well-explained concepts
2. Coherence - Logical flow and smooth transitions
3. Academic Style - Formal tone and appropriate vocabulary

CRITICAL REQUIREMENT: The revised text MUST maintain EXACTLY {word_count} words (±10 words). This is non-negotiable.
You MUST preserve the ENTIRE content and maintain the same word count. Do NOT shorten or truncate the text.
Make targeted improvements to specific sentences or phrases while keeping the overall structure and length intact.

For each change, explain:
1. What was changed
2. Where in the text (e.g., "First paragraph", "Second sentence", etc.)
3. Why the change improves the text

Original text:

{content}

Provide your response in this format:

Revised content:
[The complete revised text - MUST include ALL paragraphs and maintain EXACTLY {word_count} words (±10 words)]

Revision changes:
1. [Location]: [What was changed and why]
2. [Location]: [What was changed and why]
[etc.]

Before submitting your response, you MUST:
1. Count the words in your revised text
2. Verify it has EXACTLY {word_count} words (±10 words)
3. If the word count is off, adjust your text to meet this requirement
4. Only after confirming the word count, verify that:
   - The revised content includes ALL paragraphs from the original text
   - No content has been truncated or removed
   - The overall structure remains the same
   - Each paragraph maintains its original length and scope
   - All key points and arguments are preserved
   - Technical terms and concepts are accurately represented
   - Citations and references are preserved in their original form"""

    response = client.chat.completions.create(
        messages=[
            {"role": "system", "content": "You are an expert academic editor. Focus on making meaningful improvements to clarity, coherence, and academic style while preserving the FULL content and EXACT word count. Do NOT truncate or shorten the text. Make targeted improvements while maintaining the same length and structure."},
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
        operation="revise_content"
    )
    
    # Parse response
    response_text = response.choices[0].message.content
    sections = response_text.split("\n\n")
    
    revised_content = ""
    revision_changes = []
    
    for section in sections:
        if section.startswith("Revised content:"):
            revised_content = section.replace("Revised content:", "").strip()
        elif section.startswith("Revision changes:"):
            changes_text = section.replace("Revision changes:", "").strip()
            for change in changes_text.split("\n"):
                if not change.strip() or ":" not in change:
                    continue
                try:
                    # Extract location and change description
                    location, description = change.split(":", 1)
                    # Remove any numbering from the location
                    location = re.sub(r'^\d+\.\s*', '', location.strip())
                    description = description.strip()
                    
                    revision_changes.append(RevisionChange(
                        type="revision",
                        location=location,
                        change=description
                    ))
                except ValueError:
                    continue
    
    # If no revised content was found or it's empty, use original content
    if not revised_content or not revised_content.strip():
        revised_content = content
    
    # If no changes were found, add a note about that
    if not revision_changes:
        revision_changes.append(RevisionChange(
            type="revision",
            location="General",
            change="No specific changes were needed; the text was already well-written."
        ))
    
    return RevisedContent(
        original_content=content,
        revised_content=revised_content,
        revision_changes=revision_changes,
        revision_summary=f"Made {len(revision_changes)} revisions to improve clarity, coherence, and style while preserving the full content."
    ) 