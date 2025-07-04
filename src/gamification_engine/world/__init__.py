"""
🌍 WORLD BUILDING SYSTEM - Minecraft & Factorio Inspired Learning Spaces
Mathematical dimensions, base building, resource gathering, and exploration quests
"""

import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Set, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import uuid
import random

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WorldDimension(Enum):
    """Different mathematical dimensions to explore"""
    VECTOR_SPACE = "Vector Space"
    MATRIX_REALM = "Matrix Realm" 
    TRANSFORMATION_GALAXY = "Transformation Galaxy"
    EIGENVALUE_UNIVERSE = "Eigenvalue Universe"
    ABSTRACT_ALGEBRA_VOID = "Abstract Algebra Void"

class ResourceType(Enum):
    """Mathematical resources that can be gathered"""
    VECTOR_CRYSTALS = "Vector Crystals"
    MATRIX_STONES = "Matrix Stones"
    DETERMINANT_GEMS = "Determinant Gems"
    EIGENVALUE_SHARDS = "Eigenvalue Shards"
    LINEAR_ESSENCE = "Linear Essence"
    TRANSFORMATION_ENERGY = "Transformation Energy"
    KNOWLEDGE_FRAGMENTS = "Knowledge Fragments"

class BuildingType(Enum):
    """Types of structures students can build"""
    STUDY_DESK = "Study Desk"
    CALCULATION_LAB = "Calculation Laboratory"
    MATRIX_FORGE = "Matrix Forge"
    VECTOR_GARDEN = "Vector Garden"
    EIGEN_OBSERVATORY = "Eigen Observatory"
    KNOWLEDGE_LIBRARY = "Knowledge Library"
    COLLABORATION_HALL = "Collaboration Hall"
    PRACTICE_ARENA = "Practice Arena"

class QuestType(Enum):
    """Different types of exploration quests"""
    RESOURCE_GATHERING = "Resource Gathering"
    CONCEPT_DISCOVERY = "Concept Discovery"
    THEOREM_EXPEDITION = "Theorem Expedition"
    PROBLEM_ARCHAEOLOGY = "Problem Archaeology"
    KNOWLEDGE_MAPPING = "Knowledge Mapping"

@dataclass
class Resource:
    """A mathematical resource item"""
    resource_type: ResourceType
    quantity: int
    quality: float = 1.0  # 0.5-2.0 multiplier for effectiveness
    discovery_location: str = ""
    discovery_date: datetime = None
    
    def __post_init__(self):
        if self.discovery_date is None:
            self.discovery_date = datetime.now()

@dataclass
class Building:
    """A structure in a student's base"""
    building_id: str
    building_type: BuildingType
    level: int = 1
    position: Tuple[int, int] = (0, 0)  # x, y coordinates
    
    # Building stats
    efficiency: float = 1.0
    capacity: int = 100
    energy_cost: int = 10
    
    # Upgrades and customization
    upgrades: List[str] = None
    decorations: List[str] = None
    custom_name: str = ""
    
    # Functionality
    production_rate: float = 1.0  # Resources or benefits per hour
    last_collected: datetime = None
    
    def __post_init__(self):
        if self.upgrades is None:
            self.upgrades = []
        if self.decorations is None:
            self.decorations = []
        if self.last_collected is None:
            self.last_collected = datetime.now()
        if not self.custom_name:
            self.custom_name = f"My {self.building_type.value}"

@dataclass
class StudyBase:
    """Student's personal base/headquarters"""
    base_id: str
    owner_id: str
    base_name: str
    dimension: WorldDimension
    
    # Base layout and buildings
    size: Tuple[int, int] = (20, 20)  # width, height
    buildings: Dict[str, Building] = None
    
    # Resources and inventory
    resources: Dict[ResourceType, int] = None
    total_energy: int = 100
    energy_capacity: int = 100
    
    # Base stats and progression
    base_level: int = 1
    total_value: int = 0  # Sum of all building values
    aesthetic_score: float = 1.0  # How well-decorated the base is
    
    # Visitor and social features
    public_visits: int = 0
    visitor_ratings: List[float] = None
    featured_base: bool = False
    
    def __post_init__(self):
        if self.buildings is None:
            self.buildings = {}
        if self.resources is None:
            self.resources = {resource_type: 0 for resource_type in ResourceType}
        if self.visitor_ratings is None:
            self.visitor_ratings = []

