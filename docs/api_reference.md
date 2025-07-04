# API Reference

## Canvas Course Gamification Framework API

### Overview

This document provides comprehensive reference for the Canvas Course Gamification Framework API. The framework is organized into several core modules that handle different aspects of gamified course creation and management.

## Core Modules

### 1. Canvas API Client (`src.canvas_api`)

#### CanvasAPIClient

The main client for interacting with Canvas LMS.

```python
from src.canvas_api import CanvasAPIClient

client = CanvasAPIClient(
    api_url="https://your-institution.instructure.com",
    api_token="your_api_token",
    course_id="12345"
)
```

**Constructor Parameters:**
- `api_url` (str, optional): Canvas instance URL. Defaults to `CANVAS_API_URL` environment variable.
- `api_token` (str, optional): Canvas API token. Defaults to `CANVAS_API_TOKEN` environment variable.
- `course_id` (str, optional): Target course ID. Defaults to `CANVAS_COURSE_ID` environment variable.

**Methods:**

##### `make_request(method, endpoint, **kwargs)`
Make a raw API request to Canvas.

**Parameters:**
- `method` (str): HTTP method (GET, POST, PUT, DELETE)
- `endpoint` (str): API endpoint without base URL
- `**kwargs`: Additional arguments for requests

**Returns:** `requests.Response`

**Raises:**
- `CanvasAPIError`: For general API errors
- `RateLimitError`: When rate limited

**Example:**
```python
response = client.make_request("GET", "courses/12345/modules")
```

##### `get(endpoint, **kwargs)`
Make a GET request and return JSON response.

**Example:**
```python
modules = client.get("courses/12345/modules")
```

##### `post(endpoint, **kwargs)`
Make a POST request and return JSON response.

**Example:**
```python
new_module = client.post(
    "courses/12345/modules",
    json={"module": {"name": "New Module"}}
)
```

##### `create_module(course_id=None, **module_data)`
Create a new module in the course.

**Parameters:**
- `course_id` (str, optional): Course ID. Uses default if not provided.
- `**module_data`: Module configuration data

**Returns:** `Dict[str, Any]` - Created module data

**Example:**
```python
module = client.create_module(
    name="Introduction",
    position=1,
    require_sequential_progress=True
)
```

##### `create_assignment(course_id=None, **assignment_data)`
Create a new assignment in the course.

**Example:**
```python
assignment = client.create_assignment(
    name="Assignment 1",
    description="First assignment",
    points_possible=100,
    due_at="2024-12-31T23:59:59Z"
)
```

##### `validate_connection()`
Test the Canvas API connection.

**Returns:** `bool` - True if connection successful

### 2. Course Builder (`src.course_builder`)

#### CourseBuilder

Handles the construction and deployment of Canvas courses from JSON configurations.

```python
from src.course_builder import CourseBuilder

builder = CourseBuilder(canvas_client)
```

**Constructor Parameters:**
- `canvas_client` (CanvasAPIClient): Initialized Canvas API client

**Methods:**

##### `load_course_config(config_path)`
Load course configuration from a directory containing JSON files.

**Parameters:**
- `config_path` (Union[str, Path]): Path to configuration directory

**Returns:** `Dict[str, Any]` - Loaded configuration data

**Expected Files:**
- `modules.json`: Course modules and structure
- `assignments.json`: Assignment definitions
- `pages.json`: Course pages and content
- `quizzes.json`: Quiz configurations
- `badges.json`: Achievement badge definitions
- `outcomes.json`: Learning outcomes

**Example:**
```python
config = builder.load_course_config("examples/linear_algebra")
```

##### `build_skill_tree(config)`
Build a skill tree from configuration data.

**Parameters:**
- `config` (Dict[str, Any]): Course configuration

**Returns:** `SkillTree` - Constructed skill tree

**Example:**
```python
skill_tree = builder.build_skill_tree(config)
```

##### `deploy_course(config, course_id=None)`
Deploy a complete course to Canvas.

**Parameters:**
- `config` (Dict[str, Any]): Course configuration
- `course_id` (str, optional): Target course ID

**Returns:** `Dict[str, Any]` - Deployment results

**Example:**
```python
results = builder.deploy_course(config)
print(f"Deployed {len(results['modules'])} modules")
```

##### `validate_configuration(config)`
Validate course configuration for consistency and completeness.

**Parameters:**
- `config` (Dict[str, Any]): Configuration to validate

**Returns:** `Dict[str, List[str]]` - Validation errors and warnings

### 3. Gamification Engine (`src.gamification`)

