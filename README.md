# Scientific Journal Article Writer

A Python-based content expansion system that uses LLMs to generate, review, and refine scientific article content.

## Features

- Content input management for article sections
- Multiple content generation using GPT-4
- Automated content review and scoring
- Content revision and refinement
- Inline citation management
- JSON-formatted output

## Setup

1. Create a virtual environment using uv:
```bash
uv venv
```

2. Activate the virtual environment:
- Windows:
```bash
.venv/Scripts/activate
```
- Unix/MacOS:
```bash
source .venv/bin/activate
```

3. Install dependencies:
```bash
uv pip install -r requirements.txt
```

4. Create a `.env` file with your API keys:
```env
OPENAI_API_KEY=your_api_key_here
```

## Project Structure

```
journal_writer/
├── src/
│   ├── input_handler/
│   ├── content_generator/
│   ├── reviewer/
│   ├── revision_agent/
│   ├── citation_editor/
│   └── publisher/
├── tests/
├── .env
├── requirements.txt
└── README.md
```

## Usage

1. Input your content:
```python
from src.input_handler import ContentInput

input_data = ContentInput(
    section="Introduction",
    keypoints=["point1", "point2"],
    word_limit=500
)
```

2. Generate and process content:
```python
from src.content_generator import generate_content
from src.reviewer import review_content
from src.revision_agent import revise_content
from src.citation_editor import add_citations
from src.publisher import publish_content

# Generate multiple versions
versions = generate_content(input_data)

# Review and select best version
reviewed_versions = review_content(versions)
best_version = select_best_version(reviewed_versions)

# Revise and add citations
revised_content = revise_content(best_version)
final_content = add_citations(revised_content)

# Publish
output = publish_content(final_content)
```

## Testing

Run tests using pytest:
```bash
pytest tests/
```

## License

MIT License 