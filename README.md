# Project VizTree: Python Project Structure Visualizer

[![CI](https://github.com/NoManNayeem/Manchitra_SDK/actions/workflows/ci.yml/badge.svg)](https://github.com/NoManNayeem/Manchitra_SDK/actions/workflows/ci.yml)

Project VizTree is a Python package and CLI tool that generates interactive visualizations of your project structure, compatible with Django, DRF, Flask, and FastAPI. It uses UV for fast dependency management and Bootstrap for interactive tree diagrams.

## Features

- 🌳 **Interactive Tree Visualization**: Browse your project structure with an intuitive tree interface
- 🔍 **Framework Detection**: Automatically detects Django, Flask, FastAPI, Pyramid, and Tornado projects
- 🚀 **Fast Performance**: Built with UV for lightning-fast dependency management
- 🎨 **Modern UI**: Beautiful Bootstrap-powered interface with responsive design
- 📊 **Multiple Views**: Tree view and diagram view for different perspectives
- 🔧 **CLI Tool**: Easy-to-use command-line interface
- 🌐 **Web Server**: Built-in FastAPI server for web-based visualization

## Installation

### Using UV (Recommended)

```bash
# Install UV if you haven't already
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create a new project directory
mkdir my-project
cd my-project

# Initialize with UV
uv init --python 3.11
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install Project VizTree
uv add projviz
```

### Traditional pip Installation

```bash
pip install projviz
```

## Quick Start

1. Navigate to your project:
```bash
cd /path/to/your/python/project
```

2. Generate project structure:
```bash
projviz scan --output structure.json
```

3. Start visualization server:
```bash
projviz serve --json structure.json --port 8000
```

4. Open your browser to http://localhost:8000

## How to Use

Using UV in editable mode and the CLI:

```powershell
# Install in editable mode
uv pip install -e .

# Scan your project and print a nested list
projviz scan --output structure.json --list

# Serve the UI on port 8000
projviz serve --json-file structure.json --port 8000
```

The scan output uses two-space indentation and prefixes folders with `=` and files with `-` for easy reading. The UI shows a collapsible tree on the left and a file preview on the right with line numbers, copy button, and wrap toggle. Markdown files (e.g., `README.md`) render as formatted HTML for better readability.

## CLI Commands

### Scan Project Structure
```bash
projviz scan [OPTIONS]

Options:
  --path TEXT     Path to the project directory [default: .]
  --output TEXT   Output JSON file name [default: project_structure.json]
```

### Start Visualization Server
```bash
projviz serve [OPTIONS]

Options:
  --json-file TEXT  JSON file with project structure [default: project_structure.json]
  --port INTEGER    Port to run the server on [default: 8000]
  --host TEXT       Host to bind the server to [default: localhost]
```

### Scan and Serve in One Command
```bash
projviz run [OPTIONS]

Options:
  --path TEXT     Path to the project directory [default: .]
  --output TEXT   Output JSON file name [default: project_structure.json]
  --port INTEGER  Port to run the server on [default: 8000]
  --host TEXT     Host to bind the server to [default: localhost]
```

## Supported Frameworks

Project VizTree automatically detects and provides enhanced visualization for:

- **Django**: Detects `manage.py`, `settings.py`, `wsgi.py`, `asgi.py`
- **Flask**: Detects `app.py`, `application.py`, `flask_app.py`
- **FastAPI**: Detects `main.py`, `app.py`, `fastapi_app.py`
- **Pyramid**: Detects `development.ini`, `production.ini`
- **Tornado**: Detects tornado-specific patterns

## Project Structure

```
projviz/
├── pyproject.toml
├── README.md
├── LICENSE
├── src/
│   └── projviz/
│       ├── __init__.py
│       ├── cli.py
│       ├── scanner.py
│       ├── server.py
│       ├── framework_detection.py
│       └── templates/
│           ├── base.html
│           ├── tree.html
│           └── diagram.html
└── tests/
    ├── test_scanner.py
    ├── test_cli.py
    └── test_frameworks.py
```

## Advanced Usage

### Customizing the Tree View

```python
from projviz import ProjectScanner

scanner = ProjectScanner('/path/to/project')
scanner.ignore_patterns = ['.git', '__pycache__', '*.pyc']  # Custom ignore patterns
data = scanner.scan_project()
```

### Framework Integration Examples

#### Django Integration
Add to your Django project's `urls.py`:

```python
from django.urls import path
from projviz.integrations.django import get_project_tree

urlpatterns = [
    # ... your existing URLs
    path('api/project-tree/', get_project_tree, name='project_tree'),
]
```

#### FastAPI Integration
Add to your FastAPI app:

```python
from fastapi import APIRouter
from projviz.integrations.fastapi import get_project_tree

router = APIRouter()
router.include_router(get_project_tree(), prefix="/api/project-tree")
```

## Building and Publishing with UV

### Build the package:
```bash
uv build
```

### Publish to PyPI:
```bash
uv publish
```

### Install in development mode:
```bash
uv pip install -e .
```

## Testing

Run tests with UV:
```bash
uv run pytest tests/
```

## API Endpoints

When running the server, the following endpoints are available:

- `GET /` - Main tree visualization interface (Bootstrap UI)
- `GET /diagram` - Overview card view
- `GET /api/tree` - JSON data for the project tree
- `GET /api/metadata` - Project metadata (name, framework, scan date)
- `GET /api/file?path=...` - File preview API returning JSON `{ content, encoding, truncated, size }`

## UI Highlights

- Accessible ARIA Tree with keyboard navigation and search
- Neumorphism surfaces with high-contrast tuning; dark mode toggle
- Code viewer with line numbers, wrap toggle, and one‑click Copy
- File type icons and color accents for quick scanning

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

MIT License - see LICENSE file for details.

## Support

For issues and questions:

- Check the documentation
- Search existing GitHub issues
- Create a new issue with detailed information

## Author

- Name: Nayeem Islam
- Email: islam.nayeem@outlook.com
- Medium: https://medium.com/@NoManNayeem
- LinkedIn: https://www.linkedin.com/in/islamnayeem
- GitHub: https://github.com/NoManNayeem
- Repository: Manchitra_SDK

If you use this project, consider giving a star on GitHub.

## Changelog

### v0.1.0
- Initial release
- Basic project structure scanning
- Framework detection for Django, Flask, FastAPI
- Interactive Bootstrap-based tree visualization
- CLI interface with scan and serve commands
- FastAPI web server
- Comprehensive test suite

---

This package provides a comprehensive solution for visualizing Python project structures with support for major frameworks and efficient dependency management using UV.



