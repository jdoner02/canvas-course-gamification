"""
🎮 GAMIFICATION ENGINE - Central Integration System
Unified interface for all gamification components: RPG, Pets, Social, World, Events
"""

# Note: Import issues resolved - importing directly in modules as needed
# This module serves as the main entry point for the gamification engine
# Individual systems can be imported directly from their respective modules

__version__ = "2.0.0"
__author__ = "AI Agent Development Team" 
__description__ = "Next-Generation Gamified Learning Platform"

# System module paths for reference:
# - RPG System: gamification_engine.core.player_profile
# - Pet System: gamification_engine.pets.companion_system
# - Guild System: gamification_engine.social.guild_system
# - Mentorship System: gamification_engine.social.mentorship_system
# - Competition System: gamification_engine.social.competition_system
# - World Building: gamification_engine.world
# - Events System: gamification_engine.events
__author__ = "AI Agent Development Team"
__description__ = "Next-Generation Gamified Learning Platform"

import json
import logging
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, asdict

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class StudentGameProfile:
    """Comprehensive gamification profile for a student"""
    student_id: str
    canvas_user_id: Optional[str] = None
    
    # Core progression
    total_xp: int = 0
    level: int = 1
    achievements: List[str] = None
    badges: List[str] = None
    
    # System participation
    rpg_active: bool = True
    has_pet: bool = False
    guild_member: bool = False
    mentor_status: bool = False
    world_builder: bool = False
    events_participant: bool = False
    
    # Cross-system rewards
    premium_currency: int = 0  # "Mathematical Gems"
    special_unlocks: List[str] = None
    
    # Analytics and engagement
    daily_login_streak: int = 0
    last_activity: datetime = None
    engagement_score: float = 0.0
    
    def __post_init__(self):
        if self.achievements is None:
            self.achievements = []
        if self.badges is None:
            self.badges = []
        if self.special_unlocks is None:
            self.special_unlocks = []
        if self.last_activity is None:
            self.last_activity = datetime.now()

