#!/usr/bin/env python3
"""
JSON-based Canvas Course Builder
Builds Canvas course structure from JSON configuration files
"""

import json
import requests
import logging
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, field
from pathlib import Path
import time
from datetime import datetime


@dataclass
class CanvasConfig:
    """Canvas API configuration"""

    base_url: str
    token: str
    account_id: int
    term_id: Optional[int] = None


@dataclass
class CourseData:
    """Container for all course JSON data"""

    assignments: Dict[str, Any] = field(default_factory=dict)
    modules: Dict[str, Any] = field(default_factory=dict)
    outcomes: Dict[str, Any] = field(default_factory=dict)
    pages: Dict[str, Any] = field(default_factory=dict)
    quizzes: Dict[str, Any] = field(default_factory=dict)
    prerequisites: Dict[str, Any] = field(default_factory=dict)
    assignment_id_map: Dict[str, int] = field(default_factory=dict)


class JsonCourseBuilder:
    """Builds Canvas course from JSON configuration files"""

    def __init__(self, data_path: str, canvas_config: CanvasConfig):
        """Initialize course builder

        Args:
            data_path: Path to directory containing JSON files
            canvas_config: Canvas API configuration
        """
        self.data_path = Path(data_path)
        self.canvas_config = canvas_config
        self.headers = {
            "Authorization": f"Bearer {canvas_config.token}",
            "Content-Type": "application/json",
        }
        self.course_data = CourseData()
        self.course_id: Optional[int] = None

        # Setup logging
        self.logger = logging.getLogger(__name__)

    def load_course_data(self) -> None:
        """Load all JSON configuration files"""
        try:
            # Load main data files
            files_to_load = [
                "assignments.json",
                "modules.json",
                "outcomes.json",
                "pages.json",
                "quizzes.json",
                "prerequisites.json",
                "assignment_id_map.json",
            ]

            for filename in files_to_load:
                file_path = self.data_path / filename
                if file_path.exists():
                    with open(file_path, "r", encoding="utf-8") as f:
                        data = json.load(f)
                        # Store data using filename (without .json) as key
                        key = filename.replace(".json", "").replace("_", "")
                        if key == "assignmentidmap":
                            self.course_data.assignment_id_map = data
                        else:
                            setattr(self.course_data, key, data)
                else:
                    self.logger.warning(f"File not found: {file_path}")

        except Exception as e:
            self.logger.error(f"Error loading course data: {e}")
            raise

    def create_course(self, course_name: str, course_code: str) -> int:
        """Create a new Canvas course

        Args:
            course_name: Full course name
            course_code: Course code (e.g., MATH231)

        Returns:
            Course ID of created course
        """
        url = f"{self.canvas_config.base_url}/api/v1/accounts/{self.canvas_config.account_id}/courses"

        course_data = {
            "course": {
                "name": course_name,
                "course_code": course_code,
                "is_public": False,
                "enrollment_term_id": self.canvas_config.term_id,
                "default_view": "modules",
                "grading_standard_enabled": True,
                "course_format": "on_campus",
            }
        }

        response = requests.post(url, headers=self.headers, json=course_data)
        response.raise_for_status()

        course = response.json()
        self.course_id = course["id"]
        self.logger.info(f"Created course: {course_name} (ID: {self.course_id})")

        return self.course_id

    def create_outcomes(self) -> Dict[str, int]:
        """Create learning outcomes

        Returns:
            Mapping of outcome IDs to Canvas outcome IDs
        """
        if not self.course_id:
            raise ValueError("Must create course first")

        url = f"{self.canvas_config.base_url}/api/v1/courses/{self.course_id}/outcome_groups"

        outcome_map = {}

        # Create outcomes from the outcomes data
        for outcome in self.course_data.outcomes.get("outcomes", []):
            outcome_data = {
                "title": outcome.get("name", ""),
                "description": outcome.get("description", ""),
                "mastery_points": 3,
                "ratings": [
                    {"description": "Exceeds Expectations", "points": 4},
                    {"description": "Meets Expectations", "points": 3},
                    {"description": "Approaches Expectations", "points": 2},
                    {"description": "Below Expectations", "points": 1},
                ],
            }

            try:
                response = requests.post(
                    f"{url}/root/outcomes",
                    headers=self.headers,
                    json={"outcome": outcome_data},
                )
                response.raise_for_status()
                created_outcome = response.json()
                outcome_map[outcome["id"]] = created_outcome["id"]
                self.logger.info(f"Created outcome: {outcome['name']}")

            except Exception as e:
                self.logger.error(
                    f"Failed to create outcome {outcome.get('name', '')}: {e}"
                )

        return outcome_map

    def create_pages(self) -> Dict[str, int]:
        """Create course pages

        Returns:
            Mapping of page titles to Canvas page IDs
        """
        if not self.course_id:
            raise ValueError("Must create course first")

        url = f"{self.canvas_config.base_url}/api/v1/courses/{self.course_id}/pages"

        page_map = {}

        for page in self.course_data.pages.get("pages", []):
            page_data = {
                "wiki_page": {
                    "title": page.get("title", "Untitled Page"),
                    "body": page.get("body", ""),
                    "published": True,
                    "front_page": page.get("front_page", False),
                }
            }

            try:
                response = requests.post(url, headers=self.headers, json=page_data)
                response.raise_for_status()
                created_page = response.json()
                page_map[page.get("title", "")] = created_page["page_id"]
                self.logger.info(f"Created page: {page.get('title', '')}")

            except Exception as e:
                self.logger.error(f"Failed to create page {page.get('title', '')}: {e}")

        return page_map

    def create_assignments(self) -> Dict[str, int]:
        """Create assignments

        Returns:
            Mapping of assignment IDs to Canvas assignment IDs
        """
        if not self.course_id:
            raise ValueError("Must create course first")

        url = (
            f"{self.canvas_config.base_url}/api/v1/courses/{self.course_id}/assignments"
        )

        assignment_map = {}

        for assignment in self.course_data.assignments.get("assignments", []):
            assignment_data = {
                "assignment": {
                    "name": assignment.get("title", ""),
                    "description": assignment.get("description", ""),
                    "points_possible": assignment.get("points_possible", 100),
                    "grading_type": "points",
                    "submission_types": ["online_text_entry", "online_upload"],
                    "published": True,
                    "due_at": assignment.get("due_at"),
                    "grading_standard_id": None,
                }
            }

            try:
                response = requests.post(
                    url, headers=self.headers, json=assignment_data
                )
                response.raise_for_status()
                created_assignment = response.json()
                assignment_map[assignment["id"]] = created_assignment["id"]
                self.logger.info(f"Created assignment: {assignment.get('title', '')}")

                # Add to assignment ID map for future reference
                self.course_data.assignment_id_map[assignment["id"]] = (
                    created_assignment["id"]
                )

            except Exception as e:
                self.logger.error(
                    f"Failed to create assignment {assignment.get('title', '')}: {e}"
                )

        return assignment_map

    def create_quizzes(self) -> Dict[str, int]:
        """Create quizzes

        Returns:
            Mapping of quiz IDs to Canvas quiz IDs
        """
        if not self.course_id:
            raise ValueError("Must create course first")

        url = f"{self.canvas_config.base_url}/api/v1/courses/{self.course_id}/quizzes"

        quiz_map = {}

        for quiz in self.course_data.quizzes.get("quizzes", []):
            quiz_data = {
                "quiz": {
                    "title": quiz.get("title", ""),
                    "description": quiz.get("description", ""),
                    "quiz_type": "assignment",
                    "time_limit": quiz.get("settings", {}).get("time_limit"),
                    "allowed_attempts": quiz.get("settings", {}).get(
                        "allowed_attempts", 1
                    ),
                    "scoring_policy": "keep_highest",
                    "shuffle_answers": quiz.get("settings", {}).get(
                        "shuffle_answers", False
                    ),
                    "published": True,
                }
            }

            try:
                response = requests.post(url, headers=self.headers, json=quiz_data)
                response.raise_for_status()
                created_quiz = response.json()
                quiz_map[quiz["id"]] = created_quiz["id"]
                self.logger.info(f"Created quiz: {quiz.get('title', '')}")

                # Create quiz questions
                self._create_quiz_questions(
                    created_quiz["id"], quiz.get("questions", [])
                )

            except Exception as e:
                self.logger.error(f"Failed to create quiz {quiz.get('title', '')}: {e}")

        return quiz_map

    def _create_quiz_questions(self, quiz_id: int, questions: List[Dict]) -> None:
        """Create questions for a quiz

        Args:
            quiz_id: Canvas quiz ID
            questions: List of question data
        """
        url = f"{self.canvas_config.base_url}/api/v1/courses/{self.course_id}/quizzes/{quiz_id}/questions"

        for question in questions:
            question_data = {
                "question": {
                    "question_name": f"Question",
                    "question_text": question.get("question_text", ""),
                    "question_type": question.get("type", "multiple_choice_question"),
                    "points_possible": question.get("points_possible", 1),
                    "answers": question.get("answers", []),
                }
            }

            try:
                response = requests.post(url, headers=self.headers, json=question_data)
                response.raise_for_status()
                self.logger.debug(f"Created question for quiz {quiz_id}")

            except Exception as e:
                self.logger.error(f"Failed to create question for quiz {quiz_id}: {e}")

    def create_modules(
        self,
        assignment_map: Dict[str, int],
        quiz_map: Dict[str, int],
        page_map: Dict[str, int],
    ) -> Dict[str, int]:
        """Create course modules

        Args:
            assignment_map: Mapping of assignment IDs to Canvas IDs
            quiz_map: Mapping of quiz IDs to Canvas IDs
            page_map: Mapping of page titles to Canvas IDs

        Returns:
            Mapping of module names to Canvas module IDs
        """
        if not self.course_id:
            raise ValueError("Must create course first")

        url = f"{self.canvas_config.base_url}/api/v1/courses/{self.course_id}/modules"

        module_map = {}

        for module in self.course_data.modules.get("modules", []):
            module_data = {
                "module": {
                    "name": module.get("name", ""),
                    "unlock_at": module.get("unlock_at"),
                    "require_sequential_progress": True,
                    "publish_final_grade": False,
                    "prerequisite_module_ids": [],
                }
            }

            try:
                response = requests.post(url, headers=self.headers, json=module_data)
                response.raise_for_status()
                created_module = response.json()
                module_map[module["name"]] = created_module["id"]
                self.logger.info(f"Created module: {module.get('name', '')}")

                # Create module items
                self._create_module_items(
                    created_module["id"],
                    module.get("items", []),
                    assignment_map,
                    quiz_map,
                    page_map,
                )

            except Exception as e:
                self.logger.error(
                    f"Failed to create module {module.get('name', '')}: {e}"
                )

        return module_map

    def _create_module_items(
        self,
        module_id: int,
        items: List[Dict],
        assignment_map: Dict[str, int],
        quiz_map: Dict[str, int],
        page_map: Dict[str, int],
    ) -> None:
        """Create items for a module

        Args:
            module_id: Canvas module ID
            items: List of module item data
            assignment_map: Assignment ID mapping
            quiz_map: Quiz ID mapping
            page_map: Page ID mapping
        """
        url = f"{self.canvas_config.base_url}/api/v1/courses/{self.course_id}/modules/{module_id}/items"

        for item in items:
            item_id = item.get("id", "")
            item_type = None
            content_id = None

            # Determine item type and Canvas ID
            if item_id in assignment_map:
                item_type = "Assignment"
                content_id = assignment_map[item_id]
            elif item_id in quiz_map:
                item_type = "Quiz"
                content_id = quiz_map[item_id]
            elif item_id in page_map:
                item_type = "Page"
                content_id = page_map[item_id]
            else:
                # Create as external URL or text header
                item_type = "SubHeader"

            item_data = {
                "module_item": {
                    "title": item.get("title", item_id),
                    "type": item_type,
                    "content_id": content_id,
                    "published": True,
                }
            }

            try:
                response = requests.post(url, headers=self.headers, json=item_data)
                response.raise_for_status()
                self.logger.debug(f"Created module item: {item.get('title', item_id)}")

            except Exception as e:
                self.logger.error(
                    f"Failed to create module item {item.get('title', item_id)}: {e}"
                )

    def build_course(self, course_name: str, course_code: str) -> int:
        """Build complete course from JSON data

        Args:
            course_name: Full course name
            course_code: Course code

        Returns:
            Canvas course ID
        """
        self.logger.info(f"Starting course build: {course_name}")

        # Load all course data
        self.load_course_data()

        # Create course
        course_id = self.create_course(course_name, course_code)

        # Create outcomes
        outcome_map = self.create_outcomes()

        # Create pages
        page_map = self.create_pages()

        # Create assignments
        assignment_map = self.create_assignments()

        # Create quizzes
        quiz_map = self.create_quizzes()

        # Create modules (must be last to reference other content)
        module_map = self.create_modules(assignment_map, quiz_map, page_map)

        self.logger.info(f"Course build complete: {course_name} (ID: {course_id})")

        return course_id

    def validate_course_data(self) -> Dict[str, List[str]]:
        """Validate course data for consistency

        Returns:
            Dictionary of validation errors by category
        """
        errors = {
            "assignments": [],
            "modules": [],
            "quizzes": [],
            "pages": [],
            "outcomes": [],
            "references": [],
        }

        # Validate assignments
        for assignment in self.course_data.assignments.get("assignments", []):
            if not assignment.get("id"):
                errors["assignments"].append("Assignment missing ID")
            if not assignment.get("title"):
                errors["assignments"].append(
                    f"Assignment {assignment.get('id', 'unknown')} missing title"
                )
            if not assignment.get("points_possible"):
                errors["assignments"].append(
                    f"Assignment {assignment.get('id', 'unknown')} missing points"
                )

        # Validate modules
        for module in self.course_data.modules.get("modules", []):
            if not module.get("name"):
                errors["modules"].append("Module missing name")

        # Validate quizzes
        for quiz in self.course_data.quizzes.get("quizzes", []):
            if not quiz.get("id"):
                errors["quizzes"].append("Quiz missing ID")
            if not quiz.get("title"):
                errors["quizzes"].append(
                    f"Quiz {quiz.get('id', 'unknown')} missing title"
                )

        # Validate pages
        for page in self.course_data.pages.get("pages", []):
            if not page.get("title"):
                errors["pages"].append("Page missing title")

        # Validate outcomes
        for outcome in self.course_data.outcomes.get("outcomes", []):
            if not outcome.get("id"):
                errors["outcomes"].append("Outcome missing ID")
            if not outcome.get("name"):
                errors["outcomes"].append(
                    f"Outcome {outcome.get('id', 'unknown')} missing name"
                )

        return {k: v for k, v in errors.items() if v}
