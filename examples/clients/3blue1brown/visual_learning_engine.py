"""
3Blue1Brown Linear Algebra - Visual Learning Implementation
Interactive animations and conceptual understanding through visualization
"""

from typing import Dict, List, Optional, Any, Tuple, Callable
from dataclasses import dataclass, field
from enum import Enum
import json
import math
import random
from datetime import datetime


class VisualizationType(Enum):
    VECTOR_FIELD = "vector_field"
    TRANSFORMATION = "transformation"
    GEOMETRIC_PROOF = "geometric_proof"
    INTERACTIVE_DEMO = "interactive_demo"
    STUDENT_CREATION = "student_creation"


class ConceptualLevel(Enum):
    INTUITIVE = 1      # Visual understanding
    COMPUTATIONAL = 2  # Can calculate
    CONCEPTUAL = 3     # Deep understanding
    CREATIVE = 4       # Can teach others


@dataclass
class VisualConcept:
    """A single visual concept with interactive elements"""

    concept_id: str
    title: str
    description: str
    essential_question: str
    prerequisites: List[str] = field(default_factory=list)
    visualization_types: List[VisualizationType] = field(default_factory=list)
    interactive_elements: List[Dict[str, Any]] = field(default_factory=list)
    concept_levels: Dict[ConceptualLevel, Dict[str, Any]] = field(default_factory=dict)
    visual_metaphors: List[str] = field(default_factory=list)
    real_world_connections: List[str] = field(default_factory=list)
    student_explorations: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class StudentVisualization:
    """Student-created visualization or explanation"""

    visualization_id: str
    student_id: str
    concept_id: str
    title: str
    description: str
    visualization_data: Dict[str, Any]
    peer_ratings: List[float] = field(default_factory=list)
    instructor_feedback: Optional[str] = None
    creation_date: datetime = field(default_factory=datetime.now)


@dataclass
class ConceptualProgress:
    """Tracks deep conceptual understanding, not just completion"""

    student_id: str
    concept_progress: Dict[str, ConceptualLevel] = field(default_factory=dict)
    insight_moments: List[Dict[str, Any]] = field(default_factory=list)
    visual_explanations_created: List[str] = field(default_factory=list)
    peer_help_provided: List[str] = field(default_factory=list)
    exploration_time: Dict[str, int] = field(default_factory=dict)  # seconds per concept
    conceptual_connections: List[Tuple[str, str]] = field(default_factory=list)