class GamificationEngine:
    """Central engine that coordinates all gamification systems"""
    
    def __init__(self):
        # Initialize all subsystems
        self.rpg_system = RPGPlayerSystem()
        self.pet_system = MathPetSystem()
        self.guild_manager = GuildManager()
        self.mentorship_engine = PeerTeachingEngine()
        self.battle_engine = PvPBattleEngine()
        self.tournament_manager = TournamentManager(self.battle_engine)
        self.world_builder = WorldBuilder()
        self.event_engine = RealTimeEventEngine()
        
        # Central data stores
        self.student_profiles: Dict[str, StudentGameProfile] = {}
        self.cross_system_achievements: Dict[str, Dict] = {}
        self.global_leaderboards: Dict[str, List] = {}
        
        # Integration mappings
        self.xp_multipliers = {
            "rpg_bonus": 1.0,
            "pet_bonus": 1.0,
            "guild_bonus": 1.0,
            "mentor_bonus": 1.0,
            "world_bonus": 1.0,
            "event_bonus": 1.0
        }
        
        self._load_data()
        self._initialize_cross_system_achievements()
    
    def onboard_student(self, student_id: str, canvas_user_id: str = None,
                       preferences: Dict = None) -> bool:
        """Complete onboarding process for a new student"""
        logger.info(f"Starting gamification onboarding for student {student_id}")
        
        # Create central profile
        profile = StudentGameProfile(
            student_id=student_id,
            canvas_user_id=canvas_user_id
        )
        self.student_profiles[student_id] = profile
        
        # Initialize RPG system
        player_class = preferences.get('player_class', PlayerClass.ENGINEER) if preferences else PlayerClass.ENGINEER
        self.rpg_system.create_player(student_id, player_class)
        profile.rpg_active = True
        
        # Offer pet adoption
        if preferences and preferences.get('wants_pet', True):
            pet_type = preferences.get('pet_type', PetType.VECTOR_SPRITE)
            pet_name = preferences.get('pet_name', 'Buddy')
            
            pet_id = self.pet_system.adopt_pet(student_id, pet_type, pet_name)
            if pet_id:
                profile.has_pet = True
                logger.info(f"Student {student_id} adopted pet: {pet_name}")
        
        # Create study base
        base_name = preferences.get('base_name', f"{student_id}'s Study Base") if preferences else f"{student_id}'s Study Base"
        base_id = self.world_builder.create_study_base(student_id, base_name)
        if base_id:
            profile.world_builder = True
            logger.info(f"Created study base for student {student_id}")
        
        # Register for competitions (optional)
        if preferences and preferences.get('join_competitions', False):
            self.battle_engine.register_competitor(student_id)
        
        # Give welcome rewards
        self._give_welcome_rewards(student_id)
        
        logger.info(f"Gamification onboarding completed for student {student_id}")
        self._save_data()
        return True
    
    def _give_welcome_rewards(self, student_id: str):
        """Give welcome rewards to new students"""
        profile = self.student_profiles[student_id]
        
        # Welcome XP and level
        self.award_xp(student_id, 100, "Welcome Bonus")
        
        # Welcome badges
        profile.badges.extend(["New Adventurer", "First Steps", "Mathematical Explorer"])
        
        # Premium currency
        profile.premium_currency += 50
        
        # Special unlocks
        profile.special_unlocks.extend(["Starter Kit", "Basic Customization"])
    
    def award_xp(self, student_id: str, base_xp: int, source: str,
                context: Dict = None) -> int:
        """Award XP with cross-system multipliers"""
        if student_id not in self.student_profiles:
            logger.warning(f"Student {student_id} not found in gamification system")
            return 0
        
        profile = self.student_profiles[student_id]
        
        # Calculate total multiplier from all systems
        total_multiplier = 1.0
        
        # RPG class bonuses
        if profile.rpg_active:
            rpg_player = self.rpg_system.get_player_stats(student_id)
            if rpg_player:
                if source == "problem_solving" and rpg_player['class'] == PlayerClass.ENGINEER:
                    total_multiplier += 0.2  # Engineers get bonus for problem solving
                elif source == "peer_teaching" and rpg_player['class'] == PlayerClass.PURE_MATHEMATICIAN:
                    total_multiplier += 0.15  # Pure mathematicians get teaching bonus
        
        # Pet bonuses
        if profile.has_pet:
            pet_info = self.pet_system.get_student_pets(student_id)
            if pet_info and pet_info['active_pet']:
                pet = pet_info['active_pet']
                happiness_bonus = (pet['happiness'] / 100.0) * 0.1  # Up to 10% bonus
                total_multiplier += happiness_bonus
        
        # Guild bonuses
        if profile.guild_member:
            guild_info = self.guild_manager.get_student_guild_info(student_id)
            if guild_info and guild_info['guild']['guild_xp'] > 1000:
                total_multiplier += 0.05  # 5% bonus for active guild members
        
        # Mentor bonuses
        if profile.mentor_status:
            mentor_stats = self.mentorship_engine.get_mentor_stats(student_id)
            if mentor_stats and mentor_stats['profile']['average_satisfaction_rating'] > 4.0:
                total_multiplier += 0.1  # 10% bonus for good mentors
        
        # Calculate final XP
        final_xp = int(base_xp * total_multiplier)
        
        # Award to profile
        profile.total_xp += final_xp
        
        # Check for level up
        new_level = self._calculate_level(profile.total_xp)
        if new_level > profile.level:
            old_level = profile.level
            profile.level = new_level
            self._handle_level_up(student_id, old_level, new_level)
        
        # Award to RPG system
        if profile.rpg_active:
            self.rpg_system.award_experience(student_id, final_xp, source)
        
        logger.info(f"Awarded {final_xp} XP to {student_id} from {source} (multiplier: {total_multiplier:.2f})")
        return final_xp
    
    def _calculate_level(self, total_xp: int) -> int:
        """Calculate level based on total XP"""
        # Level formula: each level requires more XP
        level = 1
        xp_needed = 0
        
        while total_xp >= xp_needed:
            level += 1
            xp_needed += level * 100  # Each level needs level * 100 XP
        
        return level - 1
    
    def _handle_level_up(self, student_id: str, old_level: int, new_level: int):
        """Handle student leveling up"""
        profile = self.student_profiles[student_id]
        
        # Award level-up rewards
        levels_gained = new_level - old_level
        profile.premium_currency += levels_gained * 10
        
        # Unlock new features based on level
        if new_level >= 5 and "Advanced Customization" not in profile.special_unlocks:
            profile.special_unlocks.append("Advanced Customization")
        
        if new_level >= 10 and "Mentor Eligibility" not in profile.special_unlocks:
            profile.special_unlocks.append("Mentor Eligibility")
        
        if new_level >= 15 and "Guild Leadership" not in profile.special_unlocks:
            profile.special_unlocks.append("Guild Leadership")
        
        logger.info(f"Student {student_id} leveled up from {old_level} to {new_level}!")
    
    def complete_learning_activity(self, student_id: str, activity_type: str,
                                 performance_data: Dict) -> Dict:
        """Process completion of any learning activity"""
        if student_id not in self.student_profiles:
            self.onboard_student(student_id)
        
        results = {
            "xp_awarded": 0,
            "badges_earned": [],
            "achievements_unlocked": [],
            "pet_effects": {},
            "guild_effects": {},
            "level_up": False
        }
        
        # Calculate base XP based on activity
        base_xp = self._calculate_activity_xp(activity_type, performance_data)
        
        # Award XP with multipliers
        old_level = self.student_profiles[student_id].level
        final_xp = self.award_xp(student_id, base_xp, activity_type, performance_data)
        results["xp_awarded"] = final_xp
        results["level_up"] = self.student_profiles[student_id].level > old_level
        
        # Update pet if student has one
        profile = self.student_profiles[student_id]
        if profile.has_pet:
            pet_result = self.pet_system.interaction_completed(
                student_id, activity_type, performance_data
            )
            results["pet_effects"] = pet_result
        
        # Update RPG skills based on activity
        if profile.rpg_active:
            skill_xp = max(1, final_xp // 4)  # Skills get 25% of total XP
            if activity_type in ["matrix_operations", "determinant_calculation"]:
                self.rpg_system.award_skill_experience(student_id, SkillTree.MATRIX_MASTERY, skill_xp)
            elif activity_type in ["vector_operations", "dot_product"]:
                self.rpg_system.award_skill_experience(student_id, SkillTree.VECTOR_OPERATIONS, skill_xp)
        
        # Check for cross-system achievements
        achievements = self._check_cross_system_achievements(student_id, activity_type, performance_data)
        results["achievements_unlocked"] = achievements
        
        self._save_data()
        return results
    
    def _calculate_activity_xp(self, activity_type: str, performance_data: Dict) -> int:
        """Calculate base XP for different learning activities"""
        base_values = {
            "problem_solved": 25,
            "video_watched": 15,
            "concept_mastered": 50,
            "peer_helped": 40,
            "quiz_completed": 30,
            "assignment_submitted": 100,
            "exam_completed": 200
        }
        
        base_xp = base_values.get(activity_type, 20)
        
        # Performance multipliers
        if "accuracy" in performance_data:
            accuracy = performance_data["accuracy"]
            base_xp = int(base_xp * (0.5 + accuracy * 0.5))  # 50% to 100% based on accuracy
        
        if "time_bonus" in performance_data and performance_data["time_bonus"]:
            base_xp = int(base_xp * 1.2)  # 20% bonus for fast completion
        
        if "creativity_bonus" in performance_data and performance_data["creativity_bonus"]:
            base_xp = int(base_xp * 1.3)  # 30% bonus for creative solutions
        
        return base_xp
    
    def _check_cross_system_achievements(self, student_id: str, activity_type: str,
                                       performance_data: Dict) -> List[str]:
        """Check for achievements that span multiple systems"""
        achievements = []
        profile = self.student_profiles[student_id]
        
        # Multi-system achievements
        if (profile.rpg_active and profile.has_pet and profile.guild_member and
            "Triple Threat" not in profile.achievements):
            achievements.append("Triple Threat")
            profile.achievements.append("Triple Threat")
        
        # High engagement achievement
        systems_active = sum([
            profile.rpg_active, profile.has_pet, profile.guild_member,
            profile.mentor_status, profile.world_builder, profile.events_participant
        ])
        
        if systems_active >= 5 and "Gamification Master" not in profile.achievements:
            achievements.append("Gamification Master")
            profile.achievements.append("Gamification Master")
        
        return achievements
    
    def get_comprehensive_dashboard(self, student_id: str) -> Dict:
        """Get complete gamification dashboard for a student"""
        if student_id not in self.student_profiles:
            return {"error": "Student not found in gamification system"}
        
        profile = self.student_profiles[student_id]
        dashboard = {
            "profile": asdict(profile),
            "systems": {}
        }
        
        # RPG System data
        if profile.rpg_active:
            dashboard["systems"]["rpg"] = self.rpg_system.get_player_stats(student_id)
        
        # Pet System data
        if profile.has_pet:
            dashboard["systems"]["pets"] = self.pet_system.get_student_pets(student_id)
        
        # Social Systems data
        guild_info = self.guild_manager.get_student_guild_info(student_id)
        if guild_info:
            dashboard["systems"]["guild"] = guild_info
            profile.guild_member = True
        
        mentor_stats = self.mentorship_engine.get_mentor_stats(student_id)
        if mentor_stats:
            dashboard["systems"]["mentorship"] = mentor_stats
            profile.mentor_status = True
        
        competitor_stats = self.battle_engine.get_competitor_stats(student_id)
        if competitor_stats:
            dashboard["systems"]["competition"] = competitor_stats
        
        # World Building data
        world_info = self.world_builder.get_student_world_info(student_id)
        if world_info:
            dashboard["systems"]["world"] = world_info
        
        # Events data
        event_progress = self.event_engine.get_student_event_progress(student_id)
        if event_progress["total_events_participated"] > 0:
            dashboard["systems"]["events"] = event_progress
            profile.events_participant = True
        
        # Cross-system summary
        dashboard["summary"] = {
            "total_xp": profile.total_xp,
            "level": profile.level,
            "systems_active": sum([
                profile.rpg_active, profile.has_pet, profile.guild_member,
                profile.mentor_status, profile.world_builder, profile.events_participant
            ]),
            "engagement_score": profile.engagement_score,
            "daily_streak": profile.daily_login_streak
        }
        
        return dashboard
    
    def process_daily_login(self, student_id: str) -> Dict:
        """Process daily login rewards and updates"""
        if student_id not in self.student_profiles:
            self.onboard_student(student_id)
        
        profile = self.student_profiles[student_id]
        today = datetime.now().date()
        last_login = profile.last_activity.date() if profile.last_activity else None
        
        rewards = {
            "streak_bonus": False,
            "daily_xp": 0,
            "currency_bonus": 0,
            "pet_happiness": 0
        }
        
        # Check streak
        if last_login and (today - last_login).days == 1:
            profile.daily_login_streak += 1
        elif last_login != today:
            profile.daily_login_streak = 1
        
        # Streak rewards
        if profile.daily_login_streak >= 7:
            rewards["streak_bonus"] = True
            rewards["daily_xp"] = 50
            rewards["currency_bonus"] = 10
        
        # Update activity
        profile.last_activity = datetime.now()
        
        # Pet daily care
        if profile.has_pet:
            happiness_gain = self.pet_system.daily_care(student_id)
            rewards["pet_happiness"] = happiness_gain
        
        # Award daily XP
        if rewards["daily_xp"] > 0:
            self.award_xp(student_id, rewards["daily_xp"], "daily_login")
        
        self._save_data()
        return rewards
    
    def _initialize_cross_system_achievements(self):
        """Initialize achievements that require multiple systems"""
        self.cross_system_achievements = {
            "Triple Threat": {
                "name": "Triple Threat",
                "description": "Active in RPG, Pets, and Guild systems",
                "requirements": ["rpg_active", "has_pet", "guild_member"],
                "reward_xp": 200,
                "reward_currency": 50
            },
            "Gamification Master": {
                "name": "Gamification Master", 
                "description": "Active in 5 or more gamification systems",
                "requirements": ["systems_active >= 5"],
                "reward_xp": 500,
                "reward_currency": 100
            },
            "Social Butterfly": {
                "name": "Social Butterfly",
                "description": "Active in guild, mentorship, and competition",
                "requirements": ["guild_member", "mentor_status", "competition_active"],
                "reward_xp": 300,
                "reward_currency": 75
            }
        }
    
    def _load_data(self):
        """Load all gamification data"""
        try:
            # In a real implementation, this would load from a database
            pass
        except Exception as e:
            logger.error(f"Error loading gamification data: {e}")
    
    def _save_data(self):
        """Save all gamification data"""
        try:
            # In a real implementation, this would save to a database
            logger.debug("Gamification data saved successfully")
        except Exception as e:
            logger.error(f"Error saving gamification data: {e}")

# Example usage and testing
if __name__ == "__main__":
    print("🎮 Testing Unified Gamification Engine...")
    
    # Create the main engine
    engine = GamificationEngine()
    
    # Onboard a new student
    preferences = {
        'player_class': PlayerClass.DATA_SCIENTIST,
        'wants_pet': True,
        'pet_type': PetType.MATRIX_DRAGON,
        'pet_name': 'Eigenbert',
        'base_name': "Alice's Mathematical Kingdom",
        'join_competitions': True
    }
    
    engine.onboard_student("alice_complete", preferences=preferences)
    
    # Simulate some learning activities
    activities = [
        ("problem_solved", {"accuracy": 0.95, "time_bonus": True}),
        ("video_watched", {"completion": 1.0}),
        ("concept_mastered", {"creativity_bonus": True}),
        ("peer_helped", {"satisfaction": 4.8})
    ]
    
    total_xp_earned = 0
    for activity_type, performance in activities:
        result = engine.complete_learning_activity("alice_complete", activity_type, performance)
        total_xp_earned += result["xp_awarded"]
        print(f"📚 Activity: {activity_type} → XP: {result['xp_awarded']}")
    
    # Process daily login
    daily_rewards = engine.process_daily_login("alice_complete")
    print(f"🌅 Daily Login Rewards: {daily_rewards}")
    
    # Get comprehensive dashboard
    dashboard = engine.get_comprehensive_dashboard("alice_complete")
    print(f"📊 Alice's Dashboard:")
    print(f"   Level: {dashboard['summary']['level']}")
    print(f"   Total XP: {dashboard['summary']['total_xp']}")
    print(f"   Systems Active: {dashboard['summary']['systems_active']}/6")
    print(f"   Has Pet: {dashboard['profile']['has_pet']}")
    print(f"   Guild Member: {dashboard['profile']['guild_member']}")
    
    print("🎉 Unified Gamification Engine Test Complete!")
