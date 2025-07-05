#!/usr/bin/env python3
"""
AI Persona Simulation System for Educational Research
=====================================================

This module creates realistic AI student and faculty personas for testing
gamification systems and collecting research-quality data. Designed to
simulate diverse learning styles, neurodivergent learners, different majors,
and various motivation patterns.

Features:
- Neurotypical and neurodivergent learning profiles
- Academic major-specific behaviors
- Realistic interaction patterns
- Data collection for research publication
- Stochastic behavior modeling
"""

import random
import json
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from enum import Enum
import numpy as np


class LearningStyle(Enum):
    """Learning style preferences based on educational research"""

    VISUAL_SPATIAL = "visual_spatial"
    AUDITORY_VERBAL = "auditory_verbal"
    KINESTHETIC_TACTILE = "kinesthetic_tactile"
    READING_WRITING = "reading_writing"
    MULTIMODAL = "multimodal"


class MotivationStyle(Enum):
    """Motivation patterns based on Self-Determination Theory"""

    ACHIEVEMENT_ORIENTED = "achievement_oriented"
    MASTERY_ORIENTED = "mastery_oriented"
    SOCIAL_ORIENTED = "social_oriented"
    AUTONOMY_ORIENTED = "autonomy_oriented"
    COMPETENCE_ORIENTED = "competence_oriented"
    RELATEDNESS_ORIENTED = "relatedness_oriented"


class NeurodivergenceType(Enum):
    """Neurodivergent learning profiles"""

    NEUROTYPICAL = "neurotypical"
    ADHD_INATTENTIVE = "adhd_inattentive"
    ADHD_HYPERACTIVE = "adhd_hyperactive"
    ADHD_COMBINED = "adhd_combined"
    AUTISM_SYSTEMATIC = "autism_systematic"
    AUTISM_SOCIAL = "autism_social"
    DYSLEXIA = "dyslexia"
    DYSCALCULIA = "dyscalculia"
    ANXIETY_DISORDER = "anxiety_disorder"
    DEPRESSION = "depression"


class AcademicMajor(Enum):
    """Academic majors with different math relationships"""

    ENGINEERING = "engineering"
    COMPUTER_SCIENCE = "computer_science"
    MATHEMATICS = "mathematics"
    PHYSICS = "physics"
    PSYCHOLOGY = "psychology"
    BIOLOGY = "biology"
    BUSINESS = "business"
    ART = "art"
    MUSIC = "music"
    LITERATURE = "literature"
    SOCIAL_WORK = "social_work"
    EDUCATION = "education"


@dataclass
class PersonalityProfile:
    """Comprehensive personality profile for AI persona"""

    # Core Traits (Big Five Model)
    openness: float = 0.5  # 0.0 - 1.0
    conscientiousness: float = 0.5  # 0.0 - 1.0
    extraversion: float = 0.5  # 0.0 - 1.0
    agreeableness: float = 0.5  # 0.0 - 1.0
    neuroticism: float = 0.5  # 0.0 - 1.0

    # Academic Traits
    math_anxiety: float = 0.3  # 0.0 - 1.0
    growth_mindset: float = 0.7  # 0.0 - 1.0
    perseverance: float = 0.6  # 0.0 - 1.0
    help_seeking: float = 0.5  # 0.0 - 1.0
    metacognition: float = 0.5  # 0.0 - 1.0

    # Social Traits
    collaboration_preference: float = 0.5  # 0.0 - 1.0
    competition_comfort: float = 0.5  # 0.0 - 1.0
    peer_interaction_desire: float = 0.5  # 0.0 - 1.0


@dataclass
class LearningPreferences:
    """Learning preferences and patterns"""

    primary_learning_style: LearningStyle
    secondary_learning_style: Optional[LearningStyle] = None

    # Engagement Patterns
    optimal_session_length: int = 45  # minutes
    attention_span: int = 20  # minutes
    break_frequency: int = 15  # minutes between breaks

    # Content Preferences
    prefers_visual_aids: bool = True
    prefers_audio_explanations: bool = False
    prefers_hands_on_activities: bool = False
    prefers_text_based_learning: bool = False

    # Feedback Preferences
    immediate_feedback_preference: float = 0.7  # 0.0 - 1.0
    detailed_explanations_preference: float = 0.6
    peer_feedback_comfort: float = 0.5
    public_recognition_comfort: float = 0.4


