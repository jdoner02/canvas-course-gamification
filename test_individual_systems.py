"""
🎮 Simplified Test Script for Individual Gamification Systems
Testing each system separately to demonstrate functionality
"""

import sys
import os

# Add the src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

import logging
from datetime import datetime

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

print("🎮 Testing Individual Gamification Systems...")
print("=" * 60)

# Test 1: RPG Player Profile System
print("\n1. 🏆 Testing RPG Player Profile System...")
try:
    from gamification_engine.core.player_profile import (
        PlayerProfileManager,
        MathematicalSpecialization,
    )

    rpg_manager = PlayerProfileManager()
    player_id = rpg_manager.create_player(
        "alice_rpg", MathematicalSpecialization.DATA_SCIENTIST
    )

    # Award some experience
    rpg_manager.award_experience("alice_rpg", 150, "problem_solving")
    rpg_manager.award_experience("alice_rpg", 100, "concept_mastery")

    # Get stats
    stats = rpg_manager.get_player_stats("alice_rpg")
    print(f"   ✅ Player Level: {stats['level']}")
    print(f"   ✅ Total XP: {stats['total_experience']}")
    print(f"   ✅ Specialization: {stats['specialization']}")

except Exception as e:
    print(f"   ❌ RPG System Error: {e}")

# Test 2: Pet System
print("\n2. 🐉 Testing Mathematical Pet System...")
try:
    from gamification_engine.pets.companion_system import MathPetSystem, PetType

    pet_system = MathPetSystem()
    pet_id = pet_system.adopt_pet("alice_pets", PetType.MATRIX_DRAGON, "Eigenbert")

    # Interact with pet
    result = pet_system.interaction_completed(
        "alice_pets", "problem_solved", {"accuracy": 0.95}
    )

    # Get pet info
    pet_info = pet_system.get_student_pets("alice_pets")
    if pet_info and pet_info["active_pet"]:
        pet = pet_info["active_pet"]
        print(f"   ✅ Pet Name: {pet['name']}")
        print(f"   ✅ Pet Type: {pet['pet_type']}")
        print(f"   ✅ Pet Level: {pet['level']}")
        print(f"   ✅ Pet Happiness: {pet['happiness']}")

except Exception as e:
    print(f"   ❌ Pet System Error: {e}")

# Test 3: Guild System
print("\n3. 🏰 Testing Guild System...")
try:
    from gamification_engine.social.guild_system import GuildManager

    guild_manager = GuildManager()
    guild_id = guild_manager.create_guild(
        "Linear Legends", "Elite linear algebra students", "alice_guild"
    )

    # Add members
    guild_manager.join_guild("bob_guild", guild_id)
    guild_manager.join_guild("charlie_guild", guild_id)

    # Create study party
    party_id = guild_manager.create_study_party("alice_guild")
    guild_manager.join_study_party("bob_guild", party_id)

    # Get guild info
    guild_info = guild_manager.get_student_guild_info("alice_guild")
    if guild_info:
        print(f"   ✅ Guild Name: {guild_info['guild']['name']}")
        print(f"   ✅ Guild Members: {len(guild_info['guild']['members'])}")
        print(f"   ✅ Is Leader: {guild_info['is_leader']}")

except Exception as e:
    print(f"   ❌ Guild System Error: {e}")

# Test 4: Competition System
print("\n4. ⚔️ Testing Competition System...")
try:
    from gamification_engine.social.competition_system import (
        PvPBattleEngine,
        BattleType,
    )

    battle_engine = PvPBattleEngine()
    battle_engine.register_competitor("alice_battle")
    battle_engine.register_competitor("bob_battle")

    # Queue for battle
    battle_engine.queue_for_battle("alice_battle", BattleType.SPEED_SOLVE)
    battle_engine.queue_for_battle("bob_battle", BattleType.SPEED_SOLVE)

    # Get competitor stats
    alice_stats = battle_engine.get_competitor_stats("alice_battle")
    if alice_stats:
        print(f"   ✅ Alice's Rank: {alice_stats['profile']['current_rank']}")
        print(f"   ✅ Alice's Points: {alice_stats['profile']['rank_points']}")
        print(f"   ✅ Total Battles: {alice_stats['profile']['total_battles']}")

except Exception as e:
    print(f"   ❌ Competition System Error: {e}")

# Test 5: World Building System
print("\n5. 🌍 Testing World Building System...")
try:
    from gamification_engine.world import WorldBuilder, WorldDimension

    world_builder = WorldBuilder()
    base_id = world_builder.create_study_base(
        "alice_world", "Alice's Fortress", WorldDimension.VECTOR_SPACE
    )

    # Gather resources
    resources = world_builder.gather_resources(
        "alice_world", WorldDimension.VECTOR_SPACE, 30
    )

    # Get world info
    world_info = world_builder.get_student_world_info("alice_world")
    if world_info:
        print(f"   ✅ Base Name: {world_info['base']['base_name']}")
        print(f"   ✅ Base Dimension: {world_info['base']['dimension']}")
        print(f"   ✅ Resources Gathered: {len(resources)} types")
        print(f"   ✅ Active Quests: {len(world_info['active_quests'])}")

except Exception as e:
    print(f"   ❌ World Building Error: {e}")

# Test 6: Events System
print("\n6. 🎪 Testing Real-Time Events System...")
try:
    from gamification_engine.events import RealTimeEventEngine, ChallengeType

    event_engine = RealTimeEventEngine()

    # Create flash challenge
    flash_id = event_engine.create_flash_challenge(60, ChallengeType.SPEED_SOLVE)

    # Register and attempt
    event_engine.register_for_event("alice_events", flash_id)

    # Get active events
    active_events = event_engine.get_active_events()
    print(f"   ✅ Active Events: {len(active_events)}")

    # Get student progress
    progress = event_engine.get_student_event_progress("alice_events")
    print(f"   ✅ Events Participated: {progress['total_events_participated']}")
    print(f"   ✅ Recent Badges: {len(progress['recent_badges'])}")

except Exception as e:
    print(f"   ❌ Events System Error: {e}")

print("\n" + "=" * 60)
print("🎉 Individual System Testing Complete!")
print("\n✨ Summary:")
print("   • RPG Player Profiles: Character classes and skill progression")
print("   • Mathematical Pets: Companion creatures that evolve with learning")
print("   • Guild System: Collaborative study groups and team dynamics")
print("   • Competition System: PvP battles and tournaments")
print("   • World Building: Exploration, base building, and resource gathering")
print("   • Real-Time Events: Daily challenges, boss fights, seasonal events")
print("\n🚀 Next-Generation Gamified Learning Platform Ready!")
