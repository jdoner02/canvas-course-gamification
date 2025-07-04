"""
Canvas API client specifically for course operations.

Provides high-level methods for common course management tasks.
"""

import logging
from typing import Dict, List, Optional, Any

from . import CanvasAPIClient, CanvasAPIError

logger = logging.getLogger(__name__)


class CourseManager:
    """Manages course-level operations in Canvas."""

    def __init__(self, client: CanvasAPIClient):
        self.client = client

    def deploy_modules(
        self, modules_data: List[Dict[str, Any]], course_id: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Deploy multiple modules to Canvas.

        Args:
            modules_data: List of module configurations
            course_id: Target course ID

        Returns:
            List of created module objects
        """
        results = []
        for module_config in modules_data:
            try:
                module = self.client.create_module(course_id, **module_config)
                results.append(module)
                logger.info(f"Created module: {module_config.get('name', 'Unnamed')}")
            except CanvasAPIError as e:
                logger.error(
                    f"Failed to create module {module_config.get('name', 'Unnamed')}: {e}"
                )
                raise
        return results

    def deploy_assignments(
        self, assignments_data: List[Dict[str, Any]], course_id: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Deploy multiple assignments to Canvas.

        Args:
            assignments_data: List of assignment configurations
            course_id: Target course ID

        Returns:
            List of created assignment objects
        """
        results = []
        for assignment_config in assignments_data:
            try:
                assignment = self.client.create_assignment(
                    course_id, **assignment_config
                )
                results.append(assignment)
                logger.info(
                    f"Created assignment: {assignment_config.get('name', 'Unnamed')}"
                )
            except CanvasAPIError as e:
                logger.error(
                    f"Failed to create assignment {assignment_config.get('name', 'Unnamed')}: {e}"
                )
                raise
        return results

    def deploy_pages(
        self, pages_data: List[Dict[str, Any]], course_id: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Deploy multiple pages to Canvas.

        Args:
            pages_data: List of page configurations
            course_id: Target course ID

        Returns:
            List of created page objects
        """
        results = []
        for page_config in pages_data:
            try:
                page = self.client.create_page(course_id, **page_config)
                results.append(page)
                logger.info(f"Created page: {page_config.get('title', 'Unnamed')}")
            except CanvasAPIError as e:
                logger.error(
                    f"Failed to create page {page_config.get('title', 'Unnamed')}: {e}"
                )
                raise
        return results

    def setup_prerequisites(
        self, module_id: str, prerequisites: List[str], course_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Set up module prerequisites.

        Args:
            module_id: Target module ID
            prerequisites: List of prerequisite module IDs
            course_id: Target course ID

        Returns:
            Updated module object
        """
        target_course_id = course_id or self.client.course_id
        endpoint = f"courses/{target_course_id}/modules/{module_id}"

        data = {"module": {"prerequisite_module_ids": prerequisites}}

        return self.client.put(endpoint, json=data)

    def get_course_structure(self, course_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Get the complete course structure including modules, assignments, and pages.

        Args:
            course_id: Target course ID

        Returns:
            Dictionary containing course structure
        """
        modules = self.client.get_modules(course_id)
        assignments = self.client.get_assignments(course_id)

        return {
            "modules": modules,
            "assignments": assignments,
            "course_id": course_id or self.client.course_id,
        }
