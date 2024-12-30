from typing import Dict, Any

class ContentConfig:
    """Configuration class for content generation."""
    
    @staticmethod
    def get_default_config() -> Dict[str, Any]:
        """
        Get default configuration settings.
        
        Returns:
            Dict: Default configuration
        """
        return {
            "model": "o1-2024-12-17",
            "temperature": 0.7,
            "max_tokens": 200000,
        }

    @staticmethod
    def get_prompt_template(section_type: str) -> str:
        """
        Get the prompt template for a specific section type.
        
        Args:
            section_type: Type of the section (e.g., Introduction, Methodology)
            
        Returns:
            str: Prompt template for the section
        """
        templates = {
            "Introduction": """
                Write an academic introduction section that covers these key points:
                {keypoints}
                
                The content should:
                - Be approximately {word_limit} words
                - Follow academic writing style
                - Be clear and concise
                - Flow logically between points
                - Set up the context for the rest of the paper
            """,
            "Methodology": """
                Write an academic methodology section that covers these key points:
                {keypoints}
                
                The content should:
                - Be approximately {word_limit} words
                - Be detailed and precise
                - Follow academic writing conventions
                - Explain methods clearly for reproducibility
                - Include any relevant technical details
            """,
            "Results": """
                Write an academic results section that covers these key points:
                {keypoints}
                
                The content should:
                - Be approximately {word_limit} words
                - Present findings objectively
                - Use academic language
                - Focus on data and observations
                - Avoid interpretation (save for discussion)
            """,
            "Discussion": """
                Write an academic discussion section that covers these key points:
                {keypoints}
                
                The content should:
                - Be approximately {word_limit} words
                - Interpret the results
                - Connect findings to existing literature
                - Address implications
                - Acknowledge limitations
            """,
            "Conclusion": """
                Write an academic conclusion section that covers these key points:
                {keypoints}
                
                The content should:
                - Be approximately {word_limit} words
                - Summarize main findings
                - Highlight significance
                - Suggest future directions
                - End with impact statement
            """
        }
        
        return templates.get(section_type, """
            Write an academic section that covers these key points:
            {keypoints}
            
            The content should:
            - Be approximately {word_limit} words
            - Follow academic writing style
            - Be clear and well-structured
            - Address all key points thoroughly
        """) 