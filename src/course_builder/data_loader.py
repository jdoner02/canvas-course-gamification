#!/usr/bin/env python3
"""
Course Data Loader and Validator
Loads and validates JSON course configuration files
"""

import json
import logging
from typing import Dict, List, Optional, Any, Set
from pathlib import Path
from dataclasses import dataclass
from datetime import datetime


@dataclass
class ValidationResult:
    """Result of data validation"""

    is_valid: bool
    errors: List[str]
    warnings: List[str]

    def add_error(self, message: str) -> None:
        """Add validation error"""
        self.errors.append(message)
        self.is_valid = False

    def add_warning(self, message: str) -> None:
        """Add validation warning"""
        self.warnings.append(message)


class CourseDataLoader:
    """Loads and validates course JSON data"""

    def __init__(self, data_path: str):
        """Initialize loader

        Args:
            data_path: Path to directory containing JSON files
        """
        self.data_path = Path(data_path)
        self.logger = logging.getLogger(__name__)
        self.data = {}

    def load_all_data(self) -> Dict[str, Any]:
        """Load all JSON course data files

        Returns:
            Dictionary containing all loaded data
        """
        files_to_load = {
            "assignments": "assignments.json",
            "modules": "modules.json",
            "outcomes": "outcomes.json",
            "pages": "pages.json",
            "quizzes": "quizzes.json",
            "prerequisites": "prerequisites.json",
            "assignment_id_map": "assignment_id_map.json",
        }

        for key, filename in files_to_load.items():
            file_path = self.data_path / filename
            if file_path.exists():
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        self.data[key] = json.load(f)
                    self.logger.info(f"Loaded {filename}")
                except Exception as e:
                    self.logger.error(f"Error loading {filename}: {e}")
                    self.data[key] = {}
            else:
                self.logger.warning(f"File not found: {filename}")
                self.data[key] = {}

        return self.data

    def validate_data(self) -> ValidationResult:
        """Validate all loaded course data

        Returns:
            Validation result with errors and warnings
        """
        result = ValidationResult(is_valid=True, errors=[], warnings=[])

        # Validate assignments
        self._validate_assignments(result)

        # Validate modules
        self._validate_modules(result)

        # Validate quizzes
        self._validate_quizzes(result)

        # Validate pages
        self._validate_pages(result)

        # Validate outcomes
        self._validate_outcomes(result)

        # Validate cross-references
        self._validate_references(result)

        return result

    def _validate_assignments(self, result: ValidationResult) -> None:
        """Validate assignments data"""
        assignments = self.data.get("assignments", {}).get("assignments", [])

        assignment_ids = set()

        for i, assignment in enumerate(assignments):
            prefix = f"Assignment {i + 1}"

            # Required fields
            if not assignment.get("id"):
                result.add_error(f"{prefix}: Missing required field 'id'")
            else:
                if assignment["id"] in assignment_ids:
                    result.add_error(
                        f"{prefix}: Duplicate assignment ID '{assignment['id']}'"
                    )
                assignment_ids.add(assignment["id"])

            if not assignment.get("title"):
                result.add_error(f"{prefix}: Missing required field 'title'")

            if not assignment.get("description"):
                result.add_warning(f"{prefix}: Missing description")

            # Points validation
            points = assignment.get("points_possible")
            if points is None:
                result.add_error(f"{prefix}: Missing 'points_possible'")
            elif not isinstance(points, (int, float)) or points < 0:
                result.add_error(f"{prefix}: Invalid 'points_possible' value")

            # Due date validation
            due_at = assignment.get("due_at")
            if due_at:
                try:
                    datetime.fromisoformat(due_at.replace("Z", "+00:00"))
                except ValueError:
                    result.add_error(f"{prefix}: Invalid due_at format '{due_at}'")

            # Gamification validation
            gamification = assignment.get("gamification", {})
            if "xp_value" in gamification:
                if (
                    not isinstance(gamification["xp_value"], int)
                    or gamification["xp_value"] < 0
                ):
                    result.add_error(f"{prefix}: Invalid XP value")

    def _validate_modules(self, result: ValidationResult) -> None:
        """Validate modules data"""
        modules = self.data.get("modules", {}).get("modules", [])

        module_names = set()

        for i, module in enumerate(modules):
            prefix = f"Module {i + 1}"

            # Required fields
            if not module.get("name"):
                result.add_error(f"{prefix}: Missing required field 'name'")
            else:
                if module["name"] in module_names:
                    result.add_error(
                        f"{prefix}: Duplicate module name '{module['name']}'"
                    )
                module_names.add(module["name"])

            if not module.get("overview"):
                result.add_warning(f"{prefix}: Missing overview")

            # Unlock requirements validation
            unlock_reqs = module.get("unlock_requirements", [])
            if not isinstance(unlock_reqs, list):
                result.add_error(f"{prefix}: unlock_requirements must be a list")

            # Mastery criteria validation
            mastery = module.get("mastery_criteria", {})
            if "min_score" in mastery:
                min_score = mastery["min_score"]
                if min_score is not None and (
                    not isinstance(min_score, (int, float))
                    or min_score < 0
                    or min_score > 100
                ):
                    result.add_error(f"{prefix}: Invalid min_score value")

            # Items validation
            items = module.get("items", [])
            if not isinstance(items, list):
                result.add_error(f"{prefix}: items must be a list")
            elif not items:
                result.add_warning(f"{prefix}: No items defined")

    def _validate_quizzes(self, result: ValidationResult) -> None:
        """Validate quizzes data"""
        quizzes = self.data.get("quizzes", {}).get("quizzes", [])

        quiz_ids = set()

        for i, quiz in enumerate(quizzes):
            prefix = f"Quiz {i + 1}"

            # Required fields
            if not quiz.get("id"):
                result.add_error(f"{prefix}: Missing required field 'id'")
            else:
                if quiz["id"] in quiz_ids:
                    result.add_error(f"{prefix}: Duplicate quiz ID '{quiz['id']}'")
                quiz_ids.add(quiz["id"])

            if not quiz.get("title"):
                result.add_error(f"{prefix}: Missing required field 'title'")

            # Settings validation
            settings = quiz.get("settings", {})
            if "allowed_attempts" in settings:
                attempts = settings["allowed_attempts"]
                if not isinstance(attempts, int) or attempts < 1:
                    result.add_error(f"{prefix}: Invalid allowed_attempts value")

            if "time_limit" in settings:
                time_limit = settings["time_limit"]
                if time_limit is not None and (
                    not isinstance(time_limit, int) or time_limit < 1
                ):
                    result.add_error(f"{prefix}: Invalid time_limit value")

            # Questions validation
            questions = quiz.get("questions", [])
            if not isinstance(questions, list):
                result.add_error(f"{prefix}: questions must be a list")
            else:
                for j, question in enumerate(questions):
                    self._validate_question(
                        question, f"{prefix} Question {j + 1}", result
                    )

    def _validate_question(
        self, question: Dict, prefix: str, result: ValidationResult
    ) -> None:
        """Validate a single quiz question"""
        if not question.get("question_text"):
            result.add_error(f"{prefix}: Missing question_text")

        if not question.get("type"):
            result.add_error(f"{prefix}: Missing question type")

        # Points validation
        points = question.get("points_possible")
        if points is None:
            result.add_warning(f"{prefix}: Missing points_possible")
        elif not isinstance(points, (int, float)) or points < 0:
            result.add_error(f"{prefix}: Invalid points_possible value")

        # Answers validation
        answers = question.get("answers", [])
        if not isinstance(answers, list):
            result.add_error(f"{prefix}: answers must be a list")
        elif not answers:
            result.add_error(f"{prefix}: No answers provided")
        else:
            correct_answers = sum(1 for ans in answers if ans.get("weight", 0) > 0)
            if correct_answers == 0:
                result.add_error(f"{prefix}: No correct answers found")

    def _validate_pages(self, result: ValidationResult) -> None:
        """Validate pages data"""
        pages = self.data.get("pages", {}).get("pages", [])

        page_titles = set()

        for i, page in enumerate(pages):
            prefix = f"Page {i + 1}"

            # Required fields
            title = page.get("title")
            if not title:
                result.add_error(f"{prefix}: Missing required field 'title'")
            else:
                if title in page_titles:
                    result.add_error(f"{prefix}: Duplicate page title '{title}'")
                page_titles.add(title)

            if not page.get("body"):
                result.add_warning(f"{prefix}: Missing page body content")

    def _validate_outcomes(self, result: ValidationResult) -> None:
        """Validate outcomes data"""
        outcomes = self.data.get("outcomes", {}).get("outcomes", [])

        outcome_ids = set()

        for i, outcome in enumerate(outcomes):
            prefix = f"Outcome {i + 1}"

            # Required fields
            if not outcome.get("id"):
                result.add_error(f"{prefix}: Missing required field 'id'")
            else:
                if outcome["id"] in outcome_ids:
                    result.add_error(
                        f"{prefix}: Duplicate outcome ID '{outcome['id']}'"
                    )
                outcome_ids.add(outcome["id"])

            if not outcome.get("name"):
                result.add_error(f"{prefix}: Missing required field 'name'")

            # Level validation
            level = outcome.get("level")
            valid_levels = [
                "Recognition",
                "Application",
                "Intuition",
                "Synthesis",
                "Mastery",
            ]
            if level and level not in valid_levels:
                result.add_warning(f"{prefix}: Unknown level '{level}'")

            # Module validation
            module = outcome.get("module")
            if module is not None and (not isinstance(module, int) or module < 0):
                result.add_error(f"{prefix}: Invalid module number")

    def _validate_references(self, result: ValidationResult) -> None:
        """Validate cross-references between data files"""
        # Get all IDs
        assignment_ids = {
            a.get("id")
            for a in self.data.get("assignments", {}).get("assignments", [])
            if a.get("id")
        }
        quiz_ids = {
            q.get("id")
            for q in self.data.get("quizzes", {}).get("quizzes", [])
            if q.get("id")
        }
        outcome_ids = {
            o.get("id")
            for o in self.data.get("outcomes", {}).get("outcomes", [])
            if o.get("id")
        }
        page_titles = {
            p.get("title")
            for p in self.data.get("pages", {}).get("pages", [])
            if p.get("title")
        }

        # Check module item references
        modules = self.data.get("modules", {}).get("modules", [])
        for module in modules:
            for item in module.get("items", []):
                item_id = item.get("id")
                if item_id:
                    if (
                        item_id not in assignment_ids
                        and item_id not in quiz_ids
                        and item_id not in page_titles
                    ):
                        result.add_warning(
                            f"Module '{module.get('name', '')}' references unknown item '{item_id}'"
                        )

        # Check assignment outcome references
        assignments = self.data.get("assignments", {}).get("assignments", [])
        for assignment in assignments:
            for outcome_id in assignment.get("outcomes", []):
                if outcome_id not in outcome_ids:
                    result.add_warning(
                        f"Assignment '{assignment.get('id', '')}' references unknown outcome '{outcome_id}'"
                    )

        # Check quiz outcome references
        quizzes = self.data.get("quizzes", {}).get("quizzes", [])
        for quiz in quizzes:
            for outcome_id in quiz.get("outcomes", []):
                if outcome_id not in outcome_ids:
                    result.add_warning(
                        f"Quiz '{quiz.get('id', '')}' references unknown outcome '{outcome_id}'"
                    )

    def get_statistics(self) -> Dict[str, Any]:
        """Get statistics about the course data

        Returns:
            Dictionary with data statistics
        """
        stats = {
            "assignments": len(self.data.get("assignments", {}).get("assignments", [])),
            "modules": len(self.data.get("modules", {}).get("modules", [])),
            "quizzes": len(self.data.get("quizzes", {}).get("quizzes", [])),
            "pages": len(self.data.get("pages", {}).get("pages", [])),
            "outcomes": len(self.data.get("outcomes", {}).get("outcomes", [])),
            "total_questions": 0,
            "total_points": 0,
            "xp_available": 0,
        }

        # Count quiz questions
        for quiz in self.data.get("quizzes", {}).get("quizzes", []):
            stats["total_questions"] += len(quiz.get("questions", []))

        # Count points and XP
        for assignment in self.data.get("assignments", {}).get("assignments", []):
            stats["total_points"] += assignment.get("points_possible", 0)
            stats["xp_available"] += assignment.get("gamification", {}).get(
                "xp_value", 0
            )

        return stats

    def export_summary(self, output_path: str) -> None:
        """Export a summary of the course data

        Args:
            output_path: Path to save summary file
        """
        validation = self.validate_data()
        stats = self.get_statistics()

        summary = {
            "validation": {
                "is_valid": validation.is_valid,
                "error_count": len(validation.errors),
                "warning_count": len(validation.warnings),
                "errors": validation.errors,
                "warnings": validation.warnings,
            },
            "statistics": stats,
            "generated_at": datetime.now().isoformat(),
        }

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)

        self.logger.info(f"Course summary exported to {output_path}")
