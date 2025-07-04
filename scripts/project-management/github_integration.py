#!/usr/bin/env python3
"""
GitHub CLI Integration for Issue Management
==========================================

Professional GitHub integration following enterprise development practices.
Automates issue creation, project board management, and workflow tracking.

Features:
- Bulk issue creation from local files
- Automated labeling and prioritization
- Project board integration
- Milestone management
- Progress tracking and metrics

Best Practices:
- DevOps automation standards
- Educational technology workflow
- Accessibility and UDL considerations
- Faculty-friendly documentation
"""

import json
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Optional
import click
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn

console = Console()


class GitHubIntegration:
    """Professional GitHub CLI integration for educational technology projects."""

    def __init__(self, repo_owner: str = None, repo_name: str = None):
        self.repo_owner = repo_owner
        self.repo_name = repo_name
        self.verify_gh_cli()

    def verify_gh_cli(self):
        """Verify GitHub CLI is installed and authenticated."""
        try:
            result = subprocess.run(['gh', 'auth', 'status'], 
                                  capture_output=True, text=True, check=True)
            console.print("✅ GitHub CLI authenticated", style="green")
        except subprocess.CalledProcessError:
            console.print("❌ GitHub CLI not authenticated", style="red")
            console.print("Run: gh auth login")
            sys.exit(1)
        except FileNotFoundError:
            console.print("❌ GitHub CLI not installed", style="red")
            console.print("Install from: https://cli.github.com/")
            sys.exit(1)

    def create_project_board(self, name: str = "Canvas Course Gamification") -> str:
        """Create GitHub project board with proper columns."""
        
        console.print(f"🔄 Creating project board: {name}")
        
        try:
            # Create project
            result = subprocess.run([
                'gh', 'project', 'create',
                '--title', name,
                '--body', 'Canvas Course Gamification Framework - Professional project tracking'
            ], capture_output=True, text=True, check=True)
            
            project_url = result.stdout.strip()
            console.print(f"✅ Project created: {project_url}", style="green")
            
            # Add standard columns
            columns = [
                "📋 Backlog",
                "🔄 In Progress", 
                "👀 In Review",
                "✅ Done",
                "🚫 Blocked"
            ]
            
            for column in columns:
                try:
                    subprocess.run([
                        'gh', 'project', 'field-create', project_url,
                        '--name', column,
                        '--type', 'single_select'
                    ], capture_output=True, text=True, check=True)
                    console.print(f"   ✅ Added column: {column}")
                except subprocess.CalledProcessError as e:
                    console.print(f"   ⚠️  Column may already exist: {column}")
            
            return project_url
            
        except subprocess.CalledProcessError as e:
            console.print(f"❌ Failed to create project: {e.stderr}", style="red")
            return None

    def create_labels(self):
        """Create standardized labels for educational technology projects."""
        
        labels = {
            # Priority Labels
            "priority/P0": {"color": "d73a4a", "description": "Critical - Blocks core functionality"},
            "priority/P1": {"color": "fbca04", "description": "High - Important for user experience"},
            "priority/P2": {"color": "0075ca", "description": "Medium - Nice to have"},
            "priority/P3": {"color": "7057ff", "description": "Low - Future enhancement"},
            
            # Component Labels
            "component/canvas-api": {"color": "d4edda", "description": "Canvas LMS integration"},
            "component/course-builder": {"color": "e2e3e5", "description": "Course structure creation"},
            "component/gamification": {"color": "fff3cd", "description": "XP, badges, skill trees"},
            "component/validation": {"color": "f8d7da", "description": "Content and accessibility validation"},
            "component/cli": {"color": "d4edda", "description": "Command line interface"},
            "component/documentation": {"color": "e2e3e5", "description": "User guides and API docs"},
            
            # Type Labels
            "type/bug": {"color": "d73a4a", "description": "Something isn't working"},
            "type/feature": {"color": "a2eeef", "description": "New feature or enhancement"},
            "type/task": {"color": "7057ff", "description": "General task or maintenance"},
            "type/documentation": {"color": "0075ca", "description": "Documentation updates"},
            
            # Educational Labels
            "edu/accessibility": {"color": "b60205", "description": "WCAG 2.1 AA compliance"},
            "edu/udl": {"color": "0e8a16", "description": "Universal Design for Learning"},
            "edu/faculty-ux": {"color": "fbca04", "description": "Faculty user experience"},
            "edu/student-engagement": {"color": "006b75", "description": "Student engagement features"},
            
            # Status Labels
            "status/blocked": {"color": "d73a4a", "description": "Blocked by external dependency"},
            "status/needs-review": {"color": "fbca04", "description": "Needs code or design review"},
            "status/ready": {"color": "0e8a16", "description": "Ready for development"},
        }
        
        console.print("🔄 Creating standardized labels...")
        
        for label_name, config in labels.items():
            try:
                subprocess.run([
                    'gh', 'label', 'create', label_name,
                    '--color', config['color'],
                    '--description', config['description']
                ], capture_output=True, text=True, check=True)
                console.print(f"   ✅ Created label: {label_name}")
            except subprocess.CalledProcessError:
                console.print(f"   ⚠️  Label exists: {label_name}")

    def create_issue_from_file(self, issue_file: Path) -> Optional[str]:
        """Create GitHub issue from markdown file."""
        
        if not issue_file.exists():
            console.print(f"❌ Issue file not found: {issue_file}", style="red")
            return None
        
        content = issue_file.read_text()
        lines = content.split('\n')
        
        # Extract title (first header)
        title = lines[0].replace('# ', '') if lines else "Untitled Issue"
        
        # Extract metadata
        labels = []
        priority = "P2"  # default
        
        for line in lines:
            if line.startswith('**Priority:**'):
                priority = line.split(':')[1].strip()
            elif line.startswith('**Labels:**'):
                labels_str = line.split(':')[1].strip()
                labels = [l.strip() for l in labels_str.split(',')]
        
        # Add priority label
        labels.append(f"priority/{priority}")
        
        try:
            cmd = ['gh', 'issue', 'create', '--title', title, '--body-file', str(issue_file)]
            if labels:
                cmd.extend(['--label', ','.join(labels)])
            
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            issue_url = result.stdout.strip()
            
            console.print(f"✅ Created issue: {title}")
            console.print(f"   🔗 {issue_url}")
            
            return issue_url
            
        except subprocess.CalledProcessError as e:
            console.print(f"❌ Failed to create issue: {e.stderr}", style="red")
            return None

    def bulk_create_issues(self, issues_dir: Path):
        """Create all issues from directory."""
        
        if not issues_dir.exists():
            console.print(f"❌ Issues directory not found: {issues_dir}", style="red")
            return
        
        issue_files = list(issues_dir.glob("*.md"))
        # Skip summary files
        issue_files = [f for f in issue_files if not f.name.startswith('00_')]
        
        console.print(f"🔄 Creating {len(issue_files)} issues...")
        
        created_issues = []
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("Creating issues...", total=len(issue_files))
            
            for issue_file in issue_files:
                issue_url = self.create_issue_from_file(issue_file)
                if issue_url:
                    created_issues.append(issue_url)
                progress.advance(task)
        
        console.print(f"✅ Created {len(created_issues)} issues successfully", style="green")
        return created_issues

    def setup_milestones(self):
        """Create project milestones."""
        
        milestones = [
            {
                "title": "Sprint 1: Core Deployment",
                "description": "Fix critical bugs and complete Canvas deployment",
                "due_date": "2025-07-18"  # 2 weeks from now
            },
            {
                "title": "Sprint 2: Enhanced Features", 
                "description": "Advanced gamification and analytics features",
                "due_date": "2025-08-01"  # 4 weeks from now
            },
            {
                "title": "v1.0 Release",
                "description": "Production-ready Canvas Course Gamification Framework",
                "due_date": "2025-08-15"  # 6 weeks from now
            }
        ]
        
        console.print("🔄 Creating project milestones...")
        
        for milestone in milestones:
            try:
                subprocess.run([
                    'gh', 'api', 'repos/:owner/:repo/milestones',
                    '--method', 'POST',
                    '--field', f'title={milestone["title"]}',
                    '--field', f'description={milestone["description"]}',
                    '--field', f'due_on={milestone["due_date"]}T23:59:59Z'
                ], capture_output=True, text=True, check=True)
                
                console.print(f"   ✅ Created milestone: {milestone['title']}")
                
            except subprocess.CalledProcessError as e:
                console.print(f"   ⚠️  Milestone may exist: {milestone['title']}")

    def generate_progress_report(self) -> Dict:
        """Generate current project progress report."""
        
        try:
            # Get issues by label
            result = subprocess.run([
                'gh', 'issue', 'list', '--json', 'title,labels,state,url'
            ], capture_output=True, text=True, check=True)
            
            issues = json.loads(result.stdout)
            
            # Categorize issues
            stats = {
                "total": len(issues),
                "open": len([i for i in issues if i['state'] == 'open']),
                "closed": len([i for i in issues if i['state'] == 'closed']),
                "by_priority": {},
                "by_component": {},
                "by_type": {}
            }
            
            for issue in issues:
                labels = [l['name'] for l in issue['labels']]
                
                # Count by priority
                priority_labels = [l for l in labels if l.startswith('priority/')]
                if priority_labels:
                    priority = priority_labels[0]
                    stats["by_priority"][priority] = stats["by_priority"].get(priority, 0) + 1
                
                # Count by component
                component_labels = [l for l in labels if l.startswith('component/')]
                for component in component_labels:
                    stats["by_component"][component] = stats["by_component"].get(component, 0) + 1
                
                # Count by type
                type_labels = [l for l in labels if l.startswith('type/')]
                for issue_type in type_labels:
                    stats["by_type"][issue_type] = stats["by_type"].get(issue_type, 0) + 1
            
            return stats
            
        except subprocess.CalledProcessError as e:
            console.print(f"❌ Failed to get project stats: {e.stderr}", style="red")
            return {}

    def display_progress_dashboard(self):
        """Display comprehensive project dashboard."""
        
        stats = self.generate_progress_report()
        
        if not stats:
            return
        
        # Main stats table
        main_table = Table(title="📊 Project Overview")
        main_table.add_column("Metric", style="cyan")
        main_table.add_column("Count", style="green")
        main_table.add_column("Percentage", style="yellow")
        
        total = stats["total"]
        if total > 0:
            main_table.add_row("Total Issues", str(total), "100%")
            main_table.add_row("Open", str(stats["open"]), f"{stats['open']/total*100:.1f}%")
            main_table.add_row("Closed", str(stats["closed"]), f"{stats['closed']/total*100:.1f}%")
        
        console.print(main_table)
        console.print()
        
        # Priority breakdown
        if stats["by_priority"]:
            priority_table = Table(title="🎯 Issues by Priority")
            priority_table.add_column("Priority", style="cyan")
            priority_table.add_column("Count", style="green")
            
            for priority, count in sorted(stats["by_priority"].items()):
                priority_table.add_row(priority, str(count))
            
            console.print(priority_table)
            console.print()
        
        # Component breakdown
        if stats["by_component"]:
            component_table = Table(title="🔧 Issues by Component")
            component_table.add_column("Component", style="cyan")
            component_table.add_column("Count", style="green")
            
            for component, count in sorted(stats["by_component"].items()):
                component_table.add_row(component, str(count))
            
            console.print(component_table)