class ThreeBlueOneBrownLinearAlgebra:
    """
    3Blue1Brown-style visual learning platform for Linear Algebra
    Emphasis on visual intuition and deep conceptual understanding
    """

    def __init__(self):
        self.concepts = self._initialize_visual_concepts()
        self.student_progress: Dict[str, ConceptualProgress] = {}
        self.visualization_engine = VisualizationEngine()
        self.conceptual_assessor = ConceptualAssessment()
        self.creation_tools = StudentCreationTools()

    def _initialize_visual_concepts(self) -> Dict[str, VisualConcept]:
        """Initialize the visual learning curriculum"""
        concepts = {}

        # Core Question: What IS a vector?
        concepts["vector_essence"] = VisualConcept(
            concept_id="vector_essence",
            title="The Essence of Vectors",
            description="Understanding what vectors truly represent",
            essential_question="What IS a vector, really?",
            visualization_types=[VisualizationType.INTERACTIVE_DEMO, VisualizationType.STUDENT_CREATION],
            interactive_elements=[
                {
                    "type": "draggable_vector",
                    "description": "Drag vectors around the coordinate plane",
                    "parameters": {"grid_size": 10, "snap_to_grid": True}
                },
                {
                    "type": "vector_addition_playground",
                    "description": "Visually explore vector addition",
                    "parameters": {"multiple_vectors": True, "show_resultant": True}
                }
            ],
            concept_levels={
                ConceptualLevel.INTUITIVE: {
                    "description": "Vectors are arrows that represent direction and magnitude",
                    "visual_cues": ["arrow_visualization", "magnitude_length", "direction_angle"],
                    "success_criteria": "Can identify vector properties visually"
                },
                ConceptualLevel.COMPUTATIONAL: {
                    "description": "Can perform vector calculations using components",
                    "visual_cues": ["component_breakdown", "coordinate_system"],
                    "success_criteria": "Correctly calculates vector operations"
                },
                ConceptualLevel.CONCEPTUAL: {
                    "description": "Understands vectors as mathematical objects independent of coordinates",
                    "visual_cues": ["basis_transformation", "coordinate_independence"],
                    "success_criteria": "Can explain vector concept in multiple ways"
                },
                ConceptualLevel.CREATIVE: {
                    "description": "Can create original visualizations to teach vector concepts",
                    "visual_cues": ["custom_metaphors", "teaching_scenarios"],
                    "success_criteria": "Creates clear explanations for others"
                }
            },
            visual_metaphors=[
                "Vectors as instructions for walking in space",
                "Vectors as arrows pointing from here to there",
                "Vectors as lists of numbers with geometric meaning"
            ],
            real_world_connections=[
                "GPS navigation and displacement",
                "Physics: velocity, force, acceleration",
                "Computer graphics and game development"
            ]
        )

        # Linear Combinations and Span
        concepts["linear_combinations"] = VisualConcept(
            concept_id="linear_combinations",
            title="Linear Combinations and Span",
            description="Mixing vectors to reach new points",
            essential_question="What can you reach by combining two vectors?",
            prerequisites=["vector_essence"],
            visualization_types=[VisualizationType.INTERACTIVE_DEMO, VisualizationType.VECTOR_FIELD],
            interactive_elements=[
                {
                    "type": "vector_mixing_sliders",
                    "description": "Use sliders to mix two vectors",
                    "parameters": {"vector_1": [3, 1], "vector_2": [1, 2], "range": [-3, 3]}
                },
                {
                    "type": "span_explorer",
                    "description": "Explore what span looks like for different vector pairs",
                    "parameters": {"show_grid_coverage": True, "highlight_unreachable": True}
                }
            ],
            concept_levels={
                ConceptualLevel.INTUITIVE: {
                    "description": "Linear combinations fill out areas of the plane",
                    "visual_cues": ["filled_regions", "color_gradients", "reachable_points"],
                    "success_criteria": "Recognizes span as filled area"
                },
                ConceptualLevel.COMPUTATIONAL: {
                    "description": "Can calculate specific linear combinations",
                    "visual_cues": ["component_calculations", "coefficient_effects"],
                    "success_criteria": "Correctly computes linear combinations"
                },
                ConceptualLevel.CONCEPTUAL: {
                    "description": "Understands span as the set of all possible linear combinations",
                    "visual_cues": ["infinite_possibilities", "set_theory_visualization"],
                    "success_criteria": "Explains span conceptually"
                }
            },
            visual_metaphors=[
                "Mixing paint colors to get all possible shades",
                "Recipes using two ingredients in varying amounts",
                "Musical harmony from combining two base notes"
            ]
        )

        # Linear Transformations as Matrix Functions
        concepts["linear_transformations"] = VisualConcept(
            concept_id="linear_transformations",
            title="Linear Transformations",
            description="Functions that transform the entire coordinate system",
            essential_question="What do matrices DO to space?",
            prerequisites=["linear_combinations"],
            visualization_types=[VisualizationType.TRANSFORMATION, VisualizationType.INTERACTIVE_DEMO],
            interactive_elements=[
                {
                    "type": "grid_transformation",
                    "description": "Watch the coordinate grid transform",
                    "parameters": {"show_grid_lines": True, "animate_transformation": True}
                },
                {
                    "type": "matrix_sliders",
                    "description": "Adjust matrix entries and see the effect",
                    "parameters": {"matrix_size": "2x2", "real_time_update": True}
                },
                {
                    "type": "vector_tracking",
                    "description": "Track where specific vectors go",
                    "parameters": {"track_basis_vectors": True, "show_trajectories": True}
                }
            ],
            concept_levels={
                ConceptualLevel.INTUITIVE: {
                    "description": "Transformations move and reshape the coordinate grid",
                    "visual_cues": ["grid_distortion", "shape_preservation", "line_mapping"],
                    "success_criteria": "Recognizes transformation effects visually"
                },
                ConceptualLevel.COMPUTATIONAL: {
                    "description": "Can apply matrix transformations to vectors",
                    "visual_cues": ["matrix_multiplication", "coordinate_tracking"],
                    "success_criteria": "Correctly applies transformations"
                },
                ConceptualLevel.CONCEPTUAL: {
                    "description": "Understands matrices as functions that transform space",
                    "visual_cues": ["function_concept", "space_mapping", "geometric_interpretation"],
                    "success_criteria": "Explains transformations as functions"
                }
            }
        )

        # Determinant as Area Scaling
        concepts["determinant_intuition"] = VisualConcept(
            concept_id="determinant_intuition",
            title="Determinant as Area Scaling",
            description="Understanding determinants through area transformation",
            essential_question="How much does a transformation scale areas?",
            prerequisites=["linear_transformations"],
            visualization_types=[VisualizationType.TRANSFORMATION, VisualizationType.GEOMETRIC_PROOF],
            interactive_elements=[
                {
                    "type": "area_scaling_demo",
                    "description": "Watch areas change under transformation",
                    "parameters": {"unit_square": True, "arbitrary_shapes": True}
                },
                {
                    "type": "determinant_calculator",
                    "description": "See determinant calculation matched with visual scaling",
                    "parameters": {"show_calculation_steps": True, "highlight_area_factor": True}
                }
            ],
            concept_levels={
                ConceptualLevel.INTUITIVE: {
                    "description": "Determinant tells you how much areas get scaled",
                    "visual_cues": ["area_comparison", "scaling_factor", "shape_preservation"],
                    "success_criteria": "Recognizes area scaling relationship"
                },
                ConceptualLevel.CONCEPTUAL: {
                    "description": "Understands determinant as measure of transformation magnitude",
                    "visual_cues": ["signed_area", "orientation_change", "volume_generalization"],
                    "success_criteria": "Explains determinant significance"
                }
            },
            visual_metaphors=[
                "Determinant as the 'zoom factor' for areas",
                "Stretching or shrinking a rubber sheet",
                "Photo enlargement/reduction factor"
            ]
        )

        # Eigenvalues and Eigenvectors
        concepts["eigenvectors"] = VisualConcept(
            concept_id="eigenvectors",
            title="Eigenvalues and Eigenvectors",
            description="Vectors that only get scaled, not rotated",
            essential_question="Which vectors don't change direction under transformation?",
            prerequisites=["determinant_intuition"],
            visualization_types=[VisualizationType.TRANSFORMATION, VisualizationType.VECTOR_FIELD],
            interactive_elements=[
                {
                    "type": "eigenvector_finder",
                    "description": "Find vectors that only get scaled",
                    "parameters": {"interactive_search": True, "highlight_special_vectors": True}
                },
                {
                    "type": "eigenvalue_explorer",
                    "description": "Explore how eigenvalues affect eigenvectors",
                    "parameters": {"multiple_eigenvectors": True, "scaling_visualization": True}
                }
            ]
        )

        return concepts

    def enroll_student(self, student_id: str, learning_style: Dict[str, Any] = None):
        """Enroll student in visual learning program"""
        if learning_style is None:
            learning_style = {}

        self.student_progress[student_id] = ConceptualProgress(student_id=student_id)

        # Initial conceptual assessment through visual exploration
        self._conduct_visual_diagnostic(student_id)

    def _conduct_visual_diagnostic(self, student_id: str):
        """Assess student's starting conceptual level through visual interactions"""
        # Simplified diagnostic - would involve interactive visual tasks
        diagnostic_results = {
            "spatial_reasoning": 0.8,
            "mathematical_intuition": 0.7,
            "visual_learning_preference": 0.9
        }

        progress = self.student_progress[student_id]
        
        # Set initial concept access
        if diagnostic_results["spatial_reasoning"] >= 0.7:
            progress.concept_progress["vector_essence"] = ConceptualLevel.INTUITIVE

    def get_next_exploration(self, student_id: str) -> Optional[str]:
        """Get next concept for visual exploration"""
        progress = self.student_progress.get(student_id)
        if not progress:
            return None

        # Find concepts ready for exploration
        available_concepts = []
        
        for concept_id, concept in self.concepts.items():
            # Check prerequisites
            prerequisites_met = all(
                concept_id in progress.concept_progress and
                progress.concept_progress[prereq] in [ConceptualLevel.CONCEPTUAL, ConceptualLevel.CREATIVE]
                for prereq in concept.prerequisites
            )
            
            current_level = progress.concept_progress.get(concept_id)
            
            if prerequisites_met and current_level != ConceptualLevel.CREATIVE:
                available_concepts.append(concept_id)

        if not available_concepts:
            return self._suggest_creative_project(student_id)

        # Prioritize based on exploration readiness
        return self._prioritize_exploration(available_concepts, progress)

    def _prioritize_exploration(self, available_concepts: List[str], progress: ConceptualProgress) -> str:
        """Prioritize which concept to explore next"""
        # Prefer concepts not yet started
        not_started = [
            cid for cid in available_concepts 
            if cid not in progress.concept_progress
        ]
        
        if not_started:
            return not_started[0]
        
        # Otherwise, concepts ready for deeper exploration
        return available_concepts[0]

    def _suggest_creative_project(self, student_id: str) -> Optional[str]:
        """Suggest creative project for advanced students"""
        progress = self.student_progress[student_id]
        
        # Find concepts at conceptual level ready for creative expression
        creative_ready = [
            cid for cid, level in progress.concept_progress.items()
            if level == ConceptualLevel.CONCEPTUAL
        ]
        
        if creative_ready:
            return f"creative_project_{creative_ready[0]}"
        
        return None

    def explore_concept(self, student_id: str, concept_id: str, interaction_data: Dict[str, Any]) -> Dict[str, Any]:
        """Student explores a visual concept"""
        concept = self.concepts.get(concept_id)
        progress = self.student_progress.get(student_id)
        
        if not concept or not progress:
            return {"error": "Invalid concept or student"}

        # Process visual interaction
        exploration_result = self._process_visual_exploration(student_id, concept_id, interaction_data)
        
        # Assess conceptual understanding
        understanding_level = self.conceptual_assessor.assess_understanding(
            concept, interaction_data, exploration_result
        )
        
        # Update progress
        current_level = progress.concept_progress.get(concept_id, ConceptualLevel.INTUITIVE)
        if understanding_level.value > current_level.value:
            progress.concept_progress[concept_id] = understanding_level
            
        # Record exploration time
        session_time = interaction_data.get("session_duration", 300)
        progress.exploration_time[concept_id] = progress.exploration_time.get(concept_id, 0) + session_time
        
        # Check for insight moments
        if self._detect_insight_moment(interaction_data, exploration_result):
            progress.insight_moments.append({
                "concept_id": concept_id,
                "timestamp": datetime.now().isoformat(),
                "insight_type": exploration_result.get("insight_type"),
                "description": exploration_result.get("insight_description")
            })

        return {
            "exploration_result": exploration_result,
            "understanding_level": understanding_level.value,
            "insights_gained": len(progress.insight_moments),
            "next_exploration": self.get_next_exploration(student_id)
        }

    def _process_visual_exploration(self, student_id: str, concept_id: str, interaction_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process student's visual exploration session"""
        concept = self.concepts[concept_id]
        
        # Analyze interaction patterns
        exploration_patterns = {
            "systematic_exploration": self._analyze_systematic_exploration(interaction_data),
            "creative_experimentation": self._analyze_creative_experimentation(interaction_data),
            "hypothesis_testing": self._analyze_hypothesis_testing(interaction_data),
            "pattern_recognition": self._analyze_pattern_recognition(interaction_data)
        }
        
        # Generate insights based on patterns
        insights = []
        if exploration_patterns["systematic_exploration"] > 0.7:
            insights.append("Demonstrates methodical approach to exploration")
        if exploration_patterns["creative_experimentation"] > 0.8:
            insights.append("Shows creative thinking and experimentation")
        if exploration_patterns["pattern_recognition"] > 0.6:
            insights.append("Successfully identifies visual patterns")
        
        return {
            "exploration_patterns": exploration_patterns,
            "insights": insights,
            "visual_understanding_score": sum(exploration_patterns.values()) / len(exploration_patterns),
            "concept_connections": self._identify_concept_connections(interaction_data, concept)
        }

    def _analyze_systematic_exploration(self, interaction_data: Dict[str, Any]) -> float:
        """Analyze how systematically student explored the concept"""
        # Simplified analysis - would examine interaction sequences
        interactions = interaction_data.get("interactions", [])
        if not interactions:
            return 0.0
        
        # Look for systematic patterns in exploration
        systematic_score = min(1.0, len(interactions) / 20)  # More interactions = more systematic
        return systematic_score

    def _analyze_creative_experimentation(self, interaction_data: Dict[str, Any]) -> float:
        """Analyze creative experimentation in student's exploration"""
        # Look for unusual parameter choices, creative combinations
        parameter_variations = interaction_data.get("parameter_variations", 0)
        return min(1.0, parameter_variations / 15)

    def _analyze_hypothesis_testing(self, interaction_data: Dict[str, Any]) -> float:
        """Analyze evidence of hypothesis formation and testing"""
        # Look for repeated similar experiments with small variations
        hypothesis_indicators = interaction_data.get("hypothesis_tests", 0)
        return min(1.0, hypothesis_indicators / 10)

    def _analyze_pattern_recognition(self, interaction_data: Dict[str, Any]) -> float:
        """Analyze pattern recognition capabilities"""
        patterns_identified = interaction_data.get("patterns_identified", 0)
        return min(1.0, patterns_identified / 8)

    def _identify_concept_connections(self, interaction_data: Dict[str, Any], concept: VisualConcept) -> List[str]:
        """Identify connections student made to other concepts"""
        # Would analyze interaction data for cross-concept references
        return interaction_data.get("concept_connections", [])

    def _detect_insight_moment(self, interaction_data: Dict[str, Any], exploration_result: Dict[str, Any]) -> bool:
        """Detect if student had a significant insight"""
        # Look for sudden changes in behavior, successful predictions, etc.
        insight_indicators = [
            exploration_result.get("visual_understanding_score", 0) > 0.8,
            len(exploration_result.get("insights", [])) > 2,
            interaction_data.get("sudden_improvement", False)
        ]
        
        return sum(insight_indicators) >= 2

    def create_student_visualization(self, student_id: str, concept_id: str, visualization_data: Dict[str, Any]) -> str:
        """Student creates their own visualization or explanation"""
        visualization_id = f"viz_{student_id}_{concept_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        student_viz = StudentVisualization(
            visualization_id=visualization_id,
            student_id=student_id,
            concept_id=concept_id,
            title=visualization_data.get("title", "Student Visualization"),
            description=visualization_data.get("description", ""),
            visualization_data=visualization_data
        )
        
        # Store in creation tools system
        self.creation_tools.store_student_creation(student_viz)
        
        # Update student progress
        progress = self.student_progress[student_id]
        progress.visual_explanations_created.append(visualization_id)
        
        # If student reached creative level for this concept
        if progress.concept_progress.get(concept_id) == ConceptualLevel.CONCEPTUAL:
            progress.concept_progress[concept_id] = ConceptualLevel.CREATIVE
        
        return visualization_id

    def get_student_portfolio(self, student_id: str) -> Dict[str, Any]:
        """Get student's visual learning portfolio"""
        progress = self.student_progress.get(student_id)
        if not progress:
            return {"error": "Student not found"}

        # Calculate conceptual mastery
        conceptual_levels = list(progress.concept_progress.values())
        avg_level = sum(level.value for level in conceptual_levels) / len(conceptual_levels) if conceptual_levels else 0

        # Get visualization contributions
        student_visualizations = self.creation_tools.get_student_visualizations(student_id)
        
        # Calculate exploration depth
        total_exploration_time = sum(progress.exploration_time.values())
        
        return {
            "student_id": student_id,
            "conceptual_mastery": avg_level / 3,  # Normalize to 0-1
            "concepts_explored": len(progress.concept_progress),
            "insight_moments": len(progress.insight_moments),
            "visualizations_created": len(progress.visual_explanations_created),
            "total_exploration_time": total_exploration_time,
            "student_visualizations": student_visualizations,
            "recent_insights": progress.insight_moments[-5:],  # Last 5 insights
            "next_exploration": self.get_next_exploration(student_id)
        }

    def get_concept_visualization(self, concept_id: str, visualization_type: VisualizationType) -> Dict[str, Any]:
        """Get visualization data for a specific concept"""
        concept = self.concepts.get(concept_id)
        if not concept:
            return {"error": "Concept not found"}

        return self.visualization_engine.generate_visualization(concept, visualization_type)


