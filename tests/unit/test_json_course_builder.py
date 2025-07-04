#!/usr/bin/env python3
"""
Tests for JsonCourseBuilder
"""

import pytest
import json
import tempfile
import responses
from pathlib import Path
from unittest.mock import patch, MagicMock

from src.course_builder.json_course_builder import (
    JsonCourseBuilder,
    CanvasConfig,
    CourseData,
)


class TestJsonCourseBuilder:
    """Test JsonCourseBuilder functionality"""

    @pytest.fixture
    def canvas_config(self):
        """Create test Canvas configuration"""
        return CanvasConfig(
            base_url="https://test.instructure.com",
            token="test_token",
            account_id=1,
            term_id=1,
        )

    @pytest.fixture
    def temp_data_dir(self):
        """Create temporary directory with test data"""
        with tempfile.TemporaryDirectory() as temp_dir:
            data_dir = Path(temp_dir)

            # Copy test fixtures to temp directory
            fixtures_dir = Path(__file__).parent.parent / "fixtures"

            test_files = [
                "test_assignments.json",
                "test_modules.json",
                "test_quizzes.json",
                "test_pages.json",
                "test_outcomes.json",
                "test_prerequisites.json",
                "test_assignment_id_map.json",
            ]

            for filename in test_files:
                if (fixtures_dir / filename).exists():
                    with open(fixtures_dir / filename, "r") as src:
                        data = json.load(src)

                    # Remove 'test_' prefix for actual data files
                    dest_name = filename.replace("test_", "")
                    with open(data_dir / dest_name, "w") as dest:
                        json.dump(data, dest)

            yield data_dir

    @pytest.fixture
    def course_builder(self, temp_data_dir, canvas_config):
        """Create JsonCourseBuilder instance"""
        return JsonCourseBuilder(str(temp_data_dir), canvas_config)

    def test_init(self, course_builder, canvas_config):
        """Test JsonCourseBuilder initialization"""
        assert course_builder.canvas_config == canvas_config
        assert course_builder.headers["Authorization"] == "Bearer test_token"
        assert course_builder.headers["Content-Type"] == "application/json"
        assert course_builder.course_id is None
        assert isinstance(course_builder.course_data, CourseData)

    def test_load_course_data(self, course_builder):
        """Test loading course data"""
        course_builder.load_course_data()

        # Verify data was loaded
        assert len(course_builder.course_data.assignments["assignments"]) == 2
        assert len(course_builder.course_data.modules["modules"]) == 2
        assert len(course_builder.course_data.quizzes["quizzes"]) == 1
        assert len(course_builder.course_data.pages["pages"]) == 2
        assert len(course_builder.course_data.outcomes["outcomes"]) == 3

        # Verify specific data
        assert (
            course_builder.course_data.assignments["assignments"][0]["id"]
            == "test-assignment-1"
        )
        assert (
            course_builder.course_data.modules["modules"][0]["name"] == "Test Module 1"
        )

    @responses.activate
    def test_create_course(self, course_builder):
        """Test course creation"""
        # Mock Canvas API response
        responses.add(
            responses.POST,
            "https://test.instructure.com/api/v1/accounts/1/courses",
            json={"id": 12345, "name": "Test Course"},
            status=200,
        )

        course_id = course_builder.create_course("Test Course", "TEST101")

        assert course_id == 12345
        assert course_builder.course_id == 12345

        # Verify API call
        assert len(responses.calls) == 1
        request_data = json.loads(responses.calls[0].request.body)
        assert request_data["course"]["name"] == "Test Course"
        assert request_data["course"]["course_code"] == "TEST101"

    def test_create_course_without_course_id_fails(self, course_builder):
        """Test that methods requiring course_id fail when course not created"""
        with pytest.raises(ValueError, match="Must create course first"):
            course_builder.create_outcomes()

        with pytest.raises(ValueError, match="Must create course first"):
            course_builder.create_pages()

        with pytest.raises(ValueError, match="Must create course first"):
            course_builder.create_assignments()

    @responses.activate
    def test_create_outcomes(self, course_builder):
        """Test outcome creation"""
        course_builder.course_id = 12345
        course_builder.load_course_data()

        # Mock Canvas API responses for each outcome
        for i in range(3):
            responses.add(
                responses.POST,
                "https://test.instructure.com/api/v1/courses/12345/outcome_groups/root/outcomes",
                json={"id": 100 + i, "title": f"Test Outcome {i + 1}"},
                status=200,
            )

        outcome_map = course_builder.create_outcomes()

        assert len(outcome_map) == 3
        assert "test_outcome_1" in outcome_map
        assert "test_outcome_2" in outcome_map
        assert "test_outcome_3" in outcome_map

    @responses.activate
    def test_create_pages(self, course_builder):
        """Test page creation"""
        course_builder.course_id = 12345
        course_builder.load_course_data()

        # Mock Canvas API responses
        responses.add(
            responses.POST,
            "https://test.instructure.com/api/v1/courses/12345/pages",
            json={"page_id": 200, "title": "Test Page 1"},
            status=200,
        )
        responses.add(
            responses.POST,
            "https://test.instructure.com/api/v1/courses/12345/pages",
            json={"page_id": 201, "title": "Course Welcome"},
            status=200,
        )

        page_map = course_builder.create_pages()

        assert len(page_map) == 2
        assert "Test Page 1" in page_map
        assert "Course Welcome" in page_map
        assert page_map["Test Page 1"] == 200

    @responses.activate
    def test_create_assignments(self, course_builder):
        """Test assignment creation"""
        course_builder.course_id = 12345
        course_builder.load_course_data()

        # Mock Canvas API responses
        responses.add(
            responses.POST,
            "https://test.instructure.com/api/v1/courses/12345/assignments",
            json={"id": 300, "name": "Test Assignment 1"},
            status=200,
        )
        responses.add(
            responses.POST,
            "https://test.instructure.com/api/v1/courses/12345/assignments",
            json={"id": 301, "name": "Test Assignment 2"},
            status=200,
        )

        assignment_map = course_builder.create_assignments()

        assert len(assignment_map) == 2
        assert "test-assignment-1" in assignment_map
        assert "test-assignment-2" in assignment_map
        assert assignment_map["test-assignment-1"] == 300

        # Verify assignment was added to ID map
        assert course_builder.course_data.assignment_id_map["test-assignment-1"] == 300

    @responses.activate
    def test_create_quizzes(self, course_builder):
        """Test quiz creation"""
        course_builder.course_id = 12345
        course_builder.load_course_data()

        # Mock Canvas API responses
        responses.add(
            responses.POST,
            "https://test.instructure.com/api/v1/courses/12345/quizzes",
            json={"id": 400, "title": "Test Quiz 1"},
            status=200,
        )

        # Mock responses for quiz questions
        responses.add(
            responses.POST,
            "https://test.instructure.com/api/v1/courses/12345/quizzes/400/questions",
            json={"id": 500, "question_text": "What is 2 + 2?"},
            status=200,
        )
        responses.add(
            responses.POST,
            "https://test.instructure.com/api/v1/courses/12345/quizzes/400/questions",
            json={"id": 501, "question_text": "What is the capital of France?"},
            status=200,
        )

        quiz_map = course_builder.create_quizzes()

        assert len(quiz_map) == 1
        assert "test-quiz-1" in quiz_map
        assert quiz_map["test-quiz-1"] == 400

        # Verify quiz questions were created
        question_calls = [
            call for call in responses.calls if "questions" in call.request.url
        ]
        assert len(question_calls) == 2

    @responses.activate
    def test_create_modules(self, course_builder):
        """Test module creation"""
        course_builder.course_id = 12345
        course_builder.load_course_data()

        # Mock module creation
        responses.add(
            responses.POST,
            "https://test.instructure.com/api/v1/courses/12345/modules",
            json={"id": 600, "name": "Test Module 1"},
            status=200,
        )
        responses.add(
            responses.POST,
            "https://test.instructure.com/api/v1/courses/12345/modules",
            json={"id": 601, "name": "Test Module 2"},
            status=200,
        )

        # Mock module item creation
        responses.add(
            responses.POST,
            "https://test.instructure.com/api/v1/courses/12345/modules/600/items",
            json={"id": 700, "title": "Test Assignment 1"},
            status=200,
        )
        responses.add(
            responses.POST,
            "https://test.instructure.com/api/v1/courses/12345/modules/600/items",
            json={"id": 701, "title": "Test Page 1"},
            status=200,
        )
        responses.add(
            responses.POST,
            "https://test.instructure.com/api/v1/courses/12345/modules/601/items",
            json={"id": 702, "title": "Test Assignment 2"},
            status=200,
        )
        responses.add(
            responses.POST,
            "https://test.instructure.com/api/v1/courses/12345/modules/601/items",
            json={"id": 703, "title": "Test Quiz 1"},
            status=200,
        )

        # Create mappings for module items
        assignment_map = {"test-assignment-1": 300, "test-assignment-2": 301}
        quiz_map = {"test-quiz-1": 400}
        page_map = {"Test Page 1": 200}

        module_map = course_builder.create_modules(assignment_map, quiz_map, page_map)

        assert len(module_map) == 2
        assert "Test Module 1" in module_map
        assert "Test Module 2" in module_map

        # Verify module items were created
        item_calls = [call for call in responses.calls if "/items" in call.request.url]
        assert len(item_calls) == 4

    @responses.activate
    def test_build_course_complete(self, course_builder):
        """Test complete course build process"""
        # Mock all Canvas API calls needed for full course build

        # Course creation
        responses.add(
            responses.POST,
            "https://test.instructure.com/api/v1/accounts/1/courses",
            json={"id": 12345, "name": "Complete Test Course"},
            status=200,
        )

        # Outcomes (3 outcomes)
        for i in range(3):
            responses.add(
                responses.POST,
                "https://test.instructure.com/api/v1/courses/12345/outcome_groups/root/outcomes",
                json={"id": 100 + i},
                status=200,
            )

        # Pages (2 pages)
        for i in range(2):
            responses.add(
                responses.POST,
                "https://test.instructure.com/api/v1/courses/12345/pages",
                json={"page_id": 200 + i},
                status=200,
            )

        # Assignments (2 assignments)
        for i in range(2):
            responses.add(
                responses.POST,
                "https://test.instructure.com/api/v1/courses/12345/assignments",
                json={"id": 300 + i},
                status=200,
            )

        # Quizzes (1 quiz)
        responses.add(
            responses.POST,
            "https://test.instructure.com/api/v1/courses/12345/quizzes",
            json={"id": 400},
            status=200,
        )

        # Quiz questions (2 questions)
        for i in range(2):
            responses.add(
                responses.POST,
                "https://test.instructure.com/api/v1/courses/12345/quizzes/400/questions",
                json={"id": 500 + i},
                status=200,
            )

        # Modules (2 modules)
        for i in range(2):
            responses.add(
                responses.POST,
                "https://test.instructure.com/api/v1/courses/12345/modules",
                json={"id": 600 + i},
                status=200,
            )

        # Module items (4 items total)
        for i in range(4):
            responses.add(
                responses.POST,
                f"https://test.instructure.com/api/v1/courses/12345/modules/{600 if i < 2 else 601}/items",
                json={"id": 700 + i},
                status=200,
            )

        course_id = course_builder.build_course("Complete Test Course", "COMPLETE101")

        assert course_id == 12345
        assert course_builder.course_id == 12345

        # Verify all API calls were made
        assert len(responses.calls) > 10  # Multiple calls for complete build

    def test_validate_course_data(self, course_builder):
        """Test course data validation"""
        course_builder.load_course_data()
        errors = course_builder.validate_course_data()

        # With valid test data, should have no errors
        assert all(len(error_list) == 0 for error_list in errors.values())

    def test_validate_course_data_invalid(self, canvas_config):
        """Test validation with invalid data"""
        with tempfile.TemporaryDirectory() as temp_dir:
            data_dir = Path(temp_dir)

            # Create invalid data
            invalid_data = {
                "assignments.json": {
                    "assignments": [
                        {
                            # Missing required fields
                            "description": "Invalid assignment"
                        }
                    ]
                },
                "modules.json": {"modules": []},
                "quizzes.json": {"quizzes": []},
                "pages.json": {"pages": []},
                "outcomes.json": {"outcomes": []},
                "prerequisites.json": {"prerequisites": []},
                "assignment_id_map.json": {},
            }

            for filename, data in invalid_data.items():
                with open(data_dir / filename, "w") as f:
                    json.dump(data, f)

            builder = JsonCourseBuilder(str(data_dir), canvas_config)
            builder.load_course_data()
            errors = builder.validate_course_data()

            # Should have validation errors
            assert len(errors["assignments"]) > 0


