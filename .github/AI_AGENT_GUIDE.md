# AI Agent Guide: Autonomous Project Management Workflow

## 🤖 Overview for AI Agents

This guide provides comprehensive instructions for AI agents (like GitHub Copilot, Claude, etc.) to autonomously manage project issues and workflows with minimal human intervention. The system is designed to enable professional project management through programmatic interfaces.

## 🔧 Setting Up GitHub Copilot Agent Mode

### For Students and Teachers

#### Step 1: Install GitHub Copilot
1. **VS Code Extension**: Install "GitHub Copilot" and "GitHub Copilot Chat" extensions
2. **Authentication**: Sign in with GitHub account that has Copilot access
3. **Agent Mode**: Enable "Agent Mode" in VS Code settings:
   ```
   Settings → Extensions → GitHub Copilot → Enable: Agent Mode
   ```

#### Step 2: Access Agent Mode
- **Command Palette**: `Ctrl/Cmd + Shift + P` → "GitHub Copilot: Open Chat"
- **Chat Interface**: Click the Copilot chat icon in the sidebar
- **Agent Activation**: Type `@agent` to activate agent mode

#### Step 3: Workspace Context
- **Add Files**: Right-click on files → "Add to Copilot Chat" 
- **Include Directories**: Right-click on folders → "Add to Copilot Chat"
- **Context Management**: Use `#file:filename` or `#folder:foldername` in prompts

#### Step 4: Follow Workflow Standards
Always reference the workflow documentation:
- **Project Status**: Read `.github/PROJECT_STATUS.md` first
- **Issue Templates**: Use `.github/ISSUE_TEMPLATE/` for consistency
- **Workflow Manager**: Follow `scripts/project-management/workflow_manager.py` patterns

## 🎯 Autonomous Issue Creation

### Programmatic Interface

Use the enhanced `local_issue_manager.py` for autonomous issue creation:

```bash
python scripts/project-management/local_issue_manager.py \
  --title "Feature: Interactive skill tree visualization" \
  --type feature \
  --priority P1 \
  --component gamification \
  --description "Create interactive D3.js visualization for student progress tracking" \
  --requirements "D3.js integration, Progress tracking API, Responsive design" \
  --acceptance-criteria "Visual displays correctly, Updates in real-time, Mobile responsive" \
  --educational-impact "Enhances student engagement and progress awareness" \
  --estimated-effort "8-12 hours" \
  --auto-sync
```

### Parameters Reference

| Parameter | Type | Options | Description |
|-----------|------|---------|-------------|
| `--title` | string | required | Clear, descriptive issue title |
| `--type` | choice | bug, feature, task, documentation | Issue type |
| `--priority` | choice | P0, P1, P2, P3 | Priority level (P0=Critical, P3=Low) |
| `--component` | choice | canvas-api, course-builder, gamification, validation, cli, documentation | Primary component |
| `--description` | string | optional | Detailed description |
| `--requirements` | string | optional | Comma-separated requirements list |
| `--acceptance-criteria` | string | optional | Comma-separated criteria list |
| `--educational-impact` | string | optional | Educational benefits description |
| `--estimated-effort` | string | optional | Time estimation (default: "2-4 hours") |
| `--related-resources` | string | optional | Comma-separated resource links |
| `--auto-sync` | flag | optional | Automatically sync to GitHub |

## 📋 AI Agent Workflow Patterns

### Pattern 1: Client Request Processing

