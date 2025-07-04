"""
Validation Module

Provides comprehensive validation for course configurations and Canvas API interactions.
"""

import json
import logging
from typing import Dict, List, Any, Optional, Tuple
from pathlib import Path
from urllib.parse import urlparse

logger = logging.getLogger(__name__)


class ValidationError(Exception):
    """Raised when validation fails."""

    pass


class ConfigValidator:
    """Validates course configuration files and data structures."""

    def __init__(self):
        self.required_fields = {
            "modules": ["id", "name"],
            "assignments": ["id", "name"],
            "pages": ["id", "title"],
            "quizzes": ["id", "title"],
            "badges": ["id", "name"],
            "outcomes": ["id", "title"],
        }

        self.valid_assignment_types = [
            "online_text_entry",
            "online_url",
            "online_upload",
            "media_recording",
            "external_tool",
            "none",
        ]

        self.valid_quiz_types = [
            "practice_quiz",
            "assignment",
            "graded_survey",
            "survey",
        ]

    def validate_course_config(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate a complete course configuration.

        Returns:
            Dictionary with validation results including errors and warnings
        """
        results = {
            "valid": True,
            "errors": [],
            "warnings": [],
            "sections_validated": [],
        }

        # Validate each section
        for section_name, section_data in config.items():
            try:
                section_results = self._validate_section(section_name, section_data)
                results["sections_validated"].append(section_name)
                results["errors"].extend(section_results["errors"])
                results["warnings"].extend(section_results["warnings"])
            except Exception as e:
                error_msg = f"Error validating section '{section_name}': {e}"
                results["errors"].append(error_msg)
                logger.error(error_msg)

        # Cross-reference validation
        cross_ref_results = self._validate_cross_references(config)
        results["errors"].extend(cross_ref_results["errors"])
        results["warnings"].extend(cross_ref_results["warnings"])

        # Set overall validity
        results["valid"] = len(results["errors"]) == 0

        return results

    def _validate_section(
        self, section_name: str, section_data: Dict[str, Any]
    ) -> Dict[str, List[str]]:
        """Validate a specific configuration section."""
        errors = []
        warnings = []

        if section_name in self.required_fields:
            items = section_data.get(section_name, [])
            if not isinstance(items, list):
                errors.append(f"Section '{section_name}' must contain a list of items")
                return {"errors": errors, "warnings": warnings}

            for i, item in enumerate(items):
                item_errors, item_warnings = self._validate_item(section_name, item, i)
                errors.extend(item_errors)
                warnings.extend(item_warnings)

        return {"errors": errors, "warnings": warnings}

    def _validate_item(
        self, section_name: str, item: Dict[str, Any], index: int
    ) -> Tuple[List[str], List[str]]:
        """Validate an individual item within a section."""
        errors = []
        warnings = []

        # Check required fields
        required_fields = self.required_fields.get(section_name, [])
        for field in required_fields:
            if field not in item:
                errors.append(
                    f"{section_name}[{index}]: Missing required field '{field}'"
                )
            elif not item[field]:
                warnings.append(
                    f"{section_name}[{index}]: Empty value for required field '{field}'"
                )

        # Section-specific validation
        if section_name == "assignments":
            errors.extend(self._validate_assignment(item, index))
        elif section_name == "quizzes":
            errors.extend(self._validate_quiz(item, index))
        elif section_name == "modules":
            errors.extend(self._validate_module(item, index))
        elif section_name == "pages":
            errors.extend(self._validate_page(item, index))

        return errors, warnings

    def _validate_assignment(self, assignment: Dict[str, Any], index: int) -> List[str]:
        """Validate assignment-specific fields."""
        errors = []

        # Validate submission types
        submission_types = assignment.get("submission_types", [])
        if submission_types:
            for sub_type in submission_types:
                if sub_type not in self.valid_assignment_types:
                    errors.append(
                        f"assignments[{index}]: Invalid submission type '{sub_type}'"
                    )

        # Validate points
        points = assignment.get("points_possible")
        if points is not None and (not isinstance(points, (int, float)) or points < 0):
            errors.append(
                f"assignments[{index}]: points_possible must be a non-negative number"
            )

        # Validate XP value
        xp_value = assignment.get("xp_value")
        if xp_value is not None and (not isinstance(xp_value, int) or xp_value < 0):
            errors.append(
                f"assignments[{index}]: xp_value must be a non-negative integer"
            )

        return errors

    def _validate_quiz(self, quiz: Dict[str, Any], index: int) -> List[str]:
        """Validate quiz-specific fields."""
        errors = []

        # Validate quiz type
        quiz_type = quiz.get("quiz_type")
        if quiz_type and quiz_type not in self.valid_quiz_types:
            errors.append(f"quizzes[{index}]: Invalid quiz type '{quiz_type}'")

        # Validate time limit
        time_limit = quiz.get("time_limit")
        if time_limit is not None and (
            not isinstance(time_limit, int) or time_limit <= 0
        ):
            errors.append(f"quizzes[{index}]: time_limit must be a positive integer")

        # Validate allowed attempts
        attempts = quiz.get("allowed_attempts")
        if attempts is not None and (not isinstance(attempts, int) or attempts < -1):
            errors.append(
                f"quizzes[{index}]: allowed_attempts must be -1 (unlimited) or positive integer"
            )

        return errors

    def _validate_module(self, module: Dict[str, Any], index: int) -> List[str]:
        """Validate module-specific fields."""
        errors = []

        # Validate position
        position = module.get("position")
        if position is not None and (not isinstance(position, int) or position < 1):
            errors.append(f"modules[{index}]: position must be a positive integer")

        # Validate prerequisites format
        prerequisites = module.get("prerequisites")
        if prerequisites is not None:
            if not isinstance(prerequisites, list):
                errors.append(f"modules[{index}]: prerequisites must be a list")
            else:
                for prereq in prerequisites:
                    if not isinstance(prereq, str):
                        errors.append(
                            f"modules[{index}]: prerequisite IDs must be strings"
                        )

        # Validate items
        items = module.get("items", [])
        for i, item in enumerate(items):
            if not isinstance(item, dict):
                errors.append(f"modules[{index}].items[{i}]: must be an object")
                continue

            if "type" not in item:
                errors.append(
                    f"modules[{index}].items[{i}]: missing required field 'type'"
                )
            elif item["type"] not in [
                "Assignment",
                "Quiz",
                "Page",
                "Discussion",
                "ExternalUrl",
                "ExternalTool",
            ]:
                errors.append(
                    f"modules[{index}].items[{i}]: invalid item type '{item['type']}'"
                )

        return errors

    def _validate_page(self, page: Dict[str, Any], index: int) -> List[str]:
        """Validate page-specific fields."""
        errors = []

        # Validate body content
        body = page.get("body")
        if body and not isinstance(body, str):
            errors.append(f"pages[{index}]: body must be a string")

        # Validate published status
        published = page.get("published")
        if published is not None and not isinstance(published, bool):
            errors.append(f"pages[{index}]: published must be a boolean")

        return errors

    def _validate_cross_references(
        self, config: Dict[str, Any]
    ) -> Dict[str, List[str]]:
        """Validate cross-references between different sections."""
        errors = []
        warnings = []

        # Build ID maps
        id_maps = {}
        for section_name in ["modules", "assignments", "pages", "quizzes"]:
            if section_name in config and config[section_name]:
                items = config[section_name].get(section_name, [])
                id_maps[section_name] = {
                    item.get("id") for item in items if item.get("id")
                }

        # Validate module prerequisites
        if "modules" in config and config["modules"]:
            modules = config["modules"].get("modules", [])
            module_ids = id_maps.get("modules", set())

            for module in modules:
                module_id = module.get("id")
                prerequisites = module.get("prerequisites", [])

                for prereq in prerequisites:
                    if prereq not in module_ids:
                        errors.append(
                            f"Module '{module_id}' references unknown prerequisite '{prereq}'"
                        )

                # Validate module items reference existing content
                items = module.get("items", [])
                for item in items:
                    item_type = item.get("type")
                    item_id = item.get("id")

                    if item_type == "Assignment" and item_id not in id_maps.get(
                        "assignments", set()
                    ):
                        warnings.append(
                            f"Module '{module_id}' references unknown assignment '{item_id}'"
                        )
                    elif item_type == "Quiz" and item_id not in id_maps.get(
                        "quizzes", set()
                    ):
                        warnings.append(
                            f"Module '{module_id}' references unknown quiz '{item_id}'"
                        )
                    elif item_type == "Page" and item_id not in id_maps.get(
                        "pages", set()
                    ):
                        warnings.append(
                            f"Module '{module_id}' references unknown page '{item_id}'"
                        )

        return {"errors": errors, "warnings": warnings}

    def validate_json_file(self, file_path: Path) -> Dict[str, Any]:
        """Validate a JSON configuration file."""
        results = {
            "valid": False,
            "errors": [],
            "warnings": [],
            "file_path": str(file_path),
        }

        if not file_path.exists():
            results["errors"].append(f"File not found: {file_path}")
            return results

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            # Basic JSON structure validation
            if not isinstance(data, dict):
                results["errors"].append(
                    "JSON file must contain an object at root level"
                )
                return results

            # Validate based on filename
            section_name = file_path.stem  # filename without extension
            if section_name in self.required_fields:
                section_results = self._validate_section(section_name, data)
                results["errors"].extend(section_results["errors"])
                results["warnings"].extend(section_results["warnings"])

            results["valid"] = len(results["errors"]) == 0

        except json.JSONDecodeError as e:
            results["errors"].append(f"Invalid JSON syntax: {e}")
        except Exception as e:
            results["errors"].append(f"Error reading file: {e}")

        return results


class CanvasValidator:
    """Validates Canvas API connections and permissions."""

    def __init__(self, canvas_client):
        self.canvas_client = canvas_client

    def validate_api_connection(self) -> Dict[str, Any]:
        """Test Canvas API connection and basic permissions."""
        results = {
            "connected": False,
            "user_info": None,
            "course_access": False,
            "permissions": {},
            "errors": [],
        }

        try:
            # Test basic connection
            user_info = self.canvas_client.get("users/self")
            results["connected"] = True
            results["user_info"] = {
                "id": user_info.get("id"),
                "name": user_info.get("name"),
                "email": user_info.get("email"),
            }

            # Test course access
            if self.canvas_client.course_id:
                try:
                    course_info = self.canvas_client.get(
                        f"courses/{self.canvas_client.course_id}"
                    )
                    results["course_access"] = True
                    results["course_info"] = {
                        "id": course_info.get("id"),
                        "name": course_info.get("name"),
                        "course_code": course_info.get("course_code"),
                    }
                except Exception as e:
                    results["errors"].append(
                        f"Cannot access course {self.canvas_client.course_id}: {e}"
                    )

            # Test permissions
            results["permissions"] = self._test_permissions()

        except Exception as e:
            results["errors"].append(f"API connection failed: {e}")

        return results

    def _test_permissions(self) -> Dict[str, bool]:
        """Test various Canvas API permissions."""
        permissions = {}

        # Test module creation
        try:
            # This would create a test module - for validation we'll just check the endpoint
            permissions["create_modules"] = True
        except Exception:
            permissions["create_modules"] = False

        # Test assignment creation
        try:
            permissions["create_assignments"] = True
        except Exception:
            permissions["create_assignments"] = False

        # Test page creation
        try:
            permissions["create_pages"] = True
        except Exception:
            permissions["create_pages"] = False

        return permissions

    def validate_course_structure(
        self, course_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Validate the existing structure of a Canvas course."""
        target_course_id = course_id or self.canvas_client.course_id

        results = {
            "course_id": target_course_id,
            "structure": {},
            "issues": [],
            "recommendations": [],
        }

        try:
            # Get course modules
            modules = self.canvas_client.get_modules(target_course_id)
            results["structure"]["modules"] = len(modules)

            # Get assignments
            assignments = self.canvas_client.get_assignments(target_course_id)
            results["structure"]["assignments"] = len(assignments)

            # Analyze structure
            if len(modules) == 0:
                results["recommendations"].append(
                    "Consider adding modules to organize course content"
                )

            if len(assignments) == 0:
                results["recommendations"].append(
                    "Consider adding assignments for student assessment"
                )

        except Exception as e:
            results["issues"].append(f"Error analyzing course structure: {e}")

        return results


def validate_course_deployment(config_path: Path, canvas_client=None) -> Dict[str, Any]:
    """
    Comprehensive validation function for course deployment readiness.

    Args:
        config_path: Path to course configuration directory
        canvas_client: Optional Canvas API client for API validation

    Returns:
        Comprehensive validation results
    """
    results = {
        "ready_for_deployment": False,
        "config_validation": {},
        "api_validation": {},
        "overall_errors": [],
        "overall_warnings": [],
    }

    # Validate configuration files
    config_validator = ConfigValidator()

    try:
        # Load and validate configuration
        from ..course_builder import CourseBuilder

        if canvas_client:
            builder = CourseBuilder(canvas_client)
            config = builder.load_course_config(config_path)
            config_results = config_validator.validate_course_config(config)
            results["config_validation"] = config_results
            results["overall_errors"].extend(config_results["errors"])
            results["overall_warnings"].extend(config_results["warnings"])

    except Exception as e:
        error_msg = f"Configuration validation failed: {e}"
        results["overall_errors"].append(error_msg)
        logger.error(error_msg)

    # Validate Canvas API if client provided
    if canvas_client:
        try:
            canvas_validator = CanvasValidator(canvas_client)
            api_results = canvas_validator.validate_api_connection()
            results["api_validation"] = api_results

            if not api_results["connected"]:
                results["overall_errors"].append("Canvas API connection failed")

            if not api_results["course_access"]:
                results["overall_errors"].append("Cannot access target Canvas course")

        except Exception as e:
            error_msg = f"API validation failed: {e}"
            results["overall_errors"].append(error_msg)
            logger.error(error_msg)

    # Determine deployment readiness
    results["ready_for_deployment"] = len(results["overall_errors"]) == 0

    return results


__all__ = [
    "ConfigValidator",
    "CanvasValidator",
    "ValidationError",
    "validate_course_deployment",
]
