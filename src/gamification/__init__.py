"""
Gamification Engine for Canvas Courses

Provides skill trees, XP systems, badges, and mastery-based progression.
"""

import logging
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from enum import Enum

logger = logging.getLogger(__name__)


class SkillLevel(Enum):
    """Skill progression levels."""

    RECOGNITION = 1  # "I know what this is"
    APPLICATION = 2  # "I can use this"
    INTUITION = 3  # "I understand why"
    SYNTHESIS = 4  # "I can connect and innovate"
    MASTERY = 5  # "I can teach this"

    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self.value < other.value
        return NotImplemented

    def __le__(self, other):
        if self.__class__ is other.__class__:
            return self.value <= other.value
        return NotImplemented

    def __gt__(self, other):
        if self.__class__ is other.__class__:
            return self.value > other.value
        return NotImplemented

    def __ge__(self, other):
        if self.__class__ is other.__class__:
            return self.value >= other.value
        return NotImplemented


@dataclass
class Badge:
    """Represents an achievement badge."""

    id: str
    name: str
    description: str
    criteria: str
    xp_value: int
    image_url: Optional[str] = None
    category: Optional[str] = None
    unlock_requirements: List[str] = field(default_factory=list)

    def to_canvas_format(self) -> Dict[str, Any]:
        """Convert badge to Canvas-compatible format."""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "criteria": self.criteria,
            "points_possible": self.xp_value,
            "image_url": self.image_url,
        }


@dataclass
class SkillNode:
    """Represents a node in the skill tree."""

    id: str
    name: str
    description: str
    level: SkillLevel
    xp_required: int
    prerequisites: List[str] = field(default_factory=list)
    unlock_requirements: Dict[str, Any] = field(default_factory=dict)
    badges: List[str] = field(default_factory=list)
    mastery_threshold: float = 0.8

    def is_unlocked(self, student_progress: Dict[str, Any]) -> bool:
        """Check if this skill node is unlocked for a student."""
        # Check prerequisite completion
        for prereq in self.prerequisites:
            if not student_progress.get(prereq, {}).get("completed", False):
                return False

        # Check XP requirements
        student_xp = student_progress.get("total_xp", 0)
        if student_xp < self.xp_required:
            return False

        # Check custom unlock requirements
        for requirement_type, requirement_value in self.unlock_requirements.items():
            if not self._check_requirement(
                requirement_type, requirement_value, student_progress
            ):
                return False

        return True

    def _check_requirement(
        self, req_type: str, req_value: Any, progress: Dict[str, Any]
    ) -> bool:
        """Check a specific unlock requirement."""
        if req_type == "quiz_score":
            quiz_id, min_score = req_value
            quiz_score = progress.get("quiz_scores", {}).get(quiz_id, 0)
            return quiz_score >= min_score

        elif req_type == "assignment_completion":
            assignment_ids = req_value if isinstance(req_value, list) else [req_value]
            for assignment_id in assignment_ids:
                if (
                    not progress.get("assignments", {})
                    .get(assignment_id, {})
                    .get("completed", False)
                ):
                    return False
            return True

        elif req_type == "badge_earned":
            badge_ids = req_value if isinstance(req_value, list) else [req_value]
            earned_badges = progress.get("badges", [])
            return all(badge_id in earned_badges for badge_id in badge_ids)

        return True


