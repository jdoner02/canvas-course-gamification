#!/usr/bin/env python3
"""
🧪 Test New Autonomous Systems
Quick test of newly created autonomous systems
"""

import asyncio
import sys
import os

sys.path.append(".")


async def test_new_systems():
    """Test all newly created autonomous systems"""
    print("🧪 Testing New Autonomous Systems")
    print("=" * 50)

    # Test Faculty Onboarding System
    try:
        from src.onboarding.faculty_automation import FacultyOnboardingSystem

        faculty_system = FacultyOnboardingSystem()
        print("✅ Faculty Onboarding System: LOADED")

        # Quick test
        test_result = await faculty_system.start_onboarding(
            "test.faculty@example.edu", "MATH231"
        )
        if test_result["success"]:
            print("✅ Faculty Onboarding System: FUNCTIONAL")
        else:
            print(
                f"⚠️ Faculty Onboarding System: {test_result.get('error', 'Unknown error')}"
            )
    except Exception as e:
        print(f"❌ Faculty Onboarding System: ERROR - {e}")

    # Test Student Onboarding System
    try:
        from src.onboarding.student_automation import StudentOnboardingSystem

        student_system = StudentOnboardingSystem()
        print("✅ Student Onboarding System: LOADED")

        # Quick test
        test_result = await student_system.onboard_student(
            "test.student@example.edu", "Test Student", ["MATH231"]
        )
        if test_result["success"]:
            print("✅ Student Onboarding System: FUNCTIONAL")
        else:
            print(
                f"⚠️ Student Onboarding System: {test_result.get('error', 'Unknown error')}"
            )
    except Exception as e:
        print(f"❌ Student Onboarding System: ERROR - {e}")

    # Test Research Analytics System
    try:
        from src.research.analytics_automation import ResearchAnalyticsSystem

        research_system = ResearchAnalyticsSystem()
        print("✅ Research Analytics System: LOADED")

        # Quick test
        from src.research.analytics_automation import StudyType

        test_result = await research_system.create_research_project(
            "Test Study",
            "Test gamification effectiveness",
            "Test Researcher",
            StudyType.CROSS_SECTIONAL,
            ["Does gamification help?"],
        )
        if test_result["success"]:
            print("✅ Research Analytics System: FUNCTIONAL")
        else:
            print(
                f"⚠️ Research Analytics System: {test_result.get('error', 'Unknown error')}"
            )
    except Exception as e:
        print(f"❌ Research Analytics System: ERROR - {e}")

    # Test Content Curation Engine
    try:
        from src.content.curation_engine import ContentCurationEngine

        content_system = ContentCurationEngine()
        print("✅ Content Curation Engine: LOADED")

        # Quick test
        from src.content.curation_engine import DifficultyLevel

        test_result = await content_system.curate_content_for_topic(
            "linear_algebra", DifficultyLevel.INTERMEDIATE, 5
        )
        if test_result["success"]:
            print("✅ Content Curation Engine: FUNCTIONAL")
        else:
            print(
                f"⚠️ Content Curation Engine: {test_result.get('error', 'Unknown error')}"
            )
    except Exception as e:
        print(f"❌ Content Curation Engine: ERROR - {e}")

    # Test Security Systems
    try:
        from src.security import get_security_status

        security_status = await get_security_status()
        if security_status["overall_status"] == "healthy":
            print("✅ Security Systems: FUNCTIONAL")
        else:
            print(f"⚠️ Security Systems: {security_status}")
    except Exception as e:
        print(f"❌ Security Systems: ERROR - {e}")

    print("\n" + "=" * 50)
    print("🎯 New Systems Test Complete!")


if __name__ == "__main__":
    asyncio.run(test_new_systems())
