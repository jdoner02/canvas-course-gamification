#!/usr/bin/env python3
"""
Performance tests for Canvas Course Gamification
"""

import pytest
import time
import json
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock

from src.course_builder.data_loader import CourseDataLoader
from src.course_builder.json_course_builder import JsonCourseBuilder, CanvasConfig


class TestPerformance:
    """Performance tests for course building operations"""

    @pytest.fixture
    def large_course_data(self):
        """Generate large course data for performance testing"""
        # Create data with many assignments, modules, etc.
        assignments = []
        for i in range(100):  # 100 assignments
            assignments.append(
                {
                    "id": f"assignment-{i}",
                    "title": f"Assignment {i}",
                    "description": f"Description for assignment {i}",
                    "points_possible": 100,
                    "due_at": "2025-12-31T23:59:00Z",
                    "gamification": {"xp_value": 100},
                    "outcomes": [f"outcome-{i % 10}"],  # 10 outcomes reused
                }
            )

        modules = []
        for i in range(20):  # 20 modules
            items = [
                {"id": f"assignment-{j}"} for j in range(i * 5, (i + 1) * 5)
            ]  # 5 assignments per module
            modules.append(
                {
                    "name": f"Module {i}",
                    "overview": f"Overview for module {i}",
                    "unlock_requirements": [] if i == 0 else [f"module_{i-1}_complete"],
                    "mastery_criteria": {"min_score": 75},
                    "items": items,
                }
            )

        quizzes = []
        for i in range(50):  # 50 quizzes
            questions = []
            for j in range(10):  # 10 questions per quiz
                questions.append(
                    {
                        "type": "multiple_choice_question",
                        "question_text": f"Question {j} for quiz {i}?",
                        "answers": [
                            {"text": "Correct", "weight": 100},
                            {"text": "Wrong 1", "weight": 0},
                            {"text": "Wrong 2", "weight": 0},
                            {"text": "Wrong 3", "weight": 0},
                        ],
                        "points_possible": 1,
                    }
                )

            quizzes.append(
                {
                    "id": f"quiz-{i}",
                    "title": f"Quiz {i}",
                    "description": f"Description for quiz {i}",
                    "settings": {"allowed_attempts": 3},
                    "questions": questions,
                }
            )

        outcomes = []
        for i in range(10):  # 10 outcomes
            outcomes.append(
                {
                    "id": f"outcome-{i}",
                    "name": f"Learning Outcome {i}",
                    "description": f"Students will be able to do task {i}",
                    "level": "Application",
                    "module": i % 5 + 1,
                }
            )

        pages = []
        for i in range(30):  # 30 pages
            pages.append(
                {
                    "title": f"Page {i}",
                    "body": f"<h1>Page {i}</h1><p>{'Content ' * 100}</p>",  # Long content
                }
            )

        return {
            "assignments.json": {"assignments": assignments},
            "modules.json": {"modules": modules},
            "quizzes.json": {"quizzes": quizzes},
            "outcomes.json": {"outcomes": outcomes},
            "pages.json": {"pages": pages},
            "prerequisites.json": {"prerequisites": []},
            "assignment_id_map.json": {
                f"assignment-{i}": 10000 + i for i in range(100)
            },
        }

    @pytest.fixture
    def large_data_dir(self, temp_dir, large_course_data):
        """Create directory with large course data"""
        for filename, data in large_course_data.items():
            with open(temp_dir / filename, "w") as f:
                json.dump(data, f)
        return temp_dir

    @pytest.mark.slow
    def test_load_large_dataset_performance(self, large_data_dir):
        """Test loading performance with large dataset"""
        loader = CourseDataLoader(str(large_data_dir))

        start_time = time.time()
        loader.load_all_data()
        load_time = time.time() - start_time

        print(f"Load time for large dataset: {load_time:.2f} seconds")

        # Should load within reasonable time (adjust threshold as needed)
        assert load_time < 5.0, f"Loading took too long: {load_time:.2f}s"

        # Verify data was loaded correctly
        assert len(loader.data["assignments"]["assignments"]) == 100
        assert len(loader.data["modules"]["modules"]) == 20
        assert len(loader.data["quizzes"]["quizzes"]) == 50

    @pytest.mark.slow
    def test_validation_performance(self, large_data_dir):
        """Test validation performance with large dataset"""
        loader = CourseDataLoader(str(large_data_dir))
        loader.load_all_data()

        start_time = time.time()
        result = loader.validate_data()
        validation_time = time.time() - start_time

        print(f"Validation time for large dataset: {validation_time:.2f} seconds")

        # Should validate within reasonable time
        assert (
            validation_time < 10.0
        ), f"Validation took too long: {validation_time:.2f}s"

        # Should be valid
        assert result.is_valid

    def test_memory_usage_large_dataset(self, large_data_dir):
        """Test memory usage with large dataset"""
        import psutil
        import os

        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss / 1024 / 1024  # MB

        loader = CourseDataLoader(str(large_data_dir))
        loader.load_all_data()

        peak_memory = process.memory_info().rss / 1024 / 1024  # MB
        memory_increase = peak_memory - initial_memory

        print(f"Memory usage increase: {memory_increase:.2f} MB")

        # Should not use excessive memory (adjust threshold as needed)
        assert memory_increase < 100, f"Memory usage too high: {memory_increase:.2f} MB"

    def test_concurrent_validation(self, sample_data_dir):
        """Test concurrent validation operations"""
        import concurrent.futures

        def validate_data():
            loader = CourseDataLoader(str(sample_data_dir))
            loader.load_all_data()
            return loader.validate_data()

        start_time = time.time()

        # Run multiple validations concurrently
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
            futures = [executor.submit(validate_data) for _ in range(10)]
            results = [
                future.result() for future in concurrent.futures.as_completed(futures)
            ]

        elapsed_time = time.time() - start_time
        print(f"Concurrent validation time: {elapsed_time:.2f} seconds")

        # All should be valid
        assert all(result.is_valid for result in results)

        # Should complete within reasonable time
        assert elapsed_time < 5.0

    @pytest.mark.slow
    def test_course_builder_initialization_performance(
        self, large_data_dir, canvas_config
    ):
        """Test course builder initialization performance"""
        start_time = time.time()

        builder = JsonCourseBuilder(str(large_data_dir), canvas_config)
        builder.load_course_data()

        init_time = time.time() - start_time
        print(f"Course builder initialization time: {init_time:.2f} seconds")

        # Should initialize quickly
        assert init_time < 3.0, f"Initialization took too long: {init_time:.2f}s"

    def test_statistics_calculation_performance(self, large_data_dir):
        """Test statistics calculation performance"""
        loader = CourseDataLoader(str(large_data_dir))
        loader.load_all_data()

        start_time = time.time()
        stats = loader.get_statistics()
        calc_time = time.time() - start_time

        print(f"Statistics calculation time: {calc_time:.2f} seconds")

        # Should calculate quickly
        assert (
            calc_time < 1.0
        ), f"Statistics calculation took too long: {calc_time:.2f}s"

        # Verify statistics are correct
        assert stats["assignments"] == 100
        assert stats["modules"] == 20
        assert stats["quizzes"] == 50
        assert stats["total_questions"] == 500  # 50 quizzes * 10 questions

    def test_json_serialization_performance(self, large_data_dir):
        """Test JSON serialization/deserialization performance"""
        loader = CourseDataLoader(str(large_data_dir))
        loader.load_all_data()

        # Test serialization
        start_time = time.time()
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json") as f:
            json.dump(loader.data, f)
        serialization_time = time.time() - start_time

        print(f"JSON serialization time: {serialization_time:.2f} seconds")
        assert serialization_time < 2.0

        # Test export summary
        start_time = time.time()
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json") as f:
            loader.export_summary(f.name)
        export_time = time.time() - start_time

        print(f"Summary export time: {export_time:.2f} seconds")
        assert export_time < 2.0


