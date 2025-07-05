"""
🧠 ADAPTIVE LEARNING ENGINE
Real-time learning adaptation based on student performance and preferences
"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Dict, List, Optional, Union, Tuple
import json
import math
import random


class LearningStyle(Enum):
    """Student learning style preferences"""

    VISUAL = "visual"
    AUDITORY = "auditory"
    KINESTHETIC = "kinesthetic"
    LOGICAL = "logical"
    SOCIAL = "social"
    VERBAL = "verbal"


class DifficultyLevel(Enum):
    """Problem difficulty levels"""

    TUTORIAL = "tutorial"
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"
    EXPERT = "expert"
    LEGENDARY = "legendary"


class ConceptCategory(Enum):
    """Linear algebra concept categories"""

    VECTORS = "vectors"
    MATRICES = "matrices"
    LINEAR_TRANSFORMATIONS = "linear_transformations"
    EIGENVALUES = "eigenvalues"
    VECTOR_SPACES = "vector_spaces"
    INNER_PRODUCTS = "inner_products"
    APPLICATIONS = "applications"


@dataclass
class LearningProfile:
    """Student's learning profile and preferences"""

    student_id: str
    learning_styles: Dict[LearningStyle, float] = field(default_factory=dict)
    skill_levels: Dict[ConceptCategory, float] = field(default_factory=dict)
    preferred_difficulty: DifficultyLevel = DifficultyLevel.MEDIUM
    attention_span: int = 25  # minutes
    optimal_session_length: int = 45  # minutes
    peak_learning_times: List[int] = field(default_factory=lambda: [9, 14, 19])  # hours
    motivation_level: float = 0.7
    confidence_level: float = 0.6
    last_updated: datetime = field(default_factory=datetime.now)

    def get_learning_style_weights(self) -> Dict[LearningStyle, float]:
        """Get normalized learning style preferences"""
        if not self.learning_styles:
            # Default equal weights
            return {style: 1.0 / len(LearningStyle) for style in LearningStyle}

        total = sum(self.learning_styles.values())
        if total == 0:
            return {style: 1.0 / len(LearningStyle) for style in LearningStyle}

        return {style: weight / total for style, weight in self.learning_styles.items()}


@dataclass
class PerformanceMetrics:
    """Student performance tracking"""

    student_id: str
    concept_category: ConceptCategory
    problems_attempted: int = 0
    problems_solved: int = 0
    average_time: float = 0.0  # seconds
    streak_current: int = 0
    streak_best: int = 0
    difficulty_progression: List[Tuple[datetime, DifficultyLevel]] = field(
        default_factory=list
    )
    mistake_patterns: Dict[str, int] = field(default_factory=dict)
    help_requests: int = 0
    last_activity: datetime = field(default_factory=datetime.now)

    @property
    def success_rate(self) -> float:
        """Calculate success rate"""
        if self.problems_attempted == 0:
            return 0.0
        return self.problems_solved / self.problems_attempted

    @property
    def efficiency_score(self) -> float:
        """Calculate efficiency based on time and accuracy"""
        if self.success_rate == 0:
            return 0.0
        # Faster solving with high accuracy = higher efficiency
        time_factor = max(0.1, 1.0 - (self.average_time / 300))  # 5 minutes = baseline
        return self.success_rate * time_factor


@dataclass
class AdaptiveRecommendation:
    """AI recommendation for next learning activity"""

    student_id: str
    concept_category: ConceptCategory
    difficulty_level: DifficultyLevel
    learning_style: LearningStyle
    content_type: str  # "problem", "video", "explanation", "practice"
    estimated_duration: int  # minutes
    confidence_score: float  # 0-1, how confident the AI is in this recommendation
    reasoning: str
    metadata: Dict = field(default_factory=dict)


