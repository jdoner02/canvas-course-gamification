#!/usr/bin/env python3
"""
Local Issue Management System
============================

Faculty-friendly interface for creating and managing project issues locally,
with seamless GitHub synchronization capabilities.

Features:
- Interactive issue creation
- Template-based issue generation
- Local markdown file management
- GitHub synchronization
- Progress tracking
- Educational workflow optimization

Best Practices:
- Faculty-centric design
- Educational technology standards
- Accessibility compliance
- Clear documentation
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
import click
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt, Confirm, IntPrompt

console = Console()


class LocalIssueManager:
    """Faculty-friendly local issue management with GitHub sync."""

    def __init__(self):
        self.project_root = Path.cwd()
        self.issues_dir = (
            self.project_root / "scripts" / "project-management" / "issues"
        )
        self.templates_dir = (
            self.project_root / "scripts" / "project-management" / "templates"
        )
        self.ensure_directories()

    def ensure_directories(self):
        """Create necessary directories if they don't exist."""
        self.issues_dir.mkdir(parents=True, exist_ok=True)
        self.templates_dir.mkdir(parents=True, exist_ok=True)

    def create_issue_templates(self):
        """Create issue templates for faculty use."""

        bug_template = """# [BUG] Brief description of the issue

**Priority:** P1
**Labels:** bug, component/[canvas-api|course-builder|gamification|validation|cli|documentation]

## 🐛 Bug Description
Clear description of what's broken or not working as expected.

## 🔄 Steps to Reproduce
1. Step one
2. Step two  
3. Step three

## ✅ Expected Behavior
What should happen instead.

## ❌ Actual Behavior
What actually happens.

## 🎯 Impact Assessment
- [ ] **Critical** - Blocks deployment/core functionality
- [ ] **High** - Affects user experience significantly
- [ ] **Medium** - Minor impact on functionality
- [ ] **Low** - Cosmetic or minor issue

## 🏷️ Component Areas
- [ ] Canvas API Integration
- [ ] Course Builder
- [ ] Gamification System
- [ ] Validation System
- [ ] CLI Interface
- [ ] Documentation

## 📋 Acceptance Criteria
- [ ] Issue is fixed
- [ ] Tests added/updated
- [ ] Documentation updated
- [ ] No regression introduced

## 🎓 Educational Impact
Brief description of how this affects teaching/learning experience.

## ⏱️ Estimated Effort
**X hours** - Brief justification
"""

        feature_template = """# [FEATURE] Brief description of the new feature

**Priority:** P2
**Labels:** feature, component/[canvas-api|course-builder|gamification|validation|cli|documentation]

## 🚀 Feature Description
Clear description of the new functionality needed.

## 💡 Problem Statement
What problem does this solve for faculty or students?

## 📋 Requirements
- [ ] Requirement 1
- [ ] Requirement 2
- [ ] Requirement 3

## 🎯 Success Criteria
- [ ] Feature works as specified
- [ ] User experience is intuitive
- [ ] Performance meets standards
- [ ] Accessibility compliance (WCAG 2.1 AA)

## 🏷️ Component Areas
- [ ] Canvas API Integration
- [ ] Course Builder
- [ ] Gamification System
- [ ] Validation System
- [ ] CLI Interface
- [ ] Documentation

## 🎓 Educational Benefits
How this feature improves teaching/learning outcomes:
- Accessibility (WCAG 2.1 AA compliance)
- UDL principles implementation
- Faculty workflow efficiency
- Student engagement enhancement

## ⏱️ Estimated Effort
**X hours** - Brief justification

## 📚 Related Resources
- Link to relevant documentation
- Related issues or features
"""

        task_template = """# [TASK] Brief description of the task

**Priority:** P2
**Labels:** task, component/[canvas-api|course-builder|gamification|validation|cli|documentation]

## 📝 Task Description
Clear description of what needs to be done.

## 🎯 Objectives
- [ ] Objective 1
- [ ] Objective 2
- [ ] Objective 3

## 📋 Acceptance Criteria
- [ ] Task completed successfully
- [ ] Quality standards met
- [ ] Documentation updated if needed

## 🏷️ Component Areas
- [ ] Canvas API Integration
- [ ] Course Builder
- [ ] Gamification System
- [ ] Validation System
- [ ] CLI Interface
- [ ] Documentation

## ⏱️ Estimated Effort
**X hours** - Brief justification
"""

        # Write templates
        (self.templates_dir / "bug_template.md").write_text(bug_template)
        (self.templates_dir / "feature_template.md").write_text(feature_template)
        (self.templates_dir / "task_template.md").write_text(task_template)

        console.print(
            "✅ Issue templates created in scripts/project-management/templates/"
        )

    def get_choice(self, prompt: str, choices: List[str], default: str = None) -> str:
        """Get user choice from a list of options."""
        console.print(f"\n[bold]{prompt}[/bold]")
        for i, choice in enumerate(choices, 1):
            marker = " (default)" if choice == default else ""
            console.print(f"  {i}. {choice}{marker}")

        while True:
            try:
                choice_input = Prompt.ask(
                    "Enter choice number or name",
                    default=str(choices.index(default) + 1) if default else "1",
                )

                # Try as number first
                try:
                    choice_num = int(choice_input)
                    if 1 <= choice_num <= len(choices):
                        return choices[choice_num - 1]
                except ValueError:
                    pass

                # Try as string match
                for choice in choices:
                    if choice.lower() == choice_input.lower():
                        return choice

                console.print(
                    f"[red]Invalid choice. Please enter 1-{len(choices)} or a valid option name.[/red]"
                )
            except KeyboardInterrupt:
                console.print("\nCancelled.")
                sys.exit(0)

    def create_issue_programmatically(
        self,
        title: str,
        issue_type: str = "feature",
        priority: str = "P2",
        component: str = "canvas-api",
        description: str = "",
        requirements: List[str] = None,
        acceptance_criteria: List[str] = None,
        educational_impact: str = "",
        estimated_effort: str = "2-4 hours",
        related_resources: List[str] = None,
        auto_sync: bool = False
    ) -> Path:
        """
        Create an issue programmatically for AI agents with minimal user interaction.
        
        Args:
            title: Issue title
            issue_type: Type of issue (bug, feature, task, documentation)
            priority: Priority level (P0, P1, P2, P3)
            component: Primary component (canvas-api, course-builder, gamification, validation, cli, documentation)
            description: Detailed description of the issue
            requirements: List of requirements (for features)
            acceptance_criteria: List of acceptance criteria
            educational_impact: Educational impact description
            estimated_effort: Effort estimation
            related_resources: List of related resources/links
            auto_sync: Whether to automatically sync to GitHub
            
        Returns:
            Path to the created issue file
        """
        
        # Validate inputs
        valid_types = ["bug", "feature", "task", "documentation"]
        valid_priorities = ["P0", "P1", "P2", "P3"]
        valid_components = ["canvas-api", "course-builder", "gamification", "validation", "cli", "documentation"]
        
        if issue_type not in valid_types:
            issue_type = "feature"
        if priority not in valid_priorities:
            priority = "P2"
        if component not in valid_components:
            component = "canvas-api"
            
        # Set defaults
        if requirements is None:
            requirements = ["Requirement to be defined"]
        if acceptance_criteria is None:
            acceptance_criteria = ["Task completed successfully", "Documentation updated", "Quality standards met"]
        if related_resources is None:
            related_resources = []
            
        # Generate filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M")
        safe_title = "".join(c for c in title.lower() if c.isalnum() or c in (' ', '-', '_')).rstrip()
        safe_title = safe_title.replace(' ', '_')[:50]
        filename = f"{timestamp}_{safe_title}.md"
        
        # Create content based on issue type
        if issue_type == "bug":
            content = self._create_bug_content(title, priority, component, description, acceptance_criteria, educational_impact, estimated_effort)
        elif issue_type == "feature":
            content = self._create_feature_content(title, priority, component, description, requirements, acceptance_criteria, educational_impact, estimated_effort, related_resources)
        elif issue_type == "task":
            content = self._create_task_content(title, priority, component, description, acceptance_criteria, estimated_effort)
        else:  # documentation
            content = self._create_documentation_content(title, priority, component, description, acceptance_criteria, estimated_effort)
        
        # Save issue file
        issue_file = self.issues_dir / filename
        issue_file.write_text(content)
        
        console.print(f"✅ Issue created programmatically: {title}")
        console.print(f"📄 File: {issue_file}")
        console.print(f"🏷️  Type: {issue_type}, Priority: {priority}, Component: {component}")
        
        # Auto-sync if requested
        if auto_sync:
            console.print("🔄 Auto-syncing to GitHub...")
            self.sync_single_issue(issue_file)
        
        return issue_file

    def _create_bug_content(self, title: str, priority: str, component: str, description: str, 
                           acceptance_criteria: List[str], educational_impact: str, estimated_effort: str) -> str:
        """Create bug issue content."""
        criteria_text = "\n".join(f"- [ ] {criteria}" for criteria in acceptance_criteria)
        
        return f"""# {title}

**Priority:** {priority}
**Labels:** bug, component/{component}

## 🐛 Bug Description
{description or "Clear description of what's broken or not working as expected."}

## 🔄 Steps to Reproduce
1. Step one to reproduce the issue
2. Step two
3. Step three

## ✅ Expected Behavior
What should happen instead.

## ❌ Actual Behavior
What actually happens.

## 🎯 Impact Assessment
- [ ] **Critical** - Blocks deployment/core functionality
- [ ] **High** - Affects user experience significantly  
- [ ] **Medium** - Minor impact on functionality
- [ ] **Low** - Cosmetic or minor issue

## 🏷️ Component Areas
- [x] {component.replace('-', ' ').title()}

## 📋 Acceptance Criteria
{criteria_text}

## 🎓 Educational Impact
{educational_impact or "Brief description of how this affects teaching/learning experience."}

## ⏱️ Estimated Effort
**{estimated_effort}** - Bug investigation and resolution
"""

    def _create_feature_content(self, title: str, priority: str, component: str, description: str,
                               requirements: List[str], acceptance_criteria: List[str], 
                               educational_impact: str, estimated_effort: str, related_resources: List[str]) -> str:
        """Create feature issue content."""
        req_text = "\n".join(f"- [ ] {req}" for req in requirements)
        criteria_text = "\n".join(f"- [ ] {criteria}" for criteria in acceptance_criteria)
        resources_text = "\n".join(f"- {resource}" for resource in related_resources) if related_resources else "- To be determined"
        
        return f"""# {title}

**Priority:** {priority}
**Labels:** feature, component/{component}

## 🚀 Feature Description
{description or "Clear description of the new functionality needed."}

## 💡 Problem Statement
What problem does this solve for faculty or students?

## 📋 Requirements
{req_text}

## 🎯 Success Criteria
{criteria_text}

## 🏷️ Component Areas
- [x] {component.replace('-', ' ').title()}

## 🎓 Educational Benefits
{educational_impact or """How this feature improves teaching/learning outcomes:
- Accessibility (WCAG 2.1 AA compliance)
- UDL principles implementation
- Faculty workflow efficiency
- Student engagement enhancement"""}

## ⏱️ Estimated Effort
**{estimated_effort}** - Feature development and testing

## 📚 Related Resources
{resources_text}
"""

    def _create_task_content(self, title: str, priority: str, component: str, description: str,
                            acceptance_criteria: List[str], estimated_effort: str) -> str:
        """Create task issue content."""
        criteria_text = "\n".join(f"- [ ] {criteria}" for criteria in acceptance_criteria)
        
        return f"""# {title}

**Priority:** {priority}
**Labels:** task, component/{component}

## 📝 Task Description
{description or "Clear description of what needs to be done."}

## 🎯 Objectives
- [ ] Primary objective
- [ ] Secondary objective  
- [ ] Quality assurance

## 📋 Acceptance Criteria
{criteria_text}

## 🏷️ Component Areas
- [x] {component.replace('-', ' ').title()}

## ⏱️ Estimated Effort
**{estimated_effort}** - Task completion and validation
"""

    def _create_documentation_content(self, title: str, priority: str, component: str, description: str,
                                     acceptance_criteria: List[str], estimated_effort: str) -> str:
        """Create documentation issue content."""
        criteria_text = "\n".join(f"- [ ] {criteria}" for criteria in acceptance_criteria)
        
        return f"""# {title}

**Priority:** {priority}
**Labels:** documentation, component/{component}

## 📚 Documentation Description
{description or "Clear description of the documentation needed."}

## 🎯 Target Audience
- [ ] Faculty/Instructors
- [ ] Students
- [ ] Developers
- [ ] Administrators

## 📋 Acceptance Criteria
{criteria_text}

## 🏷️ Component Areas
- [x] {component.replace('-', ' ').title()}

## ⏱️ Estimated Effort
**{estimated_effort}** - Documentation writing and review
"""

    def create_interactive_issue(self):
        """Interactive issue creation with templates."""

        console.print(
            Panel.fit(
                "[bold blue]📝 Interactive Issue Creator[/bold blue]\n"
                "Create professional, actionable issues for the project",
                title="Issue Creator",
            )
        )

        # Choose issue type
        issue_type = self.get_choice(
            "What type of issue would you like to create?",
            ["bug", "feature", "task", "documentation"],
            "bug",
        )

        # Get basic info
        title = Prompt.ask(
            "Issue title", default=f"[{issue_type.upper()}] Brief description"
        )

        priority = self.get_choice("Priority level", ["P0", "P1", "P2", "P3"], "P1")

        component = self.get_choice(
            "Primary component",
            [
                "canvas-api",
                "course-builder",
                "gamification",
                "validation",
                "cli",
                "documentation",
            ],
            "canvas-api",
        )

        # Generate filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M")
        safe_title = "".join(
            c for c in title.lower() if c.isalnum() or c in (" ", "-", "_")
        ).rstrip()
        safe_title = safe_title.replace(" ", "_")[:50]
        filename = f"{timestamp}_{safe_title}.md"

        # Load template
        template_file = self.templates_dir / f"{issue_type}_template.md"
        if template_file.exists():
            template_content = template_file.read_text()

            # Replace placeholders
            content = template_content.replace("Brief description of the issue", title)
            content = content.replace("Brief description of the new feature", title)
            content = content.replace("Brief description of the task", title)
            content = content.replace("**Priority:** P1", f"**Priority:** {priority}")
            content = content.replace(
                f"component/[canvas-api|course-builder|gamification|validation|cli|documentation]",
                f"component/{component}",
            )
        else:
            # Fallback basic template
            content = f"""# {title}

**Priority:** {priority}
**Labels:** {issue_type}, component/{component}

## Description
Detailed description of the {issue_type}.

## Acceptance Criteria
- [ ] Task completed
- [ ] Documentation updated
- [ ] Tests added/updated
"""

        # Save issue file
        issue_file = self.issues_dir / filename
        issue_file.write_text(content)

        console.print(f"✅ Issue created: {issue_file}")
        console.print(f"📝 Edit the file to add more details")

        # Ask if they want to sync to GitHub
        if Confirm.ask("Sync this issue to GitHub now?"):
            self.sync_single_issue(issue_file)

    def sync_single_issue(self, issue_file: Path):
        """Sync a single issue to GitHub."""
        try:
            import subprocess

            result = subprocess.run(
                [
                    "python",
                    "scripts/project-management/github_integration.py",
                    "--create-issues",
                    "--issues-dir",
                    str(issue_file.parent),
                ],
                capture_output=True,
                text=True,
                cwd=self.project_root,
            )

            if result.returncode == 0:
                console.print("✅ Issue synced to GitHub successfully!")
            else:
                console.print(f"❌ Sync failed: {result.stderr}")
        except Exception as e:
            console.print(f"❌ Sync error: {e}")

    def list_local_issues(self):
        """List all local issues."""

        console.print("\n[bold]📋 Local Issues[/bold]")

        issue_files = list(self.issues_dir.glob("*.md"))
        if not issue_files:
            console.print("No local issues found.")
            return

        table = Table(title="Local Issues")
        table.add_column("File", style="cyan")
        table.add_column("Title", style="green")
        table.add_column("Priority", style="yellow")
        table.add_column("Modified", style="blue")

        for issue_file in sorted(issue_files):
            if issue_file.name.startswith("00_"):  # Skip summary files
                continue

            content = issue_file.read_text()
            lines = content.split("\n")
            title = lines[0].replace("# ", "") if lines else "Untitled"

            priority = "P2"
            for line in lines:
                if line.startswith("**Priority:**"):
                    priority = line.split(":")[1].strip()
                    break

            modified = datetime.fromtimestamp(issue_file.stat().st_mtime).strftime(
                "%Y-%m-%d %H:%M"
            )

            table.add_row(
                issue_file.name,
                title[:60] + "..." if len(title) > 60 else title,
                priority,
                modified,
            )

        console.print(table)

    def sync_all_issues(self):
        """Sync all local issues to GitHub."""
        console.print("\n[bold]🔄 Syncing all issues to GitHub...[/bold]")

        try:
            import subprocess

            result = subprocess.run(
                [
                    "python",
                    "scripts/project-management/github_integration.py",
                    "--create-issues",
                ],
                capture_output=True,
                text=True,
                cwd=self.project_root,
            )

            if result.returncode == 0:
                console.print("✅ All issues synced successfully!")
            else:
                console.print(f"❌ Sync failed: {result.stderr}")
        except Exception as e:
            console.print(f"❌ Sync error: {e}")

    def workflow_status(self):
        """Show current workflow status."""
        try:
            import subprocess

            result = subprocess.run(
                [
                    "python",
                    "scripts/project-management/workflow_manager.py",
                    "--status",
                ],
                capture_output=True,
                text=True,
                cwd=self.project_root,
            )

            console.print(result.stdout)
        except Exception as e:
            console.print(f"❌ Status error: {e}")


