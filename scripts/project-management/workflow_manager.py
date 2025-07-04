#!/usr/bin/env python3
"""
Automated Project Management Workflow
====================================

Comprehensive workflow automation for Canvas Course Gamification project.
Implements enterprise-grade project management practices for educational technology.

Features:
- Automated commit message generation
- Issue linking in commits
- Progress tracking
- Quality gates
- Educational best practices integration

Best Practices:
- DevOps automation
- Educational technology standards
- Accessibility and UDL compliance
- Faculty workflow optimization
"""

import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
import click
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt, Confirm

console = Console()


class WorkflowManager:
    """Professional workflow management for educational technology projects."""

    def __init__(self):
        self.project_root = Path.cwd()
        self.ensure_git_repo()

    def ensure_git_repo(self):
        """Ensure we're in a git repository."""
        if not (self.project_root / ".git").exists():
            console.print("❌ Not in a git repository", style="red")
            if Confirm.ask("Initialize git repository?"):
                subprocess.run(["git", "init"], check=True)
                console.print("✅ Git repository initialized", style="green")
            else:
                sys.exit(1)

    def analyze_changes(self) -> Dict:
        """Analyze current changes for intelligent commit messaging."""

        # Get staged and unstaged changes
        staged = (
            subprocess.run(
                ["git", "diff", "--cached", "--name-only"],
                capture_output=True,
                text=True,
            )
            .stdout.strip()
            .split("\n")
        )
        unstaged = (
            subprocess.run(
                ["git", "diff", "--name-only"], capture_output=True, text=True
            )
            .stdout.strip()
            .split("\n")
        )
        untracked = (
            subprocess.run(
                ["git", "ls-files", "--others", "--exclude-standard"],
                capture_output=True,
                text=True,
            )
            .stdout.strip()
            .split("\n")
        )

        # Filter empty strings
        staged = [f for f in staged if f]
        unstaged = [f for f in unstaged if f]
        untracked = [f for f in untracked if f]

        # Categorize changes
        categories = {
            "bugfix": [],
            "feature": [],
            "docs": [],
            "config": [],
            "test": [],
            "automation": [],
            "accessibility": [],
            "other": [],
        }

        all_files = staged + unstaged + untracked

        for file in all_files:
            if any(keyword in file.lower() for keyword in ["bug", "fix", "error"]):
                categories["bugfix"].append(file)
            elif any(keyword in file.lower() for keyword in ["feature", "enhance"]):
                categories["feature"].append(file)
            elif any(keyword in file.lower() for keyword in ["doc", "readme", "md"]):
                categories["docs"].append(file)
            elif any(
                keyword in file.lower() for keyword in ["config", "yml", "yaml", "json"]
            ):
                categories["config"].append(file)
            elif any(keyword in file.lower() for keyword in ["test", "spec"]):
                categories["test"].append(file)
            elif any(
                keyword in file.lower() for keyword in ["script", "automation", "cli"]
            ):
                categories["automation"].append(file)
            elif any(
                keyword in file.lower() for keyword in ["accessibility", "wcag", "udl"]
            ):
                categories["accessibility"].append(file)
            else:
                categories["other"].append(file)

        return {
            "staged": staged,
            "unstaged": unstaged,
            "untracked": untracked,
            "categories": categories,
        }

    def generate_commit_message(
        self, changes: Dict, issue_number: Optional[str] = None
    ) -> str:
        """Generate intelligent commit message based on changes."""

        categories = changes["categories"]

        # Determine primary type
        primary_type = "feat"
        if categories["bugfix"]:
            primary_type = "fix"
        elif categories["docs"]:
            primary_type = "docs"
        elif categories["config"]:
            primary_type = "config"
        elif categories["test"]:
            primary_type = "test"
        elif categories["automation"]:
            primary_type = "ci"
        elif categories["accessibility"]:
            primary_type = "a11y"

        # Determine scope
        scope = "core"
        if any(
            "canvas" in f.lower()
            for f in changes["staged"] + changes["unstaged"] + changes["untracked"]
        ):
            scope = "canvas"
        elif any(
            "gamification" in f.lower()
            for f in changes["staged"] + changes["unstaged"] + changes["untracked"]
        ):
            scope = "gamification"
        elif any(
            "validation" in f.lower()
            for f in changes["staged"] + changes["unstaged"] + changes["untracked"]
        ):
            scope = "validation"
        elif any(
            "cli" in f.lower()
            for f in changes["staged"] + changes["unstaged"] + changes["untracked"]
        ):
            scope = "cli"

        # Generate description
        descriptions = []
        if categories["bugfix"]:
            descriptions.append(f"fix validation and deployment issues")
        if categories["feature"]:
            descriptions.append(f"add project management automation")
        if categories["docs"]:
            descriptions.append(f"update documentation")
        if categories["config"]:
            descriptions.append(f"update configuration")
        if categories["accessibility"]:
            descriptions.append(f"improve accessibility compliance")

        main_description = descriptions[0] if descriptions else "update project files"

        # Format commit message
        commit_msg = f"{primary_type}({scope}): {main_description}"

        # Add body with details
        body_parts = []

        if categories["bugfix"]:
            body_parts.append("Bug Fixes:")
            for file in categories["bugfix"][:3]:  # Limit to 3 files
                body_parts.append(f"- {file}")

        if categories["feature"]:
            body_parts.append("Features:")
            for file in categories["feature"][:3]:
                body_parts.append(f"- {file}")

        # Add educational context
        body_parts.append("")
        body_parts.append("Educational Technology Impact:")
        body_parts.append("- Improves faculty workflow automation")
        body_parts.append("- Enhances accessibility compliance (WCAG 2.1 AA)")
        body_parts.append("- Supports UDL implementation")

        if issue_number:
            body_parts.append(f"")
            body_parts.append(f"Closes #{issue_number}")

        if body_parts:
            commit_msg += "\n\n" + "\n".join(body_parts)

        return commit_msg

    def stage_all_changes(self):
        """Stage all changes for commit."""
        subprocess.run(["git", "add", "."], check=True)
        console.print("✅ All changes staged", style="green")

    def create_commit(self, message: str):
        """Create commit with given message."""
        subprocess.run(["git", "commit", "-m", message], check=True)
        console.print("✅ Commit created", style="green")

    def push_changes(self, create_pr: bool = False):
        """Push changes and optionally create PR."""

        # Get current branch
        branch = subprocess.run(
            ["git", "branch", "--show-current"], capture_output=True, text=True
        ).stdout.strip()

        # Push changes
        subprocess.run(["git", "push", "origin", branch], check=True)
        console.print(f"✅ Pushed to origin/{branch}", style="green")

        if create_pr:
            # Create pull request
            try:
                result = subprocess.run(
                    [
                        "gh",
                        "pr",
                        "create",
                        "--title",
                        f'Project Management and Bug Fixes - {datetime.now().strftime("%Y-%m-%d")}',
                        "--body",
                        "Automated PR for project management improvements and critical bug fixes",
                    ],
                    capture_output=True,
                    text=True,
                    check=True,
                )

                pr_url = result.stdout.strip()
                console.print(f"✅ Pull request created: {pr_url}", style="green")

            except subprocess.CalledProcessError as e:
                console.print(f"⚠️  Could not create PR: {e.stderr}", style="yellow")

    def run_quality_checks(self) -> bool:
        """Run quality checks before commit."""

        console.print("🔍 Running quality checks...")

        checks_passed = True

        # Check 1: Python syntax
        python_files = list(Path(".").rglob("*.py"))
        for py_file in python_files:
            try:
                subprocess.run(
                    ["python", "-m", "py_compile", str(py_file)],
                    check=True,
                    capture_output=True,
                )
            except subprocess.CalledProcessError:
                console.print(f"❌ Python syntax error in {py_file}", style="red")
                checks_passed = False

        if checks_passed:
            console.print("   ✅ Python syntax check passed")

        # Check 2: Required files exist
        required_files = ["README.md", "requirements.txt", ".github/PROJECT_STATUS.md"]

        for req_file in required_files:
            if not Path(req_file).exists():
                console.print(f"❌ Required file missing: {req_file}", style="red")
                checks_passed = False

        if checks_passed:
            console.print("   ✅ Required files check passed")

        # Check 3: No large files
        large_files = []
        for file in Path(".").rglob("*"):
            if file.is_file() and file.stat().st_size > 10 * 1024 * 1024:  # 10MB
                large_files.append(file)

        if large_files:
            console.print(f"⚠️  Large files detected: {large_files}", style="yellow")

        return checks_passed

    def display_status(self):
        """Display comprehensive project status."""

        changes = self.analyze_changes()

        # Status table
        status_table = Table(title="📊 Project Status")
        status_table.add_column("Category", style="cyan")
        status_table.add_column("Count", style="green")
        status_table.add_column("Files", style="yellow")

        status_table.add_row(
            "Staged",
            str(len(changes["staged"])),
            ", ".join(changes["staged"][:3])
            + ("..." if len(changes["staged"]) > 3 else ""),
        )
        status_table.add_row(
            "Unstaged",
            str(len(changes["unstaged"])),
            ", ".join(changes["unstaged"][:3])
            + ("..." if len(changes["unstaged"]) > 3 else ""),
        )
        status_table.add_row(
            "Untracked",
            str(len(changes["untracked"])),
            ", ".join(changes["untracked"][:3])
            + ("..." if len(changes["untracked"]) > 3 else ""),
        )

        console.print(status_table)
        console.print()

        # Changes by category
        if any(changes["categories"].values()):
            category_table = Table(title="📋 Changes by Category")
            category_table.add_column("Category", style="cyan")
            category_table.add_column("Files", style="green")

            for category, files in changes["categories"].items():
                if files:
                    category_table.add_row(category.title(), str(len(files)))

            console.print(category_table)


