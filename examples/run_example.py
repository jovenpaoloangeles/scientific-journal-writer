import os
import sys
import json
from pathlib import Path
from datetime import datetime

# Add the project root directory to Python path
project_root = str(Path(__file__).parent.parent)
sys.path.insert(0, project_root)

from src import config
from src.content_generator import generate_content_versions
from src.reviewer import review_content
from src.version_selector import select_best_version
from src.revision_agent import revise_content
from src.citation_editor import add_citations
from src.publisher import publish_content
from src.utils.cost_tracker import cost_tracker

def save_published_content(published_content, output_dir="output"):
    """Save published content to a JSON file.
    
    Args:
        published_content: The PublishedContent object to save
        output_dir: Directory to save the output file (default: 'output')
    
    Returns:
        str: Path to the saved file
    """
    # Create output directory if it doesn't exist
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Generate filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"published_content_{timestamp}.json"
    file_path = output_path / filename
    
    # Convert published content to dictionary
    content_dict = {
        "formatted_content": published_content.formatted_content,
        "metadata": published_content.metadata,
        "validation": {
            "is_valid": published_content.validation.is_valid,
            "issues": published_content.validation.issues,
            "warnings": published_content.validation.warnings
        }
    }
    
    # Save to JSON file
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(content_dict, f, indent=2, ensure_ascii=False)
    
    return str(file_path)

def main():
    """Run the example workflow."""
    try:
        # Validate configuration
        config.validate_config()
        api_key = config.OPENAI_API_KEY

        # Example input
        section_type = "Introduction"
        keypoints = [
        "Gold nanoparticles are versatile materials used in catalysis, sensing, and biomedical applications.",
        "Their unique optical properties, especially localized surface plasmon resonance (LSPR), make them suitable for Surface-Enhanced Raman Scattering (SERS).",
        "Optimizing synthesis conditions for desired nanoparticle morphologies and properties is challenging due to complex parameter interdependencies.",
        "This study uses Bayesian Optimization to systematically optimize synthesis conditions for gold nanoparticles.",
        "The optimization focuses on maximizing the wavelength of maximum absorption (λmax) to enhance SERS activity.",
        "Key parameters include gold salt concentration, reducing agent concentration, and temperature."
        ]

        word_limit = 1000

        print("1. Processing input...")
        print(f"Section type: {section_type}")
        print(f"Keypoints: {keypoints}")
        print(f"Word limit: {word_limit}")

        # Generate multiple content versions
        print("\n2. Generating content versions...")
        versions = generate_content_versions(
            section_type=section_type,
            keypoints=keypoints,
            word_limit=word_limit,
            api_key=api_key,
            num_versions=5
        )
        print(f"Generated {len(versions)} versions")
        for i, version in enumerate(versions, 1):
            print(f"\nVersion {i}:")
            print(str(version))

        # Review and score each version
        print("\n3. Reviewing content versions...")
        reviewed_versions = [
            review_content(version.content, api_key=api_key)
            for version in versions
        ]
        scores = [str(version.total_score) for version in reviewed_versions]
        print(f"Review scores: {scores}")

        # Select the best version
        print("\n4. Selecting best version...")
        selected_version = select_best_version(reviewed_versions)
        print(f"Selected version with score: {selected_version.total_score:.2f}")
        print(f"Selected content:\n{selected_version.content}")

        # Revise the selected content
        print("\n5. Revising content...")
        revised_content = revise_content(selected_version.content, api_key=api_key)
        print("Content revised")
        print(f"Revised content:\n{revised_content.revised_content}")
        print("\nRevision changes:")
        for change in revised_content.revision_changes:
            print(f"- {change.type} ({change.location}): {change.change}")

        # Add citations
        print("\n6. Adding citations...")
        cited_content = add_citations(revised_content.revised_content, api_key=api_key)
        print("Citations added")
        print(f"Cited content:\n{cited_content.cited_content}")
        print("\nCitations:")
        for citation in cited_content.citations:
            print(f"- {citation.text} (Source: {citation.source}, Location: {citation.location})")

        # Add publishing step
        print("\n7. Publishing content...")
        published_content = publish_content(cited_content)
        print("Content published successfully!")
        
        # Save to JSON file
        output_file = save_published_content(published_content)
        print(f"\nContent saved to: {output_file}")
        
        print("\nValidation results:")
        print(f"Valid: {published_content.validation.is_valid}")
        if published_content.validation.issues:
            print("Issues:")
            for issue in published_content.validation.issues:
                print(f"- {issue}")
        if published_content.validation.warnings:
            print("Warnings:")
            for warning in published_content.validation.warnings:
                print(f"- {warning}")
        
        print("\nMetadata:")
        for key, value in published_content.metadata.items():
            if isinstance(value, dict):
                print(f"- {key}:")
                for k, v in value.items():
                    print(f"  - {k}: {v}")
            else:
                print(f"- {key}: {value}")

        # Print cost summary
        cost_tracker.print_summary()

        print("\nProcess completed successfully!")

    except Exception as e:
        print(f"\nError occurred: {str(e)}")
        import traceback
        print("\nTraceback:")
        print(traceback.format_exc())

if __name__ == "__main__":
    main() 