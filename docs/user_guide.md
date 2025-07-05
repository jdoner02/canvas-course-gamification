# User Guide

## Getting Started

This guide will help you create your first gamified Canvas course.

### Prerequisites

- Canvas LMS account (free or institutional)
- Canvas API token
- Python 3.8+

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/jdoner02/canvas-course-gamification.git
   cd canvas-course-gamification
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up your environment:
   ```bash
   cp .env.example .env
   # Edit .env with your Canvas credentials
   ```

## Creating Your First Course

### 1. Course Configuration

Create a course configuration file (e.g., `my_course.json`):

```json
{
  "title": "Introduction to Programming",
  "description": "Learn programming fundamentals with gamification",
  "modules": [
    {
      "name": "Python Basics",
      "assignments": [
        {
          "name": "Hello World",
          "points": 10,
          "skill_level": "beginner"
        }
      ]
    }
  ],
  "skill_tree": {
    "levels": ["beginner", "intermediate", "advanced"],
    "badges": ["first_program", "loop_master", "function_expert"]
  }
}
```

### 2. Deploy to Canvas

```python
from src.course_builder import CourseBuilder

builder = CourseBuilder()
course = builder.load_from_config("my_course.json")
course.deploy_to_canvas()
```

## Gamification Features

### Skill Trees
- Visual progression paths
- Prerequisite-based unlocking
- Multiple learning routes

### Achievement Badges
- Custom criteria
- Visual feedback
- Progress tracking

### XP System
- Points for assignments
- Bonus multipliers
- Level progression

## Examples

Check the `examples/` directory for complete course templates:

- **linear_algebra**: Math course with skill trees
- **programming_101**: CS course with coding challenges
- **biology**: Science course with adaptive paths

## Troubleshooting

### Common Issues

**Canvas API Connection Failed**
- Verify your API token in `.env`
- Check Canvas API URL
- Ensure token has proper permissions

**Course Creation Errors**
- Validate your JSON configuration
- Check Canvas API rate limits
- Review application logs

### Getting Help

- Check [API Reference](api_reference.md)
- Review [examples](../examples/)
- Open an issue on GitHub