class AdaptiveLearningEngine:
    """
    🧠 ADAPTIVE LEARNING ENGINE

    AI-powered system that personalizes learning experiences
    Features:
    - Real-time difficulty adjustment
    - Learning style detection and adaptation
    - Personalized content recommendations
    - Optimal scheduling based on performance patterns
    - Mistake pattern analysis and remediation
    - Flow state optimization
    """

    def __init__(self):
        self.learning_profiles: Dict[str, LearningProfile] = {}
        self.performance_metrics: Dict[
            str, Dict[ConceptCategory, PerformanceMetrics]
        ] = {}
        self.recent_activities: List[Dict] = []
        self.adaptation_parameters = self._initialize_adaptation_parameters()

    def _initialize_adaptation_parameters(self) -> Dict:
        """Initialize AI adaptation parameters"""
        return {
            "difficulty_adjustment_threshold": 0.1,  # How much performance change triggers adjustment
            "learning_style_confidence_threshold": 0.15,  # Minimum difference to prefer a style
            "optimal_success_rate": 0.75,  # Target success rate for flow state
            "streak_bonus_threshold": 5,  # Consecutive successes before difficulty increase
            "struggle_threshold": 3,  # Consecutive failures before difficulty decrease
            "attention_decay_factor": 0.95,  # How attention decreases over time
            "motivation_recovery_rate": 0.1,  # How quickly motivation recovers
            "confidence_impact_factor": 0.2,  # How much confidence affects recommendations
        }

    def get_learning_profile(self, student_id: str) -> LearningProfile:
        """Get or create student learning profile"""
        if student_id not in self.learning_profiles:
            self.learning_profiles[student_id] = LearningProfile(student_id=student_id)
        return self.learning_profiles[student_id]

    def get_performance_metrics(
        self, student_id: str, concept: ConceptCategory
    ) -> PerformanceMetrics:
        """Get or create performance metrics for student and concept"""
        if student_id not in self.performance_metrics:
            self.performance_metrics[student_id] = {}

        if concept not in self.performance_metrics[student_id]:
            self.performance_metrics[student_id][concept] = PerformanceMetrics(
                student_id=student_id, concept_category=concept
            )

        return self.performance_metrics[student_id][concept]

    def record_activity(
        self,
        student_id: str,
        activity_type: str,
        concept: ConceptCategory,
        difficulty: DifficultyLevel,
        success: bool,
        time_spent: float,
        mistakes: List[str] = None,
    ):
        """Record a learning activity and update profiles"""
        profile = self.get_learning_profile(student_id)
        metrics = self.get_performance_metrics(student_id, concept)

        # Update performance metrics
        metrics.problems_attempted += 1
        if success:
            metrics.problems_solved += 1
            metrics.streak_current += 1
            metrics.streak_best = max(metrics.streak_best, metrics.streak_current)
        else:
            metrics.streak_current = 0

        # Update average time (weighted average)
        alpha = 0.2  # Learning rate
        metrics.average_time = (1 - alpha) * metrics.average_time + alpha * time_spent

        # Track difficulty progression
        metrics.difficulty_progression.append((datetime.now(), difficulty))

        # Track mistakes
        if mistakes:
            for mistake in mistakes:
                metrics.mistake_patterns[mistake] = (
                    metrics.mistake_patterns.get(mistake, 0) + 1
                )

        # Update learning profile
        self._update_learning_profile(profile, concept, success, time_spent, difficulty)

        # Record activity for pattern analysis
        self.recent_activities.append(
            {
                "student_id": student_id,
                "activity_type": activity_type,
                "concept": concept.value,
                "difficulty": difficulty.value,
                "success": success,
                "time_spent": time_spent,
                "timestamp": datetime.now(),
            }
        )

        # Keep only recent activities (last 100)
        if len(self.recent_activities) > 100:
            self.recent_activities = self.recent_activities[-100:]

    def _update_learning_profile(
        self,
        profile: LearningProfile,
        concept: ConceptCategory,
        success: bool,
        time_spent: float,
        difficulty: DifficultyLevel,
    ):
        """Update learning profile based on activity"""
        # Update skill level for concept
        skill_change = 0.05 if success else -0.02
        current_skill = profile.skill_levels.get(concept, 0.5)
        profile.skill_levels[concept] = max(0.0, min(1.0, current_skill + skill_change))

        # Update confidence based on performance
        confidence_change = 0.03 if success else -0.05
        profile.confidence_level = max(
            0.0, min(1.0, profile.confidence_level + confidence_change)
        )

        # Update motivation (decreases with failures, increases with successes)
        motivation_change = 0.02 if success else -0.03
        profile.motivation_level = max(
            0.0, min(1.0, profile.motivation_level + motivation_change)
        )

        # Adjust preferred difficulty based on performance
        difficulty_values = {d: i for i, d in enumerate(DifficultyLevel)}
        current_diff_value = difficulty_values[profile.preferred_difficulty]

        if success and profile.confidence_level > 0.8:
            # If performing well, can handle harder problems
            new_diff_value = min(len(DifficultyLevel) - 1, current_diff_value + 1)
        elif not success and profile.confidence_level < 0.4:
            # If struggling, need easier problems
            new_diff_value = max(0, current_diff_value - 1)
        else:
            new_diff_value = current_diff_value

        profile.preferred_difficulty = list(DifficultyLevel)[new_diff_value]
        profile.last_updated = datetime.now()

    def detect_learning_style(self, student_id: str) -> Dict[LearningStyle, float]:
        """Detect student's learning style preferences from activity patterns"""
        # This would analyze interaction patterns, time spent on different content types,
        # success rates with different presentation modes, etc.

        # For now, simulate learning style detection
        profile = self.get_learning_profile(student_id)

        # Analyze recent activities to infer learning style preferences
        student_activities = [
            a for a in self.recent_activities if a["student_id"] == student_id
        ]

        if len(student_activities) < 5:
            # Not enough data, use default distribution
            return {style: 0.16 for style in LearningStyle}

        # Simulate learning style detection based on activity patterns
        style_scores = {}

        # Visual learners tend to succeed more with visual content
        visual_success = sum(
            1
            for a in student_activities
            if a.get("content_type") == "visual" and a["success"]
        )
        style_scores[LearningStyle.VISUAL] = visual_success / len(student_activities)

        # Logical learners prefer step-by-step problem solving
        logical_success = sum(
            1
            for a in student_activities
            if a.get("methodology") == "step_by_step" and a["success"]
        )
        style_scores[LearningStyle.LOGICAL] = logical_success / len(student_activities)

        # Fill in other styles with baseline scores
        for style in LearningStyle:
            if style not in style_scores:
                style_scores[style] = 0.15 + random.uniform(-0.05, 0.05)

        # Normalize scores
        total = sum(style_scores.values())
        normalized_scores = {
            style: score / total for style, score in style_scores.items()
        }

        # Update profile
        profile.learning_styles = normalized_scores

        return normalized_scores

    def get_adaptive_recommendation(self, student_id: str) -> AdaptiveRecommendation:
        """
        Generate AI-powered recommendation for next learning activity

        Returns:
            AdaptiveRecommendation with personalized suggestions
        """
        profile = self.get_learning_profile(student_id)

        # Determine which concept to focus on
        concept = self._select_optimal_concept(student_id)

        # Determine optimal difficulty
        difficulty = self._calculate_optimal_difficulty(student_id, concept)

        # Determine best learning style approach
        learning_style = self._select_optimal_learning_style(student_id)

        # Determine content type
        content_type = self._select_content_type(student_id, concept)

        # Estimate duration
        duration = self._estimate_optimal_duration(student_id)

        # Calculate confidence in recommendation
        confidence = self._calculate_recommendation_confidence(student_id, concept)

        # Generate reasoning
        reasoning = self._generate_reasoning(
            student_id, concept, difficulty, learning_style
        )

        return AdaptiveRecommendation(
            student_id=student_id,
            concept_category=concept,
            difficulty_level=difficulty,
            learning_style=learning_style,
            content_type=content_type,
            estimated_duration=duration,
            confidence_score=confidence,
            reasoning=reasoning,
            metadata={
                "profile_confidence": profile.confidence_level,
                "motivation": profile.motivation_level,
                "current_time": datetime.now().hour,
            },
        )

    def _select_optimal_concept(self, student_id: str) -> ConceptCategory:
        """Select the most beneficial concept for the student to work on"""
        profile = self.get_learning_profile(student_id)

        # Find concepts that need improvement
        concept_scores = {}
        for concept in ConceptCategory:
            skill_level = profile.skill_levels.get(concept, 0.5)
            metrics = self.get_performance_metrics(student_id, concept)

            # Score based on need for improvement and recent activity
            recency_factor = 1.0
            if metrics.last_activity:
                days_since = (datetime.now() - metrics.last_activity).days
                recency_factor = max(0.5, 1.0 - days_since * 0.1)

            # Lower skill levels get higher priority, but not too low (frustration)
            skill_need = max(0.1, 1.0 - skill_level) * recency_factor
            concept_scores[concept] = skill_need

        # Select concept with highest need score
        return max(concept_scores.items(), key=lambda x: x[1])[0]

    def _calculate_optimal_difficulty(
        self, student_id: str, concept: ConceptCategory
    ) -> DifficultyLevel:
        """Calculate optimal difficulty for flow state"""
        profile = self.get_learning_profile(student_id)
        metrics = self.get_performance_metrics(student_id, concept)

        # Base difficulty on skill level and recent performance
        skill_level = profile.skill_levels.get(concept, 0.5)
        success_rate = metrics.success_rate

        # Adjust for confidence and motivation
        confidence_factor = profile.confidence_level
        motivation_factor = profile.motivation_level

        # Calculate target difficulty (0-1 scale)
        base_difficulty = skill_level * 0.8 + success_rate * 0.2
        adjusted_difficulty = base_difficulty * confidence_factor * motivation_factor

        # Map to difficulty levels
        difficulty_mapping = [
            (0.0, DifficultyLevel.TUTORIAL),
            (0.2, DifficultyLevel.EASY),
            (0.4, DifficultyLevel.MEDIUM),
            (0.6, DifficultyLevel.HARD),
            (0.8, DifficultyLevel.EXPERT),
            (0.95, DifficultyLevel.LEGENDARY),
        ]

        for threshold, level in reversed(difficulty_mapping):
            if adjusted_difficulty >= threshold:
                return level

        return DifficultyLevel.TUTORIAL

    def _select_optimal_learning_style(self, student_id: str) -> LearningStyle:
        """Select best learning style for current session"""
        style_weights = self.detect_learning_style(student_id)

        # Add some randomness to prevent getting stuck in one style
        randomized_weights = {}
        for style, weight in style_weights.items():
            randomized_weights[style] = weight + random.uniform(-0.05, 0.05)

        return max(randomized_weights.items(), key=lambda x: x[1])[0]

    def _select_content_type(self, student_id: str, concept: ConceptCategory) -> str:
        """Select optimal content type based on student needs"""
        metrics = self.get_performance_metrics(student_id, concept)
        profile = self.get_learning_profile(student_id)

        # If struggling, provide more explanation
        if metrics.success_rate < 0.5:
            return "explanation"

        # If doing well, provide practice
        elif metrics.success_rate > 0.8:
            return "challenge_problem"

        # If confidence is low, provide guided practice
        elif profile.confidence_level < 0.5:
            return "guided_practice"

        # Default to mixed practice
        else:
            return "practice"

    def _estimate_optimal_duration(self, student_id: str) -> int:
        """Estimate optimal session duration"""
        profile = self.get_learning_profile(student_id)

        # Base duration on attention span and current time
        base_duration = profile.attention_span

        # Adjust for motivation
        motivation_factor = 0.5 + profile.motivation_level * 0.5

        # Adjust for time of day (peak times get longer sessions)
        current_hour = datetime.now().hour
        time_factor = 1.2 if current_hour in profile.peak_learning_times else 0.8

        optimal_duration = int(base_duration * motivation_factor * time_factor)
        return max(10, min(60, optimal_duration))  # Clamp between 10-60 minutes

    def _calculate_recommendation_confidence(
        self, student_id: str, concept: ConceptCategory
    ) -> float:
        """Calculate confidence in the recommendation"""
        metrics = self.get_performance_metrics(student_id, concept)
        profile = self.get_learning_profile(student_id)

        # More data = higher confidence
        data_confidence = min(1.0, metrics.problems_attempted / 20)

        # Consistent performance = higher confidence
        performance_variance = self._calculate_performance_variance(student_id, concept)
        consistency_confidence = max(0.3, 1.0 - performance_variance)

        # Recent activity = higher confidence
        recency_confidence = 1.0
        if metrics.last_activity:
            days_since = (datetime.now() - metrics.last_activity).days
            recency_confidence = max(0.5, 1.0 - days_since * 0.1)

        overall_confidence = (
            data_confidence + consistency_confidence + recency_confidence
        ) / 3
        return round(overall_confidence, 2)

    def _calculate_performance_variance(
        self, student_id: str, concept: ConceptCategory
    ) -> float:
        """Calculate variance in recent performance"""
        # Simplified variance calculation
        student_activities = [
            a
            for a in self.recent_activities
            if a["student_id"] == student_id and a["concept"] == concept.value
        ]

        if len(student_activities) < 3:
            return 0.5  # Medium variance for insufficient data

        success_rates = []
        window_size = 5

        for i in range(len(student_activities) - window_size + 1):
            window = student_activities[i : i + window_size]
            success_rate = sum(1 for a in window if a["success"]) / len(window)
            success_rates.append(success_rate)

        if not success_rates:
            return 0.5

        mean_rate = sum(success_rates) / len(success_rates)
        variance = sum((rate - mean_rate) ** 2 for rate in success_rates) / len(
            success_rates
        )

        return math.sqrt(variance)

    def _generate_reasoning(
        self,
        student_id: str,
        concept: ConceptCategory,
        difficulty: DifficultyLevel,
        learning_style: LearningStyle,
    ) -> str:
        """Generate human-readable reasoning for the recommendation"""
        profile = self.get_learning_profile(student_id)
        metrics = self.get_performance_metrics(student_id, concept)

        reasoning_parts = []

        # Concept selection reasoning
        skill_level = profile.skill_levels.get(concept, 0.5)
        if skill_level < 0.4:
            reasoning_parts.append(
                f"Focusing on {concept.value.replace('_', ' ')} to build foundational skills"
            )
        elif skill_level > 0.8:
            reasoning_parts.append(
                f"Advancing in {concept.value.replace('_', ' ')} to maintain momentum"
            )
        else:
            reasoning_parts.append(
                f"Practicing {concept.value.replace('_', ' ')} for skill development"
            )

        # Difficulty reasoning
        if difficulty == DifficultyLevel.TUTORIAL:
            reasoning_parts.append("Starting with tutorial level to build confidence")
        elif difficulty in [DifficultyLevel.EXPERT, DifficultyLevel.LEGENDARY]:
            reasoning_parts.append("Challenging level to push your limits")
        else:
            reasoning_parts.append(
                f"Optimal difficulty level for your current progress"
            )

        # Learning style reasoning
        reasoning_parts.append(
            f"Using {learning_style.value} approach based on your preferences"
        )

        # Performance-based reasoning
        if metrics.success_rate > 0.8:
            reasoning_parts.append(
                "Your strong performance suggests you're ready for this challenge"
            )
        elif metrics.success_rate < 0.5:
            reasoning_parts.append(
                "This will help reinforce concepts you're still mastering"
            )

        return ". ".join(reasoning_parts) + "."