@dataclass
class ExplorationQuest:
    """Quest for exploring mathematical concepts"""
    quest_id: str
    title: str
    description: str
    quest_type: QuestType
    target_concept: str
    dimension: WorldDimension
    
    # Quest objectives
    objectives: List[str] = None
    progress: Dict[str, float] = None  # objective_id -> completion %
    
    # Rewards
    xp_reward: int = 100
    resource_rewards: Dict[ResourceType, int] = None
    building_unlock: Optional[BuildingType] = None
    
    # Quest timeline
    start_time: datetime = None
    deadline: Optional[datetime] = None
    completion_time: Optional[datetime] = None
    
    # Difficulty and requirements
    difficulty_level: int = 1  # 1-10
    required_level: int = 1
    prerequisite_quests: List[str] = None
    
    def __post_init__(self):
        if self.objectives is None:
            self.objectives = []
        if self.progress is None:
            self.progress = {}
        if self.resource_rewards is None:
            self.resource_rewards = {}
        if self.prerequisite_quests is None:
            self.prerequisite_quests = []
        if self.start_time is None:
            self.start_time = datetime.now()

class WorldBuilder:
    """Main engine for world building and exploration"""
    
    def __init__(self):
        self.study_bases: Dict[str, StudyBase] = {}
        self.exploration_quests: Dict[str, ExplorationQuest] = {}
        self.student_quests: Dict[str, List[str]] = {}  # student_id -> quest_ids
        self.global_discoveries: Dict[str, Dict] = {}  # Notable discoveries by all students
        
        # World generation settings
        self.resource_spawn_rates = {
            ResourceType.VECTOR_CRYSTALS: 0.3,
            ResourceType.MATRIX_STONES: 0.25,
            ResourceType.DETERMINANT_GEMS: 0.15,
            ResourceType.EIGENVALUE_SHARDS: 0.1,
            ResourceType.LINEAR_ESSENCE: 0.1,
            ResourceType.TRANSFORMATION_ENERGY: 0.05,
            ResourceType.KNOWLEDGE_FRAGMENTS: 0.05
        }
        
        # Building costs and requirements
        self.building_costs = {
            BuildingType.STUDY_DESK: {ResourceType.VECTOR_CRYSTALS: 10, ResourceType.MATRIX_STONES: 5},
            BuildingType.CALCULATION_LAB: {ResourceType.MATRIX_STONES: 20, ResourceType.DETERMINANT_GEMS: 10},
            BuildingType.MATRIX_FORGE: {ResourceType.DETERMINANT_GEMS: 15, ResourceType.LINEAR_ESSENCE: 5},
            BuildingType.VECTOR_GARDEN: {ResourceType.VECTOR_CRYSTALS: 25, ResourceType.TRANSFORMATION_ENERGY: 3},
            BuildingType.EIGEN_OBSERVATORY: {ResourceType.EIGENVALUE_SHARDS: 20, ResourceType.KNOWLEDGE_FRAGMENTS: 5},
            BuildingType.KNOWLEDGE_LIBRARY: {ResourceType.KNOWLEDGE_FRAGMENTS: 15, ResourceType.LINEAR_ESSENCE: 10},
            BuildingType.COLLABORATION_HALL: {ResourceType.MATRIX_STONES: 30, ResourceType.VECTOR_CRYSTALS: 30},
            BuildingType.PRACTICE_ARENA: {ResourceType.DETERMINANT_GEMS: 25, ResourceType.EIGENVALUE_SHARDS: 15}
        }
        
        self._load_data()
        self._generate_starting_quests()
    
    def create_study_base(self, student_id: str, base_name: str, 
                         dimension: WorldDimension = WorldDimension.VECTOR_SPACE) -> str:
        """Create a new study base for a student"""
        base_id = str(uuid.uuid4())
        
        # Give starter resources
        starter_resources = {
            ResourceType.VECTOR_CRYSTALS: 50,
            ResourceType.MATRIX_STONES: 30,
            ResourceType.LINEAR_ESSENCE: 10
        }
        
        base = StudyBase(
            base_id=base_id,
            owner_id=student_id,
            base_name=base_name,
            dimension=dimension,
            resources=starter_resources
        )
        
        # Add starter building (study desk)
        starter_desk = Building(
            building_id=str(uuid.uuid4()),
            building_type=BuildingType.STUDY_DESK,
            position=(10, 10)  # Center of base
        )
        base.buildings[starter_desk.building_id] = starter_desk
        
        self.study_bases[base_id] = base
        
        logger.info(f"Created study base '{base_name}' for student {student_id} in {dimension.value}")
        self._save_data()
        return base_id
    
    def construct_building(self, base_id: str, building_type: BuildingType,
                          position: Tuple[int, int], custom_name: str = "") -> Optional[str]:
        """Construct a new building in a study base"""
        if base_id not in self.study_bases:
            return None
        
        base = self.study_bases[base_id]
        
        # Check if position is available
        for building in base.buildings.values():
            if building.position == position:
                logger.warning(f"Position {position} already occupied in base {base_id}")
                return None
        
        # Check resource requirements
        required_resources = self.building_costs.get(building_type, {})
        for resource_type, cost in required_resources.items():
            if base.resources.get(resource_type, 0) < cost:
                logger.warning(f"Insufficient {resource_type.value} to build {building_type.value}")
                return None
        
        # Deduct resources
        for resource_type, cost in required_resources.items():
            base.resources[resource_type] -= cost
        
        # Create building
        building_id = str(uuid.uuid4())
        building = Building(
            building_id=building_id,
            building_type=building_type,
            position=position,
            custom_name=custom_name or f"My {building_type.value}"
        )
        
        base.buildings[building_id] = building
        base.total_value += self._calculate_building_value(building)
        
        logger.info(f"Constructed {building_type.value} at position {position} in base {base_id}")
        self._save_data()
        return building_id
    
    def upgrade_building(self, base_id: str, building_id: str) -> bool:
        """Upgrade a building to the next level"""
        if base_id not in self.study_bases:
            return False
        
        base = self.study_bases[base_id]
        if building_id not in base.buildings:
            return False
        
        building = base.buildings[building_id]
        
        # Calculate upgrade cost (increases with level)
        upgrade_cost = {
            ResourceType.LINEAR_ESSENCE: building.level * 5,
            ResourceType.KNOWLEDGE_FRAGMENTS: building.level * 2
        }
        
        # Check resources
        for resource_type, cost in upgrade_cost.items():
            if base.resources.get(resource_type, 0) < cost:
                logger.warning(f"Insufficient resources to upgrade building {building_id}")
                return False
        
        # Deduct resources and upgrade
        for resource_type, cost in upgrade_cost.items():
            base.resources[resource_type] -= cost
        
        building.level += 1
        building.efficiency *= 1.2  # 20% efficiency boost per level
        building.capacity = int(building.capacity * 1.3)  # 30% capacity boost
        
        logger.info(f"Upgraded {building.building_type.value} to level {building.level}")
        self._save_data()
        return True
    
    def gather_resources(self, student_id: str, dimension: WorldDimension, 
                        duration_minutes: int = 30) -> Dict[ResourceType, int]:
        """Student goes resource gathering in a dimension"""
        gathered = {}
        
        # Find student's base
        student_base = None
        for base in self.study_bases.values():
            if base.owner_id == student_id:
                student_base = base
                break
        
        if not student_base:
            logger.warning(f"Student {student_id} has no study base")
            return gathered
        
        # Calculate gathering efficiency based on tools/buildings
        efficiency_multiplier = 1.0
        for building in student_base.buildings.values():
            if building.building_type in [BuildingType.MATRIX_FORGE, BuildingType.VECTOR_GARDEN]:
                efficiency_multiplier += building.efficiency * 0.1
        
        # Generate resources based on dimension and time spent
        base_attempts = duration_minutes // 5  # One attempt every 5 minutes
        
        for resource_type in ResourceType:
            if self._can_find_in_dimension(resource_type, dimension):
                spawn_rate = self.resource_spawn_rates[resource_type] * efficiency_multiplier
                
                for _ in range(base_attempts):
                    if random.random() < spawn_rate:
                        quality = random.uniform(0.8, 1.5)
                        quantity = int(random.randint(1, 3) * quality)
                        gathered[resource_type] = gathered.get(resource_type, 0) + quantity
        
        # Add resources to base
        for resource_type, quantity in gathered.items():
            student_base.resources[resource_type] += quantity
        
        logger.info(f"Student {student_id} gathered {gathered} in {dimension.value}")
        self._save_data()
        return gathered
    
    def _can_find_in_dimension(self, resource: ResourceType, dimension: WorldDimension) -> bool:
        """Check if a resource can be found in a specific dimension"""
        dimension_resources = {
            WorldDimension.VECTOR_SPACE: [ResourceType.VECTOR_CRYSTALS, ResourceType.LINEAR_ESSENCE],
            WorldDimension.MATRIX_REALM: [ResourceType.MATRIX_STONES, ResourceType.DETERMINANT_GEMS],
            WorldDimension.TRANSFORMATION_GALAXY: [ResourceType.TRANSFORMATION_ENERGY, ResourceType.LINEAR_ESSENCE],
            WorldDimension.EIGENVALUE_UNIVERSE: [ResourceType.EIGENVALUE_SHARDS, ResourceType.KNOWLEDGE_FRAGMENTS],
            WorldDimension.ABSTRACT_ALGEBRA_VOID: [ResourceType.KNOWLEDGE_FRAGMENTS]  # Rare but all types possible
        }
        
        return resource in dimension_resources.get(dimension, []) or dimension == WorldDimension.ABSTRACT_ALGEBRA_VOID
    
    def create_exploration_quest(self, title: str, description: str, quest_type: QuestType,
                               target_concept: str, dimension: WorldDimension,
                               difficulty: int = 1) -> str:
        """Create a new exploration quest"""
        quest_id = str(uuid.uuid4())
        
        # Generate appropriate objectives
        objectives = self._generate_quest_objectives(quest_type, target_concept, difficulty)
        
        # Calculate rewards based on difficulty
        xp_reward = difficulty * 50
        resource_rewards = {
            ResourceType.KNOWLEDGE_FRAGMENTS: difficulty * 2,
            ResourceType.LINEAR_ESSENCE: difficulty
        }
        
        quest = ExplorationQuest(
            quest_id=quest_id,
            title=title,
            description=description,
            quest_type=quest_type,
            target_concept=target_concept,
            dimension=dimension,
            objectives=objectives,
            xp_reward=xp_reward,
            resource_rewards=resource_rewards,
            difficulty_level=difficulty,
            deadline=datetime.now() + timedelta(days=7)  # One week to complete
        )
        
        self.exploration_quests[quest_id] = quest
        
        logger.info(f"Created quest: {title} (Difficulty: {difficulty})")
        self._save_data()
        return quest_id
    
    def _generate_quest_objectives(self, quest_type: QuestType, concept: str, 
                                 difficulty: int) -> List[str]:
        """Generate appropriate objectives for a quest"""
        if quest_type == QuestType.CONCEPT_DISCOVERY:
            return [
                f"Study the fundamentals of {concept}",
                f"Solve 3 problems involving {concept}",
                f"Create a visual representation of {concept}",
                f"Explain {concept} to a peer"
            ]
        elif quest_type == QuestType.RESOURCE_GATHERING:
            return [
                f"Gather 10 Vector Crystals",
                f"Find 5 Matrix Stones",
                f"Collect 2 Knowledge Fragments"
            ]
        elif quest_type == QuestType.THEOREM_EXPEDITION:
            return [
                f"Understand the statement of {concept}",
                f"Work through the proof of {concept}",
                f"Find an application of {concept}",
                f"Create your own example using {concept}"
            ]
        else:
            return [f"Complete the {quest_type.value} for {concept}"]
    
    def assign_quest_to_student(self, student_id: str, quest_id: str) -> bool:
        """Assign a quest to a student"""
        if quest_id not in self.exploration_quests:
            return False
        
        if student_id not in self.student_quests:
            self.student_quests[student_id] = []
        
        if quest_id not in self.student_quests[student_id]:
            self.student_quests[student_id].append(quest_id)
            logger.info(f"Assigned quest {quest_id} to student {student_id}")
            self._save_data()
            return True
        
        return False
    
    def update_quest_progress(self, student_id: str, quest_id: str, 
                            objective_index: int, progress: float) -> bool:
        """Update progress on a quest objective"""
        if quest_id not in self.exploration_quests:
            return False
        
        quest = self.exploration_quests[quest_id]
        if objective_index >= len(quest.objectives):
            return False
        
        objective_id = f"obj_{objective_index}"
        quest.progress[objective_id] = min(1.0, max(0.0, progress))
        
        # Check if quest is complete
        if all(quest.progress.get(f"obj_{i}", 0) >= 1.0 for i in range(len(quest.objectives))):
            self._complete_quest(student_id, quest_id)
        
        logger.info(f"Updated quest {quest_id} objective {objective_index} to {progress * 100}%")
        self._save_data()
        return True
    
    def _complete_quest(self, student_id: str, quest_id: str) -> bool:
        """Complete a quest and give rewards"""
        quest = self.exploration_quests[quest_id]
        quest.completion_time = datetime.now()
        
        # Find student's base for rewards
        student_base = None
        for base in self.study_bases.values():
            if base.owner_id == student_id:
                student_base = base
                break
        
        if student_base:
            # Add resource rewards
            for resource_type, quantity in quest.resource_rewards.items():
                student_base.resources[resource_type] += quantity
        
        logger.info(f"Student {student_id} completed quest: {quest.title}")
        return True
    
    def _calculate_building_value(self, building: Building) -> int:
        """Calculate the total value of a building"""
        base_value = {
            BuildingType.STUDY_DESK: 100,
            BuildingType.CALCULATION_LAB: 300,
            BuildingType.MATRIX_FORGE: 250,
            BuildingType.VECTOR_GARDEN: 200,
            BuildingType.EIGEN_OBSERVATORY: 400,
            BuildingType.KNOWLEDGE_LIBRARY: 350,
            BuildingType.COLLABORATION_HALL: 500,
            BuildingType.PRACTICE_ARENA: 450
        }
        
        return int(base_value.get(building.building_type, 100) * (building.level ** 1.2))
    
    def _generate_starting_quests(self):
        """Generate some starting quests for new players"""
        starter_quests = [
            ("Welcome to Vector Space", "Learn the basics of vectors", QuestType.CONCEPT_DISCOVERY, "Basic Vectors", WorldDimension.VECTOR_SPACE, 1),
            ("Matrix Fundamentals", "Understand what matrices are", QuestType.CONCEPT_DISCOVERY, "Matrix Basics", WorldDimension.MATRIX_REALM, 1),
            ("Resource Expedition", "Gather your first resources", QuestType.RESOURCE_GATHERING, "Resource Collection", WorldDimension.VECTOR_SPACE, 1),
            ("Transformation Journey", "Explore linear transformations", QuestType.THEOREM_EXPEDITION, "Linear Transformations", WorldDimension.TRANSFORMATION_GALAXY, 2)
        ]
        
        for title, desc, quest_type, concept, dimension, difficulty in starter_quests:
            self.create_exploration_quest(title, desc, quest_type, concept, dimension, difficulty)
    
    def get_student_world_info(self, student_id: str) -> Optional[Dict]:
        """Get comprehensive world information for a student"""
        # Find student's base
        student_base = None
        for base in self.study_bases.values():
            if base.owner_id == student_id:
                student_base = base
                break
        
        if not student_base:
            return None
        
        # Get active quests
        active_quests = []
        for quest_id in self.student_quests.get(student_id, []):
            if quest_id in self.exploration_quests:
                quest = self.exploration_quests[quest_id]
                if not quest.completion_time:  # Not completed
                    active_quests.append(asdict(quest))
        
        return {
            'base': asdict(student_base),
            'active_quests': active_quests,
            'total_buildings': len(student_base.buildings),
            'base_value': student_base.total_value,
            'available_quests': len([q for q in self.exploration_quests.values() if not q.completion_time])
        }
    
    def _load_data(self):
        """Load world data from storage"""
        try:
            # In a real implementation, this would load from a database
            pass
        except Exception as e:
            logger.error(f"Error loading world data: {e}")
    
    def _save_data(self):
        """Save world data to storage"""
        try:
            # In a real implementation, this would save to a database
            logger.debug("World data saved successfully")
        except Exception as e:
            logger.error(f"Error saving world data: {e}")

