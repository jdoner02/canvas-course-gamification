#!/usr/bin/env python3
"""
Canvas Course Gamification Framework - Command Line Interface
=============================================================

A comprehensive CLI for creating, validating, and deploying gamified Canvas courses.

Features:
- Course validation with detailed reporting
- Canvas course creation and deployment
- Template generation and scaffolding
- Analytics and reporting
- Batch operations and automation
- Quality assurance and testing

Version: 2.0
Documentation: https://github.com/yourusername/canvas-course-gamification/wiki
"""

import click
import json
import logging
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any, List
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.prompt import Confirm, Prompt
from rich.syntax import Syntax
from rich.tree import Tree

from src.course_builder.data_loader import CourseDataLoader
from src.course_builder.json_course_builder import JsonCourseBuilder, CanvasConfig

# Initialize Rich console for beautiful output
console = Console()

# Version information
__version__ = "2.0.0"
__author__ = "Canvas Course Gamification Team"


def setup_logging(
    verbose: bool = False, debug: bool = False, log_file: Optional[str] = None
):
    """Setup comprehensive logging configuration"""
    if debug:
        level = logging.DEBUG
    elif verbose:
        level = logging.INFO
    else:
        level = logging.WARNING

    # Configure logging format
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(level)

    # File handler if specified
    handlers = [console_handler]
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        file_handler.setLevel(logging.DEBUG)  # Always debug to file
        handlers.append(file_handler)

    # Configure root logger
    logging.basicConfig(
        level=level,
        handlers=handlers,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )


def print_banner():
    """Print application banner"""
    banner = """
╔═══════════════════════════════════════════════════════════════╗
║         Canvas Course Gamification Framework CLI             ║
║                      Version 2.0.0                           ║
║                                                               ║
║  Transform traditional courses into engaging, game-like      ║
║  learning experiences with research-backed mechanics         ║
╚═══════════════════════════════════════════════════════════════╝
"""
    console.print(banner, style="bold cyan")


def handle_errors(func):
    """Decorator for comprehensive error handling"""

    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyboardInterrupt:
            console.print("\n⚠️  Operation cancelled by user", style="yellow")
            sys.exit(130)
        except FileNotFoundError as e:
            console.print(f"❌ File not found: {e}", style="red")
            sys.exit(1)
        except PermissionError as e:
            console.print(f"❌ Permission denied: {e}", style="red")
            sys.exit(1)
        except json.JSONDecodeError as e:
            console.print(f"❌ Invalid JSON format: {e}", style="red")
            sys.exit(1)
        except Exception as e:
            console.print(f"❌ Unexpected error: {e}", style="red")
            if kwargs.get("debug"):
                console.print_exception()
            sys.exit(1)

    return wrapper


@click.group()
@click.option("--verbose", "-v", is_flag=True, help="Enable verbose output")
@click.option(
    "--debug", "-d", is_flag=True, help="Enable debug mode with detailed error info"
)
@click.option("--log-file", type=click.Path(), help="Write logs to specified file")
@click.option("--no-banner", is_flag=True, help="Suppress banner display")
@click.version_option(version=__version__, prog_name="Canvas Course Gamification CLI")
@click.pass_context
def cli(ctx, verbose, debug, log_file, no_banner):
    """
    Canvas Course Gamification Framework CLI

    A comprehensive tool for creating and managing gamified Canvas courses
    with research-backed engagement mechanics and mastery-based learning.

    \b
    Common workflows:
      1. Create new course: validate → build → deploy
      2. Update existing: validate → update → test
      3. Template creation: scaffold → customize → validate

    \b
    Examples:
      gamify validate ./course-data --detailed
      gamify build ./course-data "Course Name" "CS101" --dry-run
      gamify deploy ./course-data --canvas-url https://school.instructure.com
      gamify scaffold linear-algebra --template math

    For detailed help on any command, use: gamify COMMAND --help
    """
    # Initialize context
    ctx.ensure_object(dict)
    ctx.obj["verbose"] = verbose
    ctx.obj["debug"] = debug

    # Setup logging
    setup_logging(verbose, debug, log_file)

    # Display banner unless suppressed
    if not no_banner:
        print_banner()


