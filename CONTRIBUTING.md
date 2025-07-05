# Contributing to Canvas Course Gamification

We welcome contributions! This guide will help you get started.

## Getting Started

### Types of Contributions

- **Bug Reports**: Found an issue? Let us know!
- **Feature Requests**: Have an idea for improvement?
- **Code Contributions**: Fix bugs or add features
- **Documentation**: Help improve our docs
- **Examples**: Share course templates

### Before Contributing

1. Check existing [issues](https://github.com/jdoner02/canvas-course-gamification/issues) and [pull requests](https://github.com/jdoner02/canvas-course-gamification/pulls)
2. For major changes, open an issue first to discuss

## Development Setup

1. **Fork and Clone**
   ```bash
   git clone https://github.com/jdoner02/canvas-course-gamification.git
   cd canvas-course-gamification
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   pip install -e .[dev]
   ```

3. **Set Up Environment**
   ```bash
   cp .env.example .env
   # Edit .env with your Canvas credentials
   ```

## Making Contributions

### Pull Request Process

1. **Create a Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make Changes**
   - Write clean, readable code
   - Follow existing code style
   - Add tests for new features
   - Update documentation as needed

3. **Test Your Changes**
   ```bash
   pytest tests/
   black src/ tests/
   flake8 src/ tests/
   ```

4. **Commit and Push**
   ```bash
   git add .
   git commit -m "Add feature: description of your changes"
   git push origin feature/your-feature-name
   ```

5. **Create Pull Request**
   - Use the GitHub web interface
   - Provide clear description of changes
   - Reference any related issues

## Code Standards

### Python Style
- Follow PEP 8
- Use Black for formatting: `black src/ tests/`
- Use type hints where appropriate
- Write docstrings for public functions

### Testing
- Add tests for new features
- Maintain or improve test coverage
- Use descriptive test names

### Documentation
- Update relevant documentation
- Include docstrings for new functions
- Add examples for new features

## Reporting Issues

When reporting bugs, please include:

- Python version
- Operating system
- Canvas instance type (free vs institutional)
- Steps to reproduce
- Expected vs actual behavior
- Error messages or logs

## Questions?

- Check the [documentation](docs/)
- Search existing [issues](https://github.com/jdoner02/canvas-course-gamification/issues)
- Open a new issue with the "question" label

Thank you for contributing! 🎉