@dataclass
class GamificationPreferences:
    """Preferences for gamification elements"""

    # Core Mechanics Preference (0.0 - 1.0)
    xp_systems: float = 0.7
    badge_collection: float = 0.6
    leaderboards: float = 0.3
    skill_trees: float = 0.8
    pet_companions: float = 0.5
    guild_systems: float = 0.6

    # Progression Preferences
    prefers_gradual_progression: bool = True
    prefers_challenge_difficulty: float = 0.6  # 0.0 - 1.0
    achievement_celebration_preference: float = 0.5

    # Social Gamification
    collaboration_over_competition: bool = True
    public_progress_sharing: bool = False
    peer_comparison_comfort: float = 0.3


@dataclass
class AIStudentPersona:
    """Complete AI student persona for simulation"""

    # Identity
    persona_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    academic_major: AcademicMajor = AcademicMajor.PSYCHOLOGY
    year_in_school: int = 2  # 1-4
    age: int = 20

    # Neurodiversity
    neurodivergence: NeurodivergenceType = NeurodivergenceType.NEUROTYPICAL
    accommodations_needed: List[str] = field(default_factory=list)

    # Core Profiles
    personality: PersonalityProfile = field(default_factory=PersonalityProfile)
    learning_preferences: LearningPreferences = field(
        default_factory=LearningPreferences
    )
    gamification_preferences: GamificationPreferences = field(
        default_factory=GamificationPreferences
    )
    motivation_style: MotivationStyle = MotivationStyle.MASTERY_ORIENTED

    # Academic Performance Patterns
    baseline_performance: float = 0.75  # 0.0 - 1.0
    performance_variability: float = 0.15  # Standard deviation
    improvement_rate: float = 0.05  # Per week

    # Behavioral Patterns
    procrastination_tendency: float = 0.3  # 0.0 - 1.0
    help_seeking_threshold: float = 0.6  # Difficulty level that triggers help-seeking
    dropout_risk: float = 0.1  # 0.0 - 1.0

    # Simulation State
    current_engagement: float = 0.7
    current_motivation: float = 0.6
    current_stress_level: float = 0.3
    session_count: int = 0
    total_time_engaged: int = 0  # minutes

    def generate_session_behavior(self) -> Dict[str, Any]:
        """Generate realistic behavior for a learning session"""

        # Factor in personality and current state
        base_engagement = self.current_engagement
        stress_factor = 1.0 - (self.current_stress_level * 0.3)
        motivation_factor = 0.5 + (self.current_motivation * 0.5)

        # Calculate session characteristics
        session_length = max(
            5,
            int(
                self.learning_preferences.optimal_session_length
                * stress_factor
                * motivation_factor
                + random.gauss(0, 10)
            ),
        )

        # Activity participation based on personality
        activities_completed = []
        if random.random() < base_engagement * motivation_factor:
            activities_completed.append("reading")
        if random.random() < base_engagement * 0.8:
            activities_completed.append("practice_problems")
        if random.random() < self.personality.collaboration_preference:
            activities_completed.append("discussion_participation")
        if random.random() < 0.3 + (self.personality.openness * 0.4):
            activities_completed.append("exploration")

        # Help-seeking behavior
        help_sought = False
        if random.random() < self.personality.help_seeking:
            help_sought = True

        # Performance modeling
        base_score = self.baseline_performance
        stress_impact = -self.current_stress_level * 0.2
        engagement_impact = (self.current_engagement - 0.5) * 0.3
        random_variation = random.gauss(0, self.performance_variability)

        performance_score = max(
            0.0,
            min(1.0, base_score + stress_impact + engagement_impact + random_variation),
        )

        # Update state for next session
        self.session_count += 1
        self.total_time_engaged += session_length

        # Gradual improvement over time
        self.baseline_performance += self.improvement_rate / 10

        # Engagement and motivation dynamics
        if performance_score > 0.8:
            self.current_motivation += 0.05
        elif performance_score < 0.6:
            self.current_motivation -= 0.03
            self.current_stress_level += 0.02

        # Bound values
        self.current_motivation = max(0.0, min(1.0, self.current_motivation))
        self.current_stress_level = max(0.0, min(1.0, self.current_stress_level))
        self.current_engagement = max(0.0, min(1.0, self.current_engagement))

        return {
            "session_id": str(uuid.uuid4()),
            "persona_id": self.persona_id,
            "timestamp": datetime.now().isoformat(),
            "session_length_minutes": session_length,
            "activities_completed": activities_completed,
            "help_sought": help_sought,
            "performance_score": round(performance_score, 3),
            "engagement_level": round(self.current_engagement, 3),
            "motivation_level": round(self.current_motivation, 3),
            "stress_level": round(self.current_stress_level, 3),
            "gamification_interactions": self._generate_gamification_interactions(),
        }

    def _generate_gamification_interactions(self) -> Dict[str, Any]:
        """Generate interactions with gamification elements"""
        interactions = {}

        # XP system interaction
        if random.random() < self.gamification_preferences.xp_systems:
            interactions["checked_xp_progress"] = True

        # Badge system interaction
        if random.random() < self.gamification_preferences.badge_collection:
            interactions["viewed_badges"] = True

        # Skill tree interaction
        if random.random() < self.gamification_preferences.skill_trees:
            interactions["explored_skill_tree"] = True

        # Pet companion interaction
        if random.random() < self.gamification_preferences.pet_companions:
            interactions["interacted_with_pet"] = True

        # Guild interaction
        if (
            random.random() < self.gamification_preferences.guild_systems
            and self.personality.collaboration_preference > 0.5
        ):
            interactions["guild_participation"] = True

        return interactions


