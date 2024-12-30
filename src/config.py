"""Configuration module for shared settings across the application."""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Model Configuration
MODEL_NAME = os.getenv('MODEL_NAME', 'o1-2024-12-17')  # Default to gpt-4 if not set
TEMPERATURE = float(os.getenv('TEMPERATURE', '0.7'))  # Default to 0.7 if not set
MAX_TOKENS = int(os.getenv('MAX_TOKENS', '200000'))  # Default to 200000 if not set

# API Configuration
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

def validate_config():
    """Validate that all required configuration is present."""
    if not OPENAI_API_KEY:
        raise ValueError("OPENAI_API_KEY environment variable is required")
    
    if not MODEL_NAME:
        raise ValueError("MODEL_NAME environment variable is required")
    
    if not TEMPERATURE:
        raise ValueError("TEMPERATURE environment variable is required")
    
    if not MAX_TOKENS:
        raise ValueError("MAX_TOKENS environment variable is required") 