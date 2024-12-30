from typing import List, Dict, Any
from openai import OpenAI
from .models import GeneratedContent
from .. import config
from ..utils.cost_tracker import cost_tracker

def generate_content(prompt: str, api_key: str) -> str:
    """Generate content using OpenAI API."""
    client = OpenAI(api_key=api_key)
    
    response = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model=config.MODEL_NAME,
        temperature=config.TEMPERATURE,
        max_tokens=config.MAX_TOKENS
    )
    
    # Track costs
    cost_tracker.add_call(
        model=config.MODEL_NAME,
        input_tokens=response.usage.prompt_tokens,
        output_tokens=response.usage.completion_tokens,
        operation="generate_content"
    )
    
    return response.choices[0].message.content

def create_prompt(section_type: str, keypoints: List[str], word_limit: int) -> str:
    """Create a prompt for content generation."""
    formatted_keypoints = chr(10).join(f'- {point}' for point in keypoints)
    
    prompt = f"""Generate an academic {section_type} section that is EXACTLY {word_limit} words (±10%). This is a CRITICAL requirement - if not met, the content will fail validation and be rejected.

Key points to cover:
{formatted_keypoints}

CRITICAL WORD COUNT REQUIREMENT:
The text MUST be between {int(word_limit * 0.7)} and {int(word_limit * 1.1)} words. This is non-negotiable. Content that does not meet this requirement will be rejected. You MUST count your words carefully and adjust your text to meet this requirement before completing your response.

Additional Requirements:
1. Academic style and formal tone
2. Clear paragraph structure
3. Thorough coverage of all key points
4. Logical flow and transitions
5. Technical precision and clarity
6. Balanced treatment of each point
7. Appropriate depth and detail
8. Professional academic language
9. Strong topic sentences

Format your response as a single, well-structured academic text with clear paragraphs. Each paragraph should thoroughly develop one or more related points while maintaining logical flow throughout the entire text.

FINAL WORD COUNT CHECK:
Before submitting your response, you MUST:
1. Count the total words in your text
2. Verify the count is between {int(word_limit * 0.7)} and {int(word_limit * 1.1)} words
3. If the word count is outside this range, revise your text to meet this requirement
4. Only after confirming the word count is correct, verify that:
   - All key points are covered thoroughly
   - The text maintains academic rigor and clarity
   - Each paragraph flows logically to the next
   - Technical terms are used appropriately
   - The overall structure is coherent

IMPORTANT: Include the word count at the end of your response in parentheses."""
    return prompt

def generate_content_version(section_type: str, keypoints: List[str], word_limit: int, api_key: str) -> GeneratedContent:
    """Generate a single version of content."""
    prompt = create_prompt(section_type, keypoints, word_limit)
    content = generate_content(prompt, api_key)
    
    return GeneratedContent(
        content=content,
        section=section_type,
        word_limit=word_limit,
        generation_params={
            "model": config.MODEL_NAME,
            "temperature": config.TEMPERATURE,
            "max_tokens": config.MAX_TOKENS
        }
    ) 

def generate_content_versions(section_type: str, keypoints: List[str], word_limit: int, api_key: str) -> List[GeneratedContent]:
    """
    Generate multiple versions of content based on key points.
    
    Args:
        section_type: Type of section to generate
        keypoints: List of key points to include
        word_limit: Target word count
        api_key: OpenAI API key
        
    Returns:
        List[GeneratedContent]: List of generated content versions
    """
    versions = []
    for _ in range(3):  # Generate 3 versions
        version = generate_content_version(section_type, keypoints, word_limit, api_key)
        versions.append(version)
    return versions 