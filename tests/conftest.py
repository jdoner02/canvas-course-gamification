"""
Pytest configuration and fixtures for the Canvas Course Gamification Framework.
"""

import pytest
import os
from pathlib import Path
from unittest.mock import Mock

# Add src to Python path for testing
import sys
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

from src.canvas_api import CanvasAPIClient
from src.course_builder import CourseBuilder
from src.gamification import SkillTree, SkillNode, Badge, SkillLevel


@pytest.fixture
def sample_env_vars():
    """Provide sample environment variables for testing."""
    return {
        "CANVAS_API_URL": "https://test.instructure.com",
        "CANVAS_API_TOKEN": "test_token_123",
        "CANVAS_COURSE_ID": "12345"
    }


@pytest.fixture
def mock_canvas_client():
    """Provide a mock Canvas API client for testing."""
    client = Mock(spec=CanvasAPIClient)
    client.api_url = "https://test.instructure.com"
    client.api_token = "test_token_123"
    client.course_id = "12345"
    client.validate_connection.return_value = True
    return client


@pytest.fixture
def canvas_client(sample_env_vars):
    """Provide a real Canvas API client for integration testing."""
    # Only create real client if environment variables are set
    if all(key in os.environ for key in sample_env_vars.keys()):
        return CanvasAPIClient()
    else:
        pytest.skip("Canvas API credentials not configured")


@pytest.fixture
def sample_skill_node():
    """Provide a sample skill node for testing."""
    return SkillNode(
        id="test_node",
        name="Test Node",
        description="A test skill node",
        level=SkillLevel.APPLICATION,
        xp_required=100,
        prerequisites=["basic_node"],
        mastery_threshold=0.8
    )


@pytest.fixture
def sample_badge():
    """Provide a sample badge for testing."""
    return Badge(
        id="test_badge",
        name="Test Badge",
        description="A test achievement badge",
        criteria="Complete a test",
        xp_value=50,
        category="testing"
    )


@pytest.fixture
def sample_skill_tree():
    """Provide a sample skill tree for testing."""
    tree = SkillTree("Test Tree", "A test skill tree")
    
    # Add some nodes
    basic_node = SkillNode(
        id="basic_node",
        name="Basic Concepts",
        description="Foundation concepts",
        level=SkillLevel.RECOGNITION,
        xp_required=0
    )
    
    intermediate_node = SkillNode(
        id="intermediate_node", 
        name="Intermediate Concepts",
        description="Building on basics",
        level=SkillLevel.APPLICATION,
        xp_required=100,
        prerequisites=["basic_node"]
    )
    
    tree.add_node(basic_node)
    tree.add_node(intermediate_node)
    
    # Add a badge
    badge = Badge(
        id="completion_badge",
        name="Completion Badge", 
        description="Completed the tree",
        criteria="Complete all nodes",
        xp_value=100
    )
    tree.add_badge(badge)
    
    return tree


@pytest.fixture
def sample_course_config():
    """Provide sample course configuration data."""
    return {
        "modules": {
            "modules": [
                {
                    "id": "module_1",
                    "name": "Introduction",
                    "description": "Course introduction",
                    "position": 1,
                    "gamification": {
                        "skill_level": "recognition",
                        "xp_required": 0
                    },
                    "items": [
                        {
                            "type": "Page",
                            "id": "welcome_page",
                            "title": "Welcome"
                        }
                    ]
                }
            ]
        },
        "assignments": {
            "assignments": [
                {
                    "id": "assignment_1",
                    "name": "First Assignment",
                    "description": "Introduction assignment",
                    "points_possible": 100,
                    "xp_value": 25
                }
            ]
        },
        "badges": {
            "badges": [
                {
                    "id": "first_steps",
                    "name": "First Steps",
                    "description": "Complete your first assignment",
                    "criteria": "Submit assignment_1",
                    "xp_value": 50
                }
            ]
        }
    }


@pytest.fixture
def sample_student_progress():
    """Provide sample student progress data."""
    return {
        "total_xp": 250,
        "level": "intermediate",
        "modules_completed": ["module_1"],
        "assignments": {
            "assignment_1": {
                "completed": True,
                "score": 85,
                "submitted_at": "2024-07-01T10:00:00Z"
            }
        },
        "badges_earned": ["first_steps"],
        "quiz_scores": {
            "quiz_1": 0.9
        },
        "streak_days": 5
    }


@pytest.fixture
def temp_config_dir(tmp_path):
    """Create a temporary directory with sample configuration files."""
    config_dir = tmp_path / "config"
    config_dir.mkdir()
    
    # Create sample JSON files
    modules_file = config_dir / "modules.json"
    modules_file.write_text('''
    {
        "modules": [
            {
                "id": "test_module",
                "name": "Test Module",
                "description": "A test module",
                "position": 1
            }
        ]
    }
    ''')
    
    assignments_file = config_dir / "assignments.json"
    assignments_file.write_text('''
    {
        "assignments": [
            {
                "id": "test_assignment",
                "name": "Test Assignment", 
                "description": "A test assignment",
                "points_possible": 100
            }
        ]
    }
    ''')
    
    return config_dir


# Pytest configuration
def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line(
        "markers", "integration: mark test as integration test requiring Canvas API"
    )
    config.addinivalue_line(
        "markers", "slow: mark test as slow running"
    )
    config.addinivalue_line(
        "markers", "canvas_required: mark test as requiring Canvas instance access"
    )


def pytest_collection_modifyitems(config, items):
    """Automatically mark tests based on their location."""
    for item in items:
        # Mark integration tests
        if "integration" in str(item.fspath):
            item.add_marker(pytest.mark.integration)
        
        # Mark tests that use real Canvas client
        if "canvas_client" in item.fixturenames:
            item.add_marker(pytest.mark.canvas_required)