@click.command()
@click.option('--setup', is_flag=True, help='Setup project board and labels')
@click.option('--create-issues', is_flag=True, help='Create issues from local files')
@click.option('--dashboard', is_flag=True, help='Show project dashboard')
@click.option('--issues-dir', default='scripts/project-management/issues', 
              help='Directory containing issue files')
def main(setup, create_issues, dashboard, issues_dir):
    """GitHub integration for Canvas Course Gamification project management."""
    
    console.print(Panel.fit(
        "[bold blue]🚀 Canvas Course Gamification - GitHub Integration[/bold blue]\n"
        "Professional project management automation",
        title="GitHub Project Manager"
    ))
    
    gh = GitHubIntegration()
    
    if setup:
        console.print("\n[bold]🔧 Setting up project infrastructure...[/bold]")
        gh.create_labels()
        gh.setup_milestones()
        project_url = gh.create_project_board()
        if project_url:
            console.print(f"\n✅ Project setup complete!")
            console.print(f"🔗 Project board: {project_url}")
    
    if create_issues:
        console.print(f"\n[bold]📝 Creating issues from {issues_dir}...[/bold]")
        issues_path = Path(issues_dir)
        created_issues = gh.bulk_create_issues(issues_path)
        if created_issues:
            console.print(f"\n✅ Successfully created {len(created_issues)} issues!")
    
    if dashboard:
        console.print("\n[bold]📊 Project Dashboard[/bold]")
        gh.display_progress_dashboard()
    
    if not (setup or create_issues or dashboard):
        console.print("\n[bold yellow]ℹ️  No action specified. Use --help for options.[/bold yellow]")

if __name__ == "__main__":
    main()
