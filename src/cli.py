#!/usr/bin/env python3
"""
Command-line interface for Canvas Course Gamification
"""

import click
import json
import logging
from pathlib import Path
from typing import Optional

from src.course_builder.data_loader import CourseDataLoader
from src.course_builder.json_course_builder import JsonCourseBuilder, CanvasConfig


def setup_logging(verbose: bool = False):
    """Setup logging configuration"""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )


@click.group()
@click.option("--verbose", "-v", is_flag=True, help="Enable verbose logging")
def cli(verbose):
    """Canvas Course Gamification CLI"""
    setup_logging(verbose)


@cli.command()
@click.argument("data_path", type=click.Path(exists=True))
@click.option("--output", "-o", type=click.Path(), help="Output summary file")
def validate(data_path, output):
    """Validate course JSON data files"""
    click.echo(f"Validating course data in: {data_path}")

    loader = CourseDataLoader(data_path)
    loader.load_all_data()

    # Run validation
    result = loader.validate_data()
    stats = loader.get_statistics()

    # Display results
    if result.is_valid:
        click.echo(click.style("✓ Validation passed", fg="green"))
    else:
        click.echo(click.style("✗ Validation failed", fg="red"))

    click.echo(f"\nErrors: {len(result.errors)}")
    for error in result.errors:
        click.echo(f"  - {error}", err=True)

    click.echo(f"\nWarnings: {len(result.warnings)}")
    for warning in result.warnings:
        click.echo(f"  - {warning}")

    # Display statistics
    click.echo(f"\nCourse Statistics:")
    click.echo(f"  Assignments: {stats['assignments']}")
    click.echo(f"  Modules: {stats['modules']}")
    click.echo(f"  Quizzes: {stats['quizzes']}")
    click.echo(f"  Pages: {stats['pages']}")
    click.echo(f"  Outcomes: {stats['outcomes']}")
    click.echo(f"  Total Questions: {stats['total_questions']}")
    click.echo(f"  Total Points: {stats['total_points']}")
    click.echo(f"  Total XP: {stats['xp_available']}")

    # Export summary if requested
    if output:
        loader.export_summary(output)
        click.echo(f"\nSummary exported to: {output}")


@cli.command()
@click.argument("data_path", type=click.Path(exists=True))
def stats(data_path):
    """Show course data statistics"""
    loader = CourseDataLoader(data_path)
    loader.load_all_data()
    stats = loader.get_statistics()

    click.echo("Course Data Statistics:")
    click.echo("=" * 30)

    for key, value in stats.items():
        formatted_key = key.replace("_", " ").title()
        click.echo(f"{formatted_key:20}: {value:>8}")


@cli.command()
@click.argument("data_path", type=click.Path(exists=True))
@click.argument("course_name")
@click.argument("course_code")
@click.option("--canvas-url", required=True, help="Canvas instance URL")
@click.option("--token", required=True, help="Canvas API token")
@click.option("--account-id", required=True, type=int, help="Canvas account ID")
@click.option("--term-id", type=int, help="Canvas term ID")
@click.option("--dry-run", is_flag=True, help="Validate but do not create course")
def build(
    data_path, course_name, course_code, canvas_url, token, account_id, term_id, dry_run
):
    """Build Canvas course from JSON data"""
    click.echo(f"Building course: {course_name} ({course_code})")

    # Validate data first
    loader = CourseDataLoader(data_path)
    loader.load_all_data()
    validation = loader.validate_data()

    if not validation.is_valid:
        click.echo(click.style("❌ Data validation failed", fg="red"))
        for error in validation.errors:
            click.echo(f"  - {error}", err=True)
        return

    if validation.warnings:
        click.echo(click.style("⚠️  Validation warnings:", fg="yellow"))
        for warning in validation.warnings:
            click.echo(f"  - {warning}")
        if not click.confirm("Continue despite warnings?"):
            return

    if dry_run:
        click.echo(
            click.style("✓ Dry run: Data is valid for course creation", fg="green")
        )
        stats = loader.get_statistics()
        click.echo(
            f"Would create course with {stats['assignments']} assignments, {stats['modules']} modules"
        )
        return

    # Create course
    canvas_config = CanvasConfig(
        base_url=canvas_url, token=token, account_id=account_id, term_id=term_id
    )

    builder = JsonCourseBuilder(data_path, canvas_config)

    try:
        course_id = builder.build_course(course_name, course_code)
        click.echo(
            click.style(
                f"✓ Course created successfully! Course ID: {course_id}", fg="green"
            )
        )
        click.echo(f"View course at: {canvas_url}/courses/{course_id}")

    except Exception as e:
        click.echo(click.style(f"❌ Course creation failed: {e}", fg="red"))
        raise


