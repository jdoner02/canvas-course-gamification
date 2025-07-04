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
        self.issues_dir = self.project_root / "scripts" / "project-management" / "issues"
        self.templates_dir = self.project_root / "scripts" / "project-management" / "templates"
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
        
        console.print("✅ Issue templates created in scripts/project-management/templates/")

    def get_choice(self, prompt: str, choices: List[str], default: str = None) -> str:
        """Get user choice from a list of options."""
        console.print(f"\n[bold]{prompt}[/bold]")
        for i, choice in enumerate(choices, 1):
            marker = " (default)" if choice == default else ""
            console.print(f"  {i}. {choice}{marker}")
        
        while True:
            try:
                choice_input = Prompt.ask("Enter choice number or name", default=str(choices.index(default) + 1) if default else "1")
                
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
                
                console.print(f"[red]Invalid choice. Please enter 1-{len(choices)} or a valid option name.[/red]")
            except KeyboardInterrupt:
                console.print("\nCancelled.")
                sys.exit(0)

    def create_interactive_issue(self):
        """Interactive issue creation with templates."""
        
        console.print(Panel.fit(
            "[bold blue]📝 Interactive Issue Creator[/bold blue]\n"
            "Create professional, actionable issues for the project",
            title="Issue Creator"
        ))
        
        # Choose issue type
        issue_type = self.get_choice(
            "What type of issue would you like to create?",
            ["bug", "feature", "task", "documentation"],
            "bug"
        )
        
        # Get basic info
        title = Prompt.ask("Issue title", default=f"[{issue_type.upper()}] Brief description")
        
        priority = self.get_choice(
            "Priority level",
            ["P0", "P1", "P2", "P3"],
            "P1"
        )
        
        component = self.get_choice(
            "Primary component",
            ["canvas-api", "course-builder", "gamification", "validation", "cli", "documentation"],
            "canvas-api"
        )
        
        # Generate filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M")
        safe_title = "".join(c for c in title.lower() if c.isalnum() or c in (' ', '-', '_')).rstrip()
        safe_title = safe_title.replace(' ', '_')[:50]
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
            content = content.replace(f"component/[canvas-api|course-builder|gamification|validation|cli|documentation]", f"component/{component}")
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
            result = subprocess.run([
                'python', 'scripts/project-management/github_integration.py', 
                '--create-issues', '--issues-dir', str(issue_file.parent)
            ], capture_output=True, text=True, cwd=self.project_root)
            
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
            lines = content.split('\n')
            title = lines[0].replace('# ', '') if lines else "Untitled"
            
            priority = "P2"
            for line in lines:
                if line.startswith('**Priority:**'):
                    priority = line.split(':')[1].strip()
                    break
            
            modified = datetime.fromtimestamp(issue_file.stat().st_mtime).strftime("%Y-%m-%d %H:%M")
            
            table.add_row(
                issue_file.name,
                title[:60] + "..." if len(title) > 60 else title,
                priority,
                modified
            )
        
        console.print(table)

    def sync_all_issues(self):
        """Sync all local issues to GitHub."""
        console.print("\n[bold]🔄 Syncing all issues to GitHub...[/bold]")
        
        try:
            import subprocess
            result = subprocess.run([
                'python', 'scripts/project-management/github_integration.py', 
                '--create-issues'
            ], capture_output=True, text=True, cwd=self.project_root)
            
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
            result = subprocess.run([
                'python', 'scripts/project-management/workflow_manager.py', 
                '--status'
            ], capture_output=True, text=True, cwd=self.project_root)
            
            console.print(result.stdout)
        except Exception as e:
            console.print(f"❌ Status error: {e}")


@click.command()
@click.option('--create', is_flag=True, help='Create a new issue interactively')
@click.option('--list', 'list_issues', is_flag=True, help='List all local issues')
@click.option('--sync', is_flag=True, help='Sync all issues to GitHub')
@click.option('--status', is_flag=True, help='Show project status')
@click.option('--setup', is_flag=True, help='Setup issue templates')
def main(create, list_issues, sync, status, setup):
    """Faculty-friendly local issue management system."""
    
    console.print(Panel.fit(
        "[bold blue]📚 Canvas Course Gamification - Local Issue Manager[/bold blue]\n"
        "Faculty-friendly project management workflow",
        title="Local Issue Manager"
    ))
    
    manager = LocalIssueManager()
    
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
