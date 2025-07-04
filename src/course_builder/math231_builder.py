#!/usr/bin/env python3
"""
Canvas Course Builder for MATH 231 Linear Algebra
Builds Canvas course structure from skill tree configuration
"""

import yaml
import requests
import json
from typing import Dict, List, Optional
from dataclasses import dataclass
from pathlib import Path
import logging


@dataclass
class CanvasConfig:
    """Canvas API configuration"""

    base_url: str
    token: str
    account_id: int
    term_id: Optional[int] = None


@dataclass
class CourseModule:
    """Represents a Canvas course module"""

    name: str
    description: str
    prerequisites: List[str]
    items: List[Dict]
    unlock_at: Optional[str] = None
    require_sequential_progress: bool = True


class MATH231CourseBuilder:
    """Builds MATH 231 Linear Algebra course in Canvas from skill tree"""

    def __init__(self, skill_tree_path: str, canvas_config: CanvasConfig):
        """Initialize course builder"""
        self.canvas_config = canvas_config
        self.headers = {
            "Authorization": f"Bearer {canvas_config.token}",
            "Content-Type": "application/json",
        }

        # Load skill tree
        with open(skill_tree_path, "r") as f:
            self.skill_tree = yaml.safe_load(f)

        self.course_id = None
        self.modules = {}
        self.skill_to_module = {}

        # Set up logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    def create_course(self, course_name: str = "MATH 231: Linear Algebra") -> int:
        """Create the Canvas course"""
        course_data = {
            "course": {
                "name": course_name,
                "course_code": "MATH231",
                "description": "Theory and practice of vector geometry in R2 and R3, systems of linear equations, matrix algebra, determinants, vector spaces, bases and dimension, linear transformations, eigenvalues and eigenvectors, rank and nullity and applications.",
                "is_public": False,
                "syllabus_body": self._generate_syllabus(),
                "grading_standard_id": None,
                "grade_passback_setting": "nightly_sync",
            }
        }

        if self.canvas_config.term_id:
            course_data["course"]["term_id"] = self.canvas_config.term_id

        url = f"{self.canvas_config.base_url}/api/v1/accounts/{self.canvas_config.account_id}/courses"
        response = requests.post(url, headers=self.headers, json=course_data)

        if response.status_code == 200:
            course = response.json()
            self.course_id = course["id"]
            self.logger.info(f"Created course: {course['name']} (ID: {self.course_id})")
            return self.course_id
        else:
            raise Exception(
                f"Failed to create course: {response.status_code} - {response.text}"
            )

    def _generate_syllabus(self) -> str:
        """Generate course syllabus from skill tree"""
        metadata = self.skill_tree.get("math231_skill_tree", {}).get("metadata", {})

        syllabus = f"""
<h2>MATH 231: Linear Algebra</h2>
<p><strong>Credits:</strong> {self.skill_tree['math231_skill_tree']['course_info']['credits']}</p>
<p><strong>Prerequisites:</strong> {', '.join(self.skill_tree['math231_skill_tree']['course_info']['prerequisites'])}</p>

<h3>Course Description</h3>
<p>{self.skill_tree['math231_skill_tree']['course_info']['description']}</p>

<h3>Course Structure</h3>
<p>This course is organized using a <strong>skill tree approach</strong> with {metadata.get('total_skills', 'numerous')} individual learning objectives.</p>

<ul>
<li><strong>Foundational Skills:</strong> Mathematical prerequisites and basic concepts</li>
<li><strong>Core Skills:</strong> Essential linear algebra concepts</li>
<li><strong>Advanced Skills:</strong> Abstract vector spaces and transformations</li>
<li><strong>Expert Skills:</strong> Applications and advanced topics</li>
</ul>

<h3>Gamification Elements</h3>
<p>Students earn XP points and badges for mastering skills:</p>
<ul>
<li>Total XP Available: {metadata.get('total_xp_available', 'TBD')}</li>
<li>Badge Milestones: {len(metadata.get('badge_milestones', []))}</li>
<li>Multiple Learning Tracks Available</li>
</ul>

<h3>Assessment Structure</h3>
<ul>
<li>Quizzes: {metadata.get('assessment_distribution', {}).get('quizzes', 'Multiple')}</li>
<li>Assignments: {metadata.get('assessment_distribution', {}).get('assignments', 'Multiple')}</li>
<li>Projects: {metadata.get('assessment_distribution', {}).get('projects', 'Several')}</li>
<li>Final Exam: 1</li>
</ul>
"""
        return syllabus

    def create_modules_from_skill_tree(self):
        """Create Canvas modules from skill tree structure"""
        tree = self.skill_tree["math231_skill_tree"]

        # Create foundational modules
        if "foundational_skills" in tree:
            self._create_modules_from_group(
                tree["foundational_skills"], "Prerequisites"
            )

        # Create core modules
        if "linear_algebra_core" in tree:
            self._create_modules_from_group(tree["linear_algebra_core"], "Core Topics")

        # Create advanced modules
        if "applications_advanced" in tree:
            self._create_modules_from_group(
                tree["applications_advanced"], "Applications"
            )

    def _create_modules_from_group(self, group_data: Dict, group_prefix: str):
        """Create modules from a skill group"""
        for key, value in group_data.items():
            if isinstance(value, dict) and "skill_id" in value:
                # This is a major skill group - create a module
                module_name = f"{group_prefix}: {value.get('name', key)}"
                module = self._create_canvas_module(
                    name=module_name,
                    description=value.get("description", ""),
                    skills=self._get_skills_in_group(value),
                )
                self.modules[value["skill_id"]] = module

    def _get_skills_in_group(self, group_data: Dict) -> List[Dict]:
        """Get all skills within a group"""
        skills = []
        if "sub_skills" in group_data:
            skills.extend(group_data["sub_skills"])
        return skills

    def _create_canvas_module(
        self, name: str, description: str, skills: List[Dict]
    ) -> int:
        """Create a module in Canvas"""
        module_data = {
            "module": {
                "name": name,
                "description": description,
                "require_sequential_progress": True,
                "publish_final_grade": False,
            }
        }

        url = f"{self.canvas_config.base_url}/api/v1/courses/{self.course_id}/modules"
        response = requests.post(url, headers=self.headers, json=module_data)

        if response.status_code == 200:
            module = response.json()
            module_id = module["id"]
            self.logger.info(f"Created module: {name} (ID: {module_id})")

            # Add items to module
            self._add_skills_to_module(module_id, skills)

            return module_id
        else:
            raise Exception(
                f"Failed to create module: {response.status_code} - {response.text}"
            )

    def _add_skills_to_module(self, module_id: int, skills: List[Dict]):
        """Add skill-based items to a module"""
        position = 1

        for skill in skills:
            # Create a page for each skill
            page_id = self._create_skill_page(skill)

            # Add page to module
            self._add_page_to_module(module_id, page_id, skill, position)

            # Create assessment if specified
            if "assessment" in skill:
                assessment_id = self._create_skill_assessment(skill)
                if assessment_id:
                    self._add_assessment_to_module(
                        module_id, assessment_id, skill, position + 1
                    )
                    position += 1

            position += 1

    def _create_skill_page(self, skill: Dict) -> int:
        """Create a page for a skill"""
        page_data = {
            "wiki_page": {
                "title": skill.get("name", skill.get("skill_id", "Unnamed Skill")),
                "body": self._generate_skill_content(skill),
                "published": True,
            }
        }

        url = f"{self.canvas_config.base_url}/api/v1/courses/{self.course_id}/pages"
        response = requests.post(url, headers=self.headers, json=page_data)

        if response.status_code == 201:
            page = response.json()
            self.logger.info(f"Created page: {page['title']}")
            return page["page_id"]
        else:
            raise Exception(
                f"Failed to create page: {response.status_code} - {response.text}"
            )

    def _generate_skill_content(self, skill: Dict) -> str:
        """Generate HTML content for a skill page"""
        skill_name = skill.get("name", "Unnamed Skill")
        description = skill.get("description", "No description available")
        level = skill.get("level", "unknown")
        xp_value = skill.get("xp_value", 0)
        prerequisites = skill.get("prerequisites", [])

        content = f"""
<h2>{skill_name}</h2>
<div class="skill-info">
    <p><strong>Description:</strong> {description}</p>
    <p><strong>Level:</strong> {level.title()}</p>
    <p><strong>XP Value:</strong> {xp_value}</p>
"""

        if prerequisites:
            content += f"    <p><strong>Prerequisites:</strong> {', '.join(prerequisites)}</p>\n"

        content += """
</div>

<h3>Learning Objectives</h3>
<p>By the end of this section, you should be able to:</p>
<ul>
<li>Understand the key concepts related to this skill</li>
<li>Apply the techniques in practice problems</li>
<li>Connect this skill to other areas of linear algebra</li>
</ul>

<h3>Content</h3>
<p><em>Detailed content for this skill will be added based on the specific learning objectives.</em></p>

<h3>Examples</h3>
<p><em>Worked examples demonstrating this skill will be provided.</em></p>

<h3>Practice</h3>
<p><em>Practice problems and exercises will be available.</em></p>
"""

        return content

    def _create_skill_assessment(self, skill: Dict) -> Optional[int]:
        """Create an assessment (quiz or assignment) for a skill"""
        assessment_info = skill.get("assessment", {})
        assessment_type = assessment_info.get("type", "quiz")

        if assessment_type == "quiz":
            return self._create_quiz(skill, assessment_info)
        elif assessment_type == "assignment":
            return self._create_assignment(skill, assessment_info)

        return None

    def _create_quiz(self, skill: Dict, assessment_info: Dict) -> int:
        """Create a quiz for a skill"""
        quiz_data = {
            "quiz": {
                "title": f"{skill.get('name', 'Skill')} - Quiz",
                "description": f"Assessment for {skill.get('name', 'this skill')}",
                "quiz_type": "assignment",
                "assignment_group_id": None,
                "time_limit": 30,
                "allowed_attempts": 3,
                "scoring_policy": "keep_highest",
                "published": True,
                "show_correct_answers": True,
                "show_correct_answers_last_attempt": True,
                "question_count": assessment_info.get("questions", 5),
                "points_possible": assessment_info.get("questions", 5) * 2,
            }
        }

        url = f"{self.canvas_config.base_url}/api/v1/courses/{self.course_id}/quizzes"
        response = requests.post(url, headers=self.headers, json=quiz_data)

        if response.status_code == 200:
            quiz = response.json()
            self.logger.info(f"Created quiz: {quiz['title']}")
            return quiz["id"]
        else:
            raise Exception(
                f"Failed to create quiz: {response.status_code} - {response.text}"
            )

    def _create_assignment(self, skill: Dict, assessment_info: Dict) -> int:
        """Create an assignment for a skill"""
        assignment_data = {
            "assignment": {
                "name": f"{skill.get('name', 'Skill')} - Assignment",
                "description": f"Practice assignment for {skill.get('name', 'this skill')}",
                "points_possible": assessment_info.get("problems", 10) * 5,
                "submission_types": ["online_text_entry", "online_upload"],
                "published": True,
                "grading_type": "points",
            }
        }

        url = (
            f"{self.canvas_config.base_url}/api/v1/courses/{self.course_id}/assignments"
        )
        response = requests.post(url, headers=self.headers, json=assignment_data)

        if response.status_code == 201:
            assignment = response.json()
            self.logger.info(f"Created assignment: {assignment['name']}")
            return assignment["id"]
        else:
            raise Exception(
                f"Failed to create assignment: {response.status_code} - {response.text}"
            )

    def _add_page_to_module(
        self, module_id: int, page_id: int, skill: Dict, position: int
    ):
        """Add a page to a module"""
        item_data = {
            "module_item": {
                "type": "Page",
                "content_id": page_id,
                "position": position,
                "title": skill.get("name", "Skill Page"),
            }
        }

        url = f"{self.canvas_config.base_url}/api/v1/courses/{self.course_id}/modules/{module_id}/items"
        response = requests.post(url, headers=self.headers, json=item_data)

        if response.status_code == 200:
            self.logger.info(f"Added page to module: {skill.get('name', 'Page')}")
        else:
            self.logger.error(f"Failed to add page to module: {response.status_code}")

    def _add_assessment_to_module(
        self, module_id: int, assessment_id: int, skill: Dict, position: int
    ):
        """Add an assessment to a module"""
        assessment_info = skill.get("assessment", {})
        assessment_type = assessment_info.get("type", "quiz")

        item_data = {
            "module_item": {
                "type": "Quiz" if assessment_type == "quiz" else "Assignment",
                "content_id": assessment_id,
                "position": position,
                "title": f"{skill.get('name', 'Skill')} - {assessment_type.title()}",
            }
        }

        url = f"{self.canvas_config.base_url}/api/v1/courses/{self.course_id}/modules/{module_id}/items"
        response = requests.post(url, headers=self.headers, json=item_data)

        if response.status_code == 200:
            self.logger.info(
                f"Added {assessment_type} to module: {skill.get('name', 'Assessment')}"
            )
        else:
            self.logger.error(
                f"Failed to add {assessment_type} to module: {response.status_code}"
            )

    def setup_gamification(self):
        """Set up gamification elements in the course"""
        # This would integrate with Canvas badges and outcomes
        # For now, we'll create outcome groups based on skill levels
        self._create_outcome_groups()

    def _create_outcome_groups(self):
        """Create learning outcome groups for different skill levels"""
        skill_levels = ["foundational", "core", "advanced", "expert"]

        for level in skill_levels:
            group_data = {
                "outcome_group": {
                    "title": f"{level.title()} Skills",
                    "description": f"Learning outcomes for {level} level skills",
                }
            }

            url = f"{self.canvas_config.base_url}/api/v1/courses/{self.course_id}/outcome_groups"
            response = requests.post(url, headers=self.headers, json=group_data)

            if response.status_code == 200:
                self.logger.info(f"Created outcome group: {level.title()} Skills")

    def build_course(self, course_name: str = "MATH 231: Linear Algebra") -> int:
        """Build the complete course"""
        self.logger.info("Starting course build process...")

        # Create course
        course_id = self.create_course(course_name)

        # Create modules from skill tree
        self.create_modules_from_skill_tree()

        # Set up gamification
        self.setup_gamification()

        self.logger.info(f"Course build complete! Course ID: {course_id}")
        return course_id


def main():
    """Example usage"""
    # Configuration would typically come from environment or config file
    config = CanvasConfig(
        base_url="https://your-canvas-instance.instructure.com",
        token="your-canvas-api-token",
        account_id=1,
        term_id=None,
    )

    builder = MATH231CourseBuilder(
        skill_tree_path="config/math231_skill_tree.yml", canvas_config=config
    )

    # This would build the actual course - commented out for safety
    # course_id = builder.build_course()
    # print(f"Created course with ID: {course_id}")

    print("Course builder initialized successfully!")


if __name__ == "__main__":
    main()
