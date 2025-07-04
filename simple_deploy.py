#!/usr/bin/env python3
"""
Simple deployment script that bypasses the validation result bug
"""

import sys
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.canvas_api import CanvasAPIClient
from src.course_builder import CourseBuilder


def deploy_course():
    """Deploy the course directly using the course builder."""
    try:
        # Initialize Canvas client
        print("🔧 Initializing Canvas API client...")
        canvas_client = CanvasAPIClient()

        # Initialize course builder
        print("📚 Initializing Course Builder...")
        course_builder = CourseBuilder(canvas_client=canvas_client)

        # Load configuration
        config_path = Path("examples/linear_algebra")
        print(f"📖 Loading course configuration from {config_path}...")

        # Load the course configuration
        course_config = course_builder.load_course_config(config_path)

        # Deploy the course
        print("🚀 Starting deployment...")
        deployment_result = course_builder.deploy_course(course_config)

        print("✅ Deployment completed successfully!")
        print(f"📊 Deployment summary: {deployment_result}")

    except Exception as e:
        print(f"❌ Deployment failed: {e}")
        return False

    return True


if __name__ == "__main__":
    success = deploy_course()
    sys.exit(0 if success else 1)