class VisualizationEngine:
    """Generates interactive mathematical visualizations"""
    
    def generate_visualization(self, concept: VisualConcept, viz_type: VisualizationType) -> Dict[str, Any]:
        """Generate visualization data for rendering"""
        if viz_type == VisualizationType.TRANSFORMATION:
            return self._generate_transformation_viz(concept)
        elif viz_type == VisualizationType.VECTOR_FIELD:
            return self._generate_vector_field_viz(concept)
        elif viz_type == VisualizationType.INTERACTIVE_DEMO:
            return self._generate_interactive_demo(concept)
        else:
            return {"error": "Visualization type not supported"}
    
    def _generate_transformation_viz(self, concept: VisualConcept) -> Dict[str, Any]:
        """Generate transformation visualization data"""
        return {
            "type": "transformation",
            "grid_size": 20,
            "transformation_matrix": [[1, 0], [0, 1]],  # Identity matrix initially
            "animation_speed": 1.0,
            "show_basis_vectors": True,
            "show_grid_lines": True,
            "interactive_controls": {
                "matrix_sliders": True,
                "preset_transformations": ["rotation", "scaling", "shear", "reflection"]
            }
        }
    
    def _generate_vector_field_viz(self, concept: VisualConcept) -> Dict[str, Any]:
        """Generate vector field visualization"""
        return {
            "type": "vector_field",
            "field_density": 15,
            "vector_scaling": 0.8,
            "color_coding": "magnitude",
            "interactive_controls": {
                "field_function": "editable",
                "density_slider": True,
                "color_options": ["magnitude", "direction", "custom"]
            }
        }
    
    def _generate_interactive_demo(self, concept: VisualConcept) -> Dict[str, Any]:
        """Generate interactive demonstration"""
        return {
            "type": "interactive_demo",
            "elements": concept.interactive_elements,
            "guided_exploration": True,
            "hint_system": True,
            "parameter_ranges": self._get_safe_parameter_ranges(concept)
        }
    
    def _get_safe_parameter_ranges(self, concept: VisualConcept) -> Dict[str, Any]:
        """Get safe parameter ranges for interactive elements"""
        return {
            "vector_components": {"min": -10, "max": 10},
            "scalar_multipliers": {"min": -3, "max": 3},
            "matrix_entries": {"min": -2, "max": 2}
        }


