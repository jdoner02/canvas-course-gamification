# Canvas Course Gamification

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Canvas API](https://img.shields.io/badge/Canvas-API%20Ready-green.svg)](https://canvas.instructure.com/doc/api/)

A Python framework for adding gamification elements to Canvas LMS courses. Transform traditional courses into engaging learning experiences with skill trees, achievement badges, XP systems, and adaptive content paths.

## Features

- **Skill Trees**: Visual learning progressions with unlockable content
- **Achievement System**: Badges and XP points for student milestones  
- **Canvas Integration**: Automated course creation and content deployment
- **Mastery-Based Learning**: Conditional content release based on student progress
- **Analytics**: Progress tracking and engagement metrics

## Quick Start

### Prerequisites

- Python 3.8+
- Canvas LMS account with API access
- Canvas API token

### Installation

```bash
git clone https://github.com/jdoner02/canvas-course-gamification.git
cd canvas-course-gamification
pip install -r requirements.txt
```

### Configuration

1. Copy the environment template:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` with your Canvas credentials:
   ```
   CANVAS_API_URL=https://your-canvas-instance.instructure.com
   CANVAS_API_TOKEN=your_api_token_here
   ```

### Basic Usage

```python
from src.course_builder import CourseBuilder

# Create a new gamified course
builder = CourseBuilder()
course = builder.create_course("Linear Algebra with Skill Trees")

# Add gamification elements
course.add_skill_tree("algebra_basics")
course.add_achievement_badges()
course.deploy_to_canvas()
```

## Project Structure

```
canvas-course-gamification/
├── src/                    # Core framework code
│   ├── gamification/       # Gamification engine
│   ├── canvas_api/         # Canvas API integration
│   └── course_builder/     # Course creation tools
├── examples/               # Example courses and templates
├── tests/                  # Test suite
├── docs/                   # Documentation
└── config/                 # Configuration files
```

## Examples

Check out the `examples/` directory for sample courses:

- **Linear Algebra**: Complete math course with skill trees
- **Programming 101**: CS course with coding challenges
- **Biology**: Science course with adaptive learning paths

## Documentation

- [User Guide](docs/user_guide.md) - Getting started with course creation
- [API Reference](docs/api_reference.md) - Complete API documentation
- [Examples](examples/) - Sample courses and templates
- [Contributing](CONTRIBUTING.md) - How to contribute to the project

## Canvas API Permissions

This framework requires the following Canvas API permissions:

- Read and write access to courses
- Manage assignments and modules
- Access to outcomes and assessments
- User enrollment management

## Testing

Run the test suite:

```bash
pytest tests/
```

For integration tests with Canvas:

```bash
pytest tests/integration/ --canvas-instance
```

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

- [GitHub Issues](https://github.com/jdoner02/canvas-course-gamification/issues) - Bug reports and feature requests
- [Discussions](https://github.com/jdoner02/canvas-course-gamification/discussions) - Questions and community discussion
- [Documentation](docs/) - Comprehensive guides and API reference

## Acknowledgments

- Canvas LMS API for providing the integration foundation
- Educational technology research community for gamification best practices
- Open source contributors who made this project possible
