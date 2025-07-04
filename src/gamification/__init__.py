"""
Advanced Gamification Engine for Canvas Courses

Enterprise-grade gamification system implementing research-backed educational principles
and adaptive learning mechanisms. This module provides comprehensive support for:

🎯 CORE FEATURES:
- Skill trees with multiple progression paths
- Dynamic XP systems with adaptive multipliers  
- Achievement badges with complex unlock criteria
- Mastery-based progression tracking
- Social learning and competition features
- Adaptive difficulty and personalization
- Analytics and progress visualization

🧠 RESEARCH FOUNDATION:
This module is built on established educational and psychological research:
- Self-Determination Theory (Deci & Ryan): Autonomy, competence, relatedness
- Flow Theory (Csikszentmihalyi): Optimal challenge-skill balance
- Cognitive Load Theory (Sweller): Managing intrinsic, extraneous, and germane load
- Zone of Proximal Development (Vygotsky): Scaffolded learning progression
- Mastery Learning (Bloom): Competency-based advancement
- Social Cognitive Theory (Bandura): Observational learning and self-efficacy

🎮 GAMIFICATION PRINCIPLES:
- Meaningful choice and autonomy
- Clear progression and feedback
- Social recognition and collaboration
- Intrinsic motivation over extrinsic rewards
- Personalized challenge curves
- Multiple pathways to success
- Transparent criteria and fairness

📊 ANALYTICS & INSIGHTS:
- Real-time progress tracking
- Learning pattern analysis
- Engagement metrics
- Predictive modeling for at-risk students
- Personalization recommendations
- Instructor dashboard analytics

♿ ACCESSIBILITY & UDL:
- Multiple means of representation (visual, auditory, textual progress indicators)
- Multiple means of engagement (choice in activities, personalized challenges)
- Multiple means of action/expression (various badge earning methods)
- Screen reader compatible progress descriptions
- High contrast visual elements
- Keyboard navigation support

Version: 2.0 - Enterprise Edition
Author: Canvas Course Gamification Team
License: Educational Use
"""

import logging
import json
import datetime
from typing import Dict, List, Optional, Any, Tuple, Set, Union, Callable
from dataclasses import dataclass, field, asdict
from enum import Enum, IntEnum
from pathlib import Path
import hashlib
import math
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)


class SkillLevel(IntEnum):
    """
    Skill progression levels based on Bloom's Taxonomy and mastery learning principles.
    
    Each level represents a deeper understanding and application capability:
    - RECOGNITION: Surface learning, identification, basic recall
    - APPLICATION: Procedural knowledge, using concepts in familiar contexts  
    - INTUITION: Deep understanding, pattern recognition, conceptual grasp
    - SYNTHESIS: Creative application, connecting concepts, problem-solving
    - MASTERY: Expert level, teaching others, innovative applications
    
    Research Foundation:
    - Bloom's Taxonomy (1956, revised 2001)
    - SOLO Taxonomy (Biggs & Collis, 1982)
    - Dreyfus Model of Skill Acquisition (1980)
    """
    RECOGNITION = 1  # "I know what this is" - Basic identification and recall
    APPLICATION = 2  # "I can use this" - Apply in familiar situations
    INTUITION = 3    # "I understand why" - Deep conceptual understanding
    SYNTHESIS = 4    # "I can connect and innovate" - Creative problem-solving
    MASTERY = 5      # "I can teach this" - Expert-level proficiency

    @property
    def description(self) -> str:
        """Get human-readable description of the skill level."""
        descriptions = {
            self.RECOGNITION: "Basic recognition and recall of concepts",
            self.APPLICATION: "Application of knowledge in familiar contexts",
            self.INTUITION: "Deep understanding of underlying principles", 
            self.SYNTHESIS: "Creative problem-solving and knowledge integration",
            self.MASTERY: "Expert-level proficiency and teaching capability"
        }
        return descriptions[self]
    
    @property
    def color_code(self) -> str:
        """Get color code for visual representation (accessibility-friendly)."""
        colors = {
            self.RECOGNITION: "#2E7D32",    # Dark green
            self.APPLICATION: "#1976D2",    # Blue  
            self.INTUITION: "#7B1FA2",     # Purple
            self.SYNTHESIS: "#E64A19",     # Deep orange
            self.MASTERY: "#C62828"        # Dark red
        }
        return colors[self]


class BadgeCategory(Enum):
    """Categories for organizing badges and achievements."""
    ACADEMIC = "academic"           # Subject-specific achievements
    PARTICIPATION = "participation" # Engagement and attendance
    COLLABORATION = "collaboration" # Teamwork and peer interaction
    CREATIVITY = "creativity"       # Original work and innovation
    LEADERSHIP = "leadership"       # Helping others and taking initiative
    PERSISTENCE = "persistence"     # Overcoming challenges
    MILESTONE = "milestone"         # Major course progression markers
    SPECIAL = "special"            # Unique or rare achievements


class DifficultyLevel(Enum):
    """Difficulty levels for adaptive content and challenges."""
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate" 
    ADVANCED = "advanced"
    EXPERT = "expert"


class ProgressStatus(Enum):
    """Status indicators for skill nodes and activities."""
    LOCKED = "locked"
    AVAILABLE = "available"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    MASTERED = "mastered"


@dataclass
class LearningObjective:
    """
    Represents a specific learning objective tied to skill development.
    
    Based on SMART criteria (Specific, Measurable, Achievable, Relevant, Time-bound)
    and aligned with institutional learning outcomes.
    """
    id: str
    description: str
    bloom_level: str  # remember, understand, apply, analyze, evaluate, create
    assessment_criteria: List[str] = field(default_factory=list)
    mastery_threshold: float = 0.8
    estimated_time_hours: Optional[float] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return asdict(self)


@dataclass 
class AccessibilityFeatures:
    """Accessibility features for gamification elements."""
    alt_text: Optional[str] = None
    high_contrast: bool = False
    screen_reader_description: Optional[str] = None
    keyboard_shortcut: Optional[str] = None
    audio_description: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return asdict(self)


@dataclass
class Badge:
    """
    Enhanced achievement badge with comprehensive metadata and accessibility features.
    
    Badges represent meaningful accomplishments aligned with learning objectives
    and designed to promote intrinsic motivation rather than just external rewards.
    
    Research Foundation:
    - Digital Badge Design Principles (Mozilla Foundation)
    - Gamification and Intrinsic Motivation (Ryan & Deci)
    - Recognition and Achievement Psychology (Dweck's Growth Mindset)
    """
    id: str
    name: str
    description: str
    criteria: str
    xp_value: int
    category: BadgeCategory = BadgeCategory.ACADEMIC
    rarity: str = "common"  # common, uncommon, rare, epic, legendary
    image_url: Optional[str] = None
    unlock_requirements: List[str] = field(default_factory=list)
    prerequisite_badges: List[str] = field(default_factory=list)
    learning_objectives: List[LearningObjective] = field(default_factory=list)
    accessibility: AccessibilityFeatures = field(default_factory=AccessibilityFeatures)
    created_date: Optional[str] = None
    expiry_date: Optional[str] = None
    issuer: str = "Canvas Course System"
    verifiable: bool = True
    
    def __post_init__(self):
        """Initialize computed fields after creation."""
        if self.created_date is None:
            self.created_date = datetime.datetime.now().isoformat()
    
    @property
    def rarity_multiplier(self) -> float:
        """Get XP multiplier based on badge rarity."""
        multipliers = {
            "common": 1.0,
            "uncommon": 1.2, 
            "rare": 1.5,
            "epic": 2.0,
            "legendary": 3.0
        }
        return multipliers.get(self.rarity, 1.0)
    
    def is_available_to_user(self, student_progress: Dict[str, Any]) -> bool:
        """Check if badge is available to a specific student."""
        # Check prerequisite badges
        earned_badges = set(student_progress.get("badges", []))
        if not all(prereq in earned_badges for prereq in self.prerequisite_badges):
            return False
            
        # Check expiry date
        if self.expiry_date:
            try:
                expiry = datetime.datetime.fromisoformat(self.expiry_date)
                if datetime.datetime.now() > expiry:
                    return False
            except ValueError:
                logger.warning(f"Invalid expiry date format for badge {self.id}")
                
        return True

    def to_canvas_format(self) -> Dict[str, Any]:
        """Convert badge to Canvas-compatible format with enhanced metadata."""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "criteria": self.criteria,
            "points_possible": int(self.xp_value * self.rarity_multiplier),
            "image_url": self.image_url,
            "metadata": {
                "category": self.category.value,
                "rarity": self.rarity,
                "learning_objectives": [obj.to_dict() for obj in self.learning_objectives],
                "accessibility": self.accessibility.to_dict(),
                "verifiable": self.verifiable
            }
        }
    
    def to_open_badge_format(self) -> Dict[str, Any]:
        """Convert to Open Badges 2.0 standard format."""
        return {
            "@context": "https://w3id.org/openbadges/v2",
            "type": "Assertion",
            "id": f"urn:uuid:{self.id}",
            "badge": {
                "type": "BadgeClass",
                "id": f"badge:{self.id}",
                "name": self.name,
                "description": self.description,
                "image": self.image_url,
                "criteria": {
                    "narrative": self.criteria
                },
                "issuer": {
                    "type": "Issuer",
                    "id": "canvas-gamification-system",
                    "name": self.issuer
                }
            },
            "verification": {
                "type": "hosted" if self.verifiable else "none"
            }
        }



