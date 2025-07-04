#!/usr/bin/env python3
"""
GitHub Issue and Project Management Automation
==============================================

Professional project management automation for Canvas Course Gamification project.
Follows software engineering best practices for issue tracking, project boards,
and workflow automation.

Features:
- Automated issue creation with proper labeling
- Project board management
- Sprint planning automation
- Metrics collection and reporting
- Integration with GitHub CLI

Author: Canvas Course Gamification Team
License: Educational Use
"""

import json
import subprocess
import sys
import yaml
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any
import click
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt, Confirm

console = Console()


class GitHubProjectManager:
    """
    Professional GitHub project management automation following enterprise practices.

    Best Practices Implemented:
    - Issue-driven development workflow
    - Automated project board management
    - Comprehensive labeling system
    - Sprint planning and metrics
    - Educational technology considerations
    """

    def __init__(
        self,
        repo_owner: str = "jdoner02",
        repo_name: str = "canvas-course-gamification",
    ):
        self.repo_owner = repo_owner
        self.repo_name = repo_name
        self.repo_full = f"{repo_owner}/{repo_name}"
        self.issues_file = Path("project_data/issues_tracking.json")
        self.issues_file.parent.mkdir(exist_ok=True)

    def check_gh_cli(self) -> bool:
        """Verify GitHub CLI is installed and authenticated."""
        try:
            result = subprocess.run(
                ["gh", "auth", "status"], capture_output=True, text=True, check=True
            )
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            console.print("❌ GitHub CLI not found or not authenticated", style="red")
            console.print("Please install and authenticate with: gh auth login")
            return False

    def create_issue_from_template(
        self,
        issue_type: str,
        title: str,
        labels: List[str],
        priority: str = "medium",
        education_context: Dict[str, Any] = None,
    ) -> Dict[str, Any]:
        """
        Create GitHub issue following educational technology best practices.

        Educational Context Integration:
        - Learning outcome alignment
        - UDL principle consideration
        - Accessibility impact assessment
        - Faculty workload impact
        """

        templates = {
            "bug": self._create_bug_issue,
            "feature": self._create_feature_issue,
            "task": self._create_task_issue,
            "accessibility": self._create_accessibility_issue,
            "security": self._create_security_issue,
            "education": self._create_education_issue,
        }

        if issue_type not in templates:
            raise ValueError(f"Unknown issue type: {issue_type}")

        return templates[issue_type](title, labels, priority, education_context)

    def _create_bug_issue(
        self,
        title: str,
        labels: List[str],
        priority: str,
        context: Dict[str, Any] = None,
    ) -> Dict[str, Any]:
        """Create bug issue with comprehensive tracking."""

        body = f"""
## 🐛 Bug Description
{context.get('description', 'Bug description needed')}

## 🎓 Educational Impact
- **Student Experience Impact**: {context.get('student_impact', 'TBD')}
- **Faculty Workflow Impact**: {context.get('faculty_impact', 'TBD')}
- **Accessibility Concerns**: {context.get('accessibility_impact', 'None identified')}

## 🔄 Reproduction Steps
{context.get('reproduction_steps', '1. Step one\\n2. Step two\\n3. See error')}

## ✅ Expected Behavior
{context.get('expected_behavior', 'Expected behavior description needed')}

## 🖥️ Environment
- **OS**: {context.get('os', 'TBD')}
- **Browser**: {context.get('browser', 'TBD')}
- **Canvas Environment**: {context.get('canvas_env', 'TBD')}

## 🏷️ Classification
- Priority: {priority.upper()}
- Severity: {context.get('severity', 'Medium')}
- Component: {context.get('component', 'Core System')}

## 🎯 Acceptance Criteria
- [ ] Bug is reproducible and root cause identified
- [ ] Fix implemented with no regression
- [ ] Accessibility impact assessed and addressed
- [ ] Educational workflow impact minimized
- [ ] Test coverage updated
- [ ] Documentation updated if needed
"""

        issue_data = {
            "title": f"🐛 {title}",
            "body": body,
            "labels": labels + ["bug", f"priority-{priority}"],
            "type": "bug",
            "created_at": datetime.now().isoformat(),
            "educational_context": context or {},
        }

        return self._submit_github_issue(issue_data)

    def _create_feature_issue(
        self,
        title: str,
        labels: List[str],
        priority: str,
        context: Dict[str, Any] = None,
    ) -> Dict[str, Any]:
        """Create feature issue with educational technology focus."""

        body = f"""
## 🚀 Feature Summary
{context.get('summary', 'Feature summary needed')}

## 🎓 Educational Rationale
- **Learning Outcome Alignment**: {context.get('learning_outcomes', 'TBD')}
- **UDL Principles Supported**: {context.get('udl_principles', 'TBD')}
- **Gamification Enhancement**: {context.get('gamification_impact', 'TBD')}
- **Faculty Benefit**: {context.get('faculty_benefit', 'TBD')}

## 💡 Motivation
{context.get('motivation', 'Motivation description needed')}

## 📋 Detailed Description
{context.get('detailed_description', 'Detailed description needed')}

## 🎯 Success Criteria
{context.get('success_criteria', '- [ ] Success criterion 1\\n- [ ] Success criterion 2')}

## ♿ Accessibility Requirements
- **WCAG 2.1 AA Compliance**: {context.get('wcag_compliance', 'Required')}
- **Screen Reader Support**: {context.get('screen_reader', 'Required')}
- **Keyboard Navigation**: {context.get('keyboard_nav', 'Required')}

## 🔧 Technical Considerations
- **API Changes**: {context.get('api_changes', 'TBD')}
- **Database Impact**: {context.get('db_impact', 'TBD')}
- **Performance Impact**: {context.get('performance', 'TBD')}
- **Security Considerations**: {context.get('security', 'TBD')}

## 📊 Priority Justification
Priority: {priority.upper()}
Reasoning: {context.get('priority_reasoning', 'Priority reasoning needed')}

## 🎯 Acceptance Criteria
- [ ] Feature implemented according to specifications
- [ ] Accessibility requirements met (WCAG 2.1 AA)
- [ ] UDL principles integrated
- [ ] Educational effectiveness validated
- [ ] Performance impact assessed
- [ ] Security review completed
- [ ] Documentation updated
- [ ] User testing completed
"""

        issue_data = {
            "title": f"✨ {title}",
            "body": body,
            "labels": labels + ["enhancement", f"priority-{priority}"],
            "type": "feature",
            "created_at": datetime.now().isoformat(),
            "educational_context": context or {},
        }

        return self._submit_github_issue(issue_data)

    def _create_accessibility_issue(
        self,
        title: str,
        labels: List[str],
        priority: str,
        context: Dict[str, Any] = None,
    ) -> Dict[str, Any]:
        """Create accessibility-focused issue following WCAG 2.1 AA standards."""

        body = f"""
## ♿ Accessibility Issue Summary
{context.get('summary', 'Accessibility issue summary needed')}

## 🎯 WCAG 2.1 Guidelines Affected
- **Principle**: {context.get('wcag_principle', 'TBD')}
- **Guideline**: {context.get('wcag_guideline', 'TBD')}
- **Success Criterion**: {context.get('wcag_criterion', 'TBD')}
- **Level**: {context.get('wcag_level', 'AA')}

## 👥 User Impact
- **Affected User Groups**: {context.get('affected_users', 'Students with disabilities')}
- **Assistive Technologies**: {context.get('assistive_tech', 'Screen readers, keyboard navigation')}
- **Severity of Barrier**: {context.get('barrier_severity', 'Medium')}

## 🎓 Educational Impact
- **Learning Outcome Access**: {context.get('learning_access', 'TBD')}
- **UDL Principle Alignment**: {context.get('udl_alignment', 'TBD')}
- **Inclusive Design Benefit**: {context.get('inclusive_benefit', 'TBD')}

## 🧪 Testing Requirements
- [ ] Screen reader testing (NVDA, JAWS, VoiceOver)
- [ ] Keyboard-only navigation testing
- [ ] Color contrast verification
- [ ] Text scaling testing (200% zoom)
- [ ] Focus management verification
- [ ] Alternative text validation

## 🛠️ Proposed Solution
{context.get('proposed_solution', 'Solution proposal needed')}

## ✅ Definition of Done
- [ ] WCAG 2.1 AA compliance verified
- [ ] Assistive technology testing completed
- [ ] User testing with disability community
- [ ] Accessibility documentation updated
- [ ] Team training provided if needed
- [ ] Automated accessibility tests added
"""

        issue_data = {
            "title": f"♿ {title}",
            "body": body,
            "labels": labels + ["accessibility", f"priority-{priority}", "wcag-2.1"],
            "type": "accessibility",
            "created_at": datetime.now().isoformat(),
            "educational_context": context or {},
        }

        return self._submit_github_issue(issue_data)

    def _submit_github_issue(self, issue_data: Dict[str, Any]) -> Dict[str, Any]:
        """Submit issue to GitHub using CLI."""

        if not self.check_gh_cli():
            console.print("❌ Cannot submit issue - GitHub CLI not available")
            return {"error": "GitHub CLI not available"}

        # Prepare GitHub CLI command
        cmd = [
            "gh",
            "issue",
            "create",
            "--repo",
            self.repo_full,
            "--title",
            issue_data["title"],
            "--body",
            issue_data["body"],
            "--label",
            ",".join(issue_data["labels"]),
        ]

        try:
            # Execute GitHub CLI command
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            issue_url = result.stdout.strip()

            # Extract issue number from URL
            issue_number = issue_url.split("/")[-1]

            # Save to local tracking
            self._save_issue_locally(issue_data, issue_number, issue_url)

            console.print(f"✅ Issue created successfully: {issue_url}", style="green")
            return {
                "success": True,
                "issue_number": issue_number,
                "issue_url": issue_url,
                "data": issue_data,
            }

        except subprocess.CalledProcessError as e:
            console.print(f"❌ Failed to create issue: {e.stderr}", style="red")
            return {"error": e.stderr}

    def _save_issue_locally(
        self, issue_data: Dict[str, Any], issue_number: str, issue_url: str
    ):
        """Save issue data locally for project tracking."""

        # Load existing issues
        if self.issues_file.exists():
            with open(self.issues_file, "r") as f:
                issues = json.load(f)
        else:
            issues = {
                "issues": [],
                "metadata": {"last_updated": None, "total_count": 0},
            }

        # Add new issue
        issue_record = {
            "number": issue_number,
            "url": issue_url,
            "title": issue_data["title"],
            "type": issue_data["type"],
            "labels": issue_data["labels"],
            "created_at": issue_data["created_at"],
            "educational_context": issue_data.get("educational_context", {}),
            "status": "open",
        }

        issues["issues"].append(issue_record)
        issues["metadata"]["last_updated"] = datetime.now().isoformat()
        issues["metadata"]["total_count"] = len(issues["issues"])

        # Save back to file
        with open(self.issues_file, "w") as f:
            json.dump(issues, f, indent=2)


