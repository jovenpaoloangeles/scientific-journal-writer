"""Version selector module for choosing the best content version."""
from .models import SelectedContent
from .selector import select_best_version

__all__ = ['select_best_version', 'SelectedContent'] 