@cli.command()
@click.argument("input_path", type=click.Path(exists=True))
@click.argument("output_path", type=click.Path())
def export_template(input_path, output_path):
    """Export a template JSON structure based on existing data"""
    loader = CourseDataLoader(input_path)
    loader.load_all_data()

    # Create template with minimal structure
    template = {
        "assignments": {
            "assignments": [
                {
                    "id": "example-assignment",
                    "title": "Example Assignment",
                    "description": "Description of the assignment",
                    "points_possible": 100,
                    "due_at": "2025-12-31T23:59:00Z",
                    "mastery_threshold": 75,
                    "gamification": {"xp_value": 100, "badges": ["example_badge"]},
                    "outcomes": ["example_outcome"],
                }
            ]
        },
        "modules": {
            "modules": [
                {
                    "name": "Example Module",
                    "overview": "Module overview",
                    "unlock_requirements": [],
                    "mastery_criteria": {
                        "completion_requirement": "min_score",
                        "min_score": 75,
                    },
                    "gamification": {
                        "theme": "Example Theme",
                        "badges": ["module_badge"],
                        "xp_value": 50,
                    },
                    "items": [{"id": "example-assignment"}],
                }
            ]
        },
        "outcomes": {
            "outcomes": [
                {
                    "id": "example_outcome",
                    "name": "Example Learning Outcome",
                    "description": "Students will be able to...",
                    "level": "Application",
                    "module": 1,
                    "badge": "example_badge",
                }
            ]
        },
        "pages": {
            "pages": [
                {
                    "title": "Example Page",
                    "body": "<h1>Example Page</h1><p>Page content here</p>",
                    "front_page": False,
                }
            ]
        },
        "quizzes": {
            "quizzes": [
                {
                    "id": "example-quiz",
                    "title": "Example Quiz",
                    "description": "Quiz description",
                    "settings": {"allowed_attempts": 3, "time_limit": 30},
                    "questions": [
                        {
                            "type": "multiple_choice_question",
                            "question_text": "Example question?",
                            "answers": [
                                {"text": "Correct answer", "weight": 100},
                                {"text": "Wrong answer", "weight": 0},
                            ],
                            "points_possible": 1,
                        }
                    ],
                }
            ]
        },
        "prerequisites": {"prerequisites": []},
        "assignment_id_map": {},
    }

    with open(output_path, "w") as f:
        json.dump(template, f, indent=2)

    click.echo(f"Template exported to: {output_path}")


@cli.command()
@click.argument("data_path", type=click.Path(exists=True))
@click.option("--assignment-id", help="Show details for specific assignment")
@click.option("--module-name", help="Show details for specific module")
@click.option("--quiz-id", help="Show details for specific quiz")
def inspect(data_path, assignment_id, module_name, quiz_id):
    """Inspect course data details"""
    loader = CourseDataLoader(data_path)
    loader.load_all_data()
    data = loader.data

    if assignment_id:
        assignments = data.get("assignments", {}).get("assignments", [])
        assignment = next((a for a in assignments if a["id"] == assignment_id), None)
        if assignment:
            click.echo(f"Assignment: {assignment['title']}")
            click.echo(f"ID: {assignment['id']}")
            click.echo(f"Points: {assignment.get('points_possible', 'N/A')}")
            click.echo(f"Due: {assignment.get('due_at', 'No due date')}")
            if "gamification" in assignment:
                click.echo(f"XP: {assignment['gamification'].get('xp_value', 0)}")
                click.echo(
                    f"Badges: {', '.join(assignment['gamification'].get('badges', []))}"
                )
        else:
            click.echo(f"Assignment '{assignment_id}' not found")

    elif module_name:
        modules = data.get("modules", {}).get("modules", [])
        module = next((m for m in modules if m["name"] == module_name), None)
        if module:
            click.echo(f"Module: {module['name']}")
            click.echo(f"Overview: {module.get('overview', '')}")
            click.echo(
                f"Prerequisites: {', '.join(module.get('unlock_requirements', []))}"
            )
            click.echo(f"Items: {len(module.get('items', []))}")
            for item in module.get("items", []):
                click.echo(f"  - {item.get('id', 'Unknown')}")
        else:
            click.echo(f"Module '{module_name}' not found")

    elif quiz_id:
        quizzes = data.get("quizzes", {}).get("quizzes", [])
        quiz = next((q for q in quizzes if q["id"] == quiz_id), None)
        if quiz:
            click.echo(f"Quiz: {quiz['title']}")
            click.echo(f"ID: {quiz['id']}")
            click.echo(f"Questions: {len(quiz.get('questions', []))}")
            settings = quiz.get("settings", {})
            click.echo(f"Time Limit: {settings.get('time_limit', 'None')} minutes")
            click.echo(f"Attempts: {settings.get('allowed_attempts', 'Unlimited')}")
        else:
            click.echo(f"Quiz '{quiz_id}' not found")
    else:
        # Show overview
        click.echo("Course Data Overview:")
        click.echo("=" * 30)

        assignments = data.get("assignments", {}).get("assignments", [])
        click.echo(f"Assignments ({len(assignments)}):")
        for assignment in assignments[:5]:  # Show first 5
            click.echo(f"  - {assignment['id']}: {assignment['title']}")
        if len(assignments) > 5:
            click.echo(f"  ... and {len(assignments) - 5} more")

        modules = data.get("modules", {}).get("modules", [])
        click.echo(f"\nModules ({len(modules)}):")
        for module in modules[:5]:
            click.echo(f"  - {module['name']}")
        if len(modules) > 5:
            click.echo(f"  ... and {len(modules) - 5} more")


if __name__ == "__main__":
    cli()