# Example usage and testing
if __name__ == "__main__":
    print("🧪 Testing Adaptive Learning Engine...")

    # Initialize engine
    engine = AdaptiveLearningEngine()

    # Simulate student activities
    student_id = "alice_123"

    # Record various activities
    activities = [
        (ConceptCategory.VECTORS, DifficultyLevel.EASY, True, 120, []),
        (ConceptCategory.VECTORS, DifficultyLevel.EASY, True, 100, []),
        (ConceptCategory.VECTORS, DifficultyLevel.MEDIUM, False, 300, ["sign_error"]),
        (ConceptCategory.MATRICES, DifficultyLevel.EASY, True, 150, []),
        (ConceptCategory.MATRICES, DifficultyLevel.MEDIUM, True, 200, []),
    ]

    for concept, difficulty, success, time_spent, mistakes in activities:
        engine.record_activity(
            student_id,
            "problem_solving",
            concept,
            difficulty,
            success,
            time_spent,
            mistakes,
        )

    # Get learning profile
    profile = engine.get_learning_profile(student_id)
    print(
        f"Student profile - Confidence: {profile.confidence_level:.2f}, Motivation: {profile.motivation_level:.2f}"
    )
    print(f"Skill levels: {profile.skill_levels}")

    # Detect learning style
    learning_styles = engine.detect_learning_style(student_id)
    print(f"Learning styles: {learning_styles}")

    # Get adaptive recommendation
    recommendation = engine.get_adaptive_recommendation(student_id)
    print(f"\n🎯 Recommendation:")
    print(f"Concept: {recommendation.concept_category.value}")
    print(f"Difficulty: {recommendation.difficulty_level.value}")
    print(f"Learning Style: {recommendation.learning_style.value}")
    print(f"Content Type: {recommendation.content_type}")
    print(f"Duration: {recommendation.estimated_duration} minutes")
    print(f"Confidence: {recommendation.confidence_score:.2f}")
    print(f"Reasoning: {recommendation.reasoning}")

    print("\n✅ Adaptive Learning Engine Tests Complete!")
