import openai
from typing import List, Dict
from .models import SelectedContent
from ..reviewer.models import ReviewedContent
from .. import config

def select_best_version(versions: List[ReviewedContent]) -> ReviewedContent:
    """
    Select the best version based on review scores.
    
    Args:
        versions: List of reviewed content versions
        
    Returns:
        ReviewedContent: The selected best version
    """
    if not versions:
        raise ValueError("No versions provided for selection")
    
    # Simple selection based on total score
    return max(versions, key=lambda x: x.total_score) 