@click.group()
def cli():
    """GitHub Project Management Automation for Canvas Course Gamification"""
    pass


@cli.command()
@click.option(
    "--type",
    type=click.Choice(["bug", "feature", "task", "accessibility", "security"]),
    required=True,
    help="Type of issue to create",
)
@click.option("--title", required=True, help="Issue title")
@click.option(
    "--priority",
    type=click.Choice(["low", "medium", "high", "critical"]),
    default="medium",
    help="Issue priority",
)
@click.option("--labels", help="Comma-separated list of additional labels")
def create_issue(type, title, priority, labels):
    """Create a new GitHub issue with educational context."""

    console.print(Panel(f"Creating {type} issue: {title}", style="blue"))

    # Parse additional labels
    label_list = []
    if labels:
        label_list = [label.strip() for label in labels.split(",")]

    # Collect context based on issue type
    context = {}

    if type == "bug":
        context["description"] = Prompt.ask("Brief bug description")
        context["student_impact"] = Prompt.ask("Impact on student experience")
        context["faculty_impact"] = Prompt.ask("Impact on faculty workflow")
        context["reproduction_steps"] = Prompt.ask("How to reproduce this bug")
        context["expected_behavior"] = Prompt.ask("What should happen instead")

    elif type == "feature":
        context["summary"] = Prompt.ask("Feature summary")
        context["learning_outcomes"] = Prompt.ask(
            "Which learning outcomes does this support"
        )
        context["udl_principles"] = Prompt.ask("UDL principles this feature addresses")
        context["faculty_benefit"] = Prompt.ask("How does this help faculty")
        context["motivation"] = Prompt.ask("Why is this feature needed")

    elif type == "accessibility":
        context["wcag_principle"] = Prompt.ask("WCAG 2.1 principle affected")
        context["affected_users"] = Prompt.ask("Which user groups are affected")
        context["barrier_severity"] = Prompt.ask(
            "How severe is this accessibility barrier"
        )
        context["proposed_solution"] = Prompt.ask("Proposed solution approach")

    # Create issue
    manager = GitHubProjectManager()
    result = manager.create_issue_from_template(
        type, title, label_list, priority, context
    )

    if result.get("success"):
        console.print("✅ Issue created successfully!", style="green")
        console.print(f"🔗 URL: {result['issue_url']}")
    else:
        console.print(f"❌ Failed to create issue: {result.get('error')}", style="red")


@cli.command()
def current_issues():
    """Display current project issues and status."""

    manager = GitHubProjectManager()

    if not manager.issues_file.exists():
        console.print(
            "No local issue tracking file found. Create some issues first!",
            style="yellow",
        )
        return

    with open(manager.issues_file, "r") as f:
        data = json.load(f)

    # Create summary table
    table = Table(title="Current Project Issues")
    table.add_column("Number", style="cyan")
    table.add_column("Type", style="magenta")
    table.add_column("Title", style="white")
    table.add_column("Priority", style="yellow")
    table.add_column("Status", style="green")

    for issue in data["issues"]:
        priority = "unknown"
        for label in issue["labels"]:
            if label.startswith("priority-"):
                priority = label.replace("priority-", "")

        table.add_row(
            issue["number"],
            issue["type"],
            issue["title"][:50] + "..." if len(issue["title"]) > 50 else issue["title"],
            priority,
            issue["status"],
        )

    console.print(table)
    console.print(f"\nTotal Issues: {data['metadata']['total_count']}")
    console.print(f"Last Updated: {data['metadata']['last_updated']}")


if __name__ == "__main__":
    cli()
