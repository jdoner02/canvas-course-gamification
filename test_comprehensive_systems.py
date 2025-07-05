#!/usr/bin/env python3
"""
🧪 COMPREHENSIVE SYSTEM TEST
Test all new gamification engine systems together
"""

import sys
import os
import traceback
from datetime import datetime, timedelta

# Add the src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))


def test_economy_system():
    """Test the economy and trading systems"""
    print("🪙 Testing Economy System...")

    try:
        from gamification_engine.economy.currency_system import (
            CurrencyManager,
            CurrencyType,
        )
        from gamification_engine.economy.trading_system import Marketplace, AuctionHouse

        # Initialize systems
        currency_manager = CurrencyManager()
        marketplace = Marketplace(currency_manager)
        auction_house = AuctionHouse(marketplace)

        # Test currency operations
        earned = currency_manager.award_currency("alice_123", "problem_solved_hard")
        print(f"  ✅ Currency earned: {earned}")

        # Test marketplace
        marketplace.give_starter_items("alice_123")
        marketplace.give_starter_items("bob_456")
        print(f"  ✅ Starter items distributed")

        # Test trading
        alice_items = marketplace.student_inventories["alice_123"]
        if alice_items:
            offer_id = marketplace.create_trade_offer(
                "alice_123",
                "bob_456",
                offered_items=[alice_items[0]],
                requested_currency={CurrencyType.COINS: 20},
            )
            print(f"  ✅ Trade offer created: {offer_id}")

        return True

    except Exception as e:
        print(f"  ❌ Economy system test failed: {e}")
        traceback.print_exc()
        return False


def test_ai_content_engine():
    """Test the AI content engine"""
    print("🤖 Testing AI Content Engine...")

    try:
        from gamification_engine.ai_content_engine.adaptive_learning import (
            AdaptiveLearningEngine,
            ConceptCategory,
            DifficultyLevel,
        )

        # Initialize engine
        engine = AdaptiveLearningEngine()

        # Record some activities
        engine.record_activity(
            "alice_123",
            "problem_solving",
            ConceptCategory.VECTORS,
            DifficultyLevel.MEDIUM,
            True,
            120.0,
        )

        # Get adaptive recommendation
        recommendation = engine.get_adaptive_recommendation("alice_123")
        print(f"  ✅ Recommendation generated: {recommendation.concept_category.value}")
        print(f"      Difficulty: {recommendation.difficulty_level.value}")
        print(f"      Confidence: {recommendation.confidence_score}")

        # Detect learning style
        learning_styles = engine.detect_learning_style("alice_123")
        print(f"  ✅ Learning styles detected: {len(learning_styles)} styles")

        return True

    except Exception as e:
        print(f"  ❌ AI content engine test failed: {e}")
        traceback.print_exc()
        return False


def test_analytics_engine():
    """Test the analytics engine"""
    print("📊 Testing Analytics Engine...")

    try:
        from gamification_engine.analytics_engine.learning_analytics import (
            LearningAnalyticsEngine,
            AnalyticsMetric,
        )

        # Initialize engine
        analytics = LearningAnalyticsEngine()

        # Record some analytics events
        analytics.record_analytics_event(
            "alice_123",
            "problem_completed",
            {"success": True, "concept": "vectors", "difficulty": "medium"},
        )

        analytics.record_analytics_event(
            "alice_123", "session_start", {"session_type": "problem_solving"}
        )

        # Calculate engagement score
        engagement = analytics.calculate_engagement_score("alice_123")
        print(f"  ✅ Engagement score calculated: {engagement}")

        # Calculate performance trend
        trend = analytics.calculate_performance_trend("alice_123")
        print(f"  ✅ Performance trend: {trend.trend_direction}")

        # Generate course analytics
        course_analytics = analytics.generate_course_analytics("MATH_231")
        print(f"  ✅ Course analytics generated")
        print(f"      Total students: {course_analytics.total_students}")
        print(f"      Average engagement: {course_analytics.average_engagement:.2f}")

        return True

    except Exception as e:
        print(f"  ❌ Analytics engine test failed: {e}")
        traceback.print_exc()
        return False