class ConceptualAssessment:
    """Assesses deep conceptual understanding through visual interactions"""
    
    def assess_understanding(self, concept: VisualConcept, interaction_data: Dict[str, Any], exploration_result: Dict[str, Any]) -> ConceptualLevel:
        """Assess student's conceptual understanding level"""
        
        # Analyze different aspects of understanding
        visual_recognition = self._assess_visual_recognition(interaction_data)
        computational_skill = self._assess_computational_skill(interaction_data)
        conceptual_depth = self._assess_conceptual_depth(exploration_result)
        creative_expression = self._assess_creative_expression(interaction_data)
        
        # Determine overall level
        if creative_expression > 0.7:
            return ConceptualLevel.CREATIVE
        elif conceptual_depth > 0.6:
            return ConceptualLevel.CONCEPTUAL
        elif computational_skill > 0.5:
            return ConceptualLevel.COMPUTATIONAL
        else:
            return ConceptualLevel.INTUITIVE
    
    def _assess_visual_recognition(self, interaction_data: Dict[str, Any]) -> float:
        """Assess visual pattern recognition"""
        return interaction_data.get("visual_recognition_score", 0.5)
    
    def _assess_computational_skill(self, interaction_data: Dict[str, Any]) -> float:
        """Assess computational abilities"""
        return interaction_data.get("computational_accuracy", 0.5)
    
    def _assess_conceptual_depth(self, exploration_result: Dict[str, Any]) -> float:
        """Assess depth of conceptual understanding"""
        return exploration_result.get("visual_understanding_score", 0.5)
    
    def _assess_creative_expression(self, interaction_data: Dict[str, Any]) -> float:
        """Assess creative and explanatory abilities"""
        return interaction_data.get("creative_expression_score", 0.0)