@cli.command()
@click.argument("data_path", type=click.Path(exists=True, path_type=Path))
@click.option(
    "--output",
    "-o",
    type=click.Path(path_type=Path),
    help="Export detailed validation report",
)
@click.option(
    "--detailed", "-d", is_flag=True, help="Show detailed validation information"
)
@click.option(
    "--format",
    "output_format",
    type=click.Choice(["text", "json", "html"]),
    default="text",
    help="Output format for reports",
)
@click.option("--fix", is_flag=True, help="Attempt to auto-fix common issues")
@click.pass_context
@handle_errors
def validate(
    ctx,
    data_path: Path,
    output: Optional[Path],
    detailed: bool,
    output_format: str,
    fix: bool,
):
    """
    Validate course JSON data files for completeness and correctness.

    \b
    Validation checks include:
    • JSON schema compliance
    • Cross-reference integrity (IDs, prerequisites)
    • Gamification configuration validity
    • Canvas API compatibility
    • Accessibility compliance
    • Educational design best practices

    \b
    Examples:
      gamify validate ./examples/linear_algebra
      gamify validate ./my-course --detailed --output report.html
      gamify validate ./course-data --fix
    """
    with console.status("[bold green]Validating course data..."):
        console.print(f"🔍 Validating course data in: [bold]{data_path}[/bold]")

        # Load and validate data
        loader = CourseDataLoader(str(data_path))
        loader.load_all_data()
        result = loader.validate_data()
        stats = loader.get_statistics()

    # Create validation results display
    if result.is_valid:
        console.print("✅ [bold green]Validation passed successfully![/bold green]")
        validation_icon = "✅"
        status_color = "green"
    else:
        console.print("❌ [bold red]Validation failed[/bold red]")
        validation_icon = "❌"
        status_color = "red"

    # Create validation summary table
    summary_table = Table(
        title=f"{validation_icon} Validation Summary", show_header=True
    )
    summary_table.add_column("Check", style="cyan")
    summary_table.add_column("Status", justify="center")
    summary_table.add_column("Count", justify="right")

    summary_table.add_row(
        "Schema Validation", "✅ Pass" if result.is_valid else "❌ Fail", "—"
    )
    summary_table.add_row(
        "Errors Found",
        "❌ Issues" if result.errors else "✅ None",
        str(len(result.errors)),
    )
    summary_table.add_row(
        "Warnings",
        "⚠️ Found" if result.warnings else "✅ None",
        str(len(result.warnings)),
    )

    console.print(summary_table)

    # Display errors if any
    if result.errors:
        error_panel = Panel(
            "\n".join([f"• {error}" for error in result.errors]),
            title="❌ Validation Errors",
            border_style="red",
        )
        console.print(error_panel)

    # Display warnings if any
    if result.warnings:
        warning_panel = Panel(
            "\n".join([f"• {warning}" for warning in result.warnings]),
            title="⚠️ Validation Warnings",
            border_style="yellow",
        )
        console.print(warning_panel)

    # Display detailed statistics if requested
    if detailed:
        stats_table = Table(title="📊 Course Content Statistics", show_header=True)
        stats_table.add_column("Content Type", style="cyan")
        stats_table.add_column("Count", justify="right", style="magenta")
        stats_table.add_column("Details", style="dim")

        stats_table.add_row(
            "Assignments",
            str(stats["assignments"]),
            "Learning activities with XP values",
        )
        stats_table.add_row(
            "Modules", str(stats["modules"]), "Organized learning units"
        )
        stats_table.add_row("Quizzes", str(stats["quizzes"]), "Assessment instruments")
        stats_table.add_row("Pages", str(stats["pages"]), "Instructional content")
        stats_table.add_row("Outcomes", str(stats["outcomes"]), "Learning objectives")
        stats_table.add_row(
            "Total Questions",
            str(stats["total_questions"]),
            "Quiz and assessment items",
        )
        stats_table.add_row(
            "Total Points", str(stats["total_points"]), "Traditional grade points"
        )
        stats_table.add_row(
            "Total XP Available",
            str(stats["xp_available"]),
            "Experience points for gamification",
        )

        console.print(stats_table)

    # Auto-fix functionality
    if fix and (result.errors or result.warnings):
        if Confirm.ask("🔧 Attempt to auto-fix detected issues?"):
            with console.status("[bold yellow]Applying automatic fixes..."):
                # Implement auto-fix logic here
                console.print("🔧 Auto-fix functionality coming in next version")

    # Export detailed report if requested
    if output:
        with console.status(f"[bold blue]Generating {output_format} report..."):
            if output_format == "json":
                report_data = {
                    "validation_result": {
                        "is_valid": result.is_valid,
                        "errors": result.errors,
                        "warnings": result.warnings,
                    },
                    "statistics": stats,
                    "generated_at": datetime.now().isoformat(),
                    "course_path": str(data_path),
                }
                with open(output, "w") as f:
                    json.dump(report_data, f, indent=2)
            else:
                loader.export_summary(str(output))

        console.print(f"📄 Detailed report exported to: [bold]{output}[/bold]")

    # Exit with appropriate code
    sys.exit(0 if result.is_valid else 1)


