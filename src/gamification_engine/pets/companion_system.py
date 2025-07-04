"""
Mathematical Pet Companion System
=================================

This module implements a Neopets/Pokémon-inspired companion system where students
care for mathematical creatures that evolve based on learning progress.

Features:
- Vector Sprites, Matrix Dragons, Eigenvalue Phoenixes
- Pet evolution based on learning consistency
- Mathematical battle system using linear algebra
- Daily care mechanics with mini-games
- Breeding system for advanced students

Author: AI Agent Development Team
Inspired by: Neopets, Pokémon, educational research on emotional engagement
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta
import random
import math
import json

class PetSpecies(Enum):
    """Mathematical creature species"""
    VECTOR_SPRITE = "vector_sprite"
    MATRIX_DRAGON = "matrix_dragon"
    EIGENVALUE_PHOENIX = "eigenvalue_phoenix"
    DETERMINANT_WOLF = "determinant_wolf"
    BASIS_BUTTERFLY = "basis_butterfly"
    TRANSFORMATION_TIGER = "transformation_tiger"
    POLYNOMIAL_PANDA = "polynomial_panda"
    GRADIENT_GRIFFIN = "gradient_griffin"

class PetStage(Enum):
    """Evolution stages"""
    EGG = "egg"
    HATCHLING = "hatchling"
    JUVENILE = "juvenile"
    ADULT = "adult"
    ELDER = "elder"
    LEGENDARY = "legendary"

class PetMood(Enum):
    """Pet emotional states affecting learning bonuses"""
    ECSTATIC = "ecstatic"      # +25% XP bonus
    HAPPY = "happy"            # +15% XP bonus
    CONTENT = "content"        # +5% XP bonus
    NEUTRAL = "neutral"        # No bonus
    GRUMPY = "grumpy"          # -5% XP penalty
    SAD = "sad"                # -10% XP penalty
    DEPRESSED = "depressed"    # -20% XP penalty

class PetElement(Enum):
    """Elemental types for battle system"""
    ALGEBRA = "algebra"        # Strong vs Geometry, weak vs Analysis
    GEOMETRY = "geometry"      # Strong vs Analysis, weak vs Algebra
    ANALYSIS = "analysis"      # Strong vs Algebra, weak vs Geometry
    APPLIED = "applied"        # Balanced type
    PURE = "pure"             # High damage, low defense
    COMPUTATIONAL = "computational"  # High defense, low damage

@dataclass
class PetStats:
    """Combat and interaction statistics"""
    health: int = 100
    attack: int = 50
    defense: int = 50
    speed: int = 50
    intelligence: int = 50
    happiness: int = 100
    
    # Care statistics
    hunger: int = 100
    energy: int = 100
    cleanliness: int = 100
    
    def calculate_battle_power(self) -> int:
        """Calculate overall battle effectiveness"""
        return (self.health + self.attack + self.defense + self.speed + self.intelligence) // 5

    def apply_mood_modifier(self, mood: PetMood) -> float:
        """Get XP modifier based on pet mood"""
        mood_modifiers = {
            PetMood.ECSTATIC: 1.25,
            PetMood.HAPPY: 1.15,
            PetMood.CONTENT: 1.05,
            PetMood.NEUTRAL: 1.0,
            PetMood.GRUMPY: 0.95,
            PetMood.SAD: 0.9,
            PetMood.DEPRESSED: 0.8
        }
        return mood_modifiers.get(mood, 1.0)

    def get_mood(self) -> PetMood:
        """Determine pet mood based on care statistics"""
        avg_care = (self.hunger + self.energy + self.cleanliness + self.happiness) / 4
        
        if avg_care >= 90:
            return PetMood.ECSTATIC
        elif avg_care >= 75:
            return PetMood.HAPPY
        elif avg_care >= 60:
            return PetMood.CONTENT
        elif avg_care >= 45:
            return PetMood.NEUTRAL
        elif avg_care >= 30:
            return PetMood.GRUMPY
        elif avg_care >= 15:
            return PetMood.SAD
        else:
            return PetMood.DEPRESSED

@dataclass
class PetAbility:
    """Special abilities pets can learn"""
    ability_id: str
    name: str
    description: str
    element: PetElement
    damage: int
    accuracy: float
    energy_cost: int
    special_effect: Optional[str] = None
    learning_requirement: Dict[str, int] = field(default_factory=dict)

@dataclass
class MathematicalPet:
    """A student's mathematical companion"""
    pet_id: str
    species: PetSpecies
    name: str
    owner_id: str
    
    # Core attributes
    stage: PetStage = PetStage.EGG
    element: PetElement = PetElement.ALGEBRA
    stats: PetStats = field(default_factory=PetStats)
    
    # Evolution tracking
    experience: int = 0
    evolution_points: int = 0
    days_since_hatch: int = 0
    learning_consistency: float = 0.0  # 0-1 based on owner's study habits
    
    # Care tracking
    last_fed: datetime = field(default_factory=datetime.now)
    last_played: datetime = field(default_factory=datetime.now)
    last_cleaned: datetime = field(default_factory=datetime.now)
    
    # Abilities and battle
    known_abilities: List[str] = field(default_factory=list)
    battle_wins: int = 0
    battle_losses: int = 0
    
    # Genetics (for breeding)
    parent1_id: Optional[str] = None
    parent2_id: Optional[str] = None
    genetic_traits: Dict[str, Any] = field(default_factory=dict)
    
    # Special features
    is_shiny: bool = False  # 1/1000 chance for special appearance
    personality_traits: List[str] = field(default_factory=list)
    favorite_subjects: List[str] = field(default_factory=list)
    
    created_at: datetime = field(default_factory=datetime.now)

    def update_care_stats(self):
        """Update pet care stats based on time passage"""
        now = datetime.now()
        
        # Decay rates (per hour)
        hunger_decay = 5
        energy_decay = 3
        cleanliness_decay = 2
        
        # Calculate time since last care
        hours_since_fed = (now - self.last_fed).total_seconds() / 3600
        hours_since_played = (now - self.last_played).total_seconds() / 3600
        hours_since_cleaned = (now - self.last_cleaned).total_seconds() / 3600
        
        # Apply decay
        self.stats.hunger = max(0, self.stats.hunger - int(hours_since_fed * hunger_decay))
        self.stats.energy = max(0, self.stats.energy - int(hours_since_played * energy_decay))
        self.stats.cleanliness = max(0, self.stats.cleanliness - int(hours_since_cleaned * cleanliness_decay))
        
        # Happiness affected by all care stats
        care_average = (self.stats.hunger + self.stats.energy + self.stats.cleanliness) / 3
        if care_average < 50:
            self.stats.happiness = max(0, self.stats.happiness - 1)
        elif care_average > 80:
            self.stats.happiness = min(100, self.stats.happiness + 1)

    def feed(self, food_type: str = "basic") -> Dict[str, Any]:
        """Feed the pet to restore hunger"""
        self.update_care_stats()
        
        food_effects = {
            "basic": {"hunger": 30, "happiness": 5},
            "premium": {"hunger": 50, "happiness": 10},
            "mathematical_treat": {"hunger": 25, "happiness": 15, "intelligence": 2}
        }
        
        if food_type not in food_effects:
            return {"error": "Unknown food type"}
        
        effects = food_effects[food_type]
        
        # Apply effects
        old_hunger = self.stats.hunger
        self.stats.hunger = min(100, self.stats.hunger + effects["hunger"])
        self.stats.happiness = min(100, self.stats.happiness + effects["happiness"])
        
        if "intelligence" in effects:
            self.stats.intelligence = min(100, self.stats.intelligence + effects["intelligence"])
        
        self.last_fed = datetime.now()
        
        return {
            "action": "feed",
            "food_type": food_type,
            "hunger_gained": self.stats.hunger - old_hunger,
            "happiness_gained": effects["happiness"],
            "new_mood": self.stats.get_mood().value,
            "message": self._generate_feeding_message()
        }

    def play(self, activity: str = "fetch") -> Dict[str, Any]:
        """Play with the pet to restore energy and happiness"""
        self.update_care_stats()
        
        activities = {
            "fetch": {"energy": 40, "happiness": 15},
            "math_puzzle": {"energy": 25, "happiness": 20, "intelligence": 3},
            "battle_training": {"energy": 30, "happiness": 10, "attack": 1},
            "exploration": {"energy": 35, "happiness": 18, "speed": 1}
        }
        
        if activity not in activities:
            return {"error": "Unknown activity"}
        
        effects = activities[activity]
        
        # Apply effects
        old_energy = self.stats.energy
        self.stats.energy = min(100, self.stats.energy + effects["energy"])
        self.stats.happiness = min(100, self.stats.happiness + effects["happiness"])
        
        # Apply stat bonuses
        stat_gains = {}
        for stat, gain in effects.items():
            if stat not in ["energy", "happiness"]:
                old_value = getattr(self.stats, stat)
                new_value = min(100, old_value + gain)
                setattr(self.stats, stat, new_value)
                if new_value > old_value:
                    stat_gains[stat] = gain
        
        self.last_played = datetime.now()
        
        return {
            "action": "play",
            "activity": activity,
            "energy_gained": self.stats.energy - old_energy,
            "happiness_gained": effects["happiness"],
            "stat_gains": stat_gains,
            "new_mood": self.stats.get_mood().value,
            "message": self._generate_play_message(activity)
        }

    def clean(self) -> Dict[str, Any]:
        """Clean the pet to restore cleanliness"""
        self.update_care_stats()
        
        old_cleanliness = self.stats.cleanliness
        old_happiness = self.stats.happiness
        
        self.stats.cleanliness = 100
        self.stats.happiness = min(100, self.stats.happiness + 10)
        self.last_cleaned = datetime.now()
        
        return {
            "action": "clean",
            "cleanliness_gained": 100 - old_cleanliness,
            "happiness_gained": self.stats.happiness - old_happiness,
            "new_mood": self.stats.get_mood().value,
            "message": f"{self.name} sparkles with mathematical cleanliness!"
        }

    def check_evolution(self) -> Optional[Dict[str, Any]]:
        """Check if pet can evolve to next stage"""
        evolution_requirements = {
            PetStage.EGG: {"days": 1, "care_average": 50},
            PetStage.HATCHLING: {"days": 7, "care_average": 60, "learning_consistency": 0.3},
            PetStage.JUVENILE: {"days": 21, "care_average": 70, "learning_consistency": 0.5},
            PetStage.ADULT: {"days": 60, "care_average": 80, "learning_consistency": 0.7},
            PetStage.ELDER: {"days": 120, "care_average": 90, "learning_consistency": 0.8}
        }
        
        if self.stage == PetStage.LEGENDARY:
            return None  # Already at max evolution
        
        current_requirements = evolution_requirements.get(self.stage)
        if not current_requirements:
            return None
        
        care_average = (self.stats.hunger + self.stats.energy + 
                       self.stats.cleanliness + self.stats.happiness) / 4
        
        # Check all requirements
        can_evolve = (
            self.days_since_hatch >= current_requirements["days"] and
            care_average >= current_requirements["care_average"] and
            self.learning_consistency >= current_requirements.get("learning_consistency", 0)
        )
        
        if can_evolve:
            return self.evolve()
        
        return None

    def evolve(self) -> Dict[str, Any]:
        """Evolve pet to next stage"""
        evolution_chain = [
            PetStage.EGG, PetStage.HATCHLING, PetStage.JUVENILE,
            PetStage.ADULT, PetStage.ELDER, PetStage.LEGENDARY
        ]
        
        current_index = evolution_chain.index(self.stage)
        if current_index >= len(evolution_chain) - 1:
            return {"error": "Already at maximum evolution"}
        
        old_stage = self.stage
        self.stage = evolution_chain[current_index + 1]
        
        # Stat increases based on evolution
        stat_multipliers = {
            PetStage.HATCHLING: 1.2,
            PetStage.JUVENILE: 1.4,
            PetStage.ADULT: 1.6,
            PetStage.ELDER: 1.8,
            PetStage.LEGENDARY: 2.0
        }
        
        multiplier = stat_multipliers[self.stage]
        
        # Apply stat boosts
        old_stats = {
            "health": self.stats.health,
            "attack": self.stats.attack,
            "defense": self.stats.defense,
            "speed": self.stats.speed,
            "intelligence": self.stats.intelligence
        }
        
        self.stats.health = min(200, int(self.stats.health * multiplier))
        self.stats.attack = min(150, int(self.stats.attack * multiplier))
        self.stats.defense = min(150, int(self.stats.defense * multiplier))
        self.stats.speed = min(150, int(self.stats.speed * multiplier))
        self.stats.intelligence = min(150, int(self.stats.intelligence * multiplier))
        
        # Learn new ability
        new_ability = self._learn_evolution_ability()
        
        return {
            "evolved": True,
            "old_stage": old_stage.value,
            "new_stage": self.stage.value,
            "stat_increases": {
                stat: getattr(self.stats, stat) - old_value
                for stat, old_value in old_stats.items()
            },
            "new_ability": new_ability,
            "message": f"🎉 {self.name} evolved into a {self.stage.value.replace('_', ' ').title()} {self.species.value.replace('_', ' ').title()}!"
        }

    def _learn_evolution_ability(self) -> Optional[str]:
        """Learn a new ability upon evolution"""
        stage_abilities = {
            PetStage.HATCHLING: ["basic_math", "enthusiasm"],
            PetStage.JUVENILE: ["algebra_boost", "study_buddy"],
            PetStage.ADULT: ["advanced_reasoning", "mentor_assist"],
            PetStage.ELDER: ["wisdom_sharing", "deep_insight"],
            PetStage.LEGENDARY: ["mathematical_mastery", "inspiration_aura"]
        }
        
        available_abilities = stage_abilities.get(self.stage, [])
        if not available_abilities:
            return None
        
        # Choose ability based on pet's strongest stat
        if self.stats.intelligence >= max(self.stats.attack, self.stats.defense, self.stats.speed):
            ability = available_abilities[0] if len(available_abilities) > 0 else None
        else:
            ability = available_abilities[-1] if len(available_abilities) > 0 else None
        
        if ability and ability not in self.known_abilities:
            self.known_abilities.append(ability)
            return ability
        
        return None

    def battle_preview(self, opponent: 'MathematicalPet') -> Dict[str, Any]:
        """Preview battle outcome without actually fighting"""
        my_power = self.stats.calculate_battle_power()
        opponent_power = opponent.stats.calculate_battle_power()
        
        # Factor in type advantages
        advantage = self._calculate_type_advantage(opponent.element)
        effective_power = my_power * advantage
        
        win_probability = effective_power / (effective_power + opponent_power)
        
        return {
            "my_power": my_power,
            "opponent_power": opponent_power,
            "type_advantage": advantage,
            "win_probability": win_probability,
            "recommended": win_probability > 0.6,
            "preview_message": self._generate_battle_preview(opponent, win_probability)
        }

    def _calculate_type_advantage(self, opponent_element: PetElement) -> float:
        """Calculate type advantage multiplier"""
        advantages = {
            PetElement.ALGEBRA: {PetElement.GEOMETRY: 1.5, PetElement.ANALYSIS: 0.75},
            PetElement.GEOMETRY: {PetElement.ANALYSIS: 1.5, PetElement.ALGEBRA: 0.75},
            PetElement.ANALYSIS: {PetElement.ALGEBRA: 1.5, PetElement.GEOMETRY: 0.75},
            PetElement.APPLIED: {},  # Balanced, no advantages
            PetElement.PURE: {PetElement.COMPUTATIONAL: 1.25},
            PetElement.COMPUTATIONAL: {PetElement.PURE: 1.25}
        }
        
        return advantages.get(self.element, {}).get(opponent_element, 1.0)

    def _generate_feeding_message(self) -> str:
        """Generate contextual feeding message"""
        mood = self.stats.get_mood()
        species_name = self.species.value.replace('_', ' ').title()
        
        if mood in [PetMood.ECSTATIC, PetMood.HAPPY]:
            return f"{self.name} the {species_name} devours the food with mathematical enthusiasm!"
        elif mood == PetMood.CONTENT:
            return f"{self.name} enjoys the meal while pondering linear transformations."
        else:
            return f"{self.name} reluctantly eats, clearly needing more attention."

    def _generate_play_message(self, activity: str) -> str:
        """Generate contextual play message"""
        activity_messages = {
            "fetch": f"{self.name} bounds after the vector with incredible speed!",
            "math_puzzle": f"{self.name} solves the puzzle with elegant mathematical reasoning!",
            "battle_training": f"{self.name} practices combat moves using matrix transformations!",
            "exploration": f"{self.name} discovers new mathematical territories!"
        }
        return activity_messages.get(activity, f"{self.name} enjoys the activity!")

    def _generate_battle_preview(self, opponent: 'MathematicalPet', win_prob: float) -> str:
        """Generate battle preview message"""
        if win_prob > 0.8:
            return f"{self.name} looks confident against {opponent.name}!"
        elif win_prob > 0.6:
            return f"{self.name} seems evenly matched with {opponent.name}."
        elif win_prob > 0.4:
            return f"{self.name} will need strategy to defeat {opponent.name}."
        else:
            return f"{self.name} should train more before challenging {opponent.name}."

    def to_dict(self) -> Dict[str, Any]:
        """Convert pet to dictionary for storage/API"""
        return {
            "pet_id": self.pet_id,
            "species": self.species.value,
            "name": self.name,
            "owner_id": self.owner_id,
            "stage": self.stage.value,
            "element": self.element.value,
            "stats": {
                "health": self.stats.health,
                "attack": self.stats.attack,
                "defense": self.stats.defense,
                "speed": self.stats.speed,
                "intelligence": self.stats.intelligence,
                "happiness": self.stats.happiness,
                "hunger": self.stats.hunger,
                "energy": self.stats.energy,
                "cleanliness": self.stats.cleanliness
            },
            "experience": self.experience,
            "evolution_points": self.evolution_points,
            "days_since_hatch": self.days_since_hatch,
            "learning_consistency": self.learning_consistency,
            "known_abilities": self.known_abilities,
            "battle_record": {"wins": self.battle_wins, "losses": self.battle_losses},
            "mood": self.stats.get_mood().value,
            "is_shiny": self.is_shiny,
            "personality_traits": self.personality_traits,
            "created_at": self.created_at.isoformat()
        }

