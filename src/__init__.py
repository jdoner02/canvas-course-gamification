"""
Canvas Course Gamification Framework

A comprehensive Python framework for creating and deploying gamified courses to Canvas LMS
with automated skill trees, XP systems, and mastery-based learning progressions.
"""

__version__ = "1.0.0"
__author__ = "Canvas Course Gamification Contributors"
__license__ = "MIT"

from .canvas_api import CanvasAPIClient
from .course_builder import CourseBuilder
from .gamification import SkillTree, SkillNode, Badge, SkillLevel
from .validators import ConfigValidator, CanvasValidator

__all__ = [
    "CanvasAPIClient",
    "CourseBuilder", 
    "SkillTree",
    "SkillNode",
    "Badge",
    "SkillLevel",
    "ConfigValidator",
    "CanvasValidator",
]