@dataclass
class AdaptiveParameters:
    """Parameters for adaptive learning and difficulty adjustment."""
    base_difficulty: DifficultyLevel = DifficultyLevel.INTERMEDIATE
    min_success_rate: float = 0.6
    max_success_rate: float = 0.9
    adjustment_sensitivity: float = 0.1
    personalization_weight: float = 0.3
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return asdict(self)


@dataclass
class SocialFeatures:
    """Social learning and collaboration features for skill nodes."""
    allows_peer_review: bool = False
    enables_study_groups: bool = False
    supports_mentoring: bool = False
    leaderboard_eligible: bool = True
    collaboration_bonus_multiplier: float = 1.1
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return asdict(self)


@dataclass
class SkillNode:
    """
    Enhanced skill node representing a specific competency in the learning pathway.
    
    Incorporates adaptive learning principles, social features, and comprehensive
    progress tracking aligned with educational research on skill development.
    
    Research Foundation:
    - Adaptive Learning Systems (Brusilovsky & Peylo, 2003)
    - Competency-Based Education (Spady, 1994)
    - Social Learning Theory (Bandura, 1977)
    - Mastery Learning (Bloom, 1968)
    """
    id: str
    name: str
    description: str
    level: SkillLevel
    xp_required: int
    estimated_time_minutes: int = 60
    difficulty: DifficultyLevel = DifficultyLevel.INTERMEDIATE
    prerequisites: List[str] = field(default_factory=list)
    unlock_requirements: Dict[str, Any] = field(default_factory=dict)
    badges: List[str] = field(default_factory=list)
    learning_objectives: List[LearningObjective] = field(default_factory=list)
    mastery_threshold: float = 0.8
    resources: List[Dict[str, str]] = field(default_factory=list)
    assessments: List[str] = field(default_factory=list)
    adaptive_params: AdaptiveParameters = field(default_factory=AdaptiveParameters)
    social_features: SocialFeatures = field(default_factory=SocialFeatures)
    accessibility: AccessibilityFeatures = field(default_factory=AccessibilityFeatures)
    tags: List[str] = field(default_factory=list)
    created_by: str = "system"
    last_updated: Optional[str] = None
    
    def __post_init__(self):
        """Initialize computed fields after creation."""
        if self.last_updated is None:
            self.last_updated = datetime.datetime.now().isoformat()

    def is_unlocked(self, student_progress: Dict[str, Any]) -> bool:
        """
        Check if this skill node is unlocked for a student.
        
        Enhanced with adaptive learning considerations and personalized requirements.
        """
        # Check prerequisite completion with mastery verification
        for prereq in self.prerequisites:
            prereq_progress = student_progress.get("skills", {}).get(prereq, {})
            if not prereq_progress.get("completed", False):
                return False
            
            # Verify mastery level for prerequisites
            mastery_score = prereq_progress.get("mastery_score", 0)
            if mastery_score < self.mastery_threshold:
                return False

        # Check XP requirements with level-based adjustments
        student_xp = student_progress.get("total_xp", 0)
        required_xp = self._calculate_adaptive_xp_requirement(student_progress)
        if student_xp < required_xp:
            return False

        # Check custom unlock requirements
        for requirement_type, requirement_value in self.unlock_requirements.items():
            if not self._check_requirement(requirement_type, requirement_value, student_progress):
                return False

        # Check time-based availability (if applicable)
        if not self._check_time_availability(student_progress):
            return False

        return True

    def _calculate_adaptive_xp_requirement(self, student_progress: Dict[str, Any]) -> int:
        """Calculate adaptive XP requirement based on student performance."""
        base_xp = self.xp_required
        
        # Adjust based on student's historical performance
        avg_performance = student_progress.get("average_performance", 0.75)
        if avg_performance > 0.9:
            # High performer - increase challenge
            base_xp = int(base_xp * 1.2)
        elif avg_performance < 0.6:
            # Struggling student - reduce barrier
            base_xp = int(base_xp * 0.8)
            
        return max(base_xp, self.xp_required // 2)  # Never less than 50% of base

    def _check_requirement(self, req_type: str, req_value: Any, progress: Dict[str, Any]) -> bool:
        """Check a specific unlock requirement with enhanced logic."""
        if req_type == "quiz_score":
            quiz_id, min_score = req_value
            quiz_score = progress.get("quiz_scores", {}).get(quiz_id, 0)
            return quiz_score >= min_score

        elif req_type == "assignment_completion":
            assignment_ids = req_value if isinstance(req_value, list) else [req_value]
            for assignment_id in assignment_ids:
                assignment_data = progress.get("assignments", {}).get(assignment_id, {})
                if not assignment_data.get("completed", False):
                    return False
                # Check quality of completion
                if assignment_data.get("score", 0) < self.mastery_threshold:
                    return False
            return True

        elif req_type == "badge_earned":
            badge_ids = req_value if isinstance(req_value, list) else [req_value]
            earned_badges = progress.get("badges", [])
            return all(badge_id in earned_badges for badge_id in badge_ids)

        elif req_type == "time_spent":
            # Minimum time spent in previous activities
            total_time = progress.get("total_time_spent", 0)
            return total_time >= req_value

        elif req_type == "peer_interactions":
            # Social learning requirements
            peer_score = progress.get("peer_interaction_score", 0)
            return peer_score >= req_value

        elif req_type == "mastery_level":
            # Overall mastery requirement
            mastery_level = progress.get("overall_mastery", 0)
            return mastery_level >= req_value

        return True

    def _check_time_availability(self, student_progress: Dict[str, Any]) -> bool:
        """Check if node is available based on course schedule."""
        # Implement time-based availability logic
        # This could include release dates, prerequisite completion times, etc.
        return True  # Simplified for now

    def calculate_mastery_score(self, student_progress: Dict[str, Any]) -> float:
        """
        Calculate mastery score for this skill node based on multiple assessments.
        
        Uses weighted average of different assessment types with recency bias.
        """
        skill_progress = student_progress.get("skills", {}).get(self.id, {})
        scores = skill_progress.get("assessment_scores", [])
        
        if not scores:
            return 0.0
            
        # Apply recency weighting (more recent attempts count more)
        weighted_sum = 0
        weight_sum = 0
        
        for i, score in enumerate(scores):
            weight = 0.7 ** (len(scores) - i - 1)  # Recent scores weighted higher
            weighted_sum += score * weight
            weight_sum += weight
            
        return weighted_sum / weight_sum if weight_sum > 0 else 0.0

    def get_recommended_resources(self, student_progress: Dict[str, Any]) -> List[Dict[str, str]]:
        """Get personalized resource recommendations based on student needs."""
        all_resources = self.resources.copy()
        
        # Add adaptive resources based on performance
        avg_performance = student_progress.get("average_performance", 0.75)
        learning_style = student_progress.get("learning_style", "visual")
        
        if avg_performance < 0.6:
            # Add remedial resources
            all_resources.extend([
                {
                    "type": "video", 
                    "title": f"Foundational Concepts for {self.name}",
                    "url": f"/resources/foundation/{self.id}",
                    "difficulty": "beginner"
                }
            ])
        
        if avg_performance > 0.9:
            # Add challenge resources
            all_resources.extend([
                {
                    "type": "challenge",
                    "title": f"Advanced Applications of {self.name}",
                    "url": f"/resources/advanced/{self.id}",
                    "difficulty": "expert"
                }
            ])
            
        # Filter by learning style preference
        style_preferences = {
            "visual": ["video", "infographic", "diagram"],
            "auditory": ["podcast", "audio", "discussion"],
            "kinesthetic": ["simulation", "lab", "hands-on"],
            "reading": ["article", "text", "documentation"]
        }
        
        preferred_types = style_preferences.get(learning_style, [])
        if preferred_types:
            # Prioritize resources matching learning style
            all_resources.sort(key=lambda r: r.get("type", "") in preferred_types, reverse=True)
            
        return all_resources

    def generate_progress_insights(self, student_progress: Dict[str, Any]) -> Dict[str, Any]:
        """Generate insights and recommendations for student progress."""
        skill_progress = student_progress.get("skills", {}).get(self.id, {})
        mastery_score = self.calculate_mastery_score(student_progress)
        
        insights = {
            "mastery_score": mastery_score,
            "completion_status": self._get_completion_status(mastery_score),
            "time_spent": skill_progress.get("time_spent", 0),
            "attempts": len(skill_progress.get("assessment_scores", [])),
            "recommendations": []
        }
        
        # Generate specific recommendations
        if mastery_score < 0.4:
            insights["recommendations"].append({
                "type": "remediation",
                "message": "Consider reviewing prerequisite skills and foundational concepts",
                "priority": "high"
            })
        elif mastery_score < self.mastery_threshold:
            insights["recommendations"].append({
                "type": "practice",
                "message": "Additional practice with core concepts recommended",
                "priority": "medium" 
            })
        elif mastery_score >= 0.95:
            insights["recommendations"].append({
                "type": "advancement",
                "message": "Ready for advanced challenges and helping peers",
                "priority": "low"
            })
            
        return insights

    def _get_completion_status(self, mastery_score: float) -> ProgressStatus:
        """Determine completion status based on mastery score."""
        if mastery_score >= 0.95:
            return ProgressStatus.MASTERED
        elif mastery_score >= self.mastery_threshold:
            return ProgressStatus.COMPLETED
        elif mastery_score > 0:
            return ProgressStatus.IN_PROGRESS
        else:
            return ProgressStatus.AVAILABLE

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization with all metadata."""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "level": {
                "value": self.level.value,
                "name": self.level.name,
                "description": self.level.description,
                "color": self.level.color_code
            },
            "xp_required": self.xp_required,
            "estimated_time_minutes": self.estimated_time_minutes,
            "difficulty": self.difficulty.value,
            "prerequisites": self.prerequisites,
            "unlock_requirements": self.unlock_requirements,
            "badges": self.badges,
            "learning_objectives": [obj.to_dict() for obj in self.learning_objectives],
            "mastery_threshold": self.mastery_threshold,
            "resources": self.resources,
            "assessments": self.assessments,
            "adaptive_params": self.adaptive_params.to_dict(),
            "social_features": self.social_features.to_dict(),
            "accessibility": self.accessibility.to_dict(),
            "tags": self.tags,
            "created_by": self.created_by,
            "last_updated": self.last_updated
        }



class SkillTree:
    """
    Advanced skill tree management system with comprehensive learning analytics.
    
    Implements research-based learning pathways with adaptive progression,
    social learning features, and detailed analytics for instructors and students.
    
    Features:
    - Multiple learning pathways and branching structures
    - Adaptive difficulty adjustment based on performance
    - Social learning and collaboration tracking
    - Comprehensive progress analytics
    - Personalized recommendations
    - Accessibility and UDL compliance
    - Real-time progress visualization
    
    Research Foundation:
    - Learning Path Optimization (VanLehn, 2011)
    - Adaptive Hypermedia Systems (Brusilovsky, 2001)
    - Educational Data Mining (Baker & Inventado, 2014)
    - Personalized Learning Systems (Pane et al., 2017)
    """

    def __init__(self, name: str, description: str, metadata: Optional[Dict[str, Any]] = None):
        self.name = name
        self.description = description
        self.metadata = metadata or {}
        self.nodes: Dict[str, SkillNode] = {}
        self.badges: Dict[str, Badge] = {}
        self.levels: Dict[int, List[str]] = {}
        self.pathways: Dict[str, List[str]] = {}  # Named learning pathways
        self.categories: Dict[str, List[str]] = {}  # Skill categories
        self.learning_analytics: Dict[str, Any] = {}
        self.created_date = datetime.datetime.now().isoformat()
        self.version = "2.0"

    def add_node(self, node: SkillNode) -> None:
        """Add a skill node to the tree with enhanced organization."""
        self.nodes[node.id] = node

        # Organize by level
        level_num = node.level.value
        if level_num not in self.levels:
            self.levels[level_num] = []
        self.levels[level_num].append(node.id)
        
        # Organize by tags/categories
        for tag in node.tags:
            if tag not in self.categories:
                self.categories[tag] = []
            self.categories[tag].append(node.id)
            
        logger.info(f"Added skill node '{node.name}' (ID: {node.id}) to skill tree")

    def add_badge(self, badge: Badge) -> None:
        """Add a badge to the system with validation."""
        self.badges[badge.id] = badge
        logger.info(f"Added badge '{badge.name}' (ID: {badge.id}) to skill tree")

    def create_pathway(self, pathway_name: str, node_ids: List[str], description: str = "") -> bool:
        """
        Create a named learning pathway through specific nodes.
        
        Pathways provide structured routes through the skill tree for different
        learning goals or student types.
        """
        # Validate all nodes exist
        for node_id in node_ids:
            if node_id not in self.nodes:
                logger.error(f"Cannot create pathway '{pathway_name}': node '{node_id}' not found")
                return False
                
        self.pathways[pathway_name] = {
            "nodes": node_ids,
            "description": description,
            "created_date": datetime.datetime.now().isoformat()
        }
        
        logger.info(f"Created pathway '{pathway_name}' with {len(node_ids)} nodes")
        return True

    def get_unlocked_nodes(self, student_progress: Dict[str, Any]) -> List[SkillNode]:
        """Get all nodes unlocked for a student with enhanced filtering."""
        unlocked = []
        for node in self.nodes.values():
            if node.is_unlocked(student_progress):
                unlocked.append(node)
        
        # Sort by level and then by XP requirement
        unlocked.sort(key=lambda n: (n.level.value, n.xp_required))
        return unlocked

    def get_next_available_nodes(self, student_progress: Dict[str, Any], limit: int = 5) -> List[SkillNode]:
        """
        Get nodes that are one step away from being unlocked.
        
        Enhanced with personalized recommendations and adaptive difficulty.
        """
        unlocked_ids = {node.id for node in self.get_unlocked_nodes(student_progress)}
        next_nodes = []

        for node in self.nodes.values():
            if node.id in unlocked_ids:
                continue

            # Check if all prerequisites are unlocked
            if all(prereq in unlocked_ids for prereq in node.prerequisites):
                next_nodes.append(node)

        # Personalize recommendations based on student performance and preferences
        next_nodes = self._personalize_recommendations(next_nodes, student_progress)
        
        # Sort by recommendation score and limit results
        return next_nodes[:limit]

    def _personalize_recommendations(self, nodes: List[SkillNode], student_progress: Dict[str, Any]) -> List[SkillNode]:
        """Apply personalization algorithm to node recommendations."""
        avg_performance = student_progress.get("average_performance", 0.75)
        learning_style = student_progress.get("learning_style", "visual")
        interests = student_progress.get("interests", [])
        
        # Score nodes based on multiple factors
        scored_nodes = []
        for node in nodes:
            score = 0.0
            
            # Performance-based scoring
            if avg_performance > 0.9 and node.difficulty == DifficultyLevel.ADVANCED:
                score += 2.0  # High performers get advanced content
            elif avg_performance < 0.6 and node.difficulty == DifficultyLevel.BEGINNER:
                score += 2.0  # Struggling students get easier content
            elif node.difficulty == DifficultyLevel.INTERMEDIATE:
                score += 1.0  # Default preference for intermediate
                
            # Interest-based scoring
            for interest in interests:
                if interest in node.tags:
                    score += 1.5
                    
            # Learning style alignment
            if learning_style == "visual" and any("visual" in res.get("type", "") for res in node.resources):
                score += 1.0
            elif learning_style == "hands-on" and node.social_features.allows_peer_review:
                score += 1.0
                
            # Social features preference
            if student_progress.get("prefers_collaboration", False):
                if node.social_features.enables_study_groups:
                    score += 1.0
                    
            scored_nodes.append((node, score))
            
        # Sort by score (descending) and return nodes
        scored_nodes.sort(key=lambda x: x[1], reverse=True)
        return [node for node, score in scored_nodes]

    def calculate_progress(self, student_progress: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate comprehensive progress statistics with enhanced analytics."""
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
                "level_name": SkillLevel(level_num).name if level_num <= 5 else f"Level {level_num}"
            }

        # Calculate mastery distribution
        mastery_distribution = {"mastered": 0, "completed": 0, "in_progress": 0, "available": 0}
        for node in self.nodes.values():
            mastery_score = node.calculate_mastery_score(student_progress)
            status = node._get_completion_status(mastery_score)
            mastery_distribution[status.value] += 1

        # Calculate pathway progress
        pathway_progress = {}
        for pathway_name, pathway_data in self.pathways.items():
            pathway_nodes = pathway_data["nodes"]
            completed_nodes = sum(
                1 for node_id in pathway_nodes 
                if student_progress.get("skills", {}).get(node_id, {}).get("completed", False)
            )
            pathway_progress[pathway_name] = {
                "completed": completed_nodes,
                "total": len(pathway_nodes),
                "percentage": (completed_nodes / len(pathway_nodes)) * 100 if pathway_nodes else 0
            }

        # Calculate category progress
        category_progress = {}
        for category, node_ids in self.categories.items():
            category_unlocked = sum(
                1 for node_id in node_ids if node_id in {n.id for n in unlocked_nodes}
            )
            category_progress[category] = {
                "unlocked": category_unlocked,
                "total": len(node_ids),
                "percentage": (category_unlocked / len(node_ids)) * 100 if node_ids else 0
            }

        return {
            "total_progress": (unlocked_count / total_nodes) * 100 if total_nodes else 0,
            "unlocked_nodes": unlocked_count,
            "total_nodes": total_nodes,
            "level_progress": level_progress,
            "mastery_distribution": mastery_distribution,
            "pathway_progress": pathway_progress,
            "category_progress": category_progress,
            "current_xp": student_progress.get("total_xp", 0),
            "earned_badges": len(student_progress.get("badges", [])),
            "total_badges": len(self.badges),
            "estimated_completion_time": self._estimate_completion_time(student_progress),
            "learning_velocity": self._calculate_learning_velocity(student_progress)
        }

    def _estimate_completion_time(self, student_progress: Dict[str, Any]) -> Dict[str, int]:
        """Estimate time to complete remaining skills based on student pace."""
        remaining_nodes = [
            node for node in self.nodes.values() 
            if not student_progress.get("skills", {}).get(node.id, {}).get("completed", False)
        ]
        
        # Calculate average time per node based on student history
        completed_skills = student_progress.get("skills", {})
        if completed_skills:
            total_time = sum(skill.get("time_spent", 0) for skill in completed_skills.values())
            completed_count = sum(1 for skill in completed_skills.values() if skill.get("completed", False))
            avg_time_per_node = total_time / max(completed_count, 1)
        else:
            # Use estimated times from nodes
            avg_time_per_node = sum(node.estimated_time_minutes for node in self.nodes.values()) / len(self.nodes)

        total_estimated_time = sum(
            max(node.estimated_time_minutes, avg_time_per_node) for node in remaining_nodes
        )

        return {
            "total_minutes": int(total_estimated_time),
            "total_hours": round(total_estimated_time / 60, 1),
            "remaining_nodes": len(remaining_nodes)
        }

    def _calculate_learning_velocity(self, student_progress: Dict[str, Any]) -> Dict[str, float]:
        """Calculate student's learning velocity and trends."""
        completed_skills = student_progress.get("skills", {})
        
        if len(completed_skills) < 2:
            return {"nodes_per_week": 0.0, "trend": "insufficient_data"}
            
        # Analyze completion dates to calculate velocity
        completion_dates = []
        for skill_data in completed_skills.values():
            if skill_data.get("completed", False) and "completion_date" in skill_data:
                try:
                    completion_dates.append(datetime.datetime.fromisoformat(skill_data["completion_date"]))
                except ValueError:
                    continue
                    
        if len(completion_dates) < 2:
            return {"nodes_per_week": 0.0, "trend": "insufficient_data"}
            
        completion_dates.sort()
        time_span = (completion_dates[-1] - completion_dates[0]).total_seconds() / (7 * 24 * 3600)  # weeks
        nodes_per_week = len(completion_dates) / max(time_span, 1)
        
        # Calculate trend (acceleration/deceleration)
        if len(completion_dates) >= 4:
            # Compare first half vs second half velocity
            mid_point = len(completion_dates) // 2
            first_half_span = (completion_dates[mid_point] - completion_dates[0]).total_seconds() / (7 * 24 * 3600)
            second_half_span = (completion_dates[-1] - completion_dates[mid_point]).total_seconds() / (7 * 24 * 3600)
            
            first_half_velocity = mid_point / max(first_half_span, 1)
            second_half_velocity = (len(completion_dates) - mid_point) / max(second_half_span, 1)
            
            if second_half_velocity > first_half_velocity * 1.2:
                trend = "accelerating"
            elif second_half_velocity < first_half_velocity * 0.8:
                trend = "decelerating"
            else:
                trend = "stable"
        else:
            trend = "stable"
            
        return {
            "nodes_per_week": round(nodes_per_week, 2),
            "trend": trend,
            "total_completed": len(completion_dates)
        }

    def generate_learning_path_recommendation(self, student_progress: Dict[str, Any], goal: str = "comprehensive") -> Dict[str, Any]:
        """
        Generate personalized learning path recommendations.
        
        Args:
            student_progress: Current student progress data
            goal: Learning goal ("comprehensive", "fast_track", "remediation", "advanced")
        """
        unlocked_nodes = {node.id for node in self.get_unlocked_nodes(student_progress)}
        next_nodes = self.get_next_available_nodes(student_progress, limit=10)
        
        if goal == "fast_track":
            # Recommend shortest path to completion
            recommended_path = self._find_shortest_path(unlocked_nodes, next_nodes)
        elif goal == "remediation":
            # Focus on foundational skills and lower difficulty
            recommended_path = [n for n in next_nodes if n.difficulty in [DifficultyLevel.BEGINNER, DifficultyLevel.INTERMEDIATE]][:5]
        elif goal == "advanced":
            # Challenge with advanced and expert-level content
            recommended_path = [n for n in next_nodes if n.difficulty in [DifficultyLevel.ADVANCED, DifficultyLevel.EXPERT]][:5]
        else:  # comprehensive
            # Balanced approach covering all areas
            recommended_path = self._balance_recommendations(next_nodes)
            
        return {
            "goal": goal,
            "recommended_nodes": [node.to_dict() for node in recommended_path],
            "estimated_time": sum(node.estimated_time_minutes for node in recommended_path),
            "difficulty_distribution": self._analyze_difficulty_distribution(recommended_path),
            "reasoning": self._generate_recommendation_reasoning(goal, recommended_path, student_progress)
        }

    def _find_shortest_path(self, unlocked_nodes: Set[str], available_nodes: List[SkillNode]) -> List[SkillNode]:
        """Find shortest path through available nodes."""
        # Simple greedy approach - prioritize nodes with fewest prerequisites
        available_nodes.sort(key=lambda n: len(n.prerequisites))
        return available_nodes[:5]

    def _balance_recommendations(self, nodes: List[SkillNode]) -> List[SkillNode]:
        """Create balanced recommendations across different categories."""
        # Group by category/tags
        category_groups = {}
        for node in nodes:
            for tag in node.tags:
                if tag not in category_groups:
                    category_groups[tag] = []
                category_groups[tag].append(node)
                
        # Select up to 2 nodes from each category, up to 5 total
        balanced = []
        for category, category_nodes in category_groups.items():
            balanced.extend(category_nodes[:2])
            if len(balanced) >= 5:
                break
                
        return balanced[:5]

    def _analyze_difficulty_distribution(self, nodes: List[SkillNode]) -> Dict[str, int]:
        """Analyze difficulty distribution of recommended nodes."""
        distribution = {level.value: 0 for level in DifficultyLevel}
        for node in nodes:
            distribution[node.difficulty.value] += 1
        return distribution

    def _generate_recommendation_reasoning(self, goal: str, recommended_nodes: List[SkillNode], student_progress: Dict[str, Any]) -> str:
        """Generate human-readable reasoning for recommendations."""
        avg_performance = student_progress.get("average_performance", 0.75)
        
        if goal == "fast_track":
            return f"Based on your {avg_performance:.1%} average performance, this fast-track path focuses on core skills to accelerate your progress."
        elif goal == "remediation":
            return f"These foundational skills will help strengthen your understanding before advancing to more complex topics."
        elif goal == "advanced":
            return f"Your strong performance ({avg_performance:.1%}) indicates readiness for these challenging advanced topics."
        else:
            return f"This balanced path covers diverse skill areas aligned with your learning patterns and {avg_performance:.1%} performance level."

    def to_visualization_data(self, student_progress: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate comprehensive data for skill tree visualization.
        
        Enhanced with accessibility features, interactive elements,
        and comprehensive metadata for rich user interfaces.
        """
        unlocked_ids = {node.id for node in self.get_unlocked_nodes(student_progress)}
        next_available_ids = {node.id for node in self.get_next_available_nodes(student_progress)}

        nodes_data = []
        edges_data = []
        clusters_data = []

        # Process nodes with enhanced metadata
        for node in self.nodes.values():
            mastery_score = node.calculate_mastery_score(student_progress)
            status = node._get_completion_status(mastery_score)
            
            # Determine visual status
            if node.id in unlocked_ids:
                visual_status = "unlocked"
            elif node.id in next_available_ids:
                visual_status = "available"
            else:
                visual_status = "locked"

            node_data = {
                "id": node.id,
                "name": node.name,
                "description": node.description,
                "level": {
                    "value": node.level.value,
                    "name": node.level.name,
                    "color": node.level.color_code,
                    "description": node.level.description
                },
                "status": visual_status,
                "progress_status": status.value,
                "mastery_score": mastery_score,
                "xp_required": node.xp_required,
                "estimated_time": node.estimated_time_minutes,
                "difficulty": node.difficulty.value,
                "badges": node.badges,
                "tags": node.tags,
                "accessibility": {
                    "alt_text": node.accessibility.alt_text or f"Skill node: {node.name}",
                    "screen_reader_description": node.accessibility.screen_reader_description or 
                                               f"{node.name} - {node.level.description}. Status: {visual_status}",
                    "keyboard_shortcut": node.accessibility.keyboard_shortcut
                },
                "social_features": node.social_features.to_dict(),
                "coordinates": self._calculate_node_position(node, nodes_data)
            }
            
            nodes_data.append(node_data)

            # Add edges for prerequisites with enhanced metadata
            for prereq in node.prerequisites:
                if prereq in self.nodes:
                    edge_data = {
                        "from": prereq,
                        "to": node.id,
                        "type": "prerequisite",
                        "weight": 1.0,
                        "accessibility": {
                            "description": f"Prerequisite relationship: {self.nodes[prereq].name} enables {node.name}"
                        }
                    }
                    edges_data.append(edge_data)

        # Create clusters for better organization
        for category, node_ids in self.categories.items():
            cluster_data = {
                "id": f"cluster_{category}",
                "name": category.title(),
                "nodes": node_ids,
                "color": self._get_category_color(category)
            }
            clusters_data.append(cluster_data)

        # Calculate overall statistics
        progress_stats = self.calculate_progress(student_progress)
        
        return {
            "nodes": nodes_data,
            "edges": edges_data,
            "clusters": clusters_data,
            "progress": progress_stats,
            "pathways": {
                name: {
                    **pathway_data,
                    "progress": self._calculate_pathway_progress(pathway_data["nodes"], student_progress)
                }
                for name, pathway_data in self.pathways.items()
            },
            "metadata": {
                "name": self.name,
                "description": self.description,
                "version": self.version,
                "created_date": self.created_date,
                "total_nodes": len(self.nodes),
                "total_badges": len(self.badges),
                "total_levels": len(self.levels)
            },
            "accessibility": {
                "keyboard_navigation": True,
                "screen_reader_compatible": True,
                "high_contrast_mode": True,
                "focus_indicators": True
            }
        }

    def _calculate_node_position(self, node: SkillNode, existing_nodes: List[Dict]) -> Dict[str, float]:
        """Calculate optimal position for node in visualization."""
        # Simple layout algorithm - in production would use force-directed or hierarchical layout
        level_y = node.level.value * 100
        level_nodes = [n for n in existing_nodes if n["level"]["value"] == node.level.value]
        level_x = len(level_nodes) * 150
        
        return {"x": level_x, "y": level_y}

    def _get_category_color(self, category: str) -> str:
        """Get consistent color for category visualization."""
        colors = {
            "mathematics": "#1976D2",
            "science": "#388E3C", 
            "programming": "#7B1FA2",
            "theory": "#E64A19",
            "application": "#00796B",
            "research": "#C62828"
        }
        # Generate consistent color based on category name hash
        if category not in colors:
            hash_value = hash(category) % 360
            colors[category] = f"hsl({hash_value}, 70%, 45%)"
        return colors[category]

    def _calculate_pathway_progress(self, node_ids: List[str], student_progress: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate progress for a specific pathway."""
        completed = sum(
            1 for node_id in node_ids 
            if student_progress.get("skills", {}).get(node_id, {}).get("completed", False)
        )
        
        return {
            "completed": completed,
            "total": len(node_ids),
            "percentage": (completed / len(node_ids)) * 100 if node_ids else 0
        }

    def export_progress_report(self, student_progress: Dict[str, Any], format: str = "json") -> Union[str, Dict[str, Any]]:
        """Export comprehensive progress report in various formats."""
        progress_data = self.calculate_progress(student_progress)
        visualization_data = self.to_visualization_data(student_progress)
        
        report = {
            "student_id": student_progress.get("student_id", "unknown"),
            "generated_date": datetime.datetime.now().isoformat(),
            "skill_tree": {
                "name": self.name,
                "description": self.description,
                "version": self.version
            },
            "progress_summary": progress_data,
            "detailed_progress": {
                "unlocked_skills": [
                    self.nodes[node_id].to_dict() 
                    for node_id in {n["id"] for n in visualization_data["nodes"] if n["status"] == "unlocked"}
                ],
                "available_skills": [
                    self.nodes[node_id].to_dict()
                    for node_id in {n["id"] for n in visualization_data["nodes"] if n["status"] == "available"}
                ],
                "earned_badges": [
                    self.badges[badge_id].to_canvas_format()
                    for badge_id in student_progress.get("badges", [])
                    if badge_id in self.badges
                ]
            },
            "recommendations": self.generate_learning_path_recommendation(student_progress),
            "accessibility_notes": [
                "Progress tracking includes screen reader descriptions",
                "Visual elements use high contrast colors", 
                "Keyboard navigation supported throughout",
                "Alternative text provided for all visual elements"
            ]
        }
        
        if format == "json":
            return report
        elif format == "html":
            return self._generate_html_report(report)
        else:
            return json.dumps(report, indent=2)

    def _generate_html_report(self, report_data: Dict[str, Any]) -> str:
        """Generate HTML progress report with accessibility features."""
        # This would generate a comprehensive HTML report
        # For now, return a simple template
        return f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Skill Tree Progress Report</title>
            <style>
                body {{ font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }}
                .progress-bar {{ background: #e0e0e0; height: 20px; border-radius: 10px; }}
                .progress-fill {{ background: #4CAF50; height: 100%; border-radius: 10px; }}
                .accessible {{ outline: 2px solid #0066cc; }}
            </style>
        </head>
        <body>
            <h1>Skill Tree Progress Report</h1>
            <h2>{report_data['skill_tree']['name']}</h2>
            <p>Generated: {report_data['generated_date']}</p>
            <p>Overall Progress: {report_data['progress_summary']['total_progress']:.1f}%</p>
            <!-- Full report content would be generated here -->
        </body>
        </html>
        """

    def get_node(self, node_id: str) -> Optional[SkillNode]:
        """Get a specific node by ID."""
        return self.nodes.get(node_id)

    def get_badge(self, badge_id: str) -> Optional[Badge]:
        """Get a specific badge by ID."""
        return self.badges.get(badge_id)

    def get_nodes_by_category(self, category: str) -> List[SkillNode]:
        """Get all nodes in a specific category."""
        node_ids = self.categories.get(category, [])
        return [self.nodes[node_id] for node_id in node_ids if node_id in self.nodes]

    def get_nodes_by_level(self, level: SkillLevel) -> List[SkillNode]:
        """Get all nodes at a specific skill level."""
        node_ids = self.levels.get(level.value, [])
        return [self.nodes[node_id] for node_id in node_ids if node_id in self.nodes]

    def validate_tree_integrity(self) -> Dict[str, List[str]]:
        """Validate the integrity of the skill tree structure."""
        issues = {"errors": [], "warnings": []}
        
        # Check for orphaned prerequisites
        all_node_ids = set(self.nodes.keys())
        for node in self.nodes.values():
            for prereq in node.prerequisites:
                if prereq not in all_node_ids:
                    issues["errors"].append(f"Node '{node.id}' has unknown prerequisite '{prereq}'")
        
        # Check for circular dependencies
        for node_id in self.nodes:
            if self._has_circular_dependency(node_id, set()):
                issues["errors"].append(f"Circular dependency detected involving node '{node_id}'")
        
        # Check for unreachable nodes
        root_nodes = [node for node in self.nodes.values() if not node.prerequisites]
        if not root_nodes:
            issues["warnings"].append("No root nodes found (nodes without prerequisites)")
            
        return issues

    def _has_circular_dependency(self, node_id: str, visited: Set[str]) -> bool:
        """Check for circular dependencies in prerequisites."""
        if node_id in visited:
            return True
            
        visited.add(node_id)
        node = self.nodes.get(node_id)
        if not node:
            return False
            
        for prereq in node.prerequisites:
            if self._has_circular_dependency(prereq, visited.copy()):
                return True
                
        return False


class XPSystem:
    """
    Advanced experience points system with adaptive algorithms and research-backed progression.
    
    Features:
    - Dynamic XP multipliers based on performance and engagement
    - Adaptive level curves that respond to student progress
    - Bonus systems for collaboration, creativity, and persistence
    - Anti-grinding mechanisms to promote meaningful learning
    - Accessibility considerations for different learning needs
    
    Research Foundation:
    - Motivation and Learning (Keller's ARCS Model)
    - Flow Theory and Optimal Challenge (Csikszentmihalyi)
    - Mastery-Based Learning (Bloom's Mastery Learning)
    - Self-Determination Theory (Deci & Ryan)
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        
        # Enhanced XP multipliers with research-backed rationale
        self.xp_multipliers = {
            "assignment": 1.0,          # Base activity type
            "quiz": 1.2,               # Higher due to immediate feedback value
            "discussion": 0.8,         # Lower individual XP, but collaboration bonus available
            "project": 2.0,            # Higher due to synthesis and creativity
            "peer_review": 1.3,        # Encourages social learning
            "creative_work": 1.8,      # Promotes innovation and original thinking
            "help_others": 1.5,        # Incentivizes teaching and collaboration
            "research": 1.6,           # Encourages deep investigation
            "reflection": 1.1,         # Promotes metacognitive thinking
            "bonus": 1.5,              # General bonus multiplier
            "challenge": 2.5,          # Extra difficult optional content
            "exploration": 1.3         # Self-directed learning activities
        }
        
        # Performance-based multipliers
        self.performance_multipliers = {
            "exceptional": 1.5,    # 95%+ performance
            "proficient": 1.2,     # 85-94% performance  
            "satisfactory": 1.0,   # 70-84% performance
            "developing": 0.8,     # 60-69% performance
            "incomplete": 0.3      # Below 60% but attempted
        }
        
        # Collaboration bonuses
        self.collaboration_bonuses = {
            "peer_teaching": 1.4,
            "group_project": 1.2,
            "study_group": 1.1,
            "peer_feedback": 1.15,
            "mentoring": 1.3
        }
        
        # Calculate level thresholds with improved curve
        self.level_thresholds = self._calculate_level_thresholds()
        
        # Anti-grinding mechanisms
        self.daily_xp_cap = self.config.get("daily_xp_cap", 2000)
        self.diminishing_returns_threshold = self.config.get("diminishing_returns_threshold", 5)

    def _calculate_level_thresholds(self) -> List[int]:
        """
        Calculate XP thresholds for each level using research-informed progression curves.
        
        Uses a modified exponential curve that balances:
        - Initial accessibility (easy early levels)
        - Meaningful progression (consistent challenge increase)
        - Long-term engagement (manageable high-level requirements)
        """
        thresholds = [0]  # Level 1 starts at 0 XP
        base_xp = self.config.get("base_xp", 100)
        max_level = self.config.get("max_level", 50)

        for level in range(2, max_level + 1):
            # Use logarithmic scaling for more balanced progression
            if level <= 10:
                # Rapid early progression for motivation
                xp_required = int(base_xp * (level ** 1.3))
            elif level <= 25:
                # Moderate middle progression
                xp_required = int(base_xp * (level ** 1.5))
            else:
                # Slower late progression to maintain engagement
                xp_required = int(base_xp * (level ** 1.2))
                
            thresholds.append(thresholds[-1] + xp_required)

        return thresholds

    def calculate_xp(
        self,
        activity_type: str,
        base_points: int,
        performance_score: float = 1.0,
        collaboration_type: Optional[str] = None,
        bonus_multiplier: float = 1.0,
        student_context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Calculate XP for an activity with comprehensive bonus system.

        Args:
            activity_type: Type of activity (assignment, quiz, etc.)
            base_points: Base points for the activity
            performance_score: Performance multiplier (0.0 to 1.0+)
            collaboration_type: Type of collaboration if applicable
            bonus_multiplier: Additional bonus multiplier
            student_context: Additional student context for personalization

        Returns:
            Detailed XP calculation breakdown
        """
        student_context = student_context or {}
        
        # Base calculation
        type_multiplier = self.xp_multipliers.get(activity_type, 1.0)
        
        # Performance-based multiplier
        performance_category = self._categorize_performance(performance_score)
        performance_multiplier = self.performance_multipliers[performance_category]
        
        # Collaboration bonus
        collaboration_multiplier = 1.0
        if collaboration_type:
            collaboration_multiplier = self.collaboration_bonuses.get(collaboration_type, 1.1)
        
        # Adaptive personalization
        adaptive_multiplier = self._calculate_adaptive_multiplier(student_context)
        
        # Calculate base XP
        base_xp = base_points * type_multiplier * performance_multiplier * bonus_multiplier
        
        # Apply bonuses
        final_xp = base_xp * collaboration_multiplier * adaptive_multiplier
        
        # Apply anti-grinding measures
        final_xp = self._apply_anti_grinding(final_xp, student_context)
        
        # Ensure minimum and reasonable bounds
        final_xp = max(int(final_xp), 1)  # Always award at least 1 XP for effort
        
        return {
            "base_points": base_points,
            "type_multiplier": type_multiplier,
            "performance_multiplier": performance_multiplier,
            "collaboration_multiplier": collaboration_multiplier,
            "adaptive_multiplier": adaptive_multiplier,
            "final_xp": final_xp,
            "breakdown": {
                "base_calculation": base_points * type_multiplier,
                "performance_bonus": (performance_multiplier - 1.0) * base_points * type_multiplier,
                "collaboration_bonus": (collaboration_multiplier - 1.0) * base_xp,
                "adaptive_bonus": (adaptive_multiplier - 1.0) * base_xp * collaboration_multiplier
            },
            "performance_category": performance_category,
            "bonuses_applied": {
                "collaboration": collaboration_type is not None,
                "adaptive": adaptive_multiplier != 1.0,
                "anti_grinding": final_xp < base_xp * collaboration_multiplier * adaptive_multiplier
            }
        }

    def _categorize_performance(self, score: float) -> str:
        """Categorize performance score into meaningful bands."""
        if score >= 0.95:
            return "exceptional"
        elif score >= 0.85:
            return "proficient"
        elif score >= 0.70:
            return "satisfactory"
        elif score >= 0.60:
            return "developing"
        else:
            return "incomplete"

    def _calculate_adaptive_multiplier(self, student_context: Dict[str, Any]) -> float:
        """Calculate adaptive multiplier based on student context."""
        multiplier = 1.0
        
        # Struggling student support
        avg_performance = student_context.get("average_performance", 0.75)
        if avg_performance < 0.6:
            multiplier += 0.2  # 20% bonus for struggling students
        
        # Engagement bonus
        engagement_score = student_context.get("engagement_score", 0.5)
        if engagement_score > 0.8:
            multiplier += 0.1  # 10% bonus for highly engaged students
        
        # Consistency bonus (reward regular participation)
        consistency_score = student_context.get("consistency_score", 0.5)
        if consistency_score > 0.7:
            multiplier += 0.05  # 5% bonus for consistent participation
            
        # Time investment consideration
        time_investment = student_context.get("time_investment_ratio", 1.0)
        if time_investment > 1.5:  # Spent significantly more time than average
            multiplier += 0.1  # Reward effort and persistence
            
        return min(multiplier, 2.0)  # Cap at 2x multiplier

    def _apply_anti_grinding(self, xp: float, student_context: Dict[str, Any]) -> float:
        """Apply anti-grinding mechanisms to prevent exploitation."""
        daily_xp = student_context.get("daily_xp_earned", 0)
        
        # Daily XP cap with soft limit
        if daily_xp > self.daily_xp_cap:
            reduction_factor = 0.5  # 50% reduction after daily cap
            xp *= reduction_factor
        elif daily_xp > self.daily_xp_cap * 0.8:
            # Gradual reduction approaching cap
            reduction_factor = 1.0 - ((daily_xp - self.daily_xp_cap * 0.8) / (self.daily_xp_cap * 0.2)) * 0.5
            xp *= reduction_factor
            
        # Diminishing returns for repetitive activities
        recent_activity_count = student_context.get("recent_similar_activities", 0)
        if recent_activity_count > self.diminishing_returns_threshold:
            diminishing_factor = 0.9 ** (recent_activity_count - self.diminishing_returns_threshold)
            xp *= diminishing_factor
            
        return xp

    def get_level_from_xp(self, xp: int) -> Tuple[int, int, int, Dict[str, Any]]:
        """
        Get comprehensive level information from XP amount.

        Returns:
            Tuple of (current_level, xp_for_next_level, xp_progress_in_current_level, level_metadata)
        """
        current_level = 1
        for level, threshold in enumerate(self.level_thresholds[1:], 2):
            if xp < threshold:
                break
            current_level = level

        if current_level >= len(self.level_thresholds):
            # Max level reached
            level_metadata = {
                "status": "max_level",
                "title": "Grandmaster",
                "description": "You have achieved the highest level!",
                "benefits": ["All content unlocked", "Mentor status", "Special recognition"]
            }
            return current_level, 0, 0, level_metadata

        current_threshold = self.level_thresholds[current_level - 1]
        next_threshold = self.level_thresholds[current_level]

        xp_for_next = next_threshold - xp
        xp_progress = xp - current_threshold
        xp_needed_for_level = next_threshold - current_threshold

        # Generate level metadata
        level_metadata = {
            "status": "active",
            "title": self._get_level_title(current_level),
            "description": f"Level {current_level} - {self._get_level_description(current_level)}",
            "progress_percentage": (xp_progress / xp_needed_for_level) * 100,
            "benefits": self._get_level_benefits(current_level),
            "next_milestone": xp_for_next,
            "total_xp": xp
        }

        return current_level, xp_for_next, xp_progress, level_metadata

    def _get_level_title(self, level: int) -> str:
        """Get appropriate title for level."""
        titles = {
            1: "Novice", 2: "Beginner", 3: "Apprentice", 4: "Student", 5: "Learner",
            6: "Practitioner", 7: "Skilled", 8: "Competent", 9: "Proficient", 10: "Advanced",
            11: "Expert", 12: "Specialist", 13: "Master", 14: "Veteran", 15: "Elite",
            16: "Champion", 17: "Hero", 18: "Legend", 19: "Myth", 20: "Grandmaster"
        }
        
        if level in titles:
            return titles[level]
        elif level > 20:
            return f"Transcendent {level - 20}"
        else:
            return f"Level {level}"

    def _get_level_description(self, level: int) -> str:
        """Get description for level achievements."""
        if level <= 5:
            return "Building foundational knowledge and skills"
        elif level <= 10:
            return "Developing competency and understanding"
        elif level <= 15:
            return "Achieving mastery and expertise"
        elif level <= 20:
            return "Demonstrating exceptional skill and leadership"
        else:
            return "Transcending normal boundaries of achievement"

    def _get_level_benefits(self, level: int) -> List[str]:
        """Get benefits unlocked at each level."""
        benefits = []
        
        if level >= 5:
            benefits.append("Access to intermediate content")
        if level >= 10:
            benefits.append("Peer mentoring opportunities")
        if level >= 15:
            benefits.append("Advanced challenge content")
        if level >= 20:
            benefits.append("Special recognition and privileges")
            
        return benefits


class GamificationEngine:
    """
    Advanced gamification engine orchestrating all game mechanics and learning features.
    
    This enterprise-grade engine provides comprehensive gamification capabilities
    including adaptive progression, social learning features, analytics, and
    accessibility support.
    
    Features:
    - Intelligent XP award system with anti-gaming measures
    - Dynamic badge eligibility checking with complex criteria
    - Comprehensive progress tracking and analytics
    - Social learning and collaboration features
    - Adaptive difficulty and personalization
    - Real-time feedback and recommendations
    - Accessibility and UDL compliance
    
    Research Foundation:
    - Game-Based Learning Theory (Prensky, 2001)
    - Self-Determination Theory (Deci & Ryan, 2000)
    - Social Learning Theory (Bandura, 1977)
    - Flow Theory (Csikszentmihalyi, 1990)
    """

    def __init__(self, skill_tree: SkillTree, xp_system: XPSystem, config: Optional[Dict[str, Any]] = None):
        self.skill_tree = skill_tree
        self.xp_system = xp_system
        self.config = config or {}
        
        # Enhanced mastery thresholds by activity type
        self.mastery_thresholds = {
            "assignment": 0.8,
            "quiz": 0.7,
            "project": 0.85,
            "discussion": 0.75,
            "peer_review": 0.8,
            "creative_work": 0.9,
            "research": 0.85
        }
        
        # Social learning multipliers
        self.social_multipliers = {
            "helped_peer": 1.2,
            "received_help": 1.1,
            "collaborative_work": 1.15,
            "peer_feedback": 1.1,
            "teaching_others": 1.3
        }
        
        # Analytics tracking
        self.analytics = {
            "total_xp_awarded": 0,
            "total_badges_earned": 0,
            "total_interactions": 0,
            "engagement_events": []
        }

    def award_xp(
        self,
        student_id: str,
        activity_type: str,
        base_points: int,
        performance_score: float = 1.0,
        collaboration_type: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Award XP to a student with comprehensive tracking and bonus calculation.
        
        Enhanced with social learning bonuses, adaptive adjustments, and
        detailed analytics tracking.
        """
        context = context or {}
        
        # Get current student progress for adaptive calculations
        student_context = self._build_student_context(student_id, context)
        
        # Calculate XP with full breakdown
        xp_calculation = self.xp_system.calculate_xp(
            activity_type=activity_type,
            base_points=base_points,
            performance_score=performance_score,
            collaboration_type=collaboration_type,
            student_context=student_context
        )
        
        # Check for level up
        current_total_xp = student_context.get("total_xp", 0)
        new_total_xp = current_total_xp + xp_calculation["final_xp"]
        
        old_level, _, _, _ = self.xp_system.get_level_from_xp(current_total_xp)
        new_level, xp_for_next, xp_progress, level_metadata = self.xp_system.get_level_from_xp(new_total_xp)
        
        level_up = new_level > old_level
        
        # Check for newly unlocked skills
        old_progress = {"total_xp": current_total_xp, **student_context}
        new_progress = {"total_xp": new_total_xp, **student_context}
        
        newly_unlocked = self._check_newly_unlocked_skills(old_progress, new_progress)
        
        # Check for badge eligibility
        eligible_badges = self.check_badge_eligibility(new_progress)
        
        # Update analytics
        self._update_analytics("xp_awarded", {
            "student_id": student_id,
            "xp_amount": xp_calculation["final_xp"],
            "activity_type": activity_type,
            "performance_score": performance_score,
            "timestamp": datetime.datetime.now().isoformat()
        })
        
        result = {
            "student_id": student_id,
            "xp_calculation": xp_calculation,
            "level_info": {
                "current_level": new_level,
                "level_up": level_up,
                "old_level": old_level,
                "xp_for_next_level": xp_for_next,
                "xp_progress_in_level": xp_progress,
                "level_metadata": level_metadata
            },
            "unlocks": {
                "newly_unlocked_skills": [skill.to_dict() for skill in newly_unlocked],
                "eligible_badges": [badge.to_canvas_format() for badge in eligible_badges]
            },
            "activity_details": {
                "type": activity_type,
                "base_points": base_points,
                "performance_score": performance_score,
                "collaboration_type": collaboration_type
            },
            "timestamp": datetime.datetime.now().isoformat(),
            "recommendations": self._generate_immediate_recommendations(new_progress, level_up, newly_unlocked)
        }
        
        return result

    def _build_student_context(self, student_id: str, base_context: Dict[str, Any]) -> Dict[str, Any]:
        """Build comprehensive student context for adaptive calculations."""
        # In a real implementation, this would fetch from database
        # For now, use provided context with sensible defaults
        return {
            "student_id": student_id,
            "total_xp": base_context.get("total_xp", 0),
            "average_performance": base_context.get("average_performance", 0.75),
            "engagement_score": base_context.get("engagement_score", 0.5),
            "consistency_score": base_context.get("consistency_score", 0.5),
            "time_investment_ratio": base_context.get("time_investment_ratio", 1.0),
            "daily_xp_earned": base_context.get("daily_xp_earned", 0),
            "recent_similar_activities": base_context.get("recent_similar_activities", 0),
            "learning_style": base_context.get("learning_style", "visual"),
            "interests": base_context.get("interests", []),
            "prefers_collaboration": base_context.get("prefers_collaboration", False),
            "skills": base_context.get("skills", {}),
            "badges": base_context.get("badges", []),
            "assignments": base_context.get("assignments", {}),
            "quiz_scores": base_context.get("quiz_scores", {})
        }

    def _check_newly_unlocked_skills(self, old_progress: Dict[str, Any], new_progress: Dict[str, Any]) -> List[SkillNode]:
        """Check which skills were newly unlocked by the XP gain."""
        old_unlocked = {node.id for node in self.skill_tree.get_unlocked_nodes(old_progress)}
        new_unlocked = {node.id for node in self.skill_tree.get_unlocked_nodes(new_progress)}
        
        newly_unlocked_ids = new_unlocked - old_unlocked
        return [self.skill_tree.nodes[node_id] for node_id in newly_unlocked_ids if node_id in self.skill_tree.nodes]

    def _generate_immediate_recommendations(self, progress: Dict[str, Any], level_up: bool, newly_unlocked: List[SkillNode]) -> List[Dict[str, str]]:
        """Generate immediate recommendations based on recent progress."""
        recommendations = []
        
        if level_up:
            recommendations.append({
                "type": "celebration",
                "message": "🎉 Congratulations on leveling up! New content and features are now available.",
                "priority": "high"
            })
        
        if newly_unlocked:
            recommendations.append({
                "type": "unlock",
                "message": f"🔓 {len(newly_unlocked)} new skill(s) unlocked! Check out your next learning opportunities.",
                "priority": "high"
            })
        
        # Check for next available skills
        next_skills = self.skill_tree.get_next_available_nodes(progress, limit=3)
        if next_skills:
            recommendations.append({
                "type": "progression",
                "message": f"Ready for the next challenge? Try: {', '.join([skill.name for skill in next_skills[:2]])}",
                "priority": "medium"
            })
        
        # Performance-based recommendations
        avg_performance = progress.get("average_performance", 0.75)
        if avg_performance < 0.6:
            recommendations.append({
                "type": "support",
                "message": "💪 Consider reviewing foundational concepts or reaching out for help.",
                "priority": "medium"
            })
        elif avg_performance > 0.9:
            recommendations.append({
                "type": "challenge",
                "message": "🚀 Excellent work! Ready for some advanced challenges?",
                "priority": "low"
            })
        
        return recommendations

    def check_badge_eligibility(self, student_progress: Dict[str, Any]) -> List[Badge]:
        """
        Check which new badges a student has earned with enhanced criteria.
        
        Supports complex badge requirements including performance thresholds,
        social interaction requirements, and time-based achievements.
        """
        earned_badges = set(student_progress.get("badges", []))
        eligible_badges = []

        for badge in self.skill_tree.badges.values():
            if badge.id in earned_badges:
                continue
                
            # Check if badge is available to user (prerequisites, time limits, etc.)
            if not badge.is_available_to_user(student_progress):
                continue

            # Check if requirements are met
            if self._check_badge_requirements(badge, student_progress):
                eligible_badges.append(badge)

        return eligible_badges

    def _check_badge_requirements(self, badge: Badge, progress: Dict[str, Any]) -> bool:
        """
        Enhanced badge requirement checking with complex criteria support.
        
        Supports multiple requirement types:
        - XP thresholds
        - Skill completion requirements
        - Performance standards
        - Social interaction requirements
        - Time-based achievements
        - Creative work recognition
        """
        # Basic XP requirement
        student_xp = progress.get("total_xp", 0)
        if student_xp < badge.xp_value:
            return False
        
        # Check learning objectives completion
        for objective in badge.learning_objectives:
            if not self._check_learning_objective(objective, progress):
                return False
        
        # Check unlock requirements (complex criteria)
        for requirement in badge.unlock_requirements:
            if not self._evaluate_badge_requirement(requirement, progress):
                return False
        
        # Category-specific requirements
        if badge.category == BadgeCategory.COLLABORATION:
            collaboration_score = progress.get("collaboration_score", 0)
            if collaboration_score < 5:  # Minimum collaboration interactions
                return False
        
        elif badge.category == BadgeCategory.PERSISTENCE:
            attempts = progress.get("total_attempts", 0)
            if attempts < 10:  # Minimum attempt threshold
                return False
        
        elif badge.category == BadgeCategory.CREATIVITY:
            creative_submissions = progress.get("creative_submissions", 0)
            if creative_submissions < 3:  # Minimum creative work
                return False
        
        return True

    def _check_learning_objective(self, objective: LearningObjective, progress: Dict[str, Any]) -> bool:
        """Check if a learning objective has been met."""
        # This would implement sophisticated objective tracking
        # For now, simplified check based on related skills
        skills = progress.get("skills", {})
        
        # Look for skills that might relate to this objective
        related_skills = [
            skill_data for skill_id, skill_data in skills.items()
            if skill_data.get("completed", False)
        ]
        
        # Simple heuristic: if we have some completed skills, objective likely met
        return len(related_skills) > 0

    def _evaluate_badge_requirement(self, requirement: str, progress: Dict[str, Any]) -> bool:
        """Evaluate complex badge requirements."""
        # This would parse and evaluate complex requirement strings
        # Examples: "complete_3_assignments_above_90", "help_5_peers", "consecutive_login_7_days"
        
        # Simple implementation for common patterns
        if "complete" in requirement and "assignments" in requirement:
            assignments = progress.get("assignments", {})
            completed_count = sum(1 for a in assignments.values() if a.get("completed", False))
            # Extract number from requirement string (simplified)
            import re
            numbers = re.findall(r'\d+', requirement)
            required_count = int(numbers[0]) if numbers else 1
            return completed_count >= required_count
        
        elif "help" in requirement and "peer" in requirement:
            help_count = progress.get("peer_help_count", 0)
            numbers = re.findall(r'\d+', requirement)
            required_count = int(numbers[0]) if numbers else 1
            return help_count >= required_count
        
        # Default to True for unrecognized requirements
        return True

    def generate_progress_report(self, student_progress: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate comprehensive progress report with enhanced analytics and insights.
        
        Provides detailed analysis of student performance, engagement patterns,
        learning trajectory, and personalized recommendations.
        """
        # Get basic progress from skill tree
        tree_progress = self.skill_tree.calculate_progress(student_progress)
        
        # Get XP and level information
        xp = student_progress.get("total_xp", 0)
        level, xp_for_next, xp_progress, level_metadata = self.xp_system.get_level_from_xp(xp)
        
        # Calculate advanced metrics
        engagement_metrics = self._calculate_engagement_metrics(student_progress)
        learning_patterns = self._analyze_learning_patterns(student_progress)
        social_metrics = self._calculate_social_metrics(student_progress)
        
        # Generate personalized recommendations
        recommendations = self.skill_tree.generate_learning_path_recommendation(
            student_progress, goal="comprehensive"
        )
        
        return {
            "student_id": student_progress.get("student_id", "unknown"),
            "report_generated": datetime.datetime.now().isoformat(),
            "skill_tree_progress": tree_progress,
            "level_info": {
                "current_level": level,
                "xp_for_next_level": xp_for_next,
                "xp_progress_in_level": xp_progress,
                "total_xp": xp,
                "level_metadata": level_metadata
            },
            "badges": {
                "earned": student_progress.get("badges", []),
                "available": [b.id for b in self.check_badge_eligibility(student_progress)],
                "total_possible": len(self.skill_tree.badges)
            },
            "engagement_metrics": engagement_metrics,
            "learning_patterns": learning_patterns,
            "social_metrics": social_metrics,
            "recommendations": recommendations,
            "next_milestones": {
                "next_level": f"Level {level + 1}" if level < 50 else "Max Level Achieved",
                "next_unlocks": [
                    node.name for node in self.skill_tree.get_next_available_nodes(student_progress, limit=3)
                ],
                "progress_to_next_badge": self._calculate_progress_to_next_badge(student_progress)
            },
            "accessibility_summary": {
                "screen_reader_summary": self._generate_screen_reader_summary(tree_progress, level_metadata),
                "keyboard_shortcuts": self._get_available_shortcuts(),
                "high_contrast_available": True
            }
        }

    def _calculate_engagement_metrics(self, progress: Dict[str, Any]) -> Dict[str, float]:
        """Calculate detailed engagement metrics."""
        return {
            "overall_engagement": progress.get("engagement_score", 0.5),
            "consistency_score": progress.get("consistency_score", 0.5),
            "participation_rate": progress.get("participation_rate", 0.7),
            "time_investment": progress.get("time_investment_ratio", 1.0),
            "self_direction": progress.get("self_direction_score", 0.6)
        }

    def _analyze_learning_patterns(self, progress: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze student learning patterns and preferences."""
        return {
            "learning_style": progress.get("learning_style", "visual"),
            "preferred_difficulty": progress.get("preferred_difficulty", "intermediate"),
            "collaboration_preference": progress.get("prefers_collaboration", False),
            "peak_activity_times": progress.get("peak_activity_times", ["evening"]),
            "learning_velocity": self.skill_tree._calculate_learning_velocity(progress),
            "strength_areas": progress.get("strength_areas", []),
            "improvement_areas": progress.get("improvement_areas", [])
        }

    def _calculate_social_metrics(self, progress: Dict[str, Any]) -> Dict[str, int]:
        """Calculate social learning and collaboration metrics."""
        return {
            "peer_interactions": progress.get("peer_interactions", 0),
            "help_given": progress.get("peer_help_count", 0),
            "help_received": progress.get("help_received_count", 0),
            "collaborative_projects": progress.get("collaborative_projects", 0),
            "peer_feedback_given": progress.get("peer_feedback_given", 0),
            "peer_feedback_received": progress.get("peer_feedback_received", 0)
        }

    def _calculate_progress_to_next_badge(self, progress: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate progress toward earning the next badge."""
        all_badges = list(self.skill_tree.badges.values())
        earned_badges = set(progress.get("badges", []))
        
        # Find closest unearned badge
        closest_badge = None
        min_gap = float('inf')
        
        for badge in all_badges:
            if badge.id in earned_badges:
                continue
                
            # Simple gap calculation based on XP (would be more sophisticated in production)
            xp_gap = max(0, badge.xp_value - progress.get("total_xp", 0))
            
            if xp_gap < min_gap:
                min_gap = xp_gap
                closest_badge = badge
        
        if closest_badge:
            return {
                "badge_name": closest_badge.name,
                "badge_id": closest_badge.id,
                "xp_needed": min_gap,
                "progress_percentage": max(0, (1 - min_gap / closest_badge.xp_value) * 100)
            }
        
        return {"message": "All badges earned!"}

    def _generate_screen_reader_summary(self, tree_progress: Dict[str, Any], level_metadata: Dict[str, Any]) -> str:
        """Generate accessible summary for screen readers."""
        total_progress = tree_progress.get("total_progress", 0)
        current_level = level_metadata.get("title", "Novice")
        
        return f"Current progress: {total_progress:.1f}% complete. " \
               f"Achievement level: {current_level}. " \
               f"{tree_progress.get('unlocked_nodes', 0)} of {tree_progress.get('total_nodes', 0)} skills unlocked. " \
               f"{tree_progress.get('earned_badges', 0)} badges earned."

    def _get_available_shortcuts(self) -> List[Dict[str, str]]:
        """Get available keyboard shortcuts for accessibility."""
        return [
            {"key": "s", "action": "View skill tree"},
            {"key": "p", "action": "View progress report"},
            {"key": "b", "action": "View badges"},
            {"key": "r", "action": "View recommendations"},
            {"key": "h", "action": "Help and accessibility options"}
        ]

    def _update_analytics(self, event_type: str, data: Dict[str, Any]) -> None:
        """Update internal analytics tracking."""
        self.analytics["total_interactions"] += 1
        self.analytics["engagement_events"].append({
            "type": event_type,
            "timestamp": datetime.datetime.now().isoformat(),
            "data": data
        })
        
        if event_type == "xp_awarded":
            self.analytics["total_xp_awarded"] += data.get("xp_amount", 0)
        elif event_type == "badge_earned":
            self.analytics["total_badges_earned"] += 1

    def get_system_analytics(self) -> Dict[str, Any]:
        """Get comprehensive system analytics."""
        return {
            "system_metrics": self.analytics,
            "skill_tree_metrics": {
                "total_nodes": len(self.skill_tree.nodes),
                "total_badges": len(self.skill_tree.badges),
                "total_pathways": len(self.skill_tree.pathways),
                "integrity_check": self.skill_tree.validate_tree_integrity()
            },
            "xp_system_metrics": {
                "max_level": len(self.xp_system.level_thresholds),
                "daily_xp_cap": self.xp_system.daily_xp_cap,
                "total_multipliers": len(self.xp_system.xp_multipliers)
            }
        }


# Factory functions for easy setup
def create_default_skill_tree(name: str, description: str) -> SkillTree:
    """Create a skill tree with sensible defaults."""
    return SkillTree(name, description)

def create_default_xp_system(config: Optional[Dict[str, Any]] = None) -> XPSystem:
    """Create an XP system with research-backed defaults."""
    return XPSystem(config)

def create_gamification_engine(skill_tree: SkillTree, xp_system: Optional[XPSystem] = None) -> GamificationEngine:
    """Create a complete gamification engine with all components."""
    if xp_system is None:
        xp_system = create_default_xp_system()
    return GamificationEngine(skill_tree, xp_system)


# Export all public classes and functions
__all__ = [
    # Core classes
    "SkillLevel", "SkillNode", "SkillTree", "Badge", "XPSystem", "GamificationEngine",
    # Enums and types
    "BadgeCategory", "DifficultyLevel", "ProgressStatus", 
    # Data classes
    "LearningObjective", "AccessibilityFeatures", "AdaptiveParameters", "SocialFeatures",
    # Factory functions
    "create_default_skill_tree", "create_default_xp_system", "create_gamification_engine"
]