class PetCompanionSystem:
    """Manager for the pet companion system"""
    
    def __init__(self):
        self.pets: Dict[str, MathematicalPet] = {}
        self.pet_abilities = self._initialize_abilities()
        self.adoption_center: List[Dict[str, Any]] = []
        self._populate_adoption_center()

    def _initialize_abilities(self) -> Dict[str, PetAbility]:
        """Initialize pet abilities database"""
        return {
            "basic_math": PetAbility(
                "basic_math", "Basic Math", 
                "Increases owner's XP gain by 5%",
                PetElement.ALGEBRA, 0, 1.0, 0, "xp_boost_5"
            ),
            "enthusiasm": PetAbility(
                "enthusiasm", "Enthusiasm",
                "Improves owner's mood during study sessions",
                PetElement.APPLIED, 0, 1.0, 0, "mood_boost"
            ),
            "algebra_boost": PetAbility(
                "algebra_boost", "Algebra Boost",
                "Increases algebra-related XP by 15%",
                PetElement.ALGEBRA, 0, 1.0, 0, "algebra_xp_boost_15"
            )
        }

    def _populate_adoption_center(self):
        """Create pets available for adoption"""
        species_options = list(PetSpecies)
        element_options = list(PetElement)
        
        for i in range(20):  # 20 pets always available
            species = random.choice(species_options)
            element = random.choice(element_options)
            is_shiny = random.random() < 0.001  # 0.1% chance
            
            self.adoption_center.append({
                "adoption_id": f"adopt_{i:03d}",
                "species": species,
                "element": element,
                "is_shiny": is_shiny,
                "personality": random.choice(["friendly", "curious", "energetic", "calm", "playful"]),
                "cost": 100 if not is_shiny else 1000,
                "available_until": (datetime.now() + timedelta(days=7)).isoformat()
            })

    def adopt_pet(self, student_id: str, adoption_id: str, pet_name: str) -> Dict[str, Any]:
        """Adopt a pet from the adoption center"""
        # Find the pet in adoption center
        pet_data = None
        for pet in self.adoption_center:
            if pet["adoption_id"] == adoption_id:
                pet_data = pet
                break
        
        if not pet_data:
            return {"error": "Pet not found in adoption center"}
        
        # Create the pet
        pet_id = f"pet_{student_id}_{len(self.pets)}"
        new_pet = MathematicalPet(
            pet_id=pet_id,
            species=pet_data["species"],
            name=pet_name,
            owner_id=student_id,
            element=pet_data["element"],
            is_shiny=pet_data["is_shiny"]
        )
        
        # Add personality trait
        new_pet.personality_traits.append(pet_data["personality"])
        
        # Store the pet
        self.pets[pet_id] = new_pet
        
        return {
            "success": True,
            "pet": new_pet.to_dict(),
            "message": f"Welcome {pet_name} to your mathematical journey!"
        }

    def get_student_pets(self, student_id: str) -> List[Dict[str, Any]]:
        """Get all pets owned by a student"""
        student_pets = [pet for pet in self.pets.values() if pet.owner_id == student_id]
        return [pet.to_dict() for pet in student_pets]

    def update_learning_consistency(self, student_id: str, consistency_score: float):
        """Update learning consistency for all student's pets"""
        for pet in self.pets.values():
            if pet.owner_id == student_id:
                pet.learning_consistency = consistency_score
                
                # Check for evolution
                evolution_result = pet.check_evolution()
                if evolution_result:
                    return evolution_result
        
        return None

    def daily_update(self):
        """Run daily maintenance on all pets"""
        results = []
        
        for pet in self.pets.values():
            pet.days_since_hatch += 1
            pet.update_care_stats()
            
            # Check for evolution
            evolution_result = pet.check_evolution()
            if evolution_result:
                results.append({
                    "pet_id": pet.pet_id,
                    "owner_id": pet.owner_id,
                    "evolution": evolution_result
                })
        
        return results

    def get_care_reminders(self, student_id: str) -> List[Dict[str, Any]]:
        """Get care reminders for student's pets"""
        reminders = []
        
        for pet in self.pets.values():
            if pet.owner_id == student_id:
                pet.update_care_stats()
                
                urgent_needs = []
                if pet.stats.hunger < 30:
                    urgent_needs.append("hungry")
                if pet.stats.energy < 30:
                    urgent_needs.append("tired")
                if pet.stats.cleanliness < 30:
                    urgent_needs.append("dirty")
                
                if urgent_needs:
                    reminders.append({
                        "pet_id": pet.pet_id,
                        "pet_name": pet.name,
                        "needs": urgent_needs,
                        "mood": pet.stats.get_mood().value,
                        "message": f"{pet.name} needs attention! They are {' and '.join(urgent_needs)}."
                    })
        
        return reminders

