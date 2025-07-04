# JSON Course Data Integration

This document describes the new JSON-based course data integration functionality added to the Canvas Course Gamification framework.

## Overview

The framework now supports building Canvas courses from structured JSON data files, providing a more flexible and maintainable approach to course creation. This includes comprehensive validation, statistics, and CLI tools.

## JSON Data Structure

### Required Files

The system expects the following JSON files in the course data directory:

- `assignments.json` - Course assignments with gamification elements
- `modules.json` - Course modules with progression requirements  
- `quizzes.json` - Quizzes with questions and mastery checks
- `pages.json` - Course pages and content
- `outcomes.json` - Learning outcomes and skill progression
- `prerequisites.json` - Course prerequisites
- `assignment_id_map.json` - Mapping of local IDs to Canvas IDs

### Data Validation

The system includes comprehensive validation for:

- **Required fields** - Ensures all necessary data is present
- **Data types** - Validates field types and formats
- **Cross-references** - Checks consistency between linked data
- **Gamification rules** - Validates XP values, badges, and progression
- **Canvas compatibility** - Ensures data can be imported to Canvas

### Example Assignment Structure

```json
{
  "assignments": [
    {
      "id": "hw-vectors",
      "title": "Vector Operations Mastery Quest",
      "description": "Master fundamental vector operations...",
      "points_possible": 100,
      "due_at": "2025-02-15T23:59:00Z",
      "mastery_threshold": 75,
      "gamification": {
        "xp_value": 100,
        "badges": ["vector_warrior"],
        "mastery_paths": {
          "express": ["bonus-content-1"],
          "standard": ["practice-1"],
          "support": ["tutorial-1", "practice-1"]
        }
      },
      "outcomes": ["vector_recognition", "vector_operations"]
    }
  ]
}
```

## CLI Commands

### Validate Course Data

```bash
python -m src.cli validate data/math231
```

Validates all JSON files and reports errors/warnings.

### Show Statistics

```bash
python -m src.cli stats data/math231
```

Displays course statistics including assignment counts, points, and XP.

### Build Canvas Course

```bash
python -m src.cli build data/math231 "Linear Algebra" "MATH231" \
  --canvas-url https://your-canvas.edu \
  --token YOUR_API_TOKEN \
  --account-id 1 \
  --term-id 123
```

Creates a complete Canvas course from JSON data.

### Inspect Course Data

```bash
# Show overview
python -m src.cli inspect data/math231

# Show specific assignment
python -m src.cli inspect data/math231 --assignment-id hw-vectors

# Show specific module  
python -m src.cli inspect data/math231 --module-name "Module 1"
```

## Programming Interface

### Data Loader

```python
from src.course_builder.data_loader import CourseDataLoader

loader = CourseDataLoader('data/math231')
loader.load_all_data()

# Validate data
result = loader.validate_data()
if result.is_valid:
    print("Data is valid!")
else:
    print("Errors:", result.errors)

# Get statistics
stats = loader.get_statistics()
print(f"Total assignments: {stats['assignments']}")
```

### Course Builder

```python
from src.course_builder.json_course_builder import JsonCourseBuilder, CanvasConfig

config = CanvasConfig(
    base_url="https://canvas.edu",
    token="your_token",
    account_id=1,
    term_id=123
)

builder = JsonCourseBuilder('data/math231', config)
course_id = builder.build_course("Linear Algebra", "MATH231")
print(f"Created course: {course_id}")
```

## MATH231 Linear Algebra Course

The framework includes a complete MATH231 Linear Algebra course with:

- **11 assignments** with gamified elements and mastery paths
- **12 modules** with sequential progression requirements
- **23 quizzes** including mastery checks and comprehensive reviews
- **41 pages** with rich content and interactive elements
- **47 learning outcomes** mapped to assignments and assessments
- **1,470 total points** and **1,510 XP** available

### Key Features

- **Skill tree progression** - Students unlock modules by mastering prerequisites
- **Gamification elements** - XP, badges, and achievement tracking
- **Mastery-based learning** - 75% threshold required for progression
- **Multiple pathways** - Express, standard, and support tracks based on performance
- **Real-world applications** - Connects linear algebra to career fields

## Testing

### Run All Tests

```bash
python run_tests.py
```

### Run Specific Test Suites

```bash
# Unit tests
pytest tests/unit/ -v

# Integration tests  
pytest tests/integration/ -v

# Performance tests
pytest tests/unit/test_performance.py -v
```

### Test Coverage

The test suite includes:

- **Unit tests** for data loading and validation
- **Integration tests** with real MATH231 data  
- **Performance tests** for scalability
- **Mock API tests** for Canvas integration
- **CLI command tests** for user interface

## Performance

The system is designed for efficiency:

- **Fast loading** - Large datasets load in < 3 seconds
- **Quick validation** - Comprehensive validation in < 10 seconds  
- **Memory efficient** - < 100MB memory usage for large courses
- **Concurrent processing** - Thread-safe validation operations

## Error Handling

Comprehensive error handling includes:

- **Validation errors** - Clear messages for data issues
- **API errors** - Graceful handling of Canvas API failures
- **File errors** - Helpful messages for missing/corrupt files
- **Performance warnings** - Alerts for slow operations

## Future Enhancements

Planned improvements include:

- **Interactive course builder GUI**
- **Automated Canvas synchronization**
- **Advanced analytics and reporting**
- **Course template library**
- **Multi-language support**

## Support

For questions or issues:

1. Check the validation output for specific error messages
2. Review the test suite for usage examples
3. Consult the API documentation for Canvas integration
4. Contact the development team for advanced support