When receiving a client request (like Dr. Lynch's MATH 231 customization):

1. **Analyze Requirements**:
   ```python
   # Read client context files
   requirements = analyze_client_needs(
       course_info="MATH 231 Linear Algebra",
       instructor="Dr. Frank Lynch",
       university="Eastern Washington University",
       student_mix=["CS", "EE", "Cyber", "Applied Math"]
   )
   ```

2. **Create Feature Issues**:
   ```bash
   # Major feature for course customization
   python scripts/project-management/local_issue_manager.py \
     --title "FEATURE: MATH 231 EWU Customization Framework" \
     --type feature \
     --priority P0 \
     --component course-builder \
     --description "Create customizable framework for Dr. Lynch's MATH 231 course at EWU" \
     --requirements "EWU branding, Multi-major pathways, YouTube integration, Flip classroom support" \
     --acceptance-criteria "Configurable per instructor, Multi-pathway support, Accessible design" \
     --educational-impact "Enables personalized learning paths for diverse student backgrounds" \
     --estimated-effort "20-30 hours" \
     --auto-sync
   ```

3. **Create Supporting Tasks**:
   ```bash
   # YouTube integration task
   python scripts/project-management/local_issue_manager.py \
     --title "TASK: YouTube Transcript Scraper for Dr. Lynch's Videos" \
     --type task \
     --priority P1 \
     --component canvas-api \
     --description "Scrape transcripts from Dr. Lynch's YouTube playlists for accessibility" \
     --requirements "YouTube API integration, Transcript extraction, Accessibility formatting" \
     --acceptance-criteria "Extracts video metadata, Generates transcripts, Creates UDL summaries" \
     --educational-impact "Improves accessibility and supports multiple learning modalities" \
     --estimated-effort "6-8 hours" \
     --auto-sync
   ```

### Pattern 2: Bug Identification and Tracking

When identifying bugs during development:

```bash
python scripts/project-management/local_issue_manager.py \
  --title "BUG: Canvas API rate limiting in batch operations" \
  --type bug \
  --priority P1 \
  --component canvas-api \
  --description "Batch course creation fails due to Canvas API rate limits" \
  --acceptance-criteria "Implement rate limiting, Add retry logic, Create progress indicators" \
  --educational-impact "Ensures reliable course deployment for faculty" \
  --estimated-effort "4-6 hours" \
  --auto-sync
```

### Pattern 3: Documentation Tasks

When documentation is needed:

```bash
python scripts/project-management/local_issue_manager.py \
  --title "DOCS: Faculty Onboarding Guide for Course Customization" \
  --type documentation \
  --priority P2 \
  --component documentation \
  --description "Create comprehensive guide for faculty to customize courses" \
  --requirements "Step-by-step instructions, Screenshots, Video tutorials" \
  --acceptance-criteria "Clear instructions, Visual aids, Tested by faculty" \
  --educational-impact "Reduces barrier to adoption for non-technical faculty" \
  --estimated-effort "12-16 hours" \
  --auto-sync
```

## 🔄 Automated Workflow Management

### Quality Checks and Commits

Always use the workflow manager for commits:

```bash
# Check current status
python scripts/project-management/workflow_manager.py --status

# Run quality checks
python scripts/project-management/workflow_manager.py --check

# Commit with intelligent messaging
python scripts/project-management/workflow_manager.py --commit --push
```

### GitHub Synchronization

Sync all issues and view dashboard:

```bash
# Sync all local issues to GitHub
python scripts/project-management/github_integration.py --create-issues

# View project dashboard
python scripts/project-management/github_integration.py --dashboard

# Setup GitHub infrastructure (run once)
python scripts/project-management/github_integration.py --setup
```

## 🎓 Educational Technology Best Practices

### Accessibility and UDL Integration

Always consider in issue creation:

- **WCAG 2.1 AA Compliance**: Include accessibility requirements
- **UDL Principles**: Address multiple learning modalities
- **Faculty Workflow**: Consider instructor experience and training needs
- **Student Engagement**: Focus on motivation and engagement features

### Example Educational Impact Statements

- **Accessibility**: "Implements WCAG 2.1 AA standards ensuring equal access for all students"
- **UDL**: "Provides multiple means of representation, engagement, and expression"
- **Faculty Support**: "Reduces instructor workload while maintaining pedagogical quality"
- **Student Engagement**: "Increases motivation through gamification and progress visualization"

## 🔧 Advanced AI Agent Patterns

### Batch Issue Creation

For complex projects, create multiple related issues:

```python
# Example: Create a complete feature set
issues = [
    {
        "title": "FEATURE: Dr. Lynch MATH 231 Base Framework",
        "type": "feature",
        "priority": "P0",
        "component": "course-builder"
    },
    {
        "title": "TASK: YouTube Video Integration",
        "type": "task", 
        "priority": "P1",
        "component": "canvas-api"
    },
    {
        "title": "TASK: Multi-Major Learning Paths",
        "type": "task",
        "priority": "P1", 
        "component": "gamification"
    }
]

for issue in issues:
    # Create each issue programmatically
    subprocess.run([
        "python", "scripts/project-management/local_issue_manager.py",
        "--title", issue["title"],
        "--type", issue["type"],
        "--priority", issue["priority"],
        "--component", issue["component"],
        "--auto-sync"
    ])
```

### File Context Management

When working with agent mode, always include relevant context:

```markdown
@agent I need to create issues for Dr. Lynch's MATH 231 course customization.

Context files:
#file:.github/PROJECT_STATUS.md
#file:scripts/project-management/README.md
#folder:examples/linear_algebra/

Please analyze the Linear Algebra examples and create appropriate issues for:
1. EWU-specific branding and customization
2. YouTube video integration for flipped classroom
3. Multi-major learning paths (CS, EE, Cyber, Applied Math)
4. Accessibility improvements for diverse learners
```

## 📊 Progress Tracking and Metrics

### Status Monitoring

Regularly check project status:

```bash
# Local issue status
python scripts/project-management/local_issue_manager.py --status

# GitHub project dashboard  
python scripts/project-management/github_integration.py --dashboard

# List all local issues
python scripts/project-management/local_issue_manager.py --list
```

### Quality Assurance

Before major commits:

```bash
# Run comprehensive quality checks
python scripts/project-management/workflow_manager.py --check

# Analyze current changes
python scripts/project-management/workflow_manager.py --status
```

## 🎯 Success Criteria for AI Agents

### Autonomous Operation Goals

1. **Minimal Human Intervention**: Only require yes/no confirmations
2. **Professional Quality**: All issues are well-documented and actionable
3. **Educational Focus**: Every issue considers teaching/learning impact
4. **Workflow Compliance**: Follow established patterns and standards
5. **Accessibility Priority**: WCAG 2.1 AA and UDL compliance by default

### Quality Standards

- **Issue Titles**: Clear, descriptive, and properly tagged
- **Descriptions**: Detailed with educational context
- **Acceptance Criteria**: Specific, measurable, achievable
- **Educational Impact**: Always included and meaningful
- **Effort Estimation**: Realistic and justified

---

*This guide enables AI agents to operate autonomously while maintaining professional standards and educational technology best practices.*