class SkillTree:
    """Manages the complete skill tree for a course."""

    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.nodes: Dict[str, SkillNode] = {}
        self.badges: Dict[str, Badge] = {}
        self.levels: Dict[int, List[str]] = {}

    def add_node(self, node: SkillNode) -> None:
        """Add a skill node to the tree."""
        self.nodes[node.id] = node

        # Organize by level
        level_num = node.level.value
        if level_num not in self.levels:
            self.levels[level_num] = []
        self.levels[level_num].append(node.id)

    def add_badge(self, badge: Badge) -> None:
        """Add a badge to the system."""
        self.badges[badge.id] = badge

    def get_unlocked_nodes(self, student_progress: Dict[str, Any]) -> List[SkillNode]:
        """Get all nodes unlocked for a student."""
        return [
            node for node in self.nodes.values() if node.is_unlocked(student_progress)
        ]

    def get_next_available_nodes(
        self, student_progress: Dict[str, Any]
    ) -> List[SkillNode]:
        """Get nodes that are one step away from being unlocked."""
        unlocked_ids = {node.id for node in self.get_unlocked_nodes(student_progress)}
        next_nodes = []

        for node in self.nodes.values():
            if node.id in unlocked_ids:
                continue

            # Check if all prerequisites are unlocked
            if all(prereq in unlocked_ids for prereq in node.prerequisites):
                next_nodes.append(node)

        return next_nodes

    def calculate_progress(self, student_progress: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate overall progress statistics."""
        unlocked_nodes = self.get_unlocked_nodes(student_progress)
        total_nodes = len(self.nodes)
        unlocked_count = len(unlocked_nodes)

        # Calculate level-wise progress
        level_progress = {}
        for level_num, node_ids in self.levels.items():
            level_unlocked = sum(
                1 for node_id in node_ids if node_id in {n.id for n in unlocked_nodes}
            )
            level_progress[level_num] = {
                "unlocked": level_unlocked,
                "total": len(node_ids),
                "percentage": (level_unlocked / len(node_ids)) * 100 if node_ids else 0,
            }

        return {
            "total_progress": (
                (unlocked_count / total_nodes) * 100 if total_nodes else 0
            ),
            "unlocked_nodes": unlocked_count,
            "total_nodes": total_nodes,
            "level_progress": level_progress,
            "current_xp": student_progress.get("total_xp", 0),
            "earned_badges": len(student_progress.get("badges", [])),
        }

    def to_visualization_data(self, student_progress: Dict[str, Any]) -> Dict[str, Any]:
        """Generate data for skill tree visualization."""
        unlocked_ids = {node.id for node in self.get_unlocked_nodes(student_progress)}
        next_available_ids = {
            node.id for node in self.get_next_available_nodes(student_progress)
        }

        nodes_data = []
        edges_data = []

        for node in self.nodes.values():
            status = (
                "unlocked"
                if node.id in unlocked_ids
                else "available" if node.id in next_available_ids else "locked"
            )

            nodes_data.append(
                {
                    "id": node.id,
                    "name": node.name,
                    "description": node.description,
                    "level": node.level.value,
                    "status": status,
                    "xp_required": node.xp_required,
                    "badges": node.badges,
                }
            )

            # Add edges for prerequisites
            for prereq in node.prerequisites:
                edges_data.append(
                    {"from": prereq, "to": node.id, "type": "prerequisite"}
                )

        return {
            "nodes": nodes_data,
            "edges": edges_data,
            "progress": self.calculate_progress(student_progress),
            "metadata": {"name": self.name, "description": self.description},
        }

    def get_node(self, node_id: str) -> Optional[SkillNode]:
        """Get a specific node by ID."""
        return self.nodes.get(node_id)

    def get_badge(self, badge_id: str) -> Optional[Badge]:
        """Get a specific badge by ID."""
        return self.badges.get(badge_id)

    def get_available_nodes(self, student_progress: Dict[str, Any]) -> List[SkillNode]:
        """Get all nodes available to a student (unlocked or currently unlocked)."""
        return self.get_unlocked_nodes(student_progress)

    def calculate_completion_percentage(
        self, student_progress: Dict[str, Any]
    ) -> float:
        """Calculate the completion percentage for a student."""
        if not self.nodes:
            return 0.0

        completed_count = 0
        for node_id in self.nodes:
            if student_progress.get(node_id, {}).get("completed", False):
                completed_count += 1

        return completed_count / len(self.nodes)


class XPSystem:
    """Manages experience points and level progression."""

    def __init__(self):
        self.xp_multipliers = {
            "assignment": 1.0,
            "quiz": 1.2,
            "discussion": 0.8,
            "project": 2.0,
            "bonus": 1.5,
        }
        self.level_thresholds = self._calculate_level_thresholds()

    def _calculate_level_thresholds(self) -> List[int]:
        """Calculate XP thresholds for each level."""
        thresholds = [0]  # Level 1 starts at 0 XP
        base_xp = 100

        for level in range(2, 51):  # Support up to level 50
            # Exponential growth with diminishing returns
            xp_required = int(base_xp * (level**1.5))
            thresholds.append(thresholds[-1] + xp_required)

        return thresholds

    def calculate_xp(
        self,
        activity_type: str,
        base_points: int,
        performance_score: float = 1.0,
        bonus_multiplier: float = 1.0,
    ) -> int:
        """
        Calculate XP for an activity.

        Args:
            activity_type: Type of activity (assignment, quiz, etc.)
            base_points: Base points for the activity
            performance_score: Performance multiplier (0.0 to 1.0+)
            bonus_multiplier: Additional bonus multiplier

        Returns:
            Total XP earned
        """
        multiplier = self.xp_multipliers.get(activity_type, 1.0)
        total_xp = int(base_points * multiplier * performance_score * bonus_multiplier)
        return max(0, total_xp)  # Ensure non-negative

    def get_level_from_xp(self, xp: int) -> Tuple[int, int, int]:
        """
        Get level information from XP amount.

        Returns:
            Tuple of (current_level, xp_for_next_level, xp_progress_in_current_level)
        """
        current_level = 1
        for level, threshold in enumerate(self.level_thresholds[1:], 2):
            if xp < threshold:
                break
            current_level = level

        if current_level >= len(self.level_thresholds):
            # Max level reached
            return current_level, 0, 0

        current_threshold = self.level_thresholds[current_level - 1]
        next_threshold = self.level_thresholds[current_level]

        xp_for_next = next_threshold - xp
        xp_progress = xp - current_threshold

        return current_level, xp_for_next, xp_progress


class GamificationEngine:
    """Main engine that orchestrates all gamification features."""

    def __init__(self, skill_tree: SkillTree, xp_system: XPSystem):
        self.skill_tree = skill_tree
        self.xp_system = xp_system
        self.mastery_thresholds = {"assignment": 0.8, "quiz": 0.7, "project": 0.85}

    def award_xp(
        self,
        student_id: str,
        activity_type: str,
        base_points: int,
        performance_score: float = 1.0,
    ) -> Dict[str, Any]:
        """Award XP to a student and check for level ups and unlocks."""
        xp_earned = self.xp_system.calculate_xp(
            activity_type, base_points, performance_score
        )

        # This would typically update a database
        # For now, return the calculation results
        return {
            "student_id": student_id,
            "xp_earned": xp_earned,
            "activity_type": activity_type,
            "performance_score": performance_score,
            "timestamp": "now",  # Would use actual timestamp
        }

    def check_badge_eligibility(self, student_progress: Dict[str, Any]) -> List[Badge]:
        """Check which new badges a student has earned."""
        earned_badges = set(student_progress.get("badges", []))
        eligible_badges = []

        for badge in self.skill_tree.badges.values():
            if badge.id in earned_badges:
                continue

            # Check if requirements are met
            if self._check_badge_requirements(badge, student_progress):
                eligible_badges.append(badge)

        return eligible_badges

    def _check_badge_requirements(self, badge: Badge, progress: Dict[str, Any]) -> bool:
        """Check if a student meets the requirements for a badge."""
        # This would implement specific badge requirement logic
        # For now, basic XP-based check
        student_xp = progress.get("total_xp", 0)
        return student_xp >= badge.xp_value

    def generate_progress_report(
        self, student_progress: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate a comprehensive progress report for a student."""
        tree_progress = self.skill_tree.calculate_progress(student_progress)
        xp = student_progress.get("total_xp", 0)
        level, xp_for_next, xp_progress = self.xp_system.get_level_from_xp(xp)

        return {
            "skill_tree_progress": tree_progress,
            "level_info": {
                "current_level": level,
                "xp_for_next_level": xp_for_next,
                "xp_progress_in_level": xp_progress,
                "total_xp": xp,
            },
            "badges": {
                "earned": student_progress.get("badges", []),
                "available": [
                    b.id for b in self.check_badge_eligibility(student_progress)
                ],
            },
            "next_unlocks": [
                node.id
                for node in self.skill_tree.get_next_available_nodes(student_progress)
            ],
        }
