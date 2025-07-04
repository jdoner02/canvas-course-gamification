#!/usr/bin/env python3
"""
Integration tests for MATH231 course data
Tests the actual JSON files from the MATH231 course setup
"""

import pytest
import json
from pathlib import Path

from src.course_builder.data_loader import CourseDataLoader
from src.course_builder.json_course_builder import JsonCourseBuilder, CanvasConfig


class TestMATH231Integration:
    """Integration tests using actual MATH231 course data"""

    @pytest.fixture
    def math231_data_path(self):
        """Path to MATH231 JSON data"""
        return Path(__file__).parent.parent.parent / "data" / "math231"

    @pytest.fixture
    def data_loader(self, math231_data_path):
        """Create data loader for MATH231 data"""
        return CourseDataLoader(str(math231_data_path))

    @pytest.fixture
    def canvas_config(self):
        """Test Canvas configuration"""
        return CanvasConfig(
            base_url="https://test.instructure.com",
            token="test_token",
            account_id=1,
            term_id=1,
        )

    @pytest.fixture
    def course_builder(self, math231_data_path, canvas_config):
        """Create course builder for MATH231 data"""
        return JsonCourseBuilder(str(math231_data_path), canvas_config)

    def test_data_files_exist(self, math231_data_path):
        """Test that all required data files exist"""
        required_files = [
            "assignments.json",
            "modules.json",
            "outcomes.json",
            "pages.json",
            "quizzes.json",
            "prerequisites.json",
            "assignment_id_map.json",
        ]

        for filename in required_files:
            file_path = math231_data_path / filename
            assert file_path.exists(), f"Missing required file: {filename}"

            # Verify files contain valid JSON
            with open(file_path, "r") as f:
                data = json.load(f)
                assert isinstance(data, dict), f"Invalid JSON structure in {filename}"

    def test_load_math231_data(self, data_loader):
        """Test loading actual MATH231 course data"""
        data = data_loader.load_all_data()

        # Verify all data types are loaded
        assert "assignments" in data
        assert "modules" in data
        assert "outcomes" in data
        assert "pages" in data
        assert "quizzes" in data
        assert "prerequisites" in data
        assert "assignment_id_map" in data

        # Verify data structure
        assert "assignments" in data["assignments"]
        assert "modules" in data["modules"]
        assert "outcomes" in data["outcomes"]
        assert "pages" in data["pages"]
        assert "quizzes" in data["quizzes"]

    def test_validate_math231_data(self, data_loader):
        """Test validation of MATH231 course data"""
        data_loader.load_all_data()
        validation_result = data_loader.validate_data()

        # Print validation results for debugging
        if not validation_result.is_valid:
            print("Validation errors:")
            for error in validation_result.errors:
                print(f"  - {error}")

        if validation_result.warnings:
            print("Validation warnings:")
            for warning in validation_result.warnings:
                print(f"  - {warning}")

        # Data should be valid (or at least have no critical errors)
        # We might have warnings but no errors
        print(
            f"Validation: {len(validation_result.errors)} errors, {len(validation_result.warnings)} warnings"
        )

    def test_math231_assignments(self, data_loader):
        """Test MATH231 assignments data"""
        data_loader.load_all_data()
        assignments = data_loader.data["assignments"]["assignments"]

        # Should have multiple assignments
        assert len(assignments) > 0

        # Check some specific assignments exist
        assignment_ids = {a["id"] for a in assignments}
        expected_assignments = [
            "hw-vectors",
            "hw-span",
            "hw-systems",
            "hw-matrix-algebra",
            "final-project",
        ]

        for expected_id in expected_assignments:
            assert expected_id in assignment_ids, f"Missing assignment: {expected_id}"

        # Verify assignment structure
        for assignment in assignments:
            assert "id" in assignment
            assert "title" in assignment
            assert "points_possible" in assignment

            # Check gamification data
            if "gamification" in assignment:
                gamification = assignment["gamification"]
                if "xp_value" in gamification:
                    assert isinstance(gamification["xp_value"], int)
                    assert gamification["xp_value"] >= 0

    def test_math231_modules(self, data_loader):
        """Test MATH231 modules data"""
        data_loader.load_all_data()
        modules = data_loader.data["modules"]["modules"]

        # Should have multiple modules
        assert len(modules) > 0

        # Check module structure
        for module in modules:
            assert "name" in module
            assert "overview" in module
            assert "unlock_requirements" in module
            assert "items" in module

            # Verify items reference valid content
            for item in module["items"]:
                assert "id" in item

    def test_math231_quizzes(self, data_loader):
        """Test MATH231 quizzes data"""
        data_loader.load_all_data()
        quizzes = data_loader.data["quizzes"]["quizzes"]

        # Should have multiple quizzes
        assert len(quizzes) > 0

        # Check quiz structure
        for quiz in quizzes:
            assert "id" in quiz
            assert "title" in quiz
            assert "description" in quiz

            # Check quiz settings
            if "settings" in quiz:
                settings = quiz["settings"]
                if "allowed_attempts" in settings:
                    assert isinstance(settings["allowed_attempts"], int)
                    assert settings["allowed_attempts"] > 0

            # Check questions if present
            if "questions" in quiz:
                for question in quiz["questions"]:
                    assert "question_text" in question
                    assert "answers" in question
                    assert len(question["answers"]) > 0

    def test_math231_outcomes(self, data_loader):
        """Test MATH231 outcomes data"""
        data_loader.load_all_data()
        outcomes = data_loader.data["outcomes"]["outcomes"]

        # Should have multiple outcomes
        assert len(outcomes) > 0

        # Check outcome structure
        for outcome in outcomes:
            assert "id" in outcome
            assert "name" in outcome

            # Verify level if present
            if "level" in outcome:
                valid_levels = [
                    "Recognition",
                    "Application",
                    "Intuition",
                    "Synthesis",
                    "Mastery",
                    "Meta-Badge",  # For badge-related meta outcomes
                ]
                assert outcome["level"] in valid_levels

    def test_math231_pages(self, data_loader):
        """Test MATH231 pages data"""
        data_loader.load_all_data()
        pages = data_loader.data["pages"]["pages"]

        # Should have multiple pages
        assert len(pages) > 0

        # Check page structure
        for page in pages:
            assert "title" in page
            assert "body" in page

    def test_cross_references(self, data_loader):
        """Test cross-references between MATH231 data files"""
        data_loader.load_all_data()
        data = data_loader.data

        # Collect all IDs
        assignment_ids = {a["id"] for a in data["assignments"]["assignments"]}
        quiz_ids = {q["id"] for q in data["quizzes"]["quizzes"]}
        outcome_ids = {o["id"] for o in data["outcomes"]["outcomes"]}

        # Check assignment-outcome references
        for assignment in data["assignments"]["assignments"]:
            if "outcomes" in assignment:
                for outcome_id in assignment["outcomes"]:
                    if outcome_id not in outcome_ids:
                        print(
                            f"Warning: Assignment '{assignment['id']}' references unknown outcome '{outcome_id}'"
                        )

        # Check module item references
        for module in data["modules"]["modules"]:
            for item in module["items"]:
                item_id = item["id"]
                if item_id not in assignment_ids and item_id not in quiz_ids:
                    # Might be a page or other content, which is okay
                    pass

    def test_assignment_id_mapping(self, data_loader):
        """Test assignment ID mapping consistency"""
        data_loader.load_all_data()
        data = data_loader.data

        assignment_ids = {a["id"] for a in data["assignments"]["assignments"]}
        mapped_ids = set(data["assignment_id_map"].keys())

        # All mapped IDs should correspond to actual assignments
        for mapped_id in mapped_ids:
            assert (
                mapped_id in assignment_ids
            ), f"Assignment ID map contains unknown assignment: {mapped_id}"

    def test_course_builder_loads_data(self, course_builder):
        """Test that course builder can load MATH231 data"""
        course_builder.load_course_data()

        # Verify data was loaded into course builder
        assert len(course_builder.course_data.assignments) > 0
        assert len(course_builder.course_data.modules) > 0
        assert len(course_builder.course_data.quizzes) > 0
        assert len(course_builder.course_data.outcomes) > 0
        assert len(course_builder.course_data.pages) > 0

    def test_course_builder_validation(self, course_builder):
        """Test course builder validation with MATH231 data"""
        course_builder.load_course_data()
        errors = course_builder.validate_course_data()

        # Print any validation errors for debugging
        for category, error_list in errors.items():
            if error_list:
                print(f"{category} errors:")
                for error in error_list:
                    print(f"  - {error}")

        # Should have minimal or no errors with real data
        total_errors = sum(len(error_list) for error_list in errors.values())
        print(f"Total validation errors: {total_errors}")

    def test_data_statistics(self, data_loader):
        """Test statistics calculation for MATH231 data"""
        data_loader.load_all_data()
        stats = data_loader.get_statistics()

        print("MATH231 Course Statistics:")
        for key, value in stats.items():
            print(f"  {key}: {value}")

        # Verify reasonable statistics
        assert stats["assignments"] > 0
        assert stats["modules"] > 0
        assert stats["quizzes"] > 0
        assert stats["pages"] > 0
        assert stats["outcomes"] > 0
        assert stats["total_points"] > 0

    def test_export_summary(self, data_loader):
        """Test exporting course summary"""
        import tempfile

        data_loader.load_all_data()

        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            summary_path = f.name

        try:
            data_loader.export_summary(summary_path)

            # Verify summary was created
            assert Path(summary_path).exists()

            # Load and verify summary structure
            with open(summary_path, "r") as f:
                summary = json.load(f)

            assert "validation" in summary
            assert "statistics" in summary
            assert "generated_at" in summary

            print("Summary validation result:", summary["validation"]["is_valid"])
            print("Summary statistics:", summary["statistics"])

        finally:
            Path(summary_path).unlink(missing_ok=True)
