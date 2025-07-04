# Instructor Guide

## Canvas Course Gamification Framework

### Table of Contents
1. [Quick Start](#quick-start)
2. [Course Configuration](#course-configuration)
3. [Gamification Elements](#gamification-elements)
4. [Deployment](#deployment)
5. [Management and Maintenance](#management-and-maintenance)
6. [Troubleshooting](#troubleshooting)

## Quick Start

### Prerequisites
- Canvas LMS account with administrator or instructor privileges
- Canvas API token with course management permissions
- Python 3.8+ installed on your system
- Git for version control

### 5-Minute Setup

1. **Clone and Install**
   ```bash
   git clone https://github.com/yourusername/canvas-course-gamification.git
   cd canvas-course-gamification
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Configure Environment**
   ```bash
   cp .env.example .env
   # Edit .env with your Canvas credentials
   ```

3. **Deploy Example Course**
   ```bash
   python deploy.py --config examples/linear_algebra
   ```

## Course Configuration

### Configuration Structure

The framework uses JSON files to define course content:

```
config/
├── course_settings.yml    # Course metadata and settings
├── gamification.yml       # Gamification rules and mechanics
└── api_config.yml        # Canvas API configuration

content/
├── modules.json          # Course modules and structure
├── assignments.json      # Assignment definitions
├── pages.json           # Course pages and content
├── quizzes.json         # Quiz configurations
├── badges.json          # Achievement badge definitions
└── outcomes.json        # Learning outcomes
```

### Basic Course Setup

1. **Define Course Metadata** (`config/course_settings.yml`)
   ```yaml
   course:
     name: "Your Course Name"
     course_code: "COURSE101"
     description: "Course description with gamification elements"
     
   gamification_settings:
     enabled: true
     xp_system: true
     badge_system: true
     skill_tree_enabled: true
   ```

2. **Create Module Structure** (`content/modules.json`)
   ```json
   {
     "modules": [
       {
         "id": "module_1",
         "name": "Introduction",
         "description": "Course introduction and basics",
         "position": 1,
         "gamification": {
           "skill_level": "recognition",
           "xp_required": 0,
           "unlock_requirements": {}
         },
         "items": [
           {
             "type": "Page",
             "id": "welcome_page",
             "title": "Welcome"
           }
         ]
       }
     ]
   }
   ```

3. **Define Assignments** (`content/assignments.json`)
   ```json
   {
     "assignments": [
       {
         "id": "assignment_1",
         "name": "Getting Started",
         "description": "Introduction assignment",
         "points_possible": 100,
         "xp_value": 25,
         "skill_level": "recognition",
         "badges": ["first_steps"]
       }
     ]
   }
   ```

## Gamification Elements

### XP (Experience Points) System

**Configuration:**
- Base XP values for different activities
- Bonus multipliers for early submission, perfect scores
- Progress tracking and level advancement

**Implementation:**
```yaml
# In config/gamification.yml
xp_system:
  base_rewards:
    assignment_completion: 25
    quiz_completion: 15
    perfect_score: 25
  
  bonuses:
    early_submission:
      multiplier: 1.2
    perfect_score:
      multiplier: 1.5
```

### Badge System

**Badge Categories:**
- **Mastery**: Skill-specific achievements
- **Engagement**: Participation and consistency
- **Achievement**: Special accomplishments
- **Collaboration**: Teamwork and helping others

**Badge Configuration:**
```json
{
  "badges": [
    {
      "id": "first_steps",
      "name": "First Steps",
      "description": "Complete your first assignment",
      "criteria": "Submit any assignment",
      "xp_value": 50,
      "category": "engagement",
      "unlock_requirements": ["assignment_completion"]
    }
  ]
}
```

### Skill Tree System

**Skill Levels:**
1. **Recognition** - "I know what this is"
2. **Application** - "I can use this"
3. **Intuition** - "I understand why"
4. **Synthesis** - "I can connect and innovate"
5. **Mastery** - "I can teach this"

**Prerequisites and Progression:**
- Sequential module unlocking
- XP thresholds for advancement
- Mastery requirements for progression

## Deployment

### Pre-Deployment Checklist

1. **Environment Setup**
   - [ ] Canvas API credentials configured
   - [ ] Course ID specified
   - [ ] Virtual environment activated
   - [ ] Dependencies installed

2. **Content Validation**
   - [ ] All JSON files are valid
   - [ ] Module prerequisites are correctly defined
   - [ ] Assignment XP values are set
   - [ ] Badge criteria are clear

3. **API Access**
   - [ ] Canvas API connection tested
   - [ ] Course access verified
   - [ ] Permissions confirmed

### Deployment Methods

#### 1. Command Line Deployment
```bash
# Deploy entire course
python deploy.py

# Deploy specific components
python deploy.py --modules-only
python deploy.py --assignments-only

# Dry run (test without making changes)
python deploy.py --dry-run

# Verbose output
python deploy.py --verbose
```

#### 2. Programmatic Deployment
```python
from src.canvas_api import CanvasAPIClient
from src.course_builder import CourseBuilder
from src.validators import validate_course_deployment

# Initialize
client = CanvasAPIClient()
builder = CourseBuilder(client)

# Load and validate configuration
config = builder.load_course_config("path/to/config")
validation_results = validate_course_deployment("path/to/config", client)

if validation_results["ready_for_deployment"]:
    # Deploy course
    results = builder.deploy_course(config)
    print(f"Deployment completed: {results}")
```

#### 3. Interactive Deployment
Use the provided Jupyter notebook for step-by-step deployment with validation checks and preview capabilities.

### Post-Deployment Verification

1. **Course Structure**
   - [ ] All modules created and properly ordered
   - [ ] Module prerequisites working correctly
   - [ ] Content items linked properly

2. **Gamification Elements**
   - [ ] XP values displaying correctly
   - [ ] Badge criteria functioning
   - [ ] Skill tree visualization working

3. **Student Experience**
   - [ ] Test with a student account
   - [ ] Verify progression mechanics
   - [ ] Check mobile responsiveness

## Management and Maintenance

### Content Updates

1. **Modify Configuration Files**
   - Update JSON files for content changes
   - Adjust XP values and badge criteria
   - Modify skill tree progression

2. **Re-deploy Changes**
   ```bash
   # Deploy only updated components
   python deploy.py --update-only
   ```

3. **Version Control**
   - Commit changes to Git
   - Tag releases for course versions
   - Maintain deployment history

### Student Progress Monitoring

1. **Analytics Dashboard**
   - Track XP accumulation
   - Monitor badge achievements
   - Analyze skill tree progression

2. **Intervention Points**
   - Identify struggling students
   - Provide additional support
   - Adjust difficulty as needed

### Course Iterations

1. **Semester Updates**
   - Refine XP values based on student performance
   - Add new badges for emerging patterns
   - Update content based on feedback

2. **Major Revisions**
   - Restructure skill tree if needed
   - Add new gamification elements
   - Integrate with new Canvas features

## Troubleshooting

### Common Issues

#### 1. API Connection Problems
**Symptoms:** Connection timeouts, authentication errors
**Solutions:**
- Verify Canvas API URL and token
- Check network connectivity
- Confirm API permissions

#### 2. Deployment Failures
**Symptoms:** Partial deployments, error messages
**Solutions:**
- Run validation before deployment
- Check Canvas course permissions
- Review error logs for specific issues

#### 3. Gamification Not Working
**Symptoms:** XP not displaying, badges not awarding
**Solutions:**
- Verify gamification is enabled in configuration
- Check Canvas custom field settings
- Ensure proper module structure

#### 4. Module Prerequisites Not Working
**Symptoms:** Students can access locked content
**Solutions:**
- Verify prerequisite IDs match module IDs
- Check Canvas module settings
- Confirm requirement types are supported

### Getting Help

1. **Documentation**
   - Read the full API reference
   - Check configuration examples
   - Review troubleshooting guides

2. **Community Support**
   - GitHub Issues for bug reports
   - Discussions for questions and ideas
   - Wiki for additional documentation

3. **Professional Support**
   - Contact for custom implementations
   - Training workshops available
   - Consulting for large deployments

## Best Practices

### Course Design
- Start with simple gamification elements
- Gradually increase complexity
- Provide clear progression paths
- Balance challenge and achievability

### XP and Badge Design
- Make rewards meaningful and motivating
- Avoid grade inflation through XP
- Create diverse achievement opportunities
- Celebrate different types of success

### Student Communication
- Explain the gamification system clearly
- Provide orientation materials
- Create help resources
- Gather regular feedback

### Technical Maintenance
- Regular backups of configuration
- Monitor API rate limits
- Keep dependencies updated
- Test changes in development environment

---

*For additional support and resources, visit the [project documentation](https://github.com/yourusername/canvas-course-gamification/wiki)*