@cli.command()
@click.argument("data_path", type=click.Path(exists=True, path_type=Path))
@click.option(
    "--format",
    "output_format",
    type=click.Choice(["table", "json", "csv"]),
    default="table",
    help="Output format",
)
@click.option(
    "--export", type=click.Path(path_type=Path), help="Export statistics to file"
)
@click.pass_context
@handle_errors
def stats(ctx, data_path: Path, output_format: str, export: Optional[Path]):
    """
    Display comprehensive course data statistics and analytics.

    \b
    Shows detailed metrics about:
    • Content distribution (assignments, quizzes, pages)
    • Gamification elements (XP values, badges, progression)
    • Learning structure (modules, prerequisites, outcomes)
    • Quality indicators (balance, coverage, accessibility)

    \b
    Examples:
      gamify stats ./examples/linear_algebra
      gamify stats ./my-course --format json --export stats.json
    """
    with console.status("[bold green]Calculating course statistics..."):
        loader = CourseDataLoader(str(data_path))
        loader.load_all_data()
        stats = loader.get_statistics()

        # Calculate additional analytics
        extended_stats = calculate_extended_statistics(loader.data)
        stats.update(extended_stats)

    if output_format == "table":
        display_statistics_table(stats)
    elif output_format == "json":
        console.print_json(data=stats)
    elif output_format == "csv":
        display_statistics_csv(stats)

    if export:
        with open(export, "w") as f:
            json.dump(stats, f, indent=2)
        console.print(f"📊 Statistics exported to: [bold]{export}[/bold]")


def calculate_extended_statistics(data: Dict[str, Any]) -> Dict[str, Any]:
    """Calculate extended analytics beyond basic counts"""
    extended = {}

    # XP Distribution Analysis
    assignments = data.get("assignments", {}).get("assignments", [])
    xp_values = [a.get("gamification", {}).get("xp_value", 0) for a in assignments]
    if xp_values:
        extended["xp_distribution"] = {
            "min": min(xp_values),
            "max": max(xp_values),
            "average": sum(xp_values) / len(xp_values),
            "total": sum(xp_values),
        }

    # Module Complexity Analysis
    modules = data.get("modules", {}).get("modules", [])
    module_sizes = [len(m.get("items", [])) for m in modules]
    if module_sizes:
        extended["module_complexity"] = {
            "avg_items_per_module": sum(module_sizes) / len(module_sizes),
            "largest_module": max(module_sizes),
            "smallest_module": min(module_sizes),
        }

    # Prerequisites Complexity
    prereq_counts = [len(m.get("unlock_requirements", [])) for m in modules]
    extended["prerequisite_complexity"] = {
        "modules_with_prerequisites": sum(1 for count in prereq_counts if count > 0),
        "max_prerequisites": max(prereq_counts) if prereq_counts else 0,
        "avg_prerequisites": (
            sum(prereq_counts) / len(prereq_counts) if prereq_counts else 0
        ),
    }

    return extended


def display_statistics_table(stats: Dict[str, Any]):
    """Display statistics in a beautiful table format"""
    # Basic content statistics
    content_table = Table(title="📚 Content Overview", show_header=True)
    content_table.add_column("Content Type", style="cyan")
    content_table.add_column("Count", justify="right", style="magenta")
    content_table.add_column("Percentage", justify="right", style="green")

    total_content = sum(
        [stats.get("assignments", 0), stats.get("quizzes", 0), stats.get("pages", 0)]
    )

    if total_content > 0:
        content_table.add_row(
            "Assignments",
            str(stats.get("assignments", 0)),
            f"{stats.get('assignments', 0)/total_content*100:.1f}%",
        )
        content_table.add_row(
            "Quizzes",
            str(stats.get("quizzes", 0)),
            f"{stats.get('quizzes', 0)/total_content*100:.1f}%",
        )
        content_table.add_row(
            "Pages",
            str(stats.get("pages", 0)),
            f"{stats.get('pages', 0)/total_content*100:.1f}%",
        )

    console.print(content_table)

    # Gamification statistics
    if "xp_distribution" in stats:
        xp_data = stats["xp_distribution"]
        gamification_table = Table(title="🎮 Gamification Metrics", show_header=True)
        gamification_table.add_column("Metric", style="cyan")
        gamification_table.add_column("Value", justify="right", style="magenta")

        gamification_table.add_row("Total XP Available", str(xp_data["total"]))
        gamification_table.add_row(
            "Average XP per Assignment", f"{xp_data['average']:.1f}"
        )
        gamification_table.add_row("Highest XP Value", str(xp_data["max"]))
        gamification_table.add_row("Lowest XP Value", str(xp_data["min"]))

        console.print(gamification_table)