def test_existing_systems():
    """Test existing systems to ensure they still work"""
    print("🔄 Testing Existing Systems...")

    try:
        # Test core systems
        from gamification_engine.core.player_profile import (
            PlayerProfile,
            MathematicalSpecialization,
            Skill,
            SkillCategory,
        )
        from gamification_engine.pets.companion_system import MathematicalPet
        from gamification_engine.social.guild_system import GuildManager
        from datetime import datetime

        # Test player profile
        profile = PlayerProfile(
            "alice_123",
            "Alice Smith",
            MathematicalSpecialization.DATA_SCIENTIST,
            datetime.now(),
        )

        # Create a skill and add it to the profile
        vector_skill = Skill(
            "vector_ops",
            "Vector Operations",
            "Basic vector operations",
            SkillCategory.VECTOR_OPERATIONS,
        )
        profile.skills["vector_ops"] = vector_skill

        # Add experience to the skill
        result = vector_skill.add_experience(
            100, MathematicalSpecialization.DATA_SCIENTIST
        )
        print(
            f"  ✅ RPG profile: Level {vector_skill.current_level}, XP {vector_skill.current_xp}, Gained {result['levels_gained']} levels"
        )

        # Test pet system
        from gamification_engine.pets.companion_system import PetSpecies

        pet = MathematicalPet(
            "pet_001", PetSpecies.VECTOR_SPRITE, "Vectra", "alice_123"
        )
        pet.feed()
        print(f"  ✅ Pet system: {pet.name} happiness {pet.stats.happiness}")

        # Test guild system
        guild_manager = GuildManager()
        guild_id = guild_manager.create_guild(
            "alice_123", "Linear Legends", "Masters of matrices"
        )
        print(f"  ✅ Guild system: Created guild {guild_id}")

        return True

    except Exception as e:
        print(f"  ❌ Existing systems test failed: {e}")
        traceback.print_exc()
        return False


def test_integration():
    """Test integration between different systems"""
    print("🔗 Testing System Integration...")

    try:
        # Import all systems
        from gamification_engine.economy.currency_system import CurrencyManager
        from gamification_engine.ai_content_engine.adaptive_learning import (
            AdaptiveLearningEngine,
            ConceptCategory,
            DifficultyLevel,
        )
        from gamification_engine.analytics_engine.learning_analytics import (
            LearningAnalyticsEngine,
        )
        from gamification_engine.core.player_profile import PlayerProfile

        # Initialize systems
        currency_manager = CurrencyManager()
        ai_engine = AdaptiveLearningEngine()
        analytics = LearningAnalyticsEngine()

        # Simulate a complete learning session
        student_id = "integration_test_student"

        # 1. Student starts session
        analytics.record_analytics_event(
            student_id, "session_start", {"session_type": "practice"}
        )

        # 2. Student solves problems and earns currency
        for i in range(5):
            success = i < 4  # Succeed on 4 out of 5 problems

            # Record with AI engine
            ai_engine.record_activity(
                student_id,
                "problem_solving",
                ConceptCategory.VECTORS,
                DifficultyLevel.MEDIUM,
                success,
                120.0,
            )

            # Record with analytics
            analytics.record_analytics_event(
                student_id,
                "problem_completed",
                {"success": success, "concept": "vectors", "difficulty": "medium"},
            )

            # Award currency
            if success:
                currency_manager.award_currency(student_id, "problem_solved_medium")

        # 3. Get AI recommendation for next activity
        recommendation = ai_engine.get_adaptive_recommendation(student_id)

        # 4. Check analytics
        engagement = analytics.calculate_engagement_score(student_id)

        # 5. Check currency balance
        balance = currency_manager.get_student_balance(student_id)

        print(f"  ✅ Integration test completed")
        print(f"      Next recommendation: {recommendation.concept_category.value}")
        print(f"      Engagement score: {engagement:.2f}")
        print(f"      Currency balance: {balance.coins} coins")

        return True

    except Exception as e:
        print(f"  ❌ Integration test failed: {e}")
        traceback.print_exc()
        return False


def main():
    """Run comprehensive system tests"""
    print("🎮 COMPREHENSIVE GAMIFICATION ENGINE TEST")
    print("=" * 50)

    tests = [
        ("Economy System", test_economy_system),
        ("AI Content Engine", test_ai_content_engine),
        ("Analytics Engine", test_analytics_engine),
        ("Existing Systems", test_existing_systems),
        ("System Integration", test_integration),
    ]

    results = {}

    for test_name, test_func in tests:
        print(f"\n{test_name}:")
        results[test_name] = test_func()

    # Summary
    print("\n" + "=" * 50)
    print("📋 TEST SUMMARY:")

    passed = sum(results.values())
    total = len(results)

    for test_name, passed_test in results.items():
        status = "✅ PASS" if passed_test else "❌ FAIL"
        print(f"  {test_name}: {status}")

    print(f"\nOverall: {passed}/{total} tests passed")

    if passed == total:
        print("🎉 ALL TESTS PASSED! Systems are ready for deployment.")
    else:
        print("⚠️ Some tests failed. Please review and fix issues.")

    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
