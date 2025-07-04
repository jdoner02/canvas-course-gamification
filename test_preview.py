#!/usr/bin/env python3
"""
Test script for the preview generator
"""

import sys
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.preview_generator import PreviewGenerator


def test_preview_generator():
    """Test the preview generator with MATH 231 data."""
    print("Testing Preview Generator...")

    # Set up paths
    data_path = "data/math231"
    output_path = "output/math231_preview.html"

    try:
        # Create preview generator
        generator = PreviewGenerator(data_path, output_path)

        # Load course data
        print("Loading course data...")
        generator.load_course_data()

        # Build skill tree
        print("Building skill tree...")
        skill_tree = generator.build_skill_tree()
        print(
            f"Skill tree built with {len(skill_tree.nodes)} nodes and {len(skill_tree.badges)} badges"
        )

        # Generate preview data
        print("Generating preview data...")
        preview_data = generator.generate_preview_data()
        print(
            f"Generated preview data with {len(preview_data['progress_scenarios'])} scenarios"
        )

        # Create the preview template if it doesn't exist
        print("Creating preview template...")
        generator.create_html_template()

        # Generate preview
        print("Generating HTML preview...")
        generator.generate_preview()

        print(f"Preview generated successfully: {output_path}")
        return True

    except Exception as e:
        print(f"Error testing preview generator: {e}")
        import traceback

        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = test_preview_generator()
    sys.exit(0 if success else 1)