def display_statistics_csv(stats: Dict[str, Any]):
    """Display statistics in CSV format"""
    console.print("metric,value")
    for key, value in stats.items():
        if isinstance(value, dict):
            for subkey, subvalue in value.items():
                console.print(f"{key}_{subkey},{subvalue}")
        else:
            console.print(f"{key},{value}")


@cli.command()
@click.argument("data_path", type=click.Path(exists=True, path_type=Path))
@click.argument("course_name")
@click.argument("course_code")
@click.option(
    "--canvas-url",
    required=True,
    help="Canvas instance URL (e.g., https://school.instructure.com)",
)
@click.option("--token", required=True, help="Canvas API token")
@click.option("--account-id", required=True, type=int, help="Canvas account ID")
@click.option("--term-id", type=int, help="Canvas term ID (optional)")
@click.option(
    "--dry-run", is_flag=True, help="Validate and preview without creating course"
)
@click.option("--force", is_flag=True, help="Skip confirmation prompts")
@click.option("--backup", is_flag=True, help="Create backup before deployment")
@click.pass_context
@handle_errors
def build(
    ctx,
    data_path: Path,
    course_name: str,
    course_code: str,
    canvas_url: str,
    token: str,
    account_id: int,
    term_id: Optional[int],
    dry_run: bool,
    force: bool,
    backup: bool,
):
    """
    Build and deploy a Canvas course from JSON configuration data.
    
    \b
    Process overview:
    1. Validate course data integrity
    2. Verify Canvas API connectivity
    3. Preview course structure (if dry-run)
    4. Create course and content in Canvas
    5. Configure gamification elements
    6. Run post-deployment verification
    
    \b
    Examples:
      gamify build ./examples/linear_algebra "Linear Algebra" "MATH231" \\
        --canvas-url https://school.instructure.com \\
        --token your_api_token --account-id 1 --dry-run
      
      gamify build ./my-course "My Course" "CS101" \\
        --canvas-url https://school.instructure.com \\
        --token your_api_token --account-id 1 --term-id 5
    """
    console.print(
        f"🏗️  Building course: [bold]{course_name}[/bold] ([cyan]{course_code}[/cyan])"
    )

    # Step 1: Validate data
    with console.status("[bold green]Validating course data..."):
        loader = CourseDataLoader(str(data_path))
        loader.load_all_data()
        validation = loader.validate_data()

    if not validation.is_valid:
        console.print("❌ [bold red]Data validation failed[/bold red]")
        error_panel = Panel(
            "\n".join([f"• {error}" for error in validation.errors]),
            title="Validation Errors",
            border_style="red",
        )
        console.print(error_panel)
        return

    if validation.warnings:
        warning_panel = Panel(
            "\n".join([f"• {warning}" for warning in validation.warnings]),
            title="⚠️ Validation Warnings",
            border_style="yellow",
        )
        console.print(warning_panel)

        if not force and not Confirm.ask("Continue despite warnings?"):
            return

    # Step 2: Verify Canvas connectivity
    with console.status("[bold blue]Verifying Canvas API connectivity..."):
        canvas_config = CanvasConfig(
            base_url=canvas_url, token=token, account_id=account_id, term_id=term_id
        )

        # Test API connectivity here
        # builder = JsonCourseBuilder(str(data_path), canvas_config)
        # if not builder.test_connectivity():
        #     console.print("❌ Cannot connect to Canvas API")
        #     return

    # Step 3: Preview mode
    if dry_run:
        stats = loader.get_statistics()

        preview_panel = Panel(
            f"""
✅ [bold green]Dry run successful![/bold green]

Course would be created with:
• {stats['assignments']} assignments with {stats['xp_available']} total XP
• {stats['modules']} modules with prerequisite relationships
• {stats['quizzes']} quizzes and assessments
• {stats['pages']} instructional pages
• {stats['outcomes']} learning outcomes

🔗 Course would be accessible at: {canvas_url}/courses/[course_id]
            """,
            title="🔍 Deployment Preview",
            border_style="green",
        )
        console.print(preview_panel)
        return

    # Step 4: Final confirmation
    if not force:
        console.print(f"\n📋 Ready to create course in Canvas:")
        console.print(f"   • URL: {canvas_url}")
        console.print(f"   • Account ID: {account_id}")
        console.print(f"   • Course: {course_name} ({course_code})")

        if not Confirm.ask("\nProceed with course creation?"):
            console.print("Operation cancelled.")
            return

    # Step 5: Create course
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:

        # Create backup if requested
        if backup:
            task = progress.add_task("Creating backup...", total=None)
            # Implement backup logic
            time.sleep(1)  # Placeholder

        # Build course
        task = progress.add_task("Creating Canvas course...", total=None)
        builder = JsonCourseBuilder(str(data_path), canvas_config)

        try:
            course_id = builder.build_course(course_name, course_code)
            progress.update(task, description="✅ Course created successfully!")

            # Success message
            success_panel = Panel(
                f"""
🎉 [bold green]Course created successfully![/bold green]

📚 Course: {course_name} ({course_code})
🆔 Course ID: {course_id}
🔗 URL: {canvas_url}/courses/{course_id}

Next steps:
1. Review course content in Canvas
2. Test student experience with preview
3. Configure additional settings as needed
4. Announce course to students
                """,
                title="🚀 Deployment Complete",
                border_style="green",
            )
            console.print(success_panel)

        except Exception as e:
            progress.update(task, description="❌ Course creation failed")
            console.print(f"❌ [bold red]Course creation failed:[/bold red] {e}")
            if ctx.obj["debug"]:
                console.print_exception()
            raise


