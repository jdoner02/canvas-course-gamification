"""
Course Builder Module

Handles the construction and deployment of Canvas courses from JSON configurations.
"""

import json
import logging
from pathlib import Path
from typing import Dict, List, Optional, Any, Union

from ..canvas_api import CanvasAPIClient, CourseManager
from ..gamification import (
    SkillTree,
    SkillNode,
    Badge,
    SkillLevel,
    GamificationEngine,
    XPSystem,
)

logger = logging.getLogger(__name__)


class CourseBuilder:
    """Builds and deploys gamified Canvas courses from configuration files."""

    def __init__(self, canvas_client: CanvasAPIClient):
        self.canvas_client = canvas_client
        self.course_manager = CourseManager(canvas_client)
        self.skill_tree = None
        self.gamification_engine = None

    def load_course_config(self, config_path: Union[str, Path]) -> Dict[str, Any]:
        """Load course configuration from a directory containing JSON files."""
        config_path = Path(config_path)
        if not config_path.exists():
            raise FileNotFoundError(f"Configuration path not found: {config_path}")

        config = {}

        # Load all JSON files in the config directory
        json_files = [
            "modules.json",
            "assignments.json",
            "pages.json",
            "quizzes.json",
            "badges.json",
            "outcomes.json",
        ]

        for filename in json_files:
            file_path = config_path / filename
            if file_path.exists():
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        config[filename.replace(".json", "")] = json.load(f)
                    logger.info(f"Loaded {filename}")
                except json.JSONDecodeError as e:
                    logger.error(f"Error parsing {filename}: {e}")
                    raise
            else:
                logger.warning(f"Configuration file not found: {filename}")
                config[filename.replace(".json", "")] = {}

        return config

    def build_skill_tree(self, config: Dict[str, Any]) -> SkillTree:
        """Build a skill tree from configuration data."""
        # Extract skill tree metadata
        tree_config = config.get("skill_tree", {})
        name = tree_config.get("name", "Course Skill Tree")
        description = tree_config.get("description", "Course progression tree")

        skill_tree = SkillTree(name, description)

        # Build skill nodes from modules
        modules = config.get("modules", {}).get("modules", [])
        for module in modules:
            skill_node = self._create_skill_node_from_module(module)
            skill_tree.add_node(skill_node)

        # Add badges
        badges_data = config.get("badges", {}).get("badges", [])
        for badge_data in badges_data:
            badge = self._create_badge_from_config(badge_data)
            skill_tree.add_badge(badge)

        self.skill_tree = skill_tree
        return skill_tree

    def _create_skill_node_from_module(
        self, module_config: Dict[str, Any]
    ) -> SkillNode:
        """Create a skill node from a module configuration."""
        # Extract gamification data
        gamification = module_config.get("gamification", {})

        # Map skill level
        level_name = gamification.get("skill_level", "application").upper()
        try:
            level = SkillLevel[level_name]
        except KeyError:
            level = SkillLevel.APPLICATION
            logger.warning(
                f"Unknown skill level '{level_name}', defaulting to APPLICATION"
            )

        # Extract prerequisites
        prerequisites = module_config.get("prerequisites", [])
        if isinstance(prerequisites, dict):
            prerequisites = prerequisites.get("module_ids", [])

        return SkillNode(
            id=module_config["id"],
            name=module_config["name"],
            description=module_config.get("description", ""),
            level=level,
            xp_required=gamification.get("xp_required", 0),
            prerequisites=prerequisites,
            unlock_requirements=gamification.get("unlock_requirements", {}),
            badges=gamification.get("badges", []),
            mastery_threshold=gamification.get("mastery_threshold", 0.8),
        )

    def _create_badge_from_config(self, badge_config: Dict[str, Any]) -> Badge:
        """Create a badge from configuration data."""
        return Badge(
            id=badge_config["id"],
            name=badge_config["name"],
            description=badge_config.get("description", ""),
            criteria=badge_config.get("criteria", ""),
            xp_value=badge_config.get("xp_value", 0),
            image_url=badge_config.get("image_url"),
            category=badge_config.get("category"),
            unlock_requirements=badge_config.get("unlock_requirements", []),
        )

    def deploy_course(
        self, config: Dict[str, Any], course_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Deploy a complete course to Canvas."""
        logger.info("Starting course deployment...")

        deployment_results = {
            "course_id": course_id or self.canvas_client.course_id,
            "modules": [],
            "assignments": [],
            "pages": [],
            "quizzes": [],
            "outcomes": [],
            "errors": [],
        }

        try:
            # Deploy outcomes first (they're referenced by other components)
            if "outcomes" in config and config["outcomes"]:
                outcomes_result = self._deploy_outcomes(config["outcomes"], course_id)
                deployment_results["outcomes"] = outcomes_result

            # Deploy pages
            if "pages" in config and config["pages"]:
                pages_result = self._deploy_pages(config["pages"], course_id)
                deployment_results["pages"] = pages_result

            # Deploy assignments
            if "assignments" in config and config["assignments"]:
                assignments_result = self._deploy_assignments(
                    config["assignments"], course_id
                )
                deployment_results["assignments"] = assignments_result

            # Deploy quizzes
            if "quizzes" in config and config["quizzes"]:
                quizzes_result = self._deploy_quizzes(config["quizzes"], course_id)
                deployment_results["quizzes"] = quizzes_result

            # Deploy modules (last, as they reference other components)
            if "modules" in config and config["modules"]:
                modules_result = self._deploy_modules(config["modules"], course_id)
                deployment_results["modules"] = modules_result

            logger.info("Course deployment completed successfully")

        except Exception as e:
            error_msg = f"Course deployment failed: {e}"
            logger.error(error_msg)
            deployment_results["errors"].append(error_msg)
            raise

        return deployment_results

    def _deploy_modules(
        self, modules_config: Dict[str, Any], course_id: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Deploy modules to Canvas."""
        modules = modules_config.get("modules", [])
        results = []

        for module_config in modules:
            try:
                # Extract Canvas-specific module data
                canvas_module_data = {
                    "name": module_config["name"],
                    "position": module_config.get("position", 1),
                    "unlock_at": module_config.get("unlock_at"),
                    "require_sequential_progress": module_config.get(
                        "require_sequential_progress", False
                    ),
                }

                # Create the module
                module = self.canvas_client.create_module(
                    course_id, **canvas_module_data
                )
                results.append(module)

                # Add items to the module if specified
                items = module_config.get("items", [])
                for item in items:
                    self._add_module_item(module["id"], item, course_id)

                logger.info(f"Deployed module: {module_config['name']}")

            except Exception as e:
                logger.error(
                    f"Failed to deploy module {module_config.get('name', 'Unknown')}: {e}"
                )
                raise

        return results

    def _add_module_item(
        self,
        module_id: str,
        item_config: Dict[str, Any],
        course_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Add an item to a Canvas module."""
        target_course_id = course_id or self.canvas_client.course_id
        endpoint = f"courses/{target_course_id}/modules/{module_id}/items"

        item_data = {
            "module_item": {
                "title": item_config.get("title", "Untitled Item"),
                "type": item_config.get("type", "Page"),
                "content_id": item_config.get("id"),
                "position": item_config.get("position", 1),
                "completion_requirement": item_config.get("completion_requirement"),
            }
        }

        return self.canvas_client.post(endpoint, json=item_data)

    def _deploy_assignments(
        self, assignments_config: Dict[str, Any], course_id: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Deploy assignments to Canvas."""
        assignments = assignments_config.get("assignments", [])
        results = []

        for assignment_config in assignments:
            try:
                # Extract Canvas assignment data
                canvas_assignment_data = {
                    "name": assignment_config["name"],
                    "description": assignment_config.get("description", ""),
                    "points_possible": assignment_config.get("points_possible", 100),
                    "due_at": assignment_config.get("due_at"),
                    "assignment_group_id": assignment_config.get("assignment_group_id"),
                    "submission_types": assignment_config.get(
                        "submission_types", ["online_text_entry"]
                    ),
                }

                assignment = self.canvas_client.create_assignment(
                    course_id, **canvas_assignment_data
                )
                results.append(assignment)

                logger.info(f"Deployed assignment: {assignment_config['name']}")

            except Exception as e:
                logger.error(
                    f"Failed to deploy assignment {assignment_config.get('name', 'Unknown')}: {e}"
                )
                raise

        return results

    def _deploy_pages(
        self, pages_config: Dict[str, Any], course_id: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Deploy pages to Canvas."""
        pages = pages_config.get("pages", [])
        results = []

        for page_config in pages:
            try:
                canvas_page_data = {
                    "title": page_config["title"],
                    "body": page_config.get("body", ""),
                    "published": page_config.get("published", True),
                    "front_page": page_config.get("front_page", False),
                }

                page = self.canvas_client.create_page(course_id, **canvas_page_data)
                results.append(page)

                logger.info(f"Deployed page: {page_config['title']}")

            except Exception as e:
                logger.error(
                    f"Failed to deploy page {page_config.get('title', 'Unknown')}: {e}"
                )
                raise

        return results

    def _deploy_quizzes(
        self, quizzes_config: Dict[str, Any], course_id: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Deploy quizzes to Canvas."""
        quizzes = quizzes_config.get("quizzes", [])
        results = []

        for quiz_config in quizzes:
            try:
                canvas_quiz_data = {
                    "title": quiz_config["title"],
                    "description": quiz_config.get("description", ""),
                    "quiz_type": quiz_config.get("quiz_type", "assignment"),
                    "points_possible": quiz_config.get("points_possible", 100),
                    "time_limit": quiz_config.get("time_limit"),
                    "allowed_attempts": quiz_config.get("allowed_attempts", 1),
                }

                quiz = self.canvas_client.create_quiz(course_id, **canvas_quiz_data)
                results.append(quiz)

                logger.info(f"Deployed quiz: {quiz_config['title']}")

            except Exception as e:
                logger.error(
                    f"Failed to deploy quiz {quiz_config.get('title', 'Unknown')}: {e}"
                )
                raise

        return results

    def _deploy_outcomes(
        self, outcomes_config: Dict[str, Any], course_id: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Deploy learning outcomes to Canvas."""
        outcomes = outcomes_config.get("outcomes", [])
        results = []

        for outcome_config in outcomes:
            try:
                # Note: Outcomes API may require special permissions
                logger.info(
                    f"Processing outcome: {outcome_config.get('title', 'Unknown')}"
                )
                # Outcome deployment would go here
                results.append({"id": outcome_config.get("id"), "status": "processed"})

            except Exception as e:
                logger.error(
                    f"Failed to deploy outcome {outcome_config.get('title', 'Unknown')}: {e}"
                )
                # Continue with other outcomes

        return results

    def validate_configuration(self, config: Dict[str, Any]) -> Dict[str, List[str]]:
        """Validate course configuration for consistency and completeness."""
        errors = []
        warnings = []

        # Check for required sections
        required_sections = ["modules", "assignments"]
        for section in required_sections:
            if section not in config or not config[section]:
                errors.append(f"Missing required section: {section}")

        # Validate module references
        if "modules" in config and config["modules"]:
            modules = config["modules"].get("modules", [])
            module_ids = {module["id"] for module in modules}

            for module in modules:
                # Check prerequisites reference valid modules
                prerequisites = module.get("prerequisites", [])
                if isinstance(prerequisites, list):
                    for prereq in prerequisites:
                        if prereq not in module_ids:
                            warnings.append(
                                f"Module {module['id']} references unknown prerequisite: {prereq}"
                            )

        # Validate assignment references
        if "assignments" in config and config["assignments"]:
            assignments = config["assignments"].get("assignments", [])
            assignment_ids = {assignment["id"] for assignment in assignments}

            # Check if module items reference valid assignments
            if "modules" in config and config["modules"]:
                for module in config["modules"].get("modules", []):
                    for item in module.get("items", []):
                        if (
                            item.get("type") == "Assignment"
                            and item.get("id") not in assignment_ids
                        ):
                            warnings.append(
                                f"Module {module['id']} references unknown assignment: {item.get('id')}"
                            )

        return {"errors": errors, "warnings": warnings, "valid": len(errors) == 0}


class CourseTemplate:
    """Creates course templates for different subjects and teaching styles."""

    @staticmethod
    def create_linear_algebra_template() -> Dict[str, Any]:
        """Create a template for a Linear Algebra course."""
        return {
            "modules": {
                "modules": [
                    {
                        "id": "foundation",
                        "name": "Foundation - Vectors and Basics",
                        "position": 1,
                        "gamification": {
                            "skill_level": "recognition",
                            "xp_required": 0,
                            "unlock_requirements": {},
                        },
                    },
                    {
                        "id": "systems",
                        "name": "Systems - Linear Equations",
                        "position": 2,
                        "prerequisites": ["foundation"],
                        "gamification": {
                            "skill_level": "application",
                            "xp_required": 100,
                            "unlock_requirements": {
                                "assignment_completion": ["vectors_basics"]
                            },
                        },
                    },
                ]
            },
            "assignments": {
                "assignments": [
                    {
                        "id": "vectors_basics",
                        "name": "Vector Operations Fundamentals",
                        "points_possible": 100,
                        "xp_value": 150,
                        "badge_eligibility": ["vector_novice"],
                    }
                ]
            },
            "badges": {
                "badges": [
                    {
                        "id": "vector_novice",
                        "name": "Vector Novice",
                        "description": "Completed basic vector operations",
                        "xp_value": 100,
                        "criteria": "Complete Vector Operations Fundamentals assignment",
                    }
                ]
            },
        }

    @staticmethod
    def create_calculus_template() -> Dict[str, Any]:
        """Create a template for a Calculus course."""
        # Similar structure for calculus
        return {
            "modules": {
                "modules": [
                    {
                        "id": "limits",
                        "name": "Limits and Continuity",
                        "position": 1,
                        "gamification": {
                            "skill_level": "recognition",
                            "xp_required": 0,
                        },
                    }
                ]
            }
        }