@click.command()
@click.option("--status", is_flag=True, help="Show project status")
@click.option("--commit", is_flag=True, help="Create intelligent commit")
@click.option("--push", is_flag=True, help="Push changes")
@click.option("--pr", is_flag=True, help="Create pull request")
@click.option("--issue", help="Link to issue number")
@click.option("--check", is_flag=True, help="Run quality checks")
def main(status, commit, push, pr, issue, check):
    """Automated workflow management for Canvas Course Gamification project."""

    console.print(
        Panel.fit(
            "[bold blue]🔄 Canvas Course Gamification - Workflow Manager[/bold blue]\n"
            "Professional development workflow automation",
            title="Workflow Manager",
        )
    )

    wf = WorkflowManager()

    if status:
        wf.display_status()
        return

    if check:
        checks_passed = wf.run_quality_checks()
        if not checks_passed:
            console.print("❌ Quality checks failed", style="red")
            sys.exit(1)
        console.print("✅ All quality checks passed", style="green")
        return

    if commit:
        # Run quality checks first
        if not wf.run_quality_checks():
            console.print(
                "❌ Quality checks failed. Fix issues before committing.", style="red"
            )
            sys.exit(1)

        changes = wf.analyze_changes()

        if not any([changes["staged"], changes["unstaged"], changes["untracked"]]):
            console.print("ℹ️  No changes to commit", style="yellow")
            return

        # Stage all changes
        wf.stage_all_changes()

        # Generate commit message
        commit_msg = wf.generate_commit_message(changes, issue)

        console.print("\n[bold]📝 Generated Commit Message:[/bold]")
        console.print(Panel(commit_msg, title="Commit Message"))

        if Confirm.ask("Proceed with this commit?"):
            wf.create_commit(commit_msg)

            if push:
                wf.push_changes(create_pr=pr)
        else:
            console.print("Commit cancelled", style="yellow")

    elif push:
        wf.push_changes(create_pr=pr)


if __name__ == "__main__":
    main()