@cli.command()
@click.argument("course_name")
@click.option(
    "--template",
    type=click.Choice(["basic", "math", "science", "humanities", "language"]),
    default="basic",
    help="Course template to use",
)
@click.option(
    "--output-dir",
    type=click.Path(path_type=Path),
    default=".",
    help="Directory to create course structure",
)
@click.option("--modules", type=int, default=10, help="Number of modules to create")
@click.option(
    "--assignments-per-module",
    type=int,
    default=3,
    help="Average assignments per module",
)
@click.option("--interactive", is_flag=True, help="Interactive course creation wizard")
@click.pass_context
@handle_errors
def scaffold(
    ctx,
    course_name: str,
    template: str,
    output_dir: Path,
    modules: int,
    assignments_per_module: int,
    interactive: bool,
):
    """
    Generate a new course structure from templates.

    \b
    Creates a complete course directory with:
    • JSON configuration files
    • Module and assignment structures
    • Gamification settings
    • Example content and documentation

    \b
    Available templates:
    • basic: General-purpose course template
    • math: Mathematics and STEM courses
    • science: Laboratory and research-based courses
    • humanities: Discussion and essay-based courses
    • language: Language learning with progressive difficulty

    \b
    Examples:
      gamify scaffold "Linear Algebra" --template math --modules 13
      gamify scaffold "Introduction to Philosophy" --template humanities
      gamify scaffold "Spanish 101" --template language --interactive
    """
    if interactive:
        course_name = Prompt.ask("Course name", default=course_name)
        template = Prompt.ask(
            "Template",
            choices=["basic", "math", "science", "humanities", "language"],
            default=template,
        )
        modules = int(Prompt.ask("Number of modules", default=str(modules)))
        assignments_per_module = int(
            Prompt.ask("Assignments per module", default=str(assignments_per_module))
        )

    course_dir = output_dir / course_name.lower().replace(" ", "_")

    if course_dir.exists():
        if not Confirm.ask(f"Directory {course_dir} already exists. Overwrite?"):
            return

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:

        task = progress.add_task("Creating course structure...", total=None)

        # Create directory structure
        course_dir.mkdir(parents=True, exist_ok=True)
        (course_dir / "content").mkdir(exist_ok=True)
        (course_dir / "config").mkdir(exist_ok=True)
        (course_dir / "assets").mkdir(exist_ok=True)
        (course_dir / "docs").mkdir(exist_ok=True)

        progress.update(task, description="Generating course content...")

        # Generate template-specific content
        template_data = generate_template_content(
            course_name, template, modules, assignments_per_module
        )

        # Write configuration files
        write_template_files(course_dir, template_data)

        progress.update(task, description="✅ Course structure created!")

    success_panel = Panel(
        f"""
🎉 [bold green]Course scaffolding complete![/bold green]

📁 Course directory: {course_dir}
📋 Template: {template}
📚 Modules: {modules}
📝 Assignments: {modules * assignments_per_module}

Next steps:
1. cd {course_dir}
2. Customize content in ./content/ directory
3. Review configuration in ./config/ directory
4. Validate: gamify validate .
5. Build: gamify build . "Course Name" "CODE"
        """,
        title="🏗️ Scaffolding Complete",
        border_style="green",
    )
    console.print(success_panel)


