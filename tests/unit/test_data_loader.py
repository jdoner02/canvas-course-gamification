#!/usr/bin/env python3
"""
Tests for CourseDataLoader
"""

import pytest
import json
import tempfile
from pathlib import Path
from unittest.mock import patch, mock_open

from src.course_builder.data_loader import CourseDataLoader, ValidationResult


class TestCourseDataLoader:
    """Test CourseDataLoader functionality"""

    @pytest.fixture
    def temp_data_dir(self):
        """Create temporary directory with test data"""
        with tempfile.TemporaryDirectory() as temp_dir:
            data_dir = Path(temp_dir)

            # Create test data files
            test_data = {
                "assignments.json": {
                    "assignments": [
                        {
                            "id": "test-assignment",
                            "title": "Test Assignment",
                            "description": "Test description",
                            "points_possible": 100,
                            "due_at": "2025-12-31T23:59:00Z",
                            "gamification": {"xp_value": 100},
                        }
                    ]
                },
                "modules.json": {
                    "modules": [
                        {
                            "name": "Test Module",
                            "overview": "Test overview",
                            "unlock_requirements": [],
                            "mastery_criteria": {"min_score": 75},
                            "items": [{"id": "test-assignment"}],
                        }
                    ]
                },
                "quizzes.json": {
                    "quizzes": [
                        {
                            "id": "test-quiz",
                            "title": "Test Quiz",
                            "description": "Test quiz description",
                            "settings": {"allowed_attempts": 3},
                            "questions": [
                                {
                                    "type": "multiple_choice_question",
                                    "question_text": "Test question?",
                                    "answers": [
                                        {"text": "Correct", "weight": 100},
                                        {"text": "Wrong", "weight": 0},
                                    ],
                                    "points_possible": 1,
                                }
                            ],
                        }
                    ]
                },
                "pages.json": {
                    "pages": [{"title": "Test Page", "body": "<p>Test content</p>"}]
                },
                "outcomes.json": {
                    "outcomes": [
                        {
                            "id": "test-outcome",
                            "name": "Test Outcome",
                            "description": "Test outcome description",
                            "level": "Application",
                            "module": 1,
                        }
                    ]
                },
                "prerequisites.json": {"prerequisites": []},
                "assignment_id_map.json": {"test-assignment": 12345},
            }

            for filename, data in test_data.items():
                with open(data_dir / filename, "w") as f:
                    json.dump(data, f)

            yield data_dir

    @pytest.fixture
    def data_loader(self, temp_data_dir):
        """Create CourseDataLoader instance"""
        return CourseDataLoader(str(temp_data_dir))

    def test_load_all_data(self, data_loader):
        """Test loading all data files"""
        data = data_loader.load_all_data()

        assert "assignments" in data
        assert "modules" in data
        assert "quizzes" in data
        assert "pages" in data
        assert "outcomes" in data
        assert "prerequisites" in data
        assert "assignment_id_map" in data

        # Verify specific data
        assert len(data["assignments"]["assignments"]) == 1
        assert data["assignments"]["assignments"][0]["id"] == "test-assignment"
        assert len(data["modules"]["modules"]) == 1
        assert data["modules"]["modules"][0]["name"] == "Test Module"

    def test_load_missing_files(self):
        """Test loading from directory with missing files"""
        with tempfile.TemporaryDirectory() as temp_dir:
            loader = CourseDataLoader(temp_dir)
            data = loader.load_all_data()

            # Should have empty dictionaries for missing files
            assert all(data[key] == {} for key in data.keys())

    def test_validate_data_valid(self, data_loader):
        """Test validation with valid data"""
        data_loader.load_all_data()
        result = data_loader.validate_data()

        assert result.is_valid
        assert len(result.errors) == 0

    def test_validate_assignments_invalid(self):
        """Test assignment validation with invalid data"""
        with tempfile.TemporaryDirectory() as temp_dir:
            data_dir = Path(temp_dir)

            # Create invalid assignment data
            invalid_data = {
                "assignments.json": {
                    "assignments": [
                        {
                            # Missing id
                            "title": "Test",
                            "points_possible": -10,  # Invalid points
                        },
                        {
                            "id": "test-1",
                            # Missing title
                            "points_possible": 100,
                            "due_at": "invalid-date",  # Invalid date format
                        },
                        {
                            "id": "test-1",  # Duplicate ID
                            "title": "Duplicate",
                            "points_possible": 50,
                        },
                    ]
                }
            }

            for filename, data in invalid_data.items():
                with open(data_dir / filename, "w") as f:
                    json.dump(data, f)

            loader = CourseDataLoader(str(data_dir))
            loader.load_all_data()
            result = loader.validate_data()

            assert not result.is_valid
            assert len(result.errors) > 0

            # Check for specific errors
            error_messages = " ".join(result.errors)
            assert "Missing required field 'id'" in error_messages
            assert "Missing required field 'title'" in error_messages
            assert "Invalid 'points_possible' value" in error_messages
            assert "Invalid due_at format" in error_messages
            assert "Duplicate assignment ID" in error_messages

    def test_validate_modules_invalid(self):
        """Test module validation with invalid data"""
        with tempfile.TemporaryDirectory() as temp_dir:
            data_dir = Path(temp_dir)

            invalid_data = {
                "modules.json": {
                    "modules": [
                        {
                            # Missing name
                            "overview": "Test",
                            "unlock_requirements": "not-a-list",  # Should be list
                            "mastery_criteria": {"min_score": 150},  # Invalid score
                        },
                        {
                            "name": "Test Module",
                            # Missing overview (warning)
                            "items": "not-a-list",  # Should be list
                        },
                    ]
                }
            }

            for filename, data in invalid_data.items():
                with open(data_dir / filename, "w") as f:
                    json.dump(data, f)

            loader = CourseDataLoader(str(data_dir))
            loader.load_all_data()
            result = loader.validate_data()

            assert not result.is_valid
            assert len(result.errors) > 0
            assert len(result.warnings) > 0

    def test_validate_quizzes_invalid(self):
        """Test quiz validation with invalid data"""
        with tempfile.TemporaryDirectory() as temp_dir:
            data_dir = Path(temp_dir)

            invalid_data = {
                "quizzes.json": {
                    "quizzes": [
                        {
                            # Missing id and title
                            "settings": {
                                "allowed_attempts": 0,  # Invalid
                                "time_limit": -5,  # Invalid
                            },
                            "questions": [
                                {
                                    # Missing question_text and type
                                    "answers": [],  # Empty answers
                                    "points_possible": -1,  # Invalid points
                                },
                                {
                                    "question_text": "Test?",
                                    "type": "multiple_choice",
                                    "answers": [
                                        {
                                            "text": "A",
                                            "weight": 0,
                                        },  # No correct answers
                                        {"text": "B", "weight": 0},
                                    ],
                                },
                            ],
                        }
                    ]
                }
            }

            for filename, data in invalid_data.items():
                with open(data_dir / filename, "w") as f:
                    json.dump(data, f)

            loader = CourseDataLoader(str(data_dir))
            loader.load_all_data()
            result = loader.validate_data()

            assert not result.is_valid
            assert len(result.errors) > 0

    def test_validate_cross_references(self):
        """Test cross-reference validation"""
        with tempfile.TemporaryDirectory() as temp_dir:
            data_dir = Path(temp_dir)

            # Data with broken references
            test_data = {
                "assignments.json": {
                    "assignments": [
                        {
                            "id": "valid-assignment",
                            "title": "Valid Assignment",
                            "points_possible": 100,
                            "outcomes": ["nonexistent-outcome"],  # Bad reference
                        }
                    ]
                },
                "modules.json": {
                    "modules": [
                        {
                            "name": "Test Module",
                            "overview": "Test",
                            "items": [{"id": "nonexistent-item"}],  # Bad reference
                        }
                    ]
                },
                "quizzes.json": {
                    "quizzes": [
                        {
                            "id": "valid-quiz",
                            "title": "Valid Quiz",
                            "questions": [],
                            "outcomes": [
                                "another-nonexistent-outcome"
                            ],  # Bad reference
                        }
                    ]
                },
                "outcomes.json": {"outcomes": []},  # Empty outcomes
                "pages.json": {"pages": []},
                "prerequisites.json": {"prerequisites": []},
                "assignment_id_map.json": {},
            }

            for filename, data in test_data.items():
                with open(data_dir / filename, "w") as f:
                    json.dump(data, f)

            loader = CourseDataLoader(str(data_dir))
            loader.load_all_data()
            result = loader.validate_data()

            # Should have warnings for broken references
            assert len(result.warnings) > 0
            warning_messages = " ".join(result.warnings)
            assert "references unknown" in warning_messages

    def test_get_statistics(self, data_loader):
        """Test statistics calculation"""
        data_loader.load_all_data()
        stats = data_loader.get_statistics()

        assert "assignments" in stats
        assert "modules" in stats
        assert "quizzes" in stats
        assert "pages" in stats
        assert "outcomes" in stats
        assert "total_questions" in stats
        assert "total_points" in stats
        assert "xp_available" in stats

        # Verify counts
        assert stats["assignments"] == 1
        assert stats["modules"] == 1
        assert stats["quizzes"] == 1
        assert stats["pages"] == 1
        assert stats["outcomes"] == 1
        assert stats["total_questions"] == 1
        assert stats["total_points"] == 100
        assert stats["xp_available"] == 100

    def test_export_summary(self, data_loader):
        """Test summary export"""
        data_loader.load_all_data()

        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            summary_path = f.name

        try:
            data_loader.export_summary(summary_path)

            # Verify summary file was created and has expected structure
            with open(summary_path, "r") as f:
                summary = json.load(f)

            assert "validation" in summary
            assert "statistics" in summary
            assert "generated_at" in summary

            assert "is_valid" in summary["validation"]
            assert "error_count" in summary["validation"]
            assert "warning_count" in summary["validation"]

        finally:
            Path(summary_path).unlink()


class TestValidationResult:
    """Test ValidationResult class"""

    def test_init(self):
        """Test ValidationResult initialization"""
        result = ValidationResult(is_valid=True, errors=[], warnings=[])

        assert result.is_valid
        assert len(result.errors) == 0
        assert len(result.warnings) == 0

    def test_add_error(self):
        """Test adding errors"""
        result = ValidationResult(is_valid=True, errors=[], warnings=[])

        result.add_error("Test error")

        assert not result.is_valid
        assert len(result.errors) == 1
        assert result.errors[0] == "Test error"

    def test_add_warning(self):
        """Test adding warnings"""
        result = ValidationResult(is_valid=True, errors=[], warnings=[])

        result.add_warning("Test warning")

        assert result.is_valid  # Warnings don't affect validity
        assert len(result.warnings) == 1
        assert result.warnings[0] == "Test warning"
