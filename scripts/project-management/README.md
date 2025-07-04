# Project Management System for Canvas Course Gamification

A comprehensive, faculty-friendly project management workflow that combines local markdown files with GitHub issue tracking for transparent, collaborative development.

## 🎯 Overview

This system enables:
- **Local Issue Management**: Create and edit issues as markdown files
- **GitHub Synchronization**: Automatically sync issues to GitHub for team collaboration  
- **Workflow Automation**: Intelligent commit messages and progress tracking
- **Educational Focus**: Designed for faculty workflow and educational technology best practices

## 🚀 Quick Start

### 1. Setup Templates
```bash
python scripts/project-management/local_issue_manager.py --setup
```

### 2. Create Your First Issue
```bash
python scripts/project-management/local_issue_manager.py --create
```

### 3. Sync to GitHub
```bash
python scripts/project-management/local_issue_manager.py --sync
```

## 📋 Core Scripts

### `local_issue_manager.py` - Faculty Interface
**Purpose**: Interactive, user-friendly issue creation and management

**Key Features**:
- Interactive issue creation with templates
- Local markdown file management
- GitHub synchronization
- Progress tracking

**Usage**:
```bash
# Interactive mode
python scripts/project-management/local_issue_manager.py

# Create new issue
python scripts/project-management/local_issue_manager.py --create

# List all local issues
python scripts/project-management/local_issue_manager.py --list

# Sync all issues to GitHub
python scripts/project-management/local_issue_manager.py --sync

# Show project status
python scripts/project-management/local_issue_manager.py --status
```

### `github_integration.py` - GitHub API Interface
**Purpose**: Professional GitHub CLI integration for issue management

**Key Features**:
- Bulk issue creation from local files
- Automated labeling and prioritization
- Project board integration
- Progress tracking and metrics

**Usage**:
```bash
# Setup GitHub project infrastructure
python scripts/project-management/github_integration.py --setup

# Create GitHub issues from local files
python scripts/project-management/github_integration.py --create-issues

# Show project dashboard
python scripts/project-management/github_integration.py --dashboard
```

### `workflow_manager.py` - Development Workflow
**Purpose**: Automated commit management and quality gates

**Key Features**:
- Intelligent commit message generation
- Quality checks and validation
- Progress tracking
- Educational technology standards compliance

**Usage**:
```bash
# Show current status
python scripts/project-management/workflow_manager.py --status

# Run quality checks
python scripts/project-management/workflow_manager.py --check

# Commit changes with automated message
python scripts/project-management/workflow_manager.py --commit

# Commit and push
python scripts/project-management/workflow_manager.py --commit --push
```

## 📝 Issue Templates

The system provides three main issue types:

### 🐛 Bug Reports
- Clear problem description
- Reproduction steps
- Impact assessment
- Educational context

### 🚀 Feature Requests  
- Problem statement
- Requirements and success criteria
- Educational benefits (UDL, accessibility, faculty workflow)
- Effort estimation

### 📋 Tasks
- Clear objectives
- Acceptance criteria
- Component areas
- Effort estimation

## 🔄 Workflow Process

### For Faculty/Individual Contributors

1. **Create Issue Locally**:
   ```bash
   python scripts/project-management/local_issue_manager.py --create
   ```

2. **Edit Issue File**: 
   - Files are created in `scripts/project-management/issues/`
   - Use any text editor to add details
   - Follow the template structure

3. **Sync to GitHub**:
   ```bash
   python scripts/project-management/local_issue_manager.py --sync
   ```

### For Development Work

1. **Check Project Status**:
   ```bash
   python scripts/project-management/workflow_manager.py --status
   ```

2. **Make Changes**: Edit code files as needed

3. **Quality Check**:
   ```bash
   python scripts/project-management/workflow_manager.py --check
   ```

4. **Commit with Automation**:
   ```bash
   python scripts/project-management/workflow_manager.py --commit --push
   ```

## 🏷️ Labels and Organization

### Priority Levels
- **P0**: Critical - Blocks core functionality
- **P1**: High - Important for user experience  
- **P2**: Medium - Nice to have
- **P3**: Low - Future enhancement

### Component Areas
- `component/canvas-api`: Canvas LMS integration
- `component/course-builder`: Course structure creation
- `component/gamification`: XP, badges, skill trees
- `component/validation`: Content and accessibility validation
- `component/cli`: Command line interface
- `component/documentation`: User guides and API docs

### Educational Labels
- `edu/accessibility`: WCAG 2.1 AA compliance
- `edu/udl`: Universal Design for Learning
- `edu/faculty-ux`: Faculty user experience
- `edu/student-engagement`: Student engagement features

## 📊 Project Tracking

### Local Status
```bash
python scripts/project-management/local_issue_manager.py --list
```

### GitHub Dashboard
```bash
python scripts/project-management/github_integration.py --dashboard
```

### Development Status  
```bash
python scripts/project-management/workflow_manager.py --status
```

## 🎓 Educational Technology Best Practices

This system implements:

- **Accessibility**: WCAG 2.1 AA compliance tracking
- **UDL**: Universal Design for Learning principles
- **Faculty Workflow**: Optimized for educational technology adoption
- **Student Engagement**: Gamification and engagement metrics
- **Transparency**: Open, trackable development process

## 🔧 Advanced Configuration

### Custom Labels
Add custom labels via GitHub CLI:
```bash
gh label create "custom/label" --color "ffffff" --description "Custom label"
```

### Project Board Customization
Access the project board at: https://github.com/users/[username]/projects/[number]

### Integration with IDEs
The markdown files can be edited in any IDE with markdown support:
- VS Code with markdown extensions
- GitHub's web interface
- Any text editor

## 🆘 Troubleshooting

### GitHub CLI Not Authenticated
```bash
gh auth login
gh auth refresh -s project
```

### Permission Issues
Ensure GitHub token has proper scopes:
- `repo` - Repository access
- `project` - Project board access

### Python Dependencies
Install required packages:
```bash
pip install click rich
```

## 📚 Additional Resources

- [GitHub CLI Documentation](https://cli.github.com/)
- [Canvas API Documentation](https://canvas.instructure.com/doc/api/)
- [WCAG 2.1 Guidelines](https://www.w3.org/WAI/WCAG21/quickref/)
- [UDL Guidelines](http://www.udlguidelines.cast.org/)

---

*This project management system is designed to support faculty adoption of educational technology through transparent, collaborative, and accessible development practices.*
