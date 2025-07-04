# Contributing to Canvas Course Gamification Framework

We welcome contributions to the Canvas Course Gamification Framework! This document provides guidelines for contributing to the project.

## Table of Contents

1. [Code of Conduct](#code-of-conduct)
2. [Getting Started](#getting-started)
3. [Development Setup](#development-setup)
4. [Making Contributions](#making-contributions)
5. [Coding Standards](#coding-standards)
6. [Testing](#testing)
7. [Documentation](#documentation)
8. [Review Process](#review-process)

## Code of Conduct

This project follows a standard code of conduct. By participating, you agree to uphold this code. Please report unacceptable behavior to the project maintainers.

### Our Standards

- Use welcoming and inclusive language
- Be respectful of differing viewpoints and experiences
- Gracefully accept constructive criticism
- Focus on what is best for the community
- Show empathy towards other community members

## Getting Started

### Types of Contributions

We welcome several types of contributions:

- **Bug Reports**: Report issues you've encountered
- **Feature Requests**: Suggest new functionality
- **Code Contributions**: Fix bugs or implement features
- **Documentation**: Improve or expand documentation
- **Examples**: Add new course examples or templates
- **Testing**: Add test cases or improve test coverage

### Before You Start

1. Check existing [issues](https://github.com/yourusername/canvas-course-gamification/issues) and [pull requests](https://github.com/yourusername/canvas-course-gamification/pulls)
2. For significant changes, open an issue first to discuss the approach
3. Make sure you can legally contribute (no employer restrictions, etc.)

## Development Setup

### Prerequisites

- Python 3.8+
- Git
- Canvas LMS test instance (optional but recommended)

### Setup Instructions

1. **Fork and Clone**
   ```bash
   git clone https://github.com/your-username/canvas-course-gamification.git
   cd canvas-course-gamification
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt  # Development dependencies
   ```

4. **Configure Environment**
   ```bash
   cp .env.example .env
   # Edit .env with your test Canvas credentials (if available)
   ```

5. **Run Tests**
   ```bash
   pytest
   ```

### Development Dependencies

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Or install individually
pip install pytest pytest-cov black flake8 mypy pre-commit
```

## Making Contributions

### Workflow

1. **Create a Branch**
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b bugfix/issue-number
   ```

2. **Make Changes**
   - Write code following our coding standards
   - Add tests for new functionality
   - Update documentation as needed

3. **Test Your Changes**
   ```bash
   # Run tests
   pytest
   
   # Check code formatting
   black --check .
   
   # Check linting
   flake8
   
   # Type checking
   mypy src/
   ```

4. **Commit Changes**
   ```bash
   git add .
   git commit -m "Brief description of changes"
   ```

5. **Push and Create Pull Request**
   ```bash
   git push origin feature/your-feature-name
   ```
   Then create a pull request on GitHub.

### Commit Message Guidelines

Use clear, descriptive commit messages:

```
Add support for custom XP multipliers

- Implement XP multiplier configuration in gamification.yml
- Add validation for multiplier values
- Update documentation with examples
- Add tests for multiplier calculations

Fixes #123
```

Format:
- First line: Brief summary (50 characters or less)
- Blank line
- Detailed description if needed
- Reference related issues

## Coding Standards

### Python Style

We follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) with some modifications:

- Line length: 88 characters (Black default)
- Use double quotes for strings
- Use type hints for function signatures
- Use docstrings for all public functions and classes

### Code Formatting

We use [Black](https://black.readthedocs.io/) for code formatting:

```bash
# Format all Python files
black .

# Check formatting without making changes
black --check .
```

### Linting

We use [flake8](https://flake8.pycqa.org/) for linting:

```bash
flake8 src/ tests/
```

### Type Checking

We use [mypy](http://mypy-lang.org/) for static type checking:

```bash
mypy src/
```

### Import Organization

Organize imports in this order:
1. Standard library imports
2. Third-party imports
3. Local application imports

```python
import json
import logging
from pathlib import Path
from typing import Dict, List, Optional

import requests
from canvasapi import Canvas

from ..canvas_api import CanvasAPIClient
from .gamification import SkillTree
```

## Testing

### Test Structure

```
tests/
├── unit/           # Unit tests for individual components
├── integration/    # Integration tests with Canvas API
├── fixtures/       # Test data and fixtures
└── conftest.py     # Pytest configuration
```

### Writing Tests

#### Unit Tests

```python
import pytest
from src.gamification import SkillNode, SkillLevel

def test_skill_node_creation():
    node = SkillNode(
        id="test_node",
        name="Test Node",
        description="Test description",
        level=SkillLevel.APPLICATION,
        xp_required=100
    )
    
    assert node.id == "test_node"
    assert node.level == SkillLevel.APPLICATION
    assert node.xp_required == 100

def test_skill_node_unlock_requirements():
    node = SkillNode(
        id="advanced_node",
        name="Advanced Node",
        description="Advanced concepts",
        level=SkillLevel.SYNTHESIS,
        xp_required=500,
        prerequisites=["basic_node"]
    )
    
    # Test with insufficient progress
    progress = {"total_xp": 300}
    assert not node.is_unlocked(progress)
    
    # Test with sufficient progress
    progress = {
        "total_xp": 600,
        "basic_node": {"completed": True}
    }
    assert node.is_unlocked(progress)
```

#### Integration Tests

```python
import pytest
from src.canvas_api import CanvasAPIClient

@pytest.mark.integration
def test_canvas_connection(canvas_client):
    """Test Canvas API connection with real instance."""
    assert canvas_client.validate_connection()

@pytest.mark.integration 
def test_module_creation(canvas_client, test_course_id):
    """Test module creation in Canvas."""
    module_data = {
        "name": "Test Module",
        "position": 1
    }
    
    module = canvas_client.create_module(test_course_id, **module_data)
    assert module["name"] == "Test Module"
    assert module["position"] == 1
```

### Test Fixtures

```python
# In conftest.py
import pytest
from src.canvas_api import CanvasAPIClient

@pytest.fixture
def canvas_client():
    """Provide Canvas API client for testing."""
    return CanvasAPIClient()

@pytest.fixture
def sample_course_config():
    """Provide sample course configuration."""
    return {
        "modules": [
            {
                "id": "module_1",
                "name": "Introduction",
                "gamification": {
                    "skill_level": "recognition",
                    "xp_required": 0
                }
            }
        ]
    }
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src

# Run specific test file
pytest tests/unit/test_gamification.py

# Run integration tests (requires Canvas setup)
pytest tests/integration/ --canvas-instance

# Run with verbose output
pytest -v

# Run and generate HTML coverage report
pytest --cov=src --cov-report=html
```

## Documentation

### Documentation Standards

- Use clear, concise language
- Include code examples
- Keep documentation up to date with code changes
- Use proper Markdown formatting

### Types of Documentation

1. **API Documentation**: Document all public classes and methods
2. **User Guides**: Step-by-step instructions for users
3. **Developer Guides**: Technical documentation for contributors
4. **Examples**: Working examples of framework usage

### Docstring Format

Use Google-style docstrings:

```python
def create_skill_node(
    node_id: str,
    name: str,
    level: SkillLevel,
    xp_required: int = 0
) -> SkillNode:
    """Create a new skill node.

    Args:
        node_id: Unique identifier for the node
        name: Display name for the node
        level: Skill level classification
        xp_required: XP required to unlock this node

    Returns:
        SkillNode: The created skill node

    Raises:
        ValidationError: If node_id is already in use
        ValueError: If xp_required is negative

    Example:
        >>> node = create_skill_node(
        ...     "vectors_basic",
        ...     "Vector Basics", 
        ...     SkillLevel.APPLICATION,
        ...     100
        ... )
        >>> node.name
        'Vector Basics'
    """
```

### Building Documentation

```bash
# Install documentation dependencies
pip install sphinx sphinx-rtd-theme

# Build documentation
cd docs/
make html

# View documentation
open _build/html/index.html
```

## Review Process

### Pull Request Guidelines

1. **Clear Description**: Explain what your PR does and why
2. **Link Issues**: Reference related issues with "Fixes #123"
3. **Small Changes**: Keep PRs focused and manageable
4. **Tests**: Include tests for new functionality
5. **Documentation**: Update documentation as needed

### Review Criteria

Reviewers will check for:

- **Functionality**: Does the code work as intended?
- **Code Quality**: Is the code clean, readable, and well-structured?
- **Testing**: Are there adequate tests with good coverage?
- **Documentation**: Is documentation clear and complete?
- **Compatibility**: Does it work with supported Python versions?
- **Performance**: Are there any performance implications?

### Review Timeline

- Initial review: Within 3-5 business days
- Follow-up reviews: Within 1-2 business days
- Complex changes may take longer

### Addressing Review Feedback

1. **Be Responsive**: Address feedback promptly and politely
2. **Ask Questions**: If feedback isn't clear, ask for clarification
3. **Make Changes**: Update code based on reviewer suggestions
4. **Test Changes**: Ensure changes don't break existing functionality

## Release Process

### Version Numbering

We use [Semantic Versioning](https://semver.org/):

- **MAJOR.MINOR.PATCH** (e.g., 1.2.3)
- **MAJOR**: Breaking changes
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes (backward compatible)

### Release Checklist

1. Update version number in `setup.py` and `__init__.py`
2. Update `CHANGELOG.md` with new features and fixes
3. Run full test suite
4. Update documentation
5. Create release tag
6. Publish to PyPI (maintainers only)

## Getting Help

### Communication Channels

- **GitHub Issues**: Bug reports and feature requests
- **GitHub Discussions**: Questions and general discussion
- **Email**: Direct contact for sensitive issues

### Resources

- [Project Documentation](docs/)
- [API Reference](docs/api_reference.md)
- [Examples](examples/)
- [Canvas API Documentation](https://canvas.instructure.com/doc/api/)

## Recognition

Contributors will be recognized in:

- `CONTRIBUTORS.md` file
- Release notes for significant contributions
- Annual contributor highlights

Thank you for contributing to the Canvas Course Gamification Framework! 🎉