#### SkillLevel (Enum)

Defines progression levels in the skill tree.

```python
from src.gamification import SkillLevel

class SkillLevel(Enum):
    RECOGNITION = 1  # "I know what this is"
    APPLICATION = 2  # "I can use this"
    INTUITION = 3    # "I understand why"
    SYNTHESIS = 4    # "I can connect and innovate"
    MASTERY = 5      # "I can teach this"
```

#### Badge

Represents an achievement badge.

```python
from src.gamification import Badge

badge = Badge(
    id="first_steps",
    name="First Steps",
    description="Complete your first assignment",
    criteria="Submit any assignment",
    xp_value=50,
    category="engagement"
)
```

**Attributes:**
- `id` (str): Unique badge identifier
- `name` (str): Display name
- `description` (str): Badge description
- `criteria` (str): Achievement criteria
- `xp_value` (int): XP reward value
- `image_url` (str, optional): Badge image URL
- `category` (str, optional): Badge category
- `unlock_requirements` (List[str]): Prerequisites for earning

**Methods:**

##### `to_canvas_format()`
Convert badge to Canvas-compatible format.

**Returns:** `Dict[str, Any]`

#### SkillNode

Represents a node in the skill tree.

```python
from src.gamification import SkillNode, SkillLevel

node = SkillNode(
    id="vectors_basics",
    name="Vector Basics",
    description="Understanding vector operations",
    level=SkillLevel.APPLICATION,
    xp_required=100,
    prerequisites=["intro_completed"],
    mastery_threshold=0.8
)
```

**Attributes:**
- `id` (str): Unique node identifier
- `name` (str): Display name
- `description` (str): Node description
- `level` (SkillLevel): Skill level
- `xp_required` (int): XP required to unlock
- `prerequisites` (List[str]): Prerequisite node IDs
- `unlock_requirements` (Dict[str, Any]): Custom unlock requirements
- `badges` (List[str]): Associated badge IDs
- `mastery_threshold` (float): Required mastery level (0.0-1.0)

**Methods:**

##### `is_unlocked(student_progress)`
Check if this skill node is unlocked for a student.

**Parameters:**
- `student_progress` (Dict[str, Any]): Student progress data

**Returns:** `bool`

#### SkillTree

Manages the complete skill tree structure.

```python
from src.gamification import SkillTree

tree = SkillTree("Course Skill Tree", "Main progression tree")
```

**Constructor Parameters:**
- `name` (str): Tree name
- `description` (str): Tree description

**Methods:**

##### `add_node(node)`
Add a skill node to the tree.

**Parameters:**
- `node` (SkillNode): Node to add

##### `add_badge(badge)`
Add a badge to the tree.

**Parameters:**
- `badge` (Badge): Badge to add

##### `get_available_nodes(student_progress)`
Get nodes available to a student based on their progress.

**Parameters:**
- `student_progress` (Dict[str, Any]): Student progress data

**Returns:** `List[SkillNode]`

##### `calculate_completion_percentage(student_progress)`
Calculate overall completion percentage for a student.

**Parameters:**
- `student_progress` (Dict[str, Any]): Student progress data

**Returns:** `float` - Completion percentage (0.0-1.0)

### 4. Validators (`src.validators`)

#### ConfigValidator

Validates course configuration files and data structures.

```python
from src.validators import ConfigValidator

validator = ConfigValidator()
```

**Methods:**

##### `validate_course_config(config)`
Validate a complete course configuration.

**Parameters:**
- `config` (Dict[str, Any]): Course configuration to validate

**Returns:** `Dict[str, Any]` - Validation results

**Example:**
```python
results = validator.validate_course_config(config)
if results["valid"]:
    print("Configuration is valid!")
else:
    print(f"Errors: {results['errors']}")
```

##### `validate_json_file(file_path)`
Validate a JSON configuration file.

**Parameters:**
- `file_path` (Path): Path to JSON file

**Returns:** `Dict[str, Any]` - Validation results

#### CanvasValidator

Validates Canvas API connections and permissions.

```python
from src.validators import CanvasValidator

validator = CanvasValidator(canvas_client)
```

**Constructor Parameters:**
- `canvas_client` (CanvasAPIClient): Canvas API client

**Methods:**

##### `validate_api_connection()`
Test Canvas API connection and basic permissions.

**Returns:** `Dict[str, Any]` - Connection validation results

**Example:**
```python
results = validator.validate_api_connection()
if results["connected"]:
    print(f"Connected as: {results['user_info']['name']}")
```

##### `validate_course_structure(course_id=None)`
Validate the existing structure of a Canvas course.