class StudentCreationTools:
    """Tools for students to create their own visualizations"""
    
    def __init__(self):
        self.student_visualizations: List[StudentVisualization] = []
    
    def store_student_creation(self, visualization: StudentVisualization):
        """Store student-created visualization"""
        self.student_visualizations.append(visualization)
    
    def get_student_visualizations(self, student_id: str) -> List[Dict[str, Any]]:
        """Get all visualizations created by a student"""
        return [
            {
                "id": viz.visualization_id,
                "title": viz.title,
                "concept": viz.concept_id,
                "creation_date": viz.creation_date.isoformat(),
                "peer_rating": sum(viz.peer_ratings) / len(viz.peer_ratings) if viz.peer_ratings else 0
            }
            for viz in self.student_visualizations
            if viz.student_id == student_id
        ]


# Example usage and testing
if __name__ == "__main__":
    print("🎨 3Blue1Brown Linear Algebra - Visual Learning System")
    print("=" * 60)
    
    # Initialize system
    visual_academy = ThreeBlueOneBrownLinearAlgebra()
    
    # Enroll test student
    student_id = "visual_learner_001"
    visual_academy.enroll_student(student_id, {
        "learning_style": "visual",
        "mathematics_background": "intermediate"
    })
    print(f"✅ Enrolled {student_id}")
    
    # Simulate visual exploration sessions
    print(f"\n🎯 Simulating Visual Exploration Sessions:")
    
    for session in range(3):
        concept_to_explore = visual_academy.get_next_exploration(student_id)
        if concept_to_explore:
            # Simulate interaction data
            interaction_data = {
                "session_duration": random.randint(600, 1800),  # 10-30 minutes
                "interactions": [f"interaction_{i}" for i in range(random.randint(15, 30))],
                "parameter_variations": random.randint(8, 20),
                "patterns_identified": random.randint(3, 10),
                "visual_recognition_score": random.uniform(0.6, 0.9),
                "computational_accuracy": random.uniform(0.5, 0.8),
                "creative_expression_score": random.uniform(0.3, 0.7)
            }
            
            print(f"\n   Session {session + 1}: Exploring '{concept_to_explore}'")
            result = visual_academy.explore_concept(student_id, concept_to_explore, interaction_data)
            print(f"   Understanding Level: {result['understanding_level']}")
            print(f"   Insights Gained: {result['insights_gained']}")
        else:
            print(f"\n   Session {session + 1}: Ready for creative projects")
            break
    
    # Simulate student creating a visualization
    print(f"\n🎨 Student Creating Visualization:")
    if concept_to_explore:
        viz_data = {
            "title": "My Vector Addition Explanation",
            "description": "Interactive demo showing why vector addition works",
            "visualization_type": "student_creation",
            "elements": ["draggable_vectors", "animation", "explanation_text"]
        }
        viz_id = visual_academy.create_student_visualization(student_id, concept_to_explore, viz_data)
        print(f"   Created visualization: {viz_id}")
    
    # Show final portfolio
    print(f"\n📊 Student Portfolio for {student_id}:")
    portfolio = visual_academy.get_student_portfolio(student_id)
    print(f"   Conceptual Mastery: {portfolio['conceptual_mastery']:.1%}")
    print(f"   Concepts Explored: {portfolio['concepts_explored']}")
    print(f"   Insight Moments: {portfolio['insight_moments']}")
    print(f"   Visualizations Created: {portfolio['visualizations_created']}")
    print(f"   Total Exploration Time: {portfolio['total_exploration_time']//60} minutes")
    
    if portfolio['next_exploration']:
        print(f"   Next Exploration: {portfolio['next_exploration']}")
    
    # Get visualization for a concept
    print(f"\n🖼️  Sample Visualization:")
    viz_data = visual_academy.get_concept_visualization("vector_essence", VisualizationType.INTERACTIVE_DEMO)
    if "error" not in viz_data:
        print(f"   Type: {viz_data['type']}")
        print(f"   Interactive Controls: {viz_data.get('interactive_controls', {})}")
        print("   Ready for rendering in web interface")