class AIPersonaGenerator:
    """Factory for generating diverse AI personas"""

    def __init__(self):
        self.generated_personas = []

    def generate_neurodivergent_personas(
        self, count: int = 10
    ) -> List[AIStudentPersona]:
        """Generate personas representing neurodivergent learners"""
        personas = []

        # ADHD personas
        for _ in range(count // 5):
            persona = self._create_adhd_persona()
            personas.append(persona)

        # Autism personas
        for _ in range(count // 5):
            persona = self._create_autism_persona()
            personas.append(persona)

        # Dyslexia personas
        for _ in range(count // 5):
            persona = self._create_dyslexia_persona()
            personas.append(persona)

        # Anxiety/Depression personas
        for _ in range(count // 5):
            persona = self._create_anxiety_persona()
            personas.append(persona)

        # Fill remaining with diverse profiles
        while len(personas) < count:
            persona = self._create_random_neurodivergent_persona()
            personas.append(persona)

        return personas

    def generate_academic_major_personas(
        self, count: int = 12
    ) -> List[AIStudentPersona]:
        """Generate personas representing different academic majors"""
        personas = []
        majors = list(AcademicMajor)

        for i in range(count):
            major = majors[i % len(majors)]
            persona = self._create_major_specific_persona(major)
            personas.append(persona)

        return personas

    def generate_motivation_style_personas(
        self, count: int = 6
    ) -> List[AIStudentPersona]:
        """Generate personas representing different motivation styles"""
        personas = []
        motivation_styles = list(MotivationStyle)

        for i in range(count):
            style = motivation_styles[i % len(motivation_styles)]
            persona = self._create_motivation_specific_persona(style)
            personas.append(persona)

        return personas

    def _create_adhd_persona(self) -> AIStudentPersona:
        """Create ADHD-specific persona"""
        persona = AIStudentPersona()
        persona.neurodivergence = random.choice(
            [
                NeurodivergenceType.ADHD_INATTENTIVE,
                NeurodivergenceType.ADHD_HYPERACTIVE,
                NeurodivergenceType.ADHD_COMBINED,
            ]
        )

        # ADHD characteristics
        persona.personality.conscientiousness = random.uniform(0.2, 0.6)
        persona.personality.neuroticism = random.uniform(0.4, 0.8)
        persona.learning_preferences.attention_span = random.randint(5, 15)
        persona.learning_preferences.break_frequency = random.randint(5, 10)
        persona.procrastination_tendency = random.uniform(0.4, 0.8)

        # Gamification preferences
        persona.gamification_preferences.xp_systems = random.uniform(0.6, 0.9)
        persona.gamification_preferences.immediate_feedback_preference = random.uniform(
            0.7, 1.0
        )

        # Accommodations
        persona.accommodations_needed = [
            "extended_time",
            "frequent_breaks",
            "minimal_distractions",
            "clear_instructions",
        ]

        return persona

    def _create_autism_persona(self) -> AIStudentPersona:
        """Create autism-specific persona"""
        persona = AIStudentPersona()
        persona.neurodivergence = random.choice(
            [NeurodivergenceType.AUTISM_SYSTEMATIC, NeurodivergenceType.AUTISM_SOCIAL]
        )

        # Autism characteristics
        persona.personality.openness = random.uniform(0.3, 0.7)
        persona.personality.conscientiousness = random.uniform(0.6, 0.9)
        persona.personality.extraversion = random.uniform(0.1, 0.4)
        persona.learning_preferences.prefers_visual_aids = True
        persona.learning_preferences.optimal_session_length = random.randint(30, 90)

        # Social preferences
        persona.gamification_preferences.guild_systems = random.uniform(0.1, 0.4)
        persona.gamification_preferences.public_progress_sharing = False
        persona.personality.collaboration_preference = random.uniform(0.1, 0.4)

        # Systematic learning preference
        persona.gamification_preferences.skill_trees = random.uniform(0.8, 1.0)
        persona.learning_preferences.detailed_explanations_preference = random.uniform(
            0.7, 1.0
        )

        return persona

    def _create_dyslexia_persona(self) -> AIStudentPersona:
        """Create dyslexia-specific persona"""
        persona = AIStudentPersona()
        persona.neurodivergence = NeurodivergenceType.DYSLEXIA

        # Dyslexia characteristics
        persona.learning_preferences.primary_learning_style = (
            LearningStyle.AUDITORY_VERBAL
        )
        persona.learning_preferences.prefers_audio_explanations = True
        persona.learning_preferences.prefers_text_based_learning = False

        # Strengths and challenges
        persona.personality.perseverance = random.uniform(0.6, 0.9)
        persona.baseline_performance = random.uniform(0.6, 0.8)
        persona.help_seeking_threshold = random.uniform(0.3, 0.6)

        # Accommodations
        persona.accommodations_needed = [
            "audio_content",
            "text_to_speech",
            "visual_supports",
            "alternative_formats",
        ]

        return persona

    def _create_anxiety_persona(self) -> AIStudentPersona:
        """Create anxiety/depression-specific persona"""
        persona = AIStudentPersona()
        persona.neurodivergence = random.choice(
            [NeurodivergenceType.ANXIETY_DISORDER, NeurodivergenceType.DEPRESSION]
        )

        # Mental health characteristics
        persona.personality.neuroticism = random.uniform(0.6, 0.9)
        persona.math_anxiety = random.uniform(0.5, 0.9)
        persona.current_stress_level = random.uniform(0.4, 0.8)
        persona.current_motivation = random.uniform(0.2, 0.6)

        # Gamification preferences
        persona.gamification_preferences.leaderboards = random.uniform(0.0, 0.3)
        persona.gamification_preferences.public_progress_sharing = False
        persona.gamification_preferences.achievement_celebration_preference = (
            random.uniform(0.2, 0.7)
        )

        return persona

    def _create_major_specific_persona(self, major: AcademicMajor) -> AIStudentPersona:
        """Create persona based on academic major"""
        persona = AIStudentPersona()
        persona.academic_major = major

        if major in [
            AcademicMajor.ENGINEERING,
            AcademicMajor.COMPUTER_SCIENCE,
            AcademicMajor.PHYSICS,
        ]:
            # STEM majors
            persona.personality.math_anxiety = random.uniform(0.1, 0.4)
            persona.baseline_performance = random.uniform(0.7, 0.9)
            persona.gamification_preferences.skill_trees = random.uniform(0.7, 0.9)

        elif major in [
            AcademicMajor.ART,
            AcademicMajor.MUSIC,
            AcademicMajor.LITERATURE,
        ]:
            # Creative majors
            persona.personality.math_anxiety = random.uniform(0.4, 0.8)
            persona.learning_preferences.primary_learning_style = (
                LearningStyle.VISUAL_SPATIAL
            )
            persona.gamification_preferences.pet_companions = random.uniform(0.6, 0.9)

        elif major in [
            AcademicMajor.PSYCHOLOGY,
            AcademicMajor.SOCIAL_WORK,
            AcademicMajor.EDUCATION,
        ]:
            # Social sciences
            persona.personality.agreeableness = random.uniform(0.6, 0.9)
            persona.personality.collaboration_preference = random.uniform(0.6, 0.9)
            persona.gamification_preferences.guild_systems = random.uniform(0.6, 0.9)

        return persona

    def _create_motivation_specific_persona(
        self, motivation: MotivationStyle
    ) -> AIStudentPersona:
        """Create persona based on motivation style"""
        persona = AIStudentPersona()
        persona.motivation_style = motivation

        if motivation == MotivationStyle.ACHIEVEMENT_ORIENTED:
            persona.gamification_preferences.leaderboards = random.uniform(0.6, 0.9)
            persona.gamification_preferences.badge_collection = random.uniform(0.7, 1.0)
            persona.personality.competition_comfort = random.uniform(0.6, 0.9)

        elif motivation == MotivationStyle.MASTERY_ORIENTED:
            persona.gamification_preferences.skill_trees = random.uniform(0.8, 1.0)
            persona.learning_preferences.detailed_explanations_preference = (
                random.uniform(0.7, 1.0)
            )
            persona.personality.perseverance = random.uniform(0.7, 0.9)

        elif motivation == MotivationStyle.SOCIAL_ORIENTED:
            persona.gamification_preferences.guild_systems = random.uniform(0.7, 1.0)
            persona.personality.collaboration_preference = random.uniform(0.7, 1.0)
            persona.learning_preferences.peer_feedback_comfort = random.uniform(
                0.6, 0.9
            )

        return persona

    def _create_random_neurodivergent_persona(self) -> AIStudentPersona:
        """Create a random neurodivergent persona"""
        neurodivergence_types = [
            t for t in NeurodivergenceType if t != NeurodivergenceType.NEUROTYPICAL
        ]
        selected_type = random.choice(neurodivergence_types)

        if "adhd" in selected_type.value:
            return self._create_adhd_persona()
        elif "autism" in selected_type.value:
            return self._create_autism_persona()
        elif selected_type == NeurodivergenceType.DYSLEXIA:
            return self._create_dyslexia_persona()
        else:
            return self._create_anxiety_persona()


# Example usage and testing
if __name__ == "__main__":
    generator = AIPersonaGenerator()

    print("🧠 AI Persona Simulation System")
    print("=" * 50)

    # Generate diverse personas
    neurodivergent_personas = generator.generate_neurodivergent_personas(5)
    major_personas = generator.generate_academic_major_personas(6)
    motivation_personas = generator.generate_motivation_style_personas(6)

    all_personas = neurodivergent_personas + major_personas + motivation_personas

    print(f"\nGenerated {len(all_personas)} AI student personas:")
    print(f"- {len(neurodivergent_personas)} neurodivergent learners")
    print(f"- {len(major_personas)} major-specific profiles")
    print(f"- {len(motivation_personas)} motivation-style profiles")

    # Simulate sessions for research data
    print("\n📊 Simulating Learning Sessions...")
    session_data = []

    for persona in all_personas[:3]:  # Sample 3 personas
        print(
            f"\nPersona: {persona.academic_major.value} | {persona.neurodivergence.value}"
        )

        # Simulate 5 sessions per persona
        for session_num in range(5):
            session = persona.generate_session_behavior()
            session_data.append(session)

            print(
                f"  Session {session_num + 1}: "
                f"{session['session_length_minutes']}min, "
                f"Performance: {session['performance_score']:.2f}, "
                f"Activities: {len(session['activities_completed'])}"
            )

    # Save research data
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"ai_persona_simulation_data_{timestamp}.json"

    research_data = {
        "metadata": {
            "generated_at": datetime.now().isoformat(),
            "total_personas": len(all_personas),
            "total_sessions": len(session_data),
            "simulation_version": "1.0",
        },
        "personas": [
            {
                "persona_id": p.persona_id,
                "academic_major": p.academic_major.value,
                "neurodivergence": p.neurodivergence.value,
                "motivation_style": p.motivation_style.value,
                "baseline_performance": p.baseline_performance,
                "math_anxiety": p.personality.math_anxiety,
            }
            for p in all_personas
        ],
        "session_data": session_data,
    }

    with open(filename, "w") as f:
        json.dump(research_data, f, indent=2)

    print(f"\n✅ Research data saved to: {filename}")
    print(f"📈 Ready for academic publication analysis!")

    # Summary statistics
    performance_scores = [s["performance_score"] for s in session_data]
    engagement_levels = [s["engagement_level"] for s in session_data]

    print(f"\n📊 Simulation Summary:")
    print(
        f"Average Performance: {np.mean(performance_scores):.3f} ± {np.std(performance_scores):.3f}"
    )
    print(
        f"Average Engagement: {np.mean(engagement_levels):.3f} ± {np.std(engagement_levels):.3f}"
    )
    print(
        f"Help-Seeking Rate: {sum(1 for s in session_data if s['help_sought']) / len(session_data):.3f}"
    )
