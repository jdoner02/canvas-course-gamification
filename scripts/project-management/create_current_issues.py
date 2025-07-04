#!/usr/bin/env python3
"""
Issue Creation Script for Current Project Status
==============================================

Creates GitHub issues for all identified bugs, features, and tasks
based on our current project analysis.

Best Practices:
- Clear, actionable titles
- Comprehensive descriptions
- Proper labeling and prioritization
- Educational technology context
- Software engineering standards
"""

import json
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Dict, List


class IssueCreator:
    """Creates and manages GitHub issues following enterprise standards."""

    def __init__(self):
        self.issues = []

    def create_critical_bugs(self):
        """Create issues for critical bugs blocking deployment."""

        # Bug 1: Validation Result Handling
        self.issues.append(
            {
                "title": "[CRITICAL BUG] ValidationResult object not subscriptable in deploy.py",
                "body": """## 🐛 Bug Description
Deployment fails due to improper handling of ValidationResult object in the deploy.py script.

## 🔄 Steps to Reproduce
1. Run `python deploy.py --config examples/linear_algebra --validate-only`
2. Validation passes but result processing fails
3. Error: `'ValidationResult' object is not subscriptable`

## ✅ Expected Behavior
Validation should complete and display results properly, allowing deployment to proceed.

## ❌ Actual Behavior
Script crashes with validation result handling error despite successful validation.

## 🎯 Impact Assessment
- [x] **Critical** - Blocks deployment/core functionality

## 🏷️ Component Areas
- [x] Canvas API Integration
- [x] Validation System

## 🔬 Technical Details
Error occurs in validation result processing around line ~325 in deploy.py.
The ValidationResult object structure has changed but the handling code expects a dictionary.

## 📋 Acceptance Criteria
- [ ] ValidationResult object properly handled
- [ ] Deployment validation completes successfully
- [ ] Error handling improved for validation failures
- [ ] Unit tests added for validation result processing

## 🎓 Educational Impact
**High** - Prevents course deployment to Canvas, blocking student access to gamified content.

## ⏱️ Estimated Effort
**2-4 hours** - Code review and validation object refactoring""",
                "labels": ["bug", "critical", "deployment", "validation"],
                "priority": "P0",
            }
        )

        # Bug 2: Missing API Method
        self.issues.append(
            {
                "title": "[HIGH BUG] CanvasAPIClient missing get_course method",
                "body": """## 🐛 Bug Description
CourseBuilder expects `get_course` method on CanvasAPIClient but method doesn't exist.

## 🔄 Steps to Reproduce
1. Initialize CourseBuilder with CanvasAPIClient
2. Attempt course deployment
3. Error: `'CanvasAPIClient' object has no attribute 'get_course'`

## ✅ Expected Behavior
CanvasAPIClient should provide get_course method for course information retrieval.

## ❌ Actual Behavior
AttributeError prevents course initialization and deployment.

## 🎯 Impact Assessment
- [x] **High** - Affects user experience significantly

## 🏷️ Component Areas
- [x] Canvas API Integration
- [x] Course Builder

## 🔬 Technical Details
CourseBuilder.deploy_course() calls `self.canvas_client.get_course()` but method is missing.
Available methods: get_course_info, get_course_modules, get_course_assignments.

## 📋 Acceptance Criteria
- [ ] Add get_course method to CanvasAPIClient
- [ ] Method returns proper course object
- [ ] Update CourseBuilder to use correct API methods
- [ ] Add integration tests for course retrieval

## 🎓 Educational Impact
**High** - Prevents Canvas integration, core functionality for course management.

## ⏱️ Estimated Effort
**3-5 hours** - API method implementation and integration testing""",
                "labels": ["bug", "high", "canvas-api", "integration"],
                "priority": "P0",
            }
        )

        # Bug 3: Table Validation Issue
        self.issues.append(
            {
                "title": "[MEDIUM BUG] Table accessibility validation regex too strict",
                "body": """## 🐛 Bug Description
Accessibility validator marks properly formatted tables as having missing headers due to overly strict regex pattern.

## 🔄 Steps to Reproduce
1. Run validation on pages with properly formatted tables
2. Tables have `<thead>`, `<th>` elements, and proper structure
3. Validator still flags as "Data tables without proper headers"

## ✅ Expected Behavior
Tables with proper semantic markup should pass accessibility validation.

## ❌ Actual Behavior
Validator regex `r"<table(?![^>]*<th)[^>]*>.*?</table>"` doesn't detect nested `<th>` elements.

## 🎯 Impact Assessment
- [x] **Medium** - Minor impact on functionality

## 🏷️ Component Areas
- [x] Validation System
- [x] Accessibility/UDL

## 🔬 Technical Details
Regex pattern in src/validators/__init__.py line ~327 needs improvement to handle:
- Nested table structures
- `<thead>/<tbody>` semantic markup
- Complex table layouts

## 📋 Acceptance Criteria
- [ ] Update regex pattern to properly detect headers
- [ ] Test with various table structures
- [ ] Maintain WCAG 2.1 AA compliance
- [ ] Add unit tests for table validation

## 🎓 Educational Impact
**Medium** - Accessibility compliance important for inclusive education.

## ⏱️ Estimated Effort
**2-3 hours** - Regex improvement and testing""",
                "labels": ["bug", "medium", "accessibility", "validation"],
                "priority": "P1",
            }
        )

    def create_priority_features(self):
        """Create issues for high-priority features."""

        # Feature 1: Deployment Automation
        self.issues.append(
            {
                "title": "[FEATURE] Complete end-to-end deployment automation",
                "body": """## 🚀 Feature Description
Implement comprehensive deployment automation that handles the complete Canvas course setup process.

## 🎯 User Story
As an **instructor**, I want to **deploy a complete gamified course to Canvas with one command** so that **I can focus on teaching instead of technical setup**.

## 📋 Requirements
### Functional Requirements
- [ ] One-command deployment (`deploy.py --config examples/linear_algebra`)
- [ ] Automatic error recovery and rollback
- [ ] Progress tracking and detailed logging
- [ ] Canvas permissions validation
- [ ] Content verification post-deployment

### Non-Functional Requirements
- [ ] Deployment completes in <5 minutes for typical course
- [ ] 99.9% success rate for valid configurations
- [ ] Comprehensive error messages for failures
- [ ] Idempotent operations (safe to re-run)

## 🏗️ Technical Design
1. **Pre-deployment validation**
   - Canvas API connectivity
   - Course configuration integrity
   - Permission checks
2. **Deployment phases**
   - Course structure creation
   - Content upload and linking
   - Gamification setup
   - Accessibility verification
3. **Post-deployment verification**
   - Link validation
   - Content accessibility
   - Student view testing

## 📋 Acceptance Criteria
- [ ] Instructor can deploy course with single command
- [ ] Deployment includes all 12 modules, 11 assignments, 30 outcomes
- [ ] Gamification elements (XP, badges) properly configured
- [ ] Skill tree progression working
- [ ] All accessibility standards met (WCAG 2.1 AA)
- [ ] Comprehensive error handling and user feedback

## 🎓 Educational Impact
**Critical** - Enables faculty to deploy engaging, accessible courses efficiently.

## ⏱️ Estimated Effort
**1-2 weeks** - Complex integration with multiple systems""",
                "labels": ["feature", "high", "deployment", "automation"],
                "priority": "P1",
            }
        )

        # Feature 2: GitHub Project Integration
        self.issues.append(
            {
                "title": "[FEATURE] GitHub Projects integration for issue tracking",
                "body": """## 🚀 Feature Description
Implement automated GitHub Projects integration for professional project management and issue tracking.

## 🎯 User Story
As a **development team member**, I want **automated project board management** so that **we can track progress and maintain professional workflows**.

## 📋 Requirements
### Functional Requirements
- [ ] Automated project board creation
- [ ] Issue categorization by component and priority
- [ ] Sprint planning and milestone tracking
- [ ] Progress metrics and reporting
- [ ] Integration with GitHub CLI

### Educational Requirements
- [ ] Faculty-friendly issue templates
- [ ] Student contribution guidelines
- [ ] Educational technology best practices documentation

## 🏗️ Technical Implementation
1. **Project Board Automation**
   - Auto-create columns (Backlog, In Progress, Review, Done)
   - Issue auto-assignment based on labels
   - Sprint milestone management
2. **CLI Integration**
   - Create issues from markdown templates
   - Bulk operations for project setup
   - Status reporting and metrics
3. **Workflow Automation**
   - PR linking to issues
   - Automated testing on issue updates
   - Release notes generation

## 📋 Acceptance Criteria
- [ ] Project board automatically maintained
- [ ] Issues properly categorized and prioritized
- [ ] CLI commands for common operations
- [ ] Sprint metrics and reporting
- [ ] Educational team workflow documentation

## 🎓 Educational Impact
**High** - Enables professional development practices for educational technology projects.

## ⏱️ Estimated Effort
**1 week** - GitHub API integration and automation setup""",
                "labels": ["feature", "high", "project-management", "automation"],
                "priority": "P1",
            }
        )

    def create_enhancement_tasks(self):
        """Create issues for system enhancements."""

        # Enhancement 1: CLI Improvement
        self.issues.append(
            {
                "title": "[ENHANCEMENT] Complete CLI command structure implementation",
                "body": """## 🔧 Enhancement Description
Expand CLI tool to provide comprehensive course management capabilities.

## 🎯 Current State
CLI has basic wrapper functionality but lacks full command structure for course operations.

## 🎯 Desired State
Complete CLI with validation, deployment, testing, and management commands.

## 📋 Requirements
### Core Commands
- [ ] `validate` - Course configuration validation
- [ ] `deploy` - Canvas deployment with options
- [ ] `test` - Integration and accessibility testing
- [ ] `scaffold` - New course creation from templates
- [ ] `status` - Project and deployment status
- [ ] `update` - Course content updates

### Advanced Commands
- [ ] `analytics` - Course engagement metrics
- [ ] `export` - Course content export
- [ ] `preview` - Local course preview
- [ ] `migrate` - Cross-platform course migration

## 📋 Acceptance Criteria
- [ ] All commands have comprehensive help text
- [ ] Progress indicators for long operations
- [ ] Colored output for better UX
- [ ] Configuration file support
- [ ] Error handling with actionable messages

## 🎓 Educational Impact
**Medium** - Improves faculty experience with course management tools.

## ⏱️ Estimated Effort
**3-5 days** - CLI framework expansion and testing""",
                "labels": ["enhancement", "medium", "cli", "ux"],
                "priority": "P2",
            }
        )

    def create_documentation_tasks(self):
        """Create issues for documentation needs."""

        self.issues.append(
            {
                "title": "[DOCUMENTATION] Faculty onboarding and workflow guide",
                "body": """## 📚 Documentation Need
Create comprehensive onboarding guide for faculty using the Canvas Course Gamification Framework.

## 🎯 Target Audience
- **Primary**: Faculty with limited technical experience
- **Secondary**: IT support staff
- **Tertiary**: Student assistants

## 📋 Content Requirements
### Getting Started Guide
- [ ] System requirements and installation
- [ ] Canvas API setup and permissions
- [ ] First course deployment walkthrough
- [ ] Troubleshooting common issues

### Course Design Guide
- [ ] Gamification best practices
- [ ] Accessibility guidelines (WCAG 2.1 AA)
- [ ] UDL implementation strategies
- [ ] Assessment design for mastery learning

### Technical Reference
- [ ] Configuration file documentation
- [ ] CLI command reference
- [ ] API integration examples
- [ ] Customization guidelines

## 📋 Acceptance Criteria
- [ ] Faculty can complete first deployment in <30 minutes
- [ ] Documentation passes accessibility review
- [ ] Examples work with current codebase
- [ ] Video tutorials for key workflows

## 🎓 Educational Impact
**High** - Reduces faculty onboarding time and improves adoption.

## ⏱️ Estimated Effort
**1 week** - Comprehensive documentation creation""",
                "labels": ["documentation", "high", "onboarding", "faculty"],
                "priority": "P1",
            }
        )

    def generate_all_issues(self):
        """Generate all identified issues."""
        self.create_critical_bugs()
        self.create_priority_features()
        self.create_enhancement_tasks()
        self.create_documentation_tasks()
        return self.issues

    def save_issues_locally(self):
        """Save issues to local files for review and GitHub CLI automation."""
        issues = self.generate_all_issues()

        # Create issues directory
        issues_dir = Path("scripts/project-management/issues")
        issues_dir.mkdir(parents=True, exist_ok=True)

        # Save each issue as a separate file
        for i, issue in enumerate(issues, 1):
            filename = f"{i:02d}_{issue['title'].lower().replace(' ', '_').replace('[', '').replace(']', '').replace(':', '')}.md"

            with open(issues_dir / filename, "w") as f:
                f.write(f"# {issue['title']}\n\n")
                f.write(f"**Priority:** {issue['priority']}\n")
                f.write(f"**Labels:** {', '.join(issue['labels'])}\n\n")
                f.write(issue["body"])

        # Create summary file
        with open(issues_dir / "00_issues_summary.json", "w") as f:
            json.dump(issues, f, indent=2)

        print(f"✅ Created {len(issues)} issue files in {issues_dir}")
        return issues_dir


if __name__ == "__main__":
    creator = IssueCreator()
    issues_dir = creator.save_issues_locally()
    print(f"📁 Issues saved to: {issues_dir}")
    print("🚀 Next steps:")
    print("   1. Review issue files")
    print("   2. Run: python scripts/project-management/create_github_issues.py")
    print("   3. Set up project board with: gh project create")