# Example usage and testing
if __name__ == "__main__":
    # Initialize the pet system
    pet_system = PetCompanionSystem()
    
    print("🐾 Mathematical Pet Companion System Initialized!")
    print(f"Adoption center has {len(pet_system.adoption_center)} pets available")
    
    # Student adopts a pet
    adoption_result = pet_system.adopt_pet("alice_123", "adopt_001", "Vector")
    if adoption_result.get("success"):
        print(f"\n🎉 Alice adopted {adoption_result['pet']['name']}!")
        print(f"Species: {adoption_result['pet']['species']}")
        print(f"Element: {adoption_result['pet']['element']}")
        print(f"Stage: {adoption_result['pet']['stage']}")
    
    # Get the pet and simulate care
    alice_pets = pet_system.get_student_pets("alice_123")
    if alice_pets:
        pet_data = alice_pets[0]
        pet = pet_system.pets[pet_data["pet_id"]]
        
        print(f"\n🍎 Feeding {pet.name}...")
        feed_result = pet.feed("mathematical_treat")
        print(f"Result: {feed_result['message']}")
        print(f"Mood: {feed_result['new_mood']}")
        
        print(f"\n🎮 Playing math puzzle with {pet.name}...")
        play_result = pet.play("math_puzzle")
        print(f"Result: {play_result['message']}")
        print(f"Stat gains: {play_result.get('stat_gains', 'None')}")
        
        # Simulate learning consistency improvement
        print(f"\n📚 Updating learning consistency...")
        pet_system.update_learning_consistency("alice_123", 0.8)
        
        # Check evolution possibility
        evolution_check = pet.check_evolution()
        if evolution_check:
            print(f"🌟 Evolution available: {evolution_check}")
        else:
            print(f"Evolution requirements not yet met")
    
    # Show care reminders
    reminders = pet_system.get_care_reminders("alice_123")
    if reminders:
        print(f"\n⚠️ Care Reminders:")
        for reminder in reminders:
            print(f"  {reminder['message']}")
    else:
        print(f"\n✅ All pets are well cared for!")