# Example usage and testing
if __name__ == "__main__":
    print("🌍 Testing World Building System...")
    
    # Create world builder
    world = WorldBuilder()
    
    # Create study base
    base_id = world.create_study_base(
        "student_alice",
        "Alice's Math Fortress",
        WorldDimension.VECTOR_SPACE
    )
    
    # Construct some buildings
    lab_id = world.construct_building(
        base_id,
        BuildingType.CALCULATION_LAB,
        (5, 5),
        "Alice's Research Lab"
    )
    
    # Upgrade the lab
    if lab_id:
        world.upgrade_building(base_id, lab_id)
    
    # Go resource gathering
    gathered = world.gather_resources("student_alice", WorldDimension.VECTOR_SPACE, 60)
    print(f"🔍 Resources gathered: {gathered}")
    
    # Assign and progress a quest
    available_quests = list(world.exploration_quests.keys())
    if available_quests:
        quest_id = available_quests[0]
        world.assign_quest_to_student("student_alice", quest_id)
        
        # Simulate quest progress
        world.update_quest_progress("student_alice", quest_id, 0, 1.0)  # Complete first objective
        world.update_quest_progress("student_alice", quest_id, 1, 0.5)  # Half complete second
    
    # Get world info
    world_info = world.get_student_world_info("student_alice")
    if world_info:
        print(f"🏠 Alice's Base Value: {world_info['base_value']}")
        print(f"🏗️ Total Buildings: {world_info['total_buildings']}")
        print(f"📋 Active Quests: {len(world_info['active_quests'])}")
    
    print("🎉 World Building System Test Complete!")