class TestScalability:
    """Test scalability with different data sizes"""

    def create_dataset(self, size_factor):
        """Create dataset of given size"""
        num_assignments = 10 * size_factor
        num_modules = 2 * size_factor
        num_quizzes = 5 * size_factor

        assignments = [
            {
                "id": f"assignment-{i}",
                "title": f"Assignment {i}",
                "description": f"Description {i}",
                "points_possible": 100,
                "gamification": {"xp_value": 100},
            }
            for i in range(num_assignments)
        ]

        modules = [
            {
                "name": f"Module {i}",
                "overview": f"Overview {i}",
                "unlock_requirements": [],
                "items": [{"id": f"assignment-{j}"} for j in range(i * 2, (i + 1) * 2)],
            }
            for i in range(num_modules)
        ]

        quizzes = [
            {
                "id": f"quiz-{i}",
                "title": f"Quiz {i}",
                "description": f"Description {i}",
                "questions": [
                    {
                        "type": "multiple_choice_question",
                        "question_text": f"Question {j}?",
                        "answers": [{"text": "Answer", "weight": 100}],
                        "points_possible": 1,
                    }
                    for j in range(5)  # 5 questions per quiz
                ],
            }
            for i in range(num_quizzes)
        ]

        return {
            "assignments.json": {"assignments": assignments},
            "modules.json": {"modules": modules},
            "quizzes.json": {"quizzes": quizzes},
            "outcomes.json": {"outcomes": []},
            "pages.json": {"pages": []},
            "prerequisites.json": {"prerequisites": []},
            "assignment_id_map.json": {},
        }

    @pytest.mark.parametrize("size_factor", [1, 2, 5, 10])
    def test_load_time_scaling(self, temp_dir, size_factor):
        """Test how load time scales with data size"""
        data = self.create_dataset(size_factor)

        # Write data files
        for filename, content in data.items():
            with open(temp_dir / filename, "w") as f:
                json.dump(content, f)

        # Measure load time
        loader = CourseDataLoader(str(temp_dir))
        start_time = time.time()
        loader.load_all_data()
        load_time = time.time() - start_time

        print(f"Size factor {size_factor}: Load time {load_time:.3f}s")

        # Load time should scale reasonably (not exponentially)
        expected_max_time = 0.1 * size_factor  # Linear scaling assumption
        assert (
            load_time < expected_max_time
        ), f"Load time {load_time:.3f}s exceeds expected {expected_max_time:.3f}s"

    @pytest.mark.parametrize("size_factor", [1, 2, 5])
    def test_validation_time_scaling(self, temp_dir, size_factor):
        """Test how validation time scales with data size"""
        data = self.create_dataset(size_factor)

        # Write data files
        for filename, content in data.items():
            with open(temp_dir / filename, "w") as f:
                json.dump(content, f)

        # Measure validation time
        loader = CourseDataLoader(str(temp_dir))
        loader.load_all_data()

        start_time = time.time()
        result = loader.validate_data()
        validation_time = time.time() - start_time

        print(f"Size factor {size_factor}: Validation time {validation_time:.3f}s")

        # Validation should complete in reasonable time
        expected_max_time = 0.5 * size_factor
        assert validation_time < expected_max_time
        assert result.is_valid
