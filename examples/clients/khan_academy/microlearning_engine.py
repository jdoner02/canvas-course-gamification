"""
Khan Academy Linear Algebra - Microlearning Implementation
Mastery-based learning with adaptive assessment and global accessibility
"""

from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from enum import Enum
import json
import time
from datetime import datetime, timedelta
import random


class MasteryLevel(Enum):
    NOT_STARTED = "not_started"
    ATTEMPTED = "attempted"
    PRACTICED = "practiced"
    MASTERED = "mastered"
    REVIEWING = "reviewing"


class DifficultyLevel(Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"
    CHALLENGE = "challenge"


@dataclass
class MicroModule:
    """A single microlearning module (3-5 minutes)"""

    module_id: str
    title: str
    description: str
    learning_objectives: List[str]
    prerequisites: List[str] = field(default_factory=list)
    estimated_time: int = 300  # seconds
    difficulty: DifficultyLevel = DifficultyLevel.MEDIUM
    content_types: List[str] = field(default_factory=list)  # video, practice, explanation
    assessment_questions: List[Dict[str, Any]] = field(default_factory=list)
    hint_progression: List[str] = field(default_factory=list)
    mastery_threshold: float = 0.95
    spaced_repetition_intervals: List[int] = field(default_factory=lambda: [1, 3, 7, 14, 30])


@dataclass
class StudentProgress:
    """Tracks individual student progress"""

    student_id: str
    module_progress: Dict[str, MasteryLevel] = field(default_factory=dict)
    attempt_history: Dict[str, List[Dict[str, Any]]] = field(default_factory=dict)
    streak_days: int = 0
    energy_points: int = 0
    badges_earned: List[str] = field(default_factory=list)
    last_activity: Optional[datetime] = None
    learning_preferences: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AssessmentResult:
    """Result of a module assessment"""

    module_id: str
    student_id: str
    score: float
    time_taken: int
    hints_used: int
    mistakes_made: List[Dict[str, Any]]
    timestamp: datetime = field(default_factory=datetime.now)


class KhanAcademyLinearAlgebra:
    """
    Khan Academy-style microlearning platform for Linear Algebra
    Features mastery-based progression with adaptive assessment
    """

    def __init__(self):
        self.modules = self._initialize_modules()
        self.student_progress: Dict[str, StudentProgress] = {}
        self.assessment_engine = AdaptiveAssessmentEngine()
        self.spaced_repetition = SpacedRepetitionSystem()
        self.gamification = GamificationEngine()

    def _initialize_modules(self) -> Dict[str, MicroModule]:
        """Initialize the complete microlearning curriculum"""
        modules = {}

        # Level 1: Vector Fundamentals
        modules["vec_intro"] = MicroModule(
            module_id="vec_intro",
            title="What is a Vector?",
            description="Introduction to vectors as quantities with magnitude and direction",
            learning_objectives=[
                "Define a vector",
                "Distinguish between scalars and vectors",
                "Represent vectors graphically"
            ],
            estimated_time=180,
            difficulty=DifficultyLevel.EASY,
            content_types=["video", "practice", "explanation"],
            assessment_questions=[
                {
                    "type": "multiple_choice",
                    "question": "Which of the following is a vector quantity?",
                    "options": ["Speed", "Velocity", "Temperature", "Mass"],
                    "correct": 1,
                    "explanation": "Velocity has both magnitude and direction, making it a vector."
                },
                {
                    "type": "drag_drop",
                    "question": "Drag the arrow to represent the vector (3, 4)",
                    "interactive": True
                }
            ],
            hint_progression=[
                "Think about quantities that have both size and direction",
                "Consider the difference between speed and velocity",
                "Velocity includes both how fast and which direction"
            ]
        )

        modules["vec_notation"] = MicroModule(
            module_id="vec_notation",
            title="Vector Notation",
            description="Different ways to write and represent vectors",
            learning_objectives=[
                "Use component notation for vectors",
                "Convert between geometric and algebraic representations",
                "Apply proper vector notation"
            ],
            prerequisites=["vec_intro"],
            estimated_time=240,
            assessment_questions=[
                {
                    "type": "fill_blank",
                    "question": "The vector from origin to point (5, -2) is written as ____",
                    "correct": ["⟨5, -2⟩", "<5, -2>", "(5, -2)"],
                    "explanation": "Vector component notation shows the x and y components."
                }
            ]
        )

        # Level 2: Vector Operations
        modules["vec_addition"] = MicroModule(
            module_id="vec_addition",
            title="Vector Addition",
            description="Adding vectors using tip-to-tail method and components",
            learning_objectives=[
                "Add vectors graphically",
                "Add vectors using components",
                "Apply commutative property of vector addition"
            ],
            prerequisites=["vec_notation"],
            estimated_time=300,
            assessment_questions=[
                {
                    "type": "computation",
                    "question": "Find ⟨3, 2⟩ + ⟨1, 4⟩",
                    "correct": [4, 6],
                    "steps": ["Add x-components: 3 + 1 = 4", "Add y-components: 2 + 4 = 6"]
                }
            ]
        )

        modules["scalar_mult"] = MicroModule(
            module_id="scalar_mult",
            title="Scalar Multiplication",
            description="Multiplying vectors by scalars",
            learning_objectives=[
                "Multiply vectors by positive scalars",
                "Understand effect of negative scalars",
                "Apply scalar multiplication to vector addition"
            ],
            prerequisites=["vec_addition"],
            estimated_time=270
        )

        # Level 3: Advanced Vector Concepts
        modules["dot_product"] = MicroModule(
            module_id="dot_product",
            title="Dot Product",
            description="Computing and interpreting the dot product",
            learning_objectives=[
                "Calculate dot product using components",
                "Understand geometric interpretation",
                "Apply dot product to find angles"
            ],
            prerequisites=["scalar_mult"],
            estimated_time=360,
            difficulty=DifficultyLevel.MEDIUM
        )

        # Level 4: Linear Systems Foundation
        modules["linear_eq_intro"] = MicroModule(
            module_id="linear_eq_intro",
            title="Linear Equations Review",
            description="Quick review of linear equations in preparation for systems",
            learning_objectives=[
                "Solve single linear equations",
                "Graph linear equations",
                "Understand slope and intercepts"
            ],
            estimated_time=240,
            difficulty=DifficultyLevel.EASY
        )

        modules["systems_2x2"] = MicroModule(
            module_id="systems_2x2",
            title="2×2 Linear Systems",
            description="Solving systems of two linear equations",
            learning_objectives=[
                "Solve by substitution",
                "Solve by elimination",
                "Interpret solutions graphically"
            ],
            prerequisites=["linear_eq_intro"],
            estimated_time=420,
            difficulty=DifficultyLevel.MEDIUM
        )

        # Level 5: Matrix Fundamentals
        modules["matrix_intro"] = MicroModule(
            module_id="matrix_intro",
            title="Introduction to Matrices",
            description="What matrices are and basic terminology",
            learning_objectives=[
                "Define matrix terminology",
                "Identify matrix dimensions",
                "Access matrix entries"
            ],
            prerequisites=["systems_2x2"],
            estimated_time=300
        )

        modules["matrix_ops"] = MicroModule(
            module_id="matrix_ops",
            title="Matrix Operations",
            description="Adding, subtracting, and multiplying matrices",
            learning_objectives=[
                "Add and subtract matrices",
                "Multiply matrices",
                "Understand matrix multiplication is not commutative"
            ],
            prerequisites=["matrix_intro"],
            estimated_time=480,
            difficulty=DifficultyLevel.MEDIUM
        )

        return modules

    def enroll_student(self, student_id: str, learning_preferences: Dict[str, Any] = None):
        """Enroll a new student in the program"""
        if learning_preferences is None:
            learning_preferences = {}

        self.student_progress[student_id] = StudentProgress(
            student_id=student_id,
            learning_preferences=learning_preferences
        )

        # Run initial diagnostic
        self._run_diagnostic_assessment(student_id)

    def _run_diagnostic_assessment(self, student_id: str):
        """Determine student's starting point through diagnostic questions"""
        # Simplified diagnostic - in practice would be more comprehensive
        diagnostic_results = {
            "basic_algebra": 0.85,
            "coordinate_geometry": 0.75,
            "graphing": 0.90
        }

        # Set initial module access based on diagnostic
        progress = self.student_progress[student_id]
        if diagnostic_results["basic_algebra"] >= 0.8:
            progress.module_progress["vec_intro"] = MasteryLevel.NOT_STARTED
        else:
            # Would assign prerequisite modules
            pass

    def get_next_recommendation(self, student_id: str) -> Optional[str]:
        """Get the next recommended module for a student"""
        progress = self.student_progress.get(student_id)
        if not progress:
            return None

        # Find available modules (prerequisites met, not mastered)
        available_modules = []
        
        for module_id, module in self.modules.items():
            # Check if prerequisites are met
            prerequisites_met = all(
                progress.module_progress.get(prereq) == MasteryLevel.MASTERED
                for prereq in module.prerequisites
            )
            
            # Check if not already mastered
            current_level = progress.module_progress.get(module_id, MasteryLevel.NOT_STARTED)
            
            if prerequisites_met and current_level != MasteryLevel.MASTERED:
                available_modules.append(module_id)

        if not available_modules:
            # Check for spaced repetition candidates
            return self.spaced_repetition.get_review_candidate(student_id, progress)

        # Prioritize based on learning path and difficulty
        return self._prioritize_modules(available_modules, progress)

    def _prioritize_modules(self, available_modules: List[str], progress: StudentProgress) -> str:
        """Prioritize which module to recommend next"""
        # Simple prioritization - could be much more sophisticated
        
        # Prefer modules with no attempts (new content)
        new_modules = [
            mid for mid in available_modules 
            if progress.module_progress.get(mid, MasteryLevel.NOT_STARTED) == MasteryLevel.NOT_STARTED
        ]
        
        if new_modules:
            return new_modules[0]
        
        # Otherwise, modules that need more practice
        return available_modules[0]

    def attempt_module(self, student_id: str, module_id: str) -> Dict[str, Any]:
        """Student attempts a module - returns results and feedback"""
        module = self.modules.get(module_id)
        progress = self.student_progress.get(student_id)
        
        if not module or not progress:
            return {"error": "Invalid module or student"}

        # Generate adaptive assessment
        assessment = self.assessment_engine.generate_assessment(
            module, progress.module_progress.get(module_id, MasteryLevel.NOT_STARTED)
        )

        # Simulate student performance (in real system, would collect answers)
        simulated_result = self._simulate_student_performance(student_id, module_id, assessment)

        # Process results
        result = self._process_assessment_result(student_id, module_id, simulated_result)

        # Update progress
        self._update_progress(student_id, module_id, result)

        # Award points and check badges
        points_earned = self.gamification.calculate_points(result)
        progress.energy_points += points_earned

        new_badges = self.gamification.check_badge_eligibility(student_id, progress)
        progress.badges_earned.extend(new_badges)

        return {
            "result": result,
            "points_earned": points_earned,
            "new_badges": new_badges,
            "next_recommendation": self.get_next_recommendation(student_id)
        }

    def _simulate_student_performance(self, student_id: str, module_id: str, assessment: Dict[str, Any]) -> AssessmentResult:
        """Simulate student performance for demonstration"""
        # This would be replaced with actual student responses
        base_ability = 0.7 + random.uniform(-0.2, 0.2)
        
        # Adjust for module difficulty
        module = self.modules[module_id]
        difficulty_adjustment = {
            DifficultyLevel.EASY: 0.1,
            DifficultyLevel.MEDIUM: 0.0,
            DifficultyLevel.HARD: -0.1,
            DifficultyLevel.CHALLENGE: -0.2
        }
        
        adjusted_ability = base_ability + difficulty_adjustment[module.difficulty]
        score = max(0.0, min(1.0, adjusted_ability + random.uniform(-0.1, 0.1)))
        
        return AssessmentResult(
            module_id=module_id,
            student_id=student_id,
            score=score,
            time_taken=int(module.estimated_time * (1.5 - score * 0.5)),  # Faster if better
            hints_used=max(0, int((1 - score) * 3)),  # More hints if struggling
            mistakes_made=[]  # Would track specific error patterns
        )

    def _process_assessment_result(self, student_id: str, module_id: str, result: AssessmentResult) -> Dict[str, Any]:
        """Process assessment result and determine next steps"""
        module = self.modules[module_id]
        
        passed_mastery = result.score >= module.mastery_threshold
        
        feedback = {
            "score": result.score,
            "passed_mastery": passed_mastery,
            "time_taken": result.time_taken,
            "hints_used": result.hints_used,
            "feedback_message": self._generate_feedback_message(result, passed_mastery),
            "next_action": "advance" if passed_mastery else "retry"
        }
        
        if not passed_mastery:
            feedback["remediation_suggestions"] = self._get_remediation_suggestions(module_id, result)
        
        return feedback

    def _generate_feedback_message(self, result: AssessmentResult, passed_mastery: bool) -> str:
        """Generate encouraging feedback message"""
        if passed_mastery:
            if result.score >= 0.98:
                return "🌟 Perfect! You've completely mastered this concept!"
            elif result.score >= 0.95:
                return "🎉 Excellent work! You've achieved mastery!"
            else:
                return "✅ Great job! You've demonstrated mastery of this topic."
        else:
            if result.score >= 0.8:
                return "💪 You're very close! Just a bit more practice and you'll have it."
            elif result.score >= 0.6:
                return "📚 Good effort! Let's review a few key concepts and try again."
            else:
                return "🤔 Let's break this down step by step. You've got this!"

    def _get_remediation_suggestions(self, module_id: str, result: AssessmentResult) -> List[str]:
        """Suggest specific remediation based on performance"""
        suggestions = []
        
        if result.hints_used > 2:
            suggestions.append("Review the concept explanation video")
        
        if result.score < 0.6:
            suggestions.append("Try the prerequisite modules again")
            suggestions.append("Use the step-by-step practice tool")
        
        suggestions.append("Ask for help in the discussion forums")
        
        return suggestions

    def _update_progress(self, student_id: str, module_id: str, result: Dict[str, Any]):
        """Update student progress based on assessment result"""
        progress = self.student_progress[student_id]
        
        if result["passed_mastery"]:
            progress.module_progress[module_id] = MasteryLevel.MASTERED
            # Schedule for spaced repetition
            self.spaced_repetition.schedule_review(student_id, module_id)
        else:
            current_level = progress.module_progress.get(module_id, MasteryLevel.NOT_STARTED)
            if current_level == MasteryLevel.NOT_STARTED:
                progress.module_progress[module_id] = MasteryLevel.ATTEMPTED
            else:
                progress.module_progress[module_id] = MasteryLevel.PRACTICED

        # Record attempt
        if module_id not in progress.attempt_history:
            progress.attempt_history[module_id] = []
        
        progress.attempt_history[module_id].append({
            "timestamp": datetime.now().isoformat(),
            "score": result["score"],
            "time_taken": result["time_taken"]
        })
        
        progress.last_activity = datetime.now()

    def get_student_dashboard(self, student_id: str) -> Dict[str, Any]:
        """Get comprehensive student dashboard data"""
        progress = self.student_progress.get(student_id)
        if not progress:
            return {"error": "Student not found"}

        # Calculate statistics
        total_modules = len(self.modules)
        mastered_modules = sum(1 for level in progress.module_progress.values() 
                             if level == MasteryLevel.MASTERED)
        
        # Get learning path progress
        learning_path = self._generate_learning_path_visualization(student_id)
        
        # Recent activity
        recent_activity = self._get_recent_activity(student_id)
        
        return {
            "student_id": student_id,
            "overall_progress": mastered_modules / total_modules if total_modules > 0 else 0,
            "mastered_modules": mastered_modules,
            "total_modules": total_modules,
            "energy_points": progress.energy_points,
            "streak_days": progress.streak_days,
            "badges": progress.badges_earned,
            "learning_path": learning_path,
            "recent_activity": recent_activity,
            "next_recommendation": self.get_next_recommendation(student_id)
        }

    def _generate_learning_path_visualization(self, student_id: str) -> Dict[str, Any]:
        """Generate visual learning path showing progress"""
        progress = self.student_progress[student_id]
        path_data = {
            "levels": [],
            "current_position": None
        }
        
        # Organize modules by conceptual levels
        levels = [
            {"name": "Vector Fundamentals", "modules": ["vec_intro", "vec_notation"]},
            {"name": "Vector Operations", "modules": ["vec_addition", "scalar_mult"]},
            {"name": "Advanced Vectors", "modules": ["dot_product"]},
            {"name": "Linear Systems", "modules": ["linear_eq_intro", "systems_2x2"]},
            {"name": "Matrix Basics", "modules": ["matrix_intro", "matrix_ops"]}
        ]
        
        for level in levels:
            level_data = {
                "name": level["name"],
                "modules": [],
                "completion_rate": 0
            }
            
            completed = 0
            for module_id in level["modules"]:
                if module_id in self.modules:
                    module_status = progress.module_progress.get(module_id, MasteryLevel.NOT_STARTED)
                    level_data["modules"].append({
                        "id": module_id,
                        "title": self.modules[module_id].title,
                        "status": module_status.value,
                        "available": self._is_module_available(student_id, module_id)
                    })
                    
                    if module_status == MasteryLevel.MASTERED:
                        completed += 1
            
            level_data["completion_rate"] = completed / len(level["modules"]) if level["modules"] else 0
            path_data["levels"].append(level_data)
        
        return path_data

    def _is_module_available(self, student_id: str, module_id: str) -> bool:
        """Check if module is available to student"""
        module = self.modules.get(module_id)
        if not module:
            return False
            
        progress = self.student_progress[student_id]
        
        # Check prerequisites
        return all(
            progress.module_progress.get(prereq) == MasteryLevel.MASTERED
            for prereq in module.prerequisites
        )

    def _get_recent_activity(self, student_id: str) -> List[Dict[str, Any]]:
        """Get recent learning activity for dashboard"""
        progress = self.student_progress[student_id]
        activities = []
        
        for module_id, attempts in progress.attempt_history.items():
            if attempts:
                latest_attempt = attempts[-1]
                activities.append({
                    "module_id": module_id,
                    "module_title": self.modules[module_id].title,
                    "timestamp": latest_attempt["timestamp"],
                    "score": latest_attempt["score"],
                    "activity_type": "practice"
                })
        
        # Sort by timestamp, most recent first
        activities.sort(key=lambda x: x["timestamp"], reverse=True)
        return activities[:10]  # Return last 10 activities


class AdaptiveAssessmentEngine:
    """Generates adaptive assessments based on student performance"""
    
    def generate_assessment(self, module: MicroModule, current_level: MasteryLevel) -> Dict[str, Any]:
        """Generate assessment adapted to student's current level"""
        # Adjust difficulty based on current mastery level
        if current_level == MasteryLevel.NOT_STARTED:
            difficulty_multiplier = 0.8  # Start easier
        elif current_level == MasteryLevel.ATTEMPTED:
            difficulty_multiplier = 1.0  # Standard difficulty
        else:  # PRACTICED
            difficulty_multiplier = 1.1  # Slightly harder
        
        # Select questions (simplified - would use item response theory)
        questions = module.assessment_questions.copy()
        
        return {
            "module_id": module.module_id,
            "questions": questions,
            "difficulty_multiplier": difficulty_multiplier,
            "hints_available": module.hint_progression
        }


class SpacedRepetitionSystem:
    """Manages spaced repetition for knowledge retention"""
    
    def __init__(self):
        self.review_schedule: Dict[str, Dict[str, datetime]] = {}
    
    def schedule_review(self, student_id: str, module_id: str):
        """Schedule future review sessions"""
        if student_id not in self.review_schedule:
            self.review_schedule[student_id] = {}
        
        # Schedule next review in 1 day, then 3, 7, 14, 30 days
        next_review = datetime.now() + timedelta(days=1)
        self.review_schedule[student_id][module_id] = next_review
    
    def get_review_candidate(self, student_id: str, progress: StudentProgress) -> Optional[str]:
        """Get module that needs review"""
        if student_id not in self.review_schedule:
            return None
        
        now = datetime.now()
        for module_id, review_time in self.review_schedule[student_id].items():
            if now >= review_time:
                return module_id
        
        return None


class GamificationEngine:
    """Handles points, badges, and other gamification elements"""
    
    def calculate_points(self, assessment_result: Dict[str, Any]) -> int:
        """Calculate energy points earned"""
        base_points = 100
        score_multiplier = assessment_result["score"]
        speed_bonus = max(0, 50 - assessment_result.get("time_taken", 300) // 10)
        hint_penalty = assessment_result.get("hints_used", 0) * 5
        
        points = int(base_points * score_multiplier + speed_bonus - hint_penalty)
        return max(10, points)  # Minimum 10 points
    
    def check_badge_eligibility(self, student_id: str, progress: StudentProgress) -> List[str]:
        """Check for new badge achievements"""
        new_badges = []
        
        mastered_count = sum(1 for level in progress.module_progress.values() 
                           if level == MasteryLevel.MASTERED)
        
        # Achievement badges
        if mastered_count >= 5 and "vector_master" not in progress.badges_earned:
            new_badges.append("vector_master")
        
        if progress.energy_points >= 1000 and "energy_collector" not in progress.badges_earned:
            new_badges.append("energy_collector")
        
        if progress.streak_days >= 7 and "week_warrior" not in progress.badges_earned:
            new_badges.append("week_warrior")
        
        return new_badges


# Example usage and testing
if __name__ == "__main__":
    print("📚 Khan Academy Linear Algebra - Microlearning System")
    print("=" * 60)
    
    # Initialize system
    khan_academy = KhanAcademyLinearAlgebra()
    
    # Enroll test students
    test_students = ["student_001", "student_002", "student_003"]
    
    for student_id in test_students:
        khan_academy.enroll_student(student_id, {
            "learning_style": "visual",
            "pace_preference": "self_paced"
        })
        print(f"✅ Enrolled {student_id}")
    
    # Simulate learning sessions
    print(f"\n🎯 Simulating Learning Sessions:")
    
    student_id = "student_001"
    for session in range(5):
        recommendation = khan_academy.get_next_recommendation(student_id)
        if recommendation:
            print(f"\n   Session {session + 1}: Attempting '{recommendation}'")
            result = khan_academy.attempt_module(student_id, recommendation)
            print(f"   Score: {result['result']['score']:.2f}, Points: {result['points_earned']}")
            if result['new_badges']:
                print(f"   🏆 New badges: {result['new_badges']}")
        else:
            print(f"\n   Session {session + 1}: No recommendations available")
            break
    
    # Show final dashboard
    print(f"\n📊 Student Dashboard for {student_id}:")
    dashboard = khan_academy.get_student_dashboard(student_id)
    print(f"   Overall Progress: {dashboard['overall_progress']:.1%}")
    print(f"   Modules Mastered: {dashboard['mastered_modules']}/{dashboard['total_modules']}")
    print(f"   Energy Points: {dashboard['energy_points']}")
    print(f"   Badges: {dashboard['badges']}")
    
    if dashboard['next_recommendation']:
        print(f"   Next Recommendation: {dashboard['next_recommendation']}")
