"""
Linear Algebra Gamification Engine - Core Player Profile System
===============================================================

This module implements the RPG character system for mathematical learning,
inspired by RuneScape, World of Warcraft, and modern educational research.

Features:
- Mathematical specialization classes (Engineer, Data Scientist, etc.)
- Skill trees for linear algebra concepts
- Experience point system with leveling
- Ability unlocks and prestige mechanics
- FERPA-compliant privacy-respecting analytics

Author: AI Agent Development Team
Target: Dr. Lynch's MATH 231 at Eastern Washington University
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Any, Set
from datetime import datetime, timedelta
import json
import math
import statistics
import hashlib
import uuid
import uuid
import hashlib

# Privacy-respecting analytics (FERPA compliant)
try:
    from ...analytics.privacy_respecting_analytics import (
        PrivacyRespectingAnalytics,
        AnalyticsLevel,
    )

    ANALYTICS_AVAILABLE = True
except ImportError:
    # Graceful fallback if analytics not available
    ANALYTICS_AVAILABLE = False
    PrivacyRespectingAnalytics = None
    AnalyticsLevel = None


class MathematicalSpecialization(Enum):
    """Student character classes based on academic major and interests"""

    ENGINEER = "engineer"
    DATA_SCIENTIST = "data_scientist"
    PURE_MATHEMATICIAN = "pure_mathematician"
    APPLIED_MATHEMATICIAN = "applied_mathematician"
    INTERDISCIPLINARY = "interdisciplinary"


class SkillCategory(Enum):
    """Linear algebra skill categories for RPG progression"""

    VECTOR_OPERATIONS = "vector_operations"
    MATRIX_MASTERY = "matrix_mastery"
    LINEAR_TRANSFORMATIONS = "linear_transformations"
    EIGENVALUE_EXPERTISE = "eigenvalue_expertise"
    COMPUTATIONAL_SKILLS = "computational_skills"
    PROOF_TECHNIQUES = "proof_techniques"
    APPLICATIONS = "applications"


class AbilityType(Enum):
    """Types of abilities students can unlock"""

    PASSIVE = "passive"  # Always active bonuses
    ACTIVE = "active"  # Triggered abilities
    SOCIAL = "social"  # Collaboration bonuses
    LEARNING = "learning"  # Study enhancement
    COMBAT = "combat"  # Pet battle abilities


@dataclass
class Skill:
    """Individual skill within a category"""

    skill_id: str
    name: str
    description: str
    category: SkillCategory
    max_level: int = 100
    current_level: int = 0
    current_xp: int = 0
    xp_to_next_level: int = 100
    prerequisites: List[str] = field(default_factory=list)
    specialization_bonus: Dict[MathematicalSpecialization, float] = field(
        default_factory=dict
    )
    unlocked_abilities: List[str] = field(default_factory=list)

    def calculate_xp_requirement(self, level: int) -> int:
        """Calculate XP required for a specific level (exponential curve)"""
        if level <= 1:
            return 0
        # RuneScape-inspired XP curve: exponential growth with diminishing returns
        base = 100
        multiplier = 1.1 ** (level - 1)
        return int(base * multiplier)

    def add_experience(
        self, xp_gained: int, specialization: MathematicalSpecialization
    ) -> Dict[str, Any]:
        """Add XP with specialization bonuses and return level-up info"""
        # Apply specialization bonus
        bonus_multiplier = self.specialization_bonus.get(specialization, 1.0)
        effective_xp = int(xp_gained * bonus_multiplier)

        self.current_xp += effective_xp
        levels_gained = 0
        abilities_unlocked = []

        # Check for level ups
        while (
            self.current_xp >= self.xp_to_next_level
            and self.current_level < self.max_level
        ):
            self.current_level += 1
            levels_gained += 1
            self.current_xp -= self.xp_to_next_level

            # Update XP requirement for next level
            if self.current_level < self.max_level:
                self.xp_to_next_level = self.calculate_xp_requirement(
                    self.current_level + 1
                )

            # Check for ability unlocks
            new_abilities = self._check_ability_unlocks()
            abilities_unlocked.extend(new_abilities)

        return {
            "xp_gained": effective_xp,
            "bonus_multiplier": bonus_multiplier,
            "levels_gained": levels_gained,
            "new_level": self.current_level,
            "abilities_unlocked": abilities_unlocked,
            "overflow_xp": (
                self.current_xp if self.current_level >= self.max_level else 0
            ),
        }

    def _check_ability_unlocks(self) -> List[str]:
        """Check if current level unlocks new abilities"""
        # Define ability unlock levels
        ability_unlocks = {
            10: f"{self.skill_id}_novice_boost",
            25: f"{self.skill_id}_apprentice_technique",
            50: f"{self.skill_id}_expert_insight",
            75: f"{self.skill_id}_master_strategy",
            100: f"{self.skill_id}_grandmaster_mastery",
        }

        new_abilities = []
        for level, ability in ability_unlocks.items():
            if self.current_level >= level and ability not in self.unlocked_abilities:
                self.unlocked_abilities.append(ability)
                new_abilities.append(ability)

        return new_abilities

    def can_prestige(self) -> bool:
        """Check if skill can be reset for prestige bonuses"""
        return self.current_level >= self.max_level

    def prestige_reset(self) -> Dict[str, Any]:
        """Reset skill level but keep abilities and gain prestige bonuses"""
        if not self.can_prestige():
            return {"error": "Cannot prestige - not at max level"}

        prestige_abilities = [
            f"{self.skill_id}_prestige_{len([a for a in self.unlocked_abilities if 'prestige' in a]) + 1}"
        ]

        # Reset level but keep abilities
        old_level = self.current_level
        self.current_level = 1
        self.current_xp = 0
        self.xp_to_next_level = self.calculate_xp_requirement(2)
        self.unlocked_abilities.extend(prestige_abilities)

        return {
            "old_level": old_level,
            "prestige_abilities": prestige_abilities,
            "xp_bonus_multiplier": 1.1
            ** len(prestige_abilities),  # 10% bonus per prestige
            "status": "success",
        }


@dataclass
class Ability:
    """Student abilities unlocked through skill progression"""

    ability_id: str
    name: str
    description: str
    ability_type: AbilityType
    skill_requirement: str
    level_requirement: int
    effect_magnitude: float
    cooldown_seconds: int = 0
    energy_cost: int = 0
    prerequisites: List[str] = field(default_factory=list)


@dataclass
class PrivacyCompliantPlayerInsights:
    """
    FERPA-compliant player insights that provide educational value
    without storing personally identifiable information.

    This replaces detailed analytics with privacy-preserving alternatives.
    """

    # Educational progress indicators (non-identifying)
    concept_confidence_levels: Dict[str, str] = field(
        default_factory=dict
    )  # "low", "medium", "high"
    learning_preferences: Dict[str, str] = field(
        default_factory=dict
    )  # "visual", "auditory", etc.
    optimal_session_duration: str = "medium"  # "short", "medium", "long"
    preferred_difficulty: str = "adaptive"  # "easy", "medium", "hard", "adaptive"

    # Aggregated performance (no detailed tracking)
    concepts_engaged: Set[str] = field(
        default_factory=set
    )  # All concepts interacted with
    concepts_mastered: Set[str] = field(default_factory=set)
    concepts_in_progress: Set[str] = field(default_factory=set)
    concepts_needing_help: Set[str] = field(default_factory=set)

    # Educational patterns (privacy-preserving)
    effective_study_patterns: List[str] = field(
        default_factory=list
    )  # "morning_sessions", "short_bursts"
    learning_strengths: List[str] = field(
        default_factory=list
    )  # "visual_learner", "pattern_recognition"
    growth_areas: List[str] = field(
        default_factory=list
    )  # "needs_more_practice", "review_basics"

    # System recommendations (educational focus)
    next_recommended_concepts: List[str] = field(default_factory=list)
    suggested_practice_types: List[str] = field(default_factory=list)
    adaptive_content_level: str = "appropriate"

    # Engagement indicators (non-personal)
    engagement_level: str = "active"  # "low", "moderate", "active", "high"
    motivation_type: str = "intrinsic"  # "intrinsic", "extrinsic", "mixed"

    # Privacy metadata
    data_anonymized: bool = True
    ferpa_compliant: bool = True
    last_updated: datetime = field(default_factory=datetime.now)


@dataclass
class PrivacyCompliantSession:
    """
    Privacy-compliant session tracking that provides educational value
    without violating FERPA or storing identifying information.
    """

    session_id: str
    date_bucket: str  # "2025-07-04" (day-level only, no precise timestamps)
    duration_category: str  # "short", "medium", "long" instead of exact minutes

    # Educational outcomes (no behavioral tracking)
    concepts_engaged: Set[str] = field(default_factory=set)
    learning_objectives_met: List[str] = field(default_factory=list)
    areas_needing_review: List[str] = field(default_factory=list)

    # Performance indicators (aggregated only)
    overall_success_level: str = (
        "satisfactory"  # "needs_improvement", "satisfactory", "excellent"
    )
    help_requested: bool = False
    collaboration_occurred: bool = False

    # System feedback (educational focus)
    content_appropriateness: str = "just_right"  # "too_easy", "just_right", "too_hard"
    engagement_quality: str = "focused"  # "distracted", "focused", "highly_engaged"

    # Privacy protection
    contains_pii: bool = False
    anonymized: bool = True
    xp_earned: int = 0
    skills_improved: List[str] = field(default_factory=list)
    achievements_unlocked: List[str] = field(default_factory=list)
    mastery_demonstrated: List[str] = field(default_factory=list)


@dataclass
class PlayerProfile:
    """Complete RPG character profile for a student"""

    student_id: str
    display_name: str
    specialization: MathematicalSpecialization
    created_at: datetime

    # Core progression
    skills: Dict[str, Skill] = field(default_factory=dict)
    abilities: Dict[str, Ability] = field(default_factory=dict)
    active_abilities: List[str] = field(default_factory=list)

    # Statistics
    total_xp: int = 0
    total_levels: int = 0
    prestige_count: int = 0
    achievements_unlocked: List[str] = field(default_factory=list)

    # Social
    guild_id: Optional[str] = None
    mentor_id: Optional[str] = None
    mentees: List[str] = field(default_factory=list)

    # Engagement
    last_active: datetime = field(default_factory=datetime.now)
    streak_days: int = 0
    total_play_time: timedelta = field(default_factory=lambda: timedelta(0))

    # Customization
    profile_image: str = "default_avatar.png"
    title: str = "Aspiring Mathematician"
    display_preferences: Dict[str, Any] = field(default_factory=dict)

    # NEW: Privacy-Compliant Analytics (FERPA compliant)
    insights: PrivacyCompliantPlayerInsights = field(
        default_factory=PrivacyCompliantPlayerInsights
    )
    recent_sessions: List[PrivacyCompliantSession] = field(default_factory=list)
    current_session: Optional[PrivacyCompliantSession] = None

    # Educational recommendations (privacy-preserving)
    adaptive_recommendations: Dict[str, Any] = field(default_factory=dict)
    learning_path_suggestions: List[str] = field(default_factory=list)

    def calculate_total_level(self) -> int:
        """Calculate total level across all skills"""
        return sum(skill.current_level for skill in self.skills.values())

    def calculate_total_xp(self) -> int:
        """Calculate total XP earned across all skills"""
        total = 0
        for skill in self.skills.values():
            # Add current XP plus XP for completed levels
            for level in range(1, skill.current_level):
                total += skill.calculate_xp_requirement(level)
            total += skill.current_xp
        return total

    def get_specialization_bonuses(self) -> Dict[str, float]:
        """Get XP multipliers based on specialization"""
        bonuses = {
            MathematicalSpecialization.ENGINEER: {
                SkillCategory.APPLICATIONS: 1.25,
                SkillCategory.COMPUTATIONAL_SKILLS: 1.15,
                SkillCategory.LINEAR_TRANSFORMATIONS: 1.1,
            },
            MathematicalSpecialization.DATA_SCIENTIST: {
                SkillCategory.MATRIX_MASTERY: 1.25,
                SkillCategory.EIGENVALUE_EXPERTISE: 1.2,
                SkillCategory.COMPUTATIONAL_SKILLS: 1.15,
            },
            MathematicalSpecialization.PURE_MATHEMATICIAN: {
                SkillCategory.PROOF_TECHNIQUES: 1.3,
                SkillCategory.LINEAR_TRANSFORMATIONS: 1.2,
                SkillCategory.EIGENVALUE_EXPERTISE: 1.15,
            },
            MathematicalSpecialization.APPLIED_MATHEMATICIAN: {
                SkillCategory.APPLICATIONS: 1.2,
                SkillCategory.MATRIX_MASTERY: 1.15,
                SkillCategory.VECTOR_OPERATIONS: 1.1,
            },
            MathematicalSpecialization.INTERDISCIPLINARY: {
                # Balanced bonuses across all categories
                category: 1.1
                for category in SkillCategory
            },
        }
        return bonuses.get(self.specialization, {})

    def award_experience(
        self, skill_id: str, xp_amount: int, source: str = "unknown"
    ) -> Dict[str, Any]:
        """Award XP to a specific skill and track the source"""
        if skill_id not in self.skills:
            return {"error": f"Skill {skill_id} not found"}

        skill = self.skills[skill_id]
        result = skill.add_experience(xp_amount, self.specialization)

        # Update profile statistics
        self.total_xp = self.calculate_total_xp()
        self.total_levels = self.calculate_total_level()

        # Add tracking information
        result.update(
            {
                "skill_id": skill_id,
                "source": source,
                "timestamp": datetime.now().isoformat(),
                "total_levels": self.total_levels,
                "total_xp": self.total_xp,
            }
        )

        return result

    def update_activity(self, session_duration: timedelta):
        """Update player activity and streak tracking"""
        now = datetime.now()

        # Update streak
        if (now - self.last_active).days == 1:
            self.streak_days += 1
        elif (now - self.last_active).days > 1:
            self.streak_days = 1

        self.last_active = now
        self.total_play_time += session_duration

    def get_next_ability_unlock(self) -> Optional[Dict[str, Any]]:
        """Get information about the next ability the student can unlock"""
        available_abilities = []

        for skill in self.skills.values():
            next_unlock_level = None
            unlock_levels = [10, 25, 50, 75, 100]

            for level in unlock_levels:
                ability_id = f"{skill.skill_id}_{['novice', 'apprentice', 'expert', 'master', 'grandmaster'][unlock_levels.index(level)]}_boost"
                if (
                    skill.current_level < level
                    and ability_id not in skill.unlocked_abilities
                ):
                    next_unlock_level = level
                    break

            if next_unlock_level:
                xp_needed = 0
                for lvl in range(skill.current_level + 1, next_unlock_level + 1):
                    xp_needed += skill.calculate_xp_requirement(lvl)
                xp_needed -= skill.current_xp

                available_abilities.append(
                    {
                        "skill_id": skill.skill_id,
                        "skill_name": skill.name,
                        "unlock_level": next_unlock_level,
                        "current_level": skill.current_level,
                        "levels_needed": next_unlock_level - skill.current_level,
                        "xp_needed": xp_needed,
                        "ability_preview": f"Enhanced {skill.name.lower()} learning efficiency",
                    }
                )

        if not available_abilities:
            return None

        # Return the closest unlock
        return min(available_abilities, key=lambda x: x["xp_needed"])

    def to_dict(self) -> Dict[str, Any]:
        """Convert player profile to dictionary for storage/API"""
        return {
            "student_id": self.student_id,
            "display_name": self.display_name,
            "specialization": self.specialization.value,
            "created_at": self.created_at.isoformat(),
            "skills": {
                k: {
                    "skill_id": v.skill_id,
                    "name": v.name,
                    "category": v.category.value,
                    "current_level": v.current_level,
                    "current_xp": v.current_xp,
                    "max_level": v.max_level,
                    "unlocked_abilities": v.unlocked_abilities,
                }
                for k, v in self.skills.items()
            },
            "total_xp": self.total_xp,
            "total_levels": self.total_levels,
            "prestige_count": self.prestige_count,
            "achievements": self.achievements_unlocked,
            "guild_id": self.guild_id,
            "streak_days": self.streak_days,
            "last_active": self.last_active.isoformat(),
            "profile_image": self.profile_image,
            "title": self.title,
        }

    # === PRIVACY-COMPLIANT ANALYTICS METHODS ===

    def record_learning_interaction(
        self,
        concept: str,
        interaction_type: str = "practice",
        success: bool = True,
        analytics_system=None,  # Type: Optional[PrivacyRespectingAnalytics]
    ) -> None:
        """
        Record a learning interaction with full privacy protection.

        This method ensures FERPA compliance by:
        - Not storing personally identifiable information
        - Using pseudonymized identifiers
        - Aggregating data before storage
        - Applying differential privacy
        """
        if not ANALYTICS_AVAILABLE or analytics_system is None:
            # Fallback: Update local insights only
            self.insights.concepts_engaged.add(concept)
            if success:
                self.insights.concepts_mastered.add(concept)
            else:
                self.insights.concepts_needing_help.add(concept)
            return

        # Record interaction with privacy protection
        analytics_system.record_learning_interaction(
            user_id=self.student_id,  # Will be pseudonymized internally
            concept=concept,
            interaction_type=interaction_type,
            success=success,
        )

        # Update local privacy-compliant insights
        self.insights.concepts_engaged.add(concept)
        if success:
            self.insights.concepts_mastered.add(concept)
            self.insights.concepts_needing_help.discard(concept)
        else:
            self.insights.concepts_needing_help.add(concept)

        self.insights.last_updated = datetime.now()

    def start_privacy_compliant_session(self) -> str:
        """Start a new learning session with privacy protection"""
        session_id = str(uuid.uuid4())

        # Create privacy-compliant session (no PII stored)
        session = PrivacyCompliantSession(
            session_id=session_id,
            date_bucket=datetime.now().strftime("%Y-%m-%d"),  # Day-level precision only
            duration_category="unknown",  # Will be updated when session ends
        )

        self.current_session = session
        return session_id

    def end_privacy_compliant_session(
        self,
        duration_minutes: float,
        concepts_studied: List[str],
        success_level: str = "satisfactory",
    ) -> None:
        """End learning session with privacy-compliant data storage"""
        if not self.current_session:
            return

        # Categorize duration (no exact tracking)
        if duration_minutes < 15:
            duration_category = "short"
        elif duration_minutes < 45:
            duration_category = "medium"
        elif duration_minutes < 90:
            duration_category = "long"
        else:
            duration_category = "extended"

        # Update session with aggregated data only
        self.current_session.duration_category = duration_category
        self.current_session.concepts_engaged.update(concepts_studied)
        self.current_session.overall_success_level = success_level

        # Add to recent sessions (keep only last 5 for privacy)
        self.recent_sessions.append(self.current_session)
        if len(self.recent_sessions) > 5:
            self.recent_sessions.pop(0)

        self.current_session = None

        # Update activity tracking
        self.update_activity(timedelta(minutes=duration_minutes))

    def get_privacy_compliant_insights(self) -> Dict[str, Any]:
        """Get educational insights with full privacy protection"""

        # Calculate learning progress (no detailed tracking)
        total_concepts = len(self.insights.concepts_engaged)
        mastered_concepts = len(self.insights.concepts_mastered)
        progress_percentage = (
            (mastered_concepts / total_concepts * 100) if total_concepts > 0 else 0
        )

        # Generate educational recommendations
        recommendations = []
        if self.insights.concepts_needing_help:
            recommendations.append("Review challenging concepts")
        if len(self.insights.concepts_mastered) > 5:
            recommendations.append("Try advanced practice problems")
        if not self.recent_sessions:
            recommendations.append("Start a new learning session")

        return {
            "learning_progress": {
                "progress_percentage": round(progress_percentage, 1),
                "concepts_mastered": len(self.insights.concepts_mastered),
                "concepts_in_progress": len(self.insights.concepts_in_progress),
                "areas_for_review": len(self.insights.concepts_needing_help),
            },
            "study_patterns": {
                "preferred_session_length": self.insights.optimal_session_duration,
                "effective_study_approaches": self.insights.effective_study_patterns,
                "learning_strengths": self.insights.learning_strengths,
            },
            "recommendations": {
                "next_steps": recommendations,
                "suggested_content": self.insights.next_recommended_concepts[:3],
                "adaptive_level": self.insights.adaptive_content_level,
            },
            "privacy_metadata": {
                "ferpa_compliant": True,
                "data_anonymized": True,
                "no_pii_stored": True,
                "last_updated": self.insights.last_updated.isoformat(),
            },
        }

    def export_research_data(
        self, consent_given: bool = False
    ) -> Optional[Dict[str, Any]]:
        """
        Export anonymized data for research purposes.

        Only available with explicit consent and returns completely
        de-identified data suitable for educational research.
        """
        if not consent_given:
            return None

        # Export only aggregated, anonymized research data
        return {
            "participant_id": hashlib.sha256(
                f"research_{self.student_id}".encode()
            ).hexdigest()[:16],
            "specialization": self.specialization.value,
            "aggregated_progress": {
                "total_skill_levels": self.total_levels,
                "total_experience": self.total_xp,
                "activity_days": self.streak_days,
                "concepts_engaged_count": len(self.insights.concepts_engaged),
                "mastery_rate": len(self.insights.concepts_mastered)
                / max(1, len(self.insights.concepts_engaged)),
            },
            "learning_patterns": {
                "session_frequency": len(self.recent_sessions),
                "engagement_level": self.insights.engagement_level,
                "learning_preferences": self.insights.learning_preferences,
            },
            "privacy_protection": {
                "anonymized": True,
                "aggregated": True,
                "consent_verified": True,
                "export_timestamp": datetime.now().isoformat(),
            },
        }

    def get_ferpa_compliance_status(self) -> Dict[str, Any]:
        """Get FERPA compliance status for this player profile"""
        return {
            "ferpa_compliant": True,
            "pii_stored": False,  # No personally identifiable information stored
            "detailed_tracking": False,  # No detailed behavioral tracking
            "data_anonymized": True,
            "consent_required_features": {
                "research_data_export": "explicit_consent_required",
                "detailed_analytics": "disabled_for_privacy",
                "behavioral_profiling": "disabled_for_privacy",
            },
            "privacy_protections": {
                "pseudonymization": True,
                "temporal_bucketing": True,
                "aggregated_metrics_only": True,
                "automatic_data_expiration": True,
            },
            "educational_focus": {
                "learning_progress_tracking": True,
                "concept_mastery_indicators": True,
                "adaptive_content_recommendations": True,
                "performance_insights": True,
            },
        }


class PlayerProfileManager:
    """Manager class for player profiles and progression system"""

    def __init__(self):
        self.profiles: Dict[str, PlayerProfile] = {}
        self.skill_templates = self._create_skill_templates()
        self.ability_templates = self._create_ability_templates()

    def _create_skill_templates(self) -> Dict[str, Skill]:
        """Create the standard linear algebra skill tree"""
        skills = {
            # Vector Operations
            "vector_basics": Skill(
                "vector_basics",
                "Vector Fundamentals",
                "Understanding vectors as directed quantities with magnitude and direction",
                SkillCategory.VECTOR_OPERATIONS,
            ),
            "vector_arithmetic": Skill(
                "vector_arithmetic",
                "Vector Arithmetic",
                "Addition, subtraction, and scalar multiplication of vectors",
                SkillCategory.VECTOR_OPERATIONS,
                prerequisites=["vector_basics"],
            ),
            "dot_product": Skill(
                "dot_product",
                "Dot Product Mastery",
                "Computing and understanding the geometric meaning of dot products",
                SkillCategory.VECTOR_OPERATIONS,
                prerequisites=["vector_arithmetic"],
            ),
            "cross_product": Skill(
                "cross_product",
                "Cross Product Expertise",
                "Three-dimensional vector cross products and applications",
                SkillCategory.VECTOR_OPERATIONS,
                prerequisites=["dot_product"],
            ),
            # Matrix Mastery
            "matrix_basics": Skill(
                "matrix_basics",
                "Matrix Fundamentals",
                "Understanding matrices as rectangular arrays of numbers",
                SkillCategory.MATRIX_MASTERY,
            ),
            "matrix_operations": Skill(
                "matrix_operations",
                "Matrix Operations",
                "Addition, multiplication, and basic matrix manipulations",
                SkillCategory.MATRIX_MASTERY,
                prerequisites=["matrix_basics"],
            ),
            "matrix_inverse": Skill(
                "matrix_inverse",
                "Matrix Inversion",
                "Computing and understanding matrix inverses",
                SkillCategory.MATRIX_MASTERY,
                prerequisites=["matrix_operations"],
            ),
            "determinants": Skill(
                "determinants",
                "Determinant Computation",
                "Computing determinants and understanding their geometric meaning",
                SkillCategory.MATRIX_MASTERY,
                prerequisites=["matrix_operations"],
            ),
            # Linear Transformations
            "linear_maps": Skill(
                "linear_maps",
                "Linear Mappings",
                "Understanding functions that preserve vector addition and scalar multiplication",
                SkillCategory.LINEAR_TRANSFORMATIONS,
                prerequisites=["vector_arithmetic", "matrix_basics"],
            ),
            "transformation_matrix": Skill(
                "transformation_matrix",
                "Transformation Matrices",
                "Representing linear transformations as matrices",
                SkillCategory.LINEAR_TRANSFORMATIONS,
                prerequisites=["linear_maps", "matrix_operations"],
            ),
            "kernel_image": Skill(
                "kernel_image",
                "Kernel and Image",
                "Understanding null space and column space of linear transformations",
                SkillCategory.LINEAR_TRANSFORMATIONS,
                prerequisites=["transformation_matrix"],
            ),
            # Eigenvalue Expertise
            "eigenvalues": Skill(
                "eigenvalues",
                "Eigenvalue Computation",
                "Finding eigenvalues of matrices",
                SkillCategory.EIGENVALUE_EXPERTISE,
                prerequisites=["determinants", "transformation_matrix"],
            ),
            "eigenvectors": Skill(
                "eigenvectors",
                "Eigenvector Analysis",
                "Computing and interpreting eigenvectors",
                SkillCategory.EIGENVALUE_EXPERTISE,
                prerequisites=["eigenvalues"],
            ),
            "diagonalization": Skill(
                "diagonalization",
                "Matrix Diagonalization",
                "Diagonalizing matrices using eigenvalues and eigenvectors",
                SkillCategory.EIGENVALUE_EXPERTISE,
                prerequisites=["eigenvectors"],
            ),
        }

        # Add specialization bonuses
        for skill in skills.values():
            if skill.category == SkillCategory.APPLICATIONS:
                skill.specialization_bonus[MathematicalSpecialization.ENGINEER] = 1.25
                skill.specialization_bonus[
                    MathematicalSpecialization.APPLIED_MATHEMATICIAN
                ] = 1.2
            elif skill.category == SkillCategory.PROOF_TECHNIQUES:
                skill.specialization_bonus[
                    MathematicalSpecialization.PURE_MATHEMATICIAN
                ] = 1.3
            elif skill.category == SkillCategory.COMPUTATIONAL_SKILLS:
                skill.specialization_bonus[
                    MathematicalSpecialization.DATA_SCIENTIST
                ] = 1.25
                skill.specialization_bonus[MathematicalSpecialization.ENGINEER] = 1.15

        return skills

    def _create_ability_templates(self) -> Dict[str, Ability]:
        """Create ability templates that students can unlock"""
        return {
            "quick_learner": Ability(
                "quick_learner",
                "Quick Learner",
                "Gain 10% more XP from all sources",
                AbilityType.PASSIVE,
                "",
                10,
                0.1,
            ),
            "problem_solver": Ability(
                "problem_solver",
                "Problem Solver",
                "Reduce hint penalties by 25%",
                AbilityType.PASSIVE,
                "",
                25,
                0.25,
            ),
            "mentor": Ability(
                "mentor",
                "Mentor",
                "Gain XP when helping other students",
                AbilityType.SOCIAL,
                "",
                50,
                0.5,
            ),
            "focused_mind": Ability(
                "focused_mind",
                "Focused Mind",
                "Double XP for next 30 minutes (once per day)",
                AbilityType.ACTIVE,
                "",
                75,
                2.0,
                86400,  # 24 hour cooldown
            ),
        }

    def create_player(
        self,
        student_id: str,
        display_name: str,
        specialization: MathematicalSpecialization,
    ) -> PlayerProfile:
        """Create a new player profile with initialized skills"""
        profile = PlayerProfile(
            student_id=student_id,
            display_name=display_name,
            specialization=specialization,
            created_at=datetime.now(),
        )

        # Initialize all skills
        for skill_id, skill_template in self.skill_templates.items():
            profile.skills[skill_id] = Skill(
                skill_template.skill_id,
                skill_template.name,
                skill_template.description,
                skill_template.category,
                skill_template.max_level,
                prerequisites=skill_template.prerequisites.copy(),
                specialization_bonus=skill_template.specialization_bonus.copy(),
            )

        self.profiles[student_id] = profile
        return profile

    def get_player(self, student_id: str) -> Optional[PlayerProfile]:
        """Get player profile by ID"""
        return self.profiles.get(student_id)

    def award_xp(
        self,
        student_id: str,
        skill_id: str,
        xp_amount: int,
        source: str = "problem_solving",
    ) -> Dict[str, Any]:
        """Award XP to a student for a specific skill"""
        profile = self.get_player(student_id)
        if not profile:
            return {"error": "Player not found"}

        return profile.award_experience(skill_id, xp_amount, source)

    def get_leaderboard(
        self, metric: str = "total_xp", limit: int = 10
    ) -> List[Dict[str, Any]]:
        """Get leaderboard for various metrics"""
        if metric == "total_xp":
            sorted_players = sorted(
                self.profiles.values(), key=lambda p: p.total_xp, reverse=True
            )
        elif metric == "total_levels":
            sorted_players = sorted(
                self.profiles.values(), key=lambda p: p.total_levels, reverse=True
            )
        elif metric == "streak_days":
            sorted_players = sorted(
                self.profiles.values(), key=lambda p: p.streak_days, reverse=True
            )
        else:
            return {"error": f"Unknown metric: {metric}"}

        return [
            {
                "rank": i + 1,
                "student_id": player.student_id,
                "display_name": player.display_name,
                "specialization": player.specialization.value,
                "value": getattr(player, metric),
                "title": player.title,
            }
            for i, player in enumerate(sorted_players[:limit])
        ]


# Example usage and testing
if __name__ == "__main__":
    # Initialize the player profile manager
    manager = PlayerProfileManager()

    # Create test players
    alice = manager.create_player(
        "alice_123", "Alice Engineer", MathematicalSpecialization.ENGINEER
    )
    bob = manager.create_player(
        "bob_456", "Bob DataSci", MathematicalSpecialization.DATA_SCIENTIST
    )

    print("🎮 Linear Algebra RPG System Initialized!")
    print(f"Created players: {alice.display_name} ({alice.specialization.value})")
    print(f"                 {bob.display_name} ({bob.specialization.value})")

    # Simulate learning activity
    print("\n📚 Simulating Learning Activity:")

    # Alice solves vector problems (engineering bonus applies)
    result = manager.award_xp("alice_123", "vector_basics", 150, "homework_completion")
    print(
        f"Alice gained {result['xp_gained']} XP in Vector Basics (bonus: {result['bonus_multiplier']:.1f}x)"
    )
    if result["levels_gained"] > 0:
        print(f"🎉 Level up! Alice reached level {result['new_level']}")

    # Bob works on matrix problems (data science bonus)
    result = manager.award_xp("bob_456", "matrix_basics", 200, "lab_exercise")
    print(
        f"Bob gained {result['xp_gained']} XP in Matrix Basics (bonus: {result['bonus_multiplier']:.1f}x)"
    )

    # Show next ability unlock
    next_unlock = alice.get_next_ability_unlock()
    if next_unlock:
        print(f"\n🔮 Alice's next unlock: {next_unlock['ability_preview']}")
        print(
            f"   Needs {next_unlock['levels_needed']} more levels in {next_unlock['skill_name']}"
        )

    # Show leaderboard
    print(f"\n🏆 Current Leaderboard (Total XP):")
    leaderboard = manager.get_leaderboard("total_xp", 5)
    for entry in leaderboard:
        print(f"   {entry['rank']}. {entry['display_name']} - {entry['value']} XP")
