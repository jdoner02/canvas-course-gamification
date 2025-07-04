#!/usr/bin/env python3
"""
Demo script showing Canvas Course Gamification functionality
"""

import os
import sys
from pathlib import Path

# Add src to path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from src.course_builder.data_loader import CourseDataLoader
from src.course_builder.json_course_builder import JsonCourseBuilder, CanvasConfig


def main():
    """Main demo function"""
    print("🎓 Canvas Course Gamification Demo")
    print("=" * 50)

    # Path to MATH231 data
    data_path = Path(__file__).parent / "data" / "math231"

    if not data_path.exists():
        print("❌ MATH231 data directory not found!")
        return 1

    print(f"📁 Loading course data from: {data_path}")

    # Load and validate data
    loader = CourseDataLoader(str(data_path))
    loader.load_all_data()

    print("✅ Course data loaded successfully!")

    # Show statistics
    stats = loader.get_statistics()
    print(f"\n📊 Course Statistics:")
    print(f"   📚 Assignments: {stats['assignments']}")
    print(f"   📖 Modules: {stats['modules']}")
    print(f"   ❓ Quizzes: {stats['quizzes']}")
    print(f"   📄 Pages: {stats['pages']}")
    print(f"   🎯 Outcomes: {stats['outcomes']}")
    print(f"   ❓ Total Questions: {stats['total_questions']}")
    print(f"   💯 Total Points: {stats['total_points']}")
    print(f"   ⭐ Total XP Available: {stats['xp_available']}")

    # Validate data
    print(f"\n🔍 Validating course data...")
    validation = loader.validate_data()

    if validation.is_valid:
        print("✅ Validation passed!")
    else:
        print("❌ Validation failed!")

    print(f"   🚨 Errors: {len(validation.errors)}")
    print(f"   ⚠️  Warnings: {len(validation.warnings)}")

    # Show some sample data
    print(f"\n📋 Sample Assignment Data:")
    assignments = loader.data["assignments"]["assignments"]
    for i, assignment in enumerate(assignments[:3]):
        print(f"   {i+1}. {assignment['title']} ({assignment['points_possible']} pts)")
        if "gamification" in assignment:
            xp = assignment["gamification"].get("xp_value", 0)
            badges = assignment["gamification"].get("badges", [])
            print(f"      ⭐ XP: {xp}, 🏆 Badges: {', '.join(badges[:2])}")

    print(f"\n📚 Sample Module Data:")
    modules = loader.data["modules"]["modules"]
    for i, module in enumerate(modules[:3]):
        print(f"   {i+1}. {module['name']}")
        print(f"      📝 Items: {len(module.get('items', []))}")
        mastery = module.get("mastery_criteria", {}).get("min_score")
        if mastery:
            print(f"      🎯 Mastery Threshold: {mastery}%")

    # Test course builder initialization (without creating actual course)
    print(f"\n🏗️  Testing Course Builder...")
    try:
        config = CanvasConfig(
            base_url="https://demo.instructure.com", token="demo_token", account_id=1
        )

        builder = JsonCourseBuilder(str(data_path), config)
        builder.load_course_data()

        # Validate the loaded data
        validation_errors = builder.validate_course_data()
        total_errors = sum(len(errors) for errors in validation_errors.values())

        print(f"✅ Course builder initialized successfully!")
        print(
            f"   📊 Data validation: {total_errors} total errors across all categories"
        )

        if total_errors == 0:
            print("   🎉 Course data is ready for Canvas deployment!")
        else:
            print("   🔧 Some data issues found - see validation report for details")

    except Exception as e:
        print(f"❌ Course builder error: {e}")

    print(f"\n🎯 Demo Complete!")
    print(f"   The MATH231 Linear Algebra course data has been successfully")
    print(f"   integrated into the Canvas Course Gamification framework!")
    print(f"   Use 'python -m src.cli --help' for more commands.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
