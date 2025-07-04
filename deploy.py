#!/usr/bin/env python3
"""
Canvas Course Gamification - Main Deployment Script

Deploy gamified courses to Canvas LMS with skill trees, XP systems, and badges.
"""

import argparse
import logging
import sys
from pathlib import Path
from typing import Optional

# Load environment variables
from dotenv import load_dotenv

load_dotenv()

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.canvas_api import CanvasAPIClient
from src.course_builder import CourseBuilder
from src.validators import validate_course_deployment
from src.gamification import GamificationEngine, XPSystem

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(), logging.FileHandler("deployment.log")],
)

logger = logging.getLogger(__name__)


def main():
    """Main deployment function."""
    parser = argparse.ArgumentParser(
        description="Deploy gamified courses to Canvas LMS",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python deploy.py --config examples/linear_algebra --validate-only
  python deploy.py --config examples/linear_algebra --course-id 12345
  python deploy.py --config examples/linear_algebra --dry-run
        """,
    )

    parser.add_argument(
        "--config",
        "-c",
        type=Path,
        required=True,
        help="Path to course configuration directory",
    )

    parser.add_argument(
        "--course-id",
        type=str,
        help="Canvas course ID (overrides environment variable)",
    )

    parser.add_argument(
        "--validate-only",
        action="store_true",
        help="Only validate configuration without deploying",
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Perform all checks but don't actually deploy to Canvas",
    )

    parser.add_argument(
        "--verbose", "-v", action="store_true", help="Enable verbose logging"
    )

    parser.add_argument(
        "--force",
        action="store_true",
        help="Deploy even if warnings exist (errors will still block deployment)",
    )

    args = parser.parse_args()

    # Set logging level
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    try:
        # Initialize Canvas client
        logger.info("Initializing Canvas API client...")
        canvas_client = CanvasAPIClient(course_id=args.course_id)

        # Validate deployment readiness
        logger.info("Validating course configuration and API access...")
        validation_results = validate_course_deployment(args.config, canvas_client)

        # Display validation results
        print_validation_results(validation_results)

        if not validation_results["ready_for_deployment"]:
            logger.error("Course is not ready for deployment due to validation errors")
            return 1

        if args.validate_only:
            logger.info(
                "Validation complete. Use --deploy to actually deploy the course."
            )
            return 0

        if validation_results["overall_warnings"] and not args.force:
            logger.warning("Warnings detected. Use --force to deploy anyway.")
            return 1

        if args.dry_run:
            logger.info("Dry run complete. Course would be ready for deployment.")
            return 0

        # Deploy the course
        logger.info("Starting course deployment...")
        deploy_course(args.config, canvas_client)

        logger.info("Course deployment completed successfully!")
        return 0

    except KeyboardInterrupt:
        logger.info("Deployment cancelled by user")
        return 1
    except Exception as e:
        logger.error(f"Deployment failed: {e}")
        return 1


def print_validation_results(results):
    """Print validation results in a user-friendly format."""
    print("\n" + "=" * 60)
    print("COURSE VALIDATION RESULTS")
    print("=" * 60)

    # Overall status
    status = "✅ READY" if results["ready_for_deployment"] else "❌ NOT READY"
    print(f"Status: {status}")

    # Configuration validation
    config_val = results.get("config_validation", {})
    if config_val:
        print(f"\nConfiguration Validation:")
        print(f"  Sections validated: {len(config_val.get('sections_validated', []))}")
        print(f"  Errors: {len(config_val.get('errors', []))}")
        print(f"  Warnings: {len(config_val.get('warnings', []))}")

    # API validation
    api_val = results.get("api_validation", {})
    if api_val:
        print(f"\nCanvas API Validation:")
        print(f"  Connected: {'✅' if api_val.get('connected') else '❌'}")
        print(f"  Course access: {'✅' if api_val.get('course_access') else '❌'}")

        user_info = api_val.get("user_info", {})
        if user_info:
            print(f"  User: {user_info.get('name', 'Unknown')}")

    # Errors
    errors = results.get("overall_errors", [])
    if errors:
        print(f"\n❌ ERRORS ({len(errors)}):")
        for i, error in enumerate(errors, 1):
            print(f"  {i}. {error}")

    # Warnings
    warnings = results.get("overall_warnings", [])
    if warnings:
        print(f"\n⚠️  WARNINGS ({len(warnings)}):")
        for i, warning in enumerate(warnings, 1):
            print(f"  {i}. {warning}")

    print("=" * 60 + "\n")


def deploy_course(config_path: Path, canvas_client: CanvasAPIClient):
    """Deploy a course to Canvas."""
    # Initialize course builder
    builder = CourseBuilder(canvas_client)

    # Load configuration
    logger.info("Loading course configuration...")
    config = builder.load_course_config(config_path)

    # Build skill tree
    logger.info("Building skill tree...")
    skill_tree = builder.build_skill_tree(config)

    # Initialize gamification engine
    xp_system = XPSystem()
    gamification_engine = GamificationEngine(skill_tree, xp_system)

    # Deploy course components
    logger.info("Deploying course to Canvas...")
    deployment_results = builder.deploy_course(config)

    # Log deployment summary
    log_deployment_summary(deployment_results)

    # Generate post-deployment report
    generate_deployment_report(deployment_results, config_path)


def log_deployment_summary(results):
    """Log a summary of deployment results."""
    logger.info("Deployment Summary:")
    logger.info(f"  Modules: {len(results.get('modules', []))}")
    logger.info(f"  Assignments: {len(results.get('assignments', []))}")
    logger.info(f"  Pages: {len(results.get('pages', []))}")
    logger.info(f"  Quizzes: {len(results.get('quizzes', []))}")
    logger.info(f"  Outcomes: {len(results.get('outcomes', []))}")

    errors = results.get("errors", [])
    if errors:
        logger.warning(f"  Errors: {len(errors)}")
        for error in errors:
            logger.error(f"    - {error}")


def generate_deployment_report(results, config_path: Path):
    """Generate a detailed deployment report."""
    report_path = config_path / "deployment_report.md"

    with open(report_path, "w") as f:
        f.write("# Course Deployment Report\n\n")
        f.write(f"**Configuration Path:** {config_path}\n")
        f.write(f"**Course ID:** {results.get('course_id', 'Unknown')}\n")
        f.write(
            f"**Deployment Date:** {__import__('datetime').datetime.now().isoformat()}\n\n"
        )

        f.write("## Deployment Results\n\n")
        f.write(f"- **Modules:** {len(results.get('modules', []))}\n")
        f.write(f"- **Assignments:** {len(results.get('assignments', []))}\n")
        f.write(f"- **Pages:** {len(results.get('pages', []))}\n")
        f.write(f"- **Quizzes:** {len(results.get('quizzes', []))}\n")
        f.write(f"- **Outcomes:** {len(results.get('outcomes', []))}\n\n")

        errors = results.get("errors", [])
        if errors:
            f.write("## Errors\n\n")
            for error in errors:
                f.write(f"- {error}\n")

        f.write("\n## Next Steps\n\n")
        f.write("1. Review course structure in Canvas\n")
        f.write("2. Test skill tree progression\n")
        f.write("3. Verify gamification elements\n")
        f.write("4. Conduct student testing\n")

    logger.info(f"Deployment report saved to: {report_path}")


if __name__ == "__main__":
    sys.exit(main())