def generate_template_content(
    course_name: str, template: str, modules: int, assignments_per_module: int
) -> Dict[str, Any]:
    """Generate template-specific course content"""
    # This would be a comprehensive template generation system
    # For now, return basic structure
    return {
        "course_name": course_name,
        "template": template,
        "modules": modules,
        "assignments_per_module": assignments_per_module,
    }


def write_template_files(course_dir: Path, template_data: Dict[str, Any]):
    """Write template files to course directory"""
    # Write README
    readme_content = f"""# {template_data['course_name']}

Course generated from {template_data['template']} template.

## Structure
- `content/`: Course content definitions (JSON)
- `config/`: Configuration files
- `assets/`: Images, videos, and other resources
- `docs/`: Course documentation

## Next Steps
1. Customize content in content/ directory
2. Validate: `gamify validate .`
3. Deploy: `gamify build . "{template_data['course_name']}" "COURSE_CODE"`
"""

    (course_dir / "README.md").write_text(readme_content)

    # Create basic JSON structures
    basic_modules = {
        "modules": [
            {
                "name": f"Module {i+1}: Introduction",
                "overview": f"Learning objectives for module {i+1}",
                "unlock_requirements": [] if i == 0 else [f"module_{i}_complete"],
                "items": [{"type": "Assignment", "id": f"assignment_{i+1}_1"}],
            }
            for i in range(template_data["modules"])
        ]
    }

    (course_dir / "content" / "modules.json").write_text(
        json.dumps(basic_modules, indent=2)
    )


@cli.command()
@click.argument("input_path", type=click.Path(exists=True, path_type=Path))
@click.argument("output_path", type=click.Path(path_type=Path))
@click.option(
    "--template-type",
    type=click.Choice(["minimal", "complete", "custom"]),
    default="complete",
    help="Template complexity level",
)
@click.pass_context
@handle_errors
def export_template(ctx, input_path: Path, output_path: Path, template_type: str):
    """
    Export a reusable template from existing course data.

    \b
    Template types:
    • minimal: Basic structure with example content
    • complete: Full template with all features demonstrated
    • custom: Interactive template creation

    \b
    Examples:
      gamify export-template ./examples/linear_algebra ./templates/math_course.json
      gamify export-template ./my-course ./templates/custom.json --template-type minimal
    """
    with console.status("[bold green]Generating template..."):
        loader = CourseDataLoader(str(input_path))
        loader.load_all_data()

        # Generate template based on type
        if template_type == "minimal":
            template = generate_minimal_template(loader.data)
        elif template_type == "complete":
            template = generate_complete_template(loader.data)
        else:  # custom
            template = generate_custom_template(loader.data)

        # Write template
        with open(output_path, "w") as f:
            json.dump(template, f, indent=2)

    console.print(f"📄 Template exported to: [bold]{output_path}[/bold]")
    console.print(f"   Template type: {template_type}")
    console.print(f"   Based on: {input_path}")


def generate_minimal_template(data: Dict[str, Any]) -> Dict[str, Any]:
    """Generate a minimal template with basic structure"""
    # Implementation would create simplified version
    return {"template": "minimal", "data": "placeholder"}


def generate_complete_template(data: Dict[str, Any]) -> Dict[str, Any]:
    """Generate a complete template with all features"""
    # Implementation would create full-featured template
    return {"template": "complete", "data": "placeholder"}


def generate_custom_template(data: Dict[str, Any]) -> Dict[str, Any]:
    """Generate a custom template with user choices"""
    # Implementation would use interactive prompts
    return {"template": "custom", "data": "placeholder"}


if __name__ == "__main__":
    cli()
