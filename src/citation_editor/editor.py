from typing import List, Dict
from openai import OpenAI
from .models import Citation, CitedContent
from ..revision_agent.models import RevisionChange
from .. import config
from ..utils.cost_tracker import cost_tracker
import re

def add_citations(content: str, api_key: str) -> CitedContent:
    """
    Add academic citations to the content.
    
    Args:
        content: Content to add citations to
        api_key: OpenAI API key
        
    Returns:
        CitedContent: Content with citations added
    """
    client = OpenAI(api_key=api_key)
    
    # Calculate original word count
    word_count = len(re.findall(r'\b\w+\b', content))
    
    prompt = f"""Add citation reasons to this text. Citation reasons should be added throughout ALL paragraphs, not just the beginning.

IMPORTANT: You MUST preserve the ENTIRE content and maintain the same word count. Do NOT shorten or truncate the text.
Add citation reasons in square brackets [Reason for citation] at appropriate points while keeping the overall structure and length intact.

Original text:

{content}

Provide your response in this format:

Cited content:
[The complete text with citation reasons added in square brackets - MUST include ALL paragraphs and maintain EXACTLY {word_count} words (±10 words)]

Citations:
1. Location: [Where in text] | Reason: [Why this part needs a citation]
2. Location: [Where in text] | Reason: [Why this part needs a citation]
[etc.]

Before submitting your response, you MUST:
1. Count the words in your text (excluding citation reasons in square brackets)
2. Verify it has EXACTLY {word_count} words (±10 words)
3. If the word count is off, adjust your text to meet this requirement
4. Only after confirming the word count, verify that:
   - The cited content includes ALL paragraphs from the original text
   - No content has been truncated or removed
   - Citation reasons are added throughout ALL paragraphs
   - Each paragraph has at least one citation reason
   - The overall structure remains the same
   - Each paragraph maintains its original length and scope
   - All key points and arguments are preserved
   - Technical terms and concepts are accurately represented"""

    response = client.chat.completions.create(
        messages=[
            {"role": "system", "content": "You are an expert academic citation editor. Your task is to add citation reasons throughout ALL paragraphs of the text, not just the beginning. Add reasons in square brackets to indicate where citations would be helpful. Ensure EVERY paragraph has at least one citation reason. Do NOT truncate or shorten the text."},
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
        operation="add_citations"
    )
    
    # Parse response
    response_text = response.choices[0].message.content
    sections = response_text.split("\n\n")
    
    cited_content = ""
    citations = []
    citation_changes = []
    
    for section in sections:
        if section.startswith("Cited content:"):
            cited_content = section.replace("Cited content:", "").strip()
        elif section.startswith("Citations:"):
            citation_lines = section.replace("Citations:", "").strip().split("\n")
            for line in citation_lines:
                if not line.strip() or "|" not in line:
                    continue
                    
                parts = [p.strip() for p in line.split("|")]
                if len(parts) < 2:
                    continue
                    
                location = parts[0].replace("Location:", "").strip()
                reason = parts[1].replace("Reason:", "").strip()
                
                citations.append(Citation(
                    text=f"[{reason}]",
                    source="Citation reason",
                    location=location,
                    reason=reason
                ))
                
                citation_changes.append(RevisionChange(
                    type="citation",
                    location=location,
                    change=f"Added citation reason: {reason}"
                ))
    
    # If no cited content was found or it's empty, use original content
    if not cited_content or not cited_content.strip():
        cited_content = content
    
    # If no citations were found, add a note about that
    if not citations:
        citations.append(Citation(
            text="[Citation needed]",
            source="No citations provided",
            location="Throughout text",
            reason="Citation reasons are needed to indicate where academic support is required"
        ))
        citation_changes.append(RevisionChange(
            type="citation",
            location="General",
            change="No citation reasons were added; the text requires indications of where academic support is needed"
        ))
    
    citation_summary = f"Added {len(citations)} citation reasons to indicate where academic support is needed throughout the text while preserving the full content."
    
    return CitedContent(
        original_content=content,
        cited_content=cited_content,
        citations=citations,
        citation_changes=citation_changes,
        citation_summary=citation_summary
    ) 