**Parameters:**
- `course_id` (str, optional): Course ID to validate

**Returns:** `Dict[str, Any]` - Structure validation results

### 5. Utility Functions

#### `validate_course_deployment(config_path, canvas_client=None)`

Comprehensive validation function for course deployment readiness.

**Parameters:**
- `config_path` (Path): Path to course configuration directory
- `canvas_client` (CanvasAPIClient, optional): Canvas API client for API validation

**Returns:** `Dict[str, Any]` - Comprehensive validation results

**Example:**
```python
from src.validators import validate_course_deployment

results = validate_course_deployment("examples/linear_algebra", client)
if results["ready_for_deployment"]:
    print("Ready to deploy!")
else:
    print(f"Issues found: {results['overall_errors']}")
```

## Configuration Schemas

### Module Configuration (`modules.json`)

```json
{
  "modules": [
    {
      "id": "string",
      "name": "string",
      "description": "string",
      "position": "integer",
      "unlock_at": "ISO 8601 date string",
      "require_sequential_progress": "boolean",
      "gamification": {
        "skill_level": "recognition|application|intuition|synthesis|mastery",
        "xp_required": "integer",
        "unlock_requirements": {},
        "mastery_threshold": "float (0.0-1.0)"
      },
      "prerequisites": ["string array of module IDs"],
      "items": [
        {
          "type": "Assignment|Quiz|Page|Discussion|ExternalUrl|ExternalTool",
          "id": "string",
          "title": "string",
          "position": "integer",
          "completion_requirement": {
            "type": "must_view|must_submit|must_mark_done|min_score",
            "min_score": "integer (for min_score type)"
          }
        }
      ]
    }
  ]
}
```

### Assignment Configuration (`assignments.json`)

```json
{
  "assignments": [
    {
      "id": "string",
      "name": "string",
      "description": "string",
      "points_possible": "integer",
      "due_at": "ISO 8601 date string",
      "unlock_at": "ISO 8601 date string",
      "lock_at": "ISO 8601 date string",
      "submission_types": ["online_text_entry", "online_url", "online_upload", "media_recording"],
      "xp_value": "integer",
      "skill_level": "string",
      "badges": ["string array of badge IDs"],
      "prerequisites": ["string array of prerequisite IDs"],
      "mastery_threshold": "float (0.0-1.0)"
    }
  ]
}
```

### Badge Configuration (`badges.json`)

```json
{
  "badges": [
    {
      "id": "string",
      "name": "string",
      "description": "string",
      "criteria": "string",
      "xp_value": "integer",
      "image_url": "string (optional)",
      "category": "string (optional)",
      "unlock_requirements": ["string array"]
    }
  ]
}
```

## Error Handling

### Exception Classes

#### `CanvasAPIError`
Base exception for Canvas API errors.

#### `RateLimitError`
Raised when API rate limit is exceeded.

#### `ValidationError`
Raised when validation fails.

### Error Response Format

All API methods return error information in a consistent format:

```python
{
    "success": False,
    "error": {
        "type": "CanvasAPIError",
        "message": "Detailed error message",
        "code": "ERROR_CODE",
        "details": {}
    }
}
```

## Rate Limiting

The framework includes automatic rate limiting and retry logic:

- Default: 10 requests per second
- Automatic exponential backoff on rate limit errors
- Configurable retry attempts (default: 3)
- Request queuing to prevent overwhelming the API

Configure rate limiting in `config/api_config.yml`:

```yaml
api:
  rate_limiting:
    requests_per_second: 10
    retry_attempts: 3
    backoff_factor: 2
```

## Environment Variables

Required environment variables:

- `CANVAS_API_URL`: Canvas instance URL
- `CANVAS_API_TOKEN`: Canvas API access token
- `CANVAS_COURSE_ID`: Default course ID

Optional environment variables:

- `DEBUG`: Enable debug mode
- `LOG_LEVEL`: Logging level (INFO, DEBUG, WARNING, ERROR)
- `API_RATE_LIMIT`: Custom rate limit
- `API_RETRY_ATTEMPTS`: Custom retry attempts

## Testing

### Unit Tests

Run the test suite:

```bash
pytest tests/
```

### Integration Tests

Test with a real Canvas instance:

```bash
pytest tests/integration/ --canvas-instance
```

### Validation Tests

Validate configuration files:

```bash
python -m src.validators validate examples/linear_algebra
```

---

*For additional examples and advanced usage, see the [examples directory](../examples/) and [instructor guide](instructor_guide.md)*
