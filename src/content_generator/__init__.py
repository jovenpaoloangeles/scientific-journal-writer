"""Content generator module for creating content versions."""
from .models import GeneratedContent
from .generator import generate_content_version

def generate_content_versions(section_type: str, keypoints: list, word_limit: int, api_key: str, num_versions: int = 3) -> list:
    """Generate multiple versions of content."""
    return [
        generate_content_version(section_type, keypoints, word_limit, api_key)
        for _ in range(num_versions)
    ]

__all__ = ['generate_content_versions', 'generate_content_version', 'GeneratedContent'] 