@click.command()
@click.option("--create", is_flag=True, help="Create a new issue interactively")
@click.option("--list", "list_issues", is_flag=True, help="List all local issues")
@click.option("--sync", is_flag=True, help="Sync all issues to GitHub")
@click.option("--status", is_flag=True, help="Show project status")
@click.option("--setup", is_flag=True, help="Setup issue templates")
# Programmatic issue creation options
@click.option("--title", help="Issue title for programmatic creation")
@click.option("--type", "issue_type", default="feature", 
              type=click.Choice(["bug", "feature", "task", "documentation"]),
              help="Issue type")
@click.option("--priority", default="P2", 
              type=click.Choice(["P0", "P1", "P2", "P3"]),
              help="Priority level")
@click.option("--component", default="canvas-api",
              type=click.Choice(["canvas-api", "course-builder", "gamification", "validation", "cli", "documentation"]),
              help="Primary component")
@click.option("--description", help="Detailed description of the issue")
@click.option("--requirements", help="Comma-separated list of requirements")
@click.option("--acceptance-criteria", help="Comma-separated list of acceptance criteria")
@click.option("--educational-impact", help="Educational impact description")
@click.option("--estimated-effort", default="2-4 hours", help="Effort estimation")
@click.option("--related-resources", help="Comma-separated list of related resources/links")
@click.option("--auto-sync", is_flag=True, help="Automatically sync to GitHub after creation")
def main(create, list_issues, sync, status, setup, title, issue_type, priority, component, 
         description, requirements, acceptance_criteria, educational_impact, 
         estimated_effort, related_resources, auto_sync):
    """Faculty-friendly local issue management system."""

    console.print(
        Panel.fit(
            "[bold blue]📚 Canvas Course Gamification - Local Issue Manager[/bold blue]\n"
            "Faculty-friendly project management workflow",
            title="Local Issue Manager",
        )
    )

    manager = LocalIssueManager()
    
    # Handle programmatic issue creation first
    if title:
        # Parse comma-separated lists
        req_list = [r.strip() for r in requirements.split(',')] if requirements else None
        criteria_list = [c.strip() for c in acceptance_criteria.split(',')] if acceptance_criteria else None
        resources_list = [r.strip() for r in related_resources.split(',')] if related_resources else None
        
        issue_file = manager.create_issue_programmatically(
            title=title,
            issue_type=issue_type,
            priority=priority,
            component=component,
            description=description or "",
            requirements=req_list,
            acceptance_criteria=criteria_list,
            educational_impact=educational_impact or "",
            estimated_effort=estimated_effort,
            related_resources=resources_list,
            auto_sync=auto_sync
        )
        return
    
    if setup:
        manager.create_issue_templates()
        return

    if create:
        manager.create_interactive_issue()
        return

    if list_issues:
        manager.list_local_issues()
        return

    if sync:
        manager.sync_all_issues()
        return

    if status:
        manager.workflow_status()
        return

    # Interactive menu if no flags
    console.print("\n[bold]Choose an action:[/bold]")

    choices = ["create", "list", "sync", "status", "setup"]
    console.print("\n[bold]What would you like to do?[/bold]")
    for i, choice in enumerate(choices, 1):
        marker = " (default)" if choice == "create" else ""
        console.print(f"  {i}. {choice}{marker}")

    choice_input = Prompt.ask("Enter choice number or name", default="1")

    # Try as number first
    try:
        choice_num = int(choice_input)
        if 1 <= choice_num <= len(choices):
            action = choices[choice_num - 1]
        else:
            action = "create"
    except ValueError:
        # Try as string match
        action = "create"
        for choice in choices:
            if choice.lower() == choice_input.lower():
                action = choice
                break

    if action == "create":
        manager.create_interactive_issue()
    elif action == "list":
        manager.list_local_issues()
    elif action == "sync":
        manager.sync_all_issues()
    elif action == "status":
        manager.workflow_status()
    elif action == "setup":
        manager.create_issue_templates()


if __name__ == "__main__":
    main()