class TestCanvasConfig:
    """Test CanvasConfig dataclass"""

    def test_init(self):
        """Test CanvasConfig initialization"""
        config = CanvasConfig(
            base_url="https://test.instructure.com",
            token="test_token",
            account_id=1,
            term_id=2,
        )

        assert config.base_url == "https://test.instructure.com"
        assert config.token == "test_token"
        assert config.account_id == 1
        assert config.term_id == 2

    def test_init_optional_term_id(self):
        """Test CanvasConfig with optional term_id"""
        config = CanvasConfig(
            base_url="https://test.instructure.com", token="test_token", account_id=1
        )

        assert config.term_id is None


class TestCourseData:
    """Test CourseData dataclass"""

    def test_init(self):
        """Test CourseData initialization"""
        data = CourseData()

        assert isinstance(data.assignments, dict)
        assert isinstance(data.modules, dict)
        assert isinstance(data.outcomes, dict)
        assert isinstance(data.pages, dict)
        assert isinstance(data.quizzes, dict)
        assert isinstance(data.prerequisites, dict)
        assert isinstance(data.assignment_id_map, dict)

        # All should be empty initially
        assert len(data.assignments) == 0
        assert len(data.modules) == 0
        assert len(data.outcomes) == 0
        assert len(data.pages) == 0
        assert len(data.quizzes) == 0
        assert len(data.prerequisites) == 0
        assert len(data.assignment_id_map) == 0
