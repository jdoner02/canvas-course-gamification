# Customization Guide

## Canvas Course Gamification Framework

This guide explains how to customize the Canvas Course Gamification Framework to meet your specific course needs and institutional requirements.

## Table of Contents

1. [Configuration Overview](#configuration-overview)
2. [Course Structure Customization](#course-structure-customization)
3. [Gamification Elements](#gamification-elements)
4. [Visual Theming](#visual-theming)
5. [XP and Progression Systems](#xp-and-progression-systems)
6. [Badge Design](#badge-design)
7. [Skill Tree Customization](#skill-tree-customization)
8. [Assessment Integration](#assessment-integration)
9. [Advanced Customizations](#advanced-customizations)

## Configuration Overview

The framework uses a layered configuration system:

```
config/
├── course_settings.yml     # High-level course configuration
├── gamification.yml        # Gamification mechanics and rules
└── api_config.yml         # Canvas API settings

content/
├── modules.json           # Course structure
├── assignments.json       # Assignment definitions
├── pages.json            # Content pages
├── quizzes.json          # Quiz configurations
├── badges.json           # Achievement badges
└── outcomes.json         # Learning outcomes
```

### Configuration Hierarchy

1. **Global Settings** (`config/*.yml`) - Framework-wide settings
2. **Course Content** (`content/*.json`) - Course-specific content
3. **Environment Variables** (`.env`) - Deployment-specific overrides

## Course Structure Customization

### Module Organization

#### Linear Progression
For courses with strict sequential learning:

```json
{
  "modules": [
    {
      "id": "module_1",
      "name": "Foundations",
      "prerequisites": [],
      "gamification": {
        "skill_level": "recognition",
        "xp_required": 0
      }
    },
    {
      "id": "module_2", 
      "name": "Applications",
      "prerequisites": ["module_1"],
      "gamification": {
        "skill_level": "application",
        "xp_required": 100
      }
    }
  ]
}
```

#### Branching Paths
For courses with multiple learning tracks:

```json
{
  "modules": [
    {
      "id": "core_concepts",
      "name": "Core Concepts",
      "prerequisites": []
    },
    {
      "id": "track_a_theory",
      "name": "Theoretical Track",
      "prerequisites": ["core_concepts"],
      "gamification": {
        "unlock_requirements": {
          "quiz_score": ["core_quiz", 0.8]
        }
      }
    },
    {
      "id": "track_b_applied",
      "name": "Applied Track", 
      "prerequisites": ["core_concepts"],
      "gamification": {
        "unlock_requirements": {
          "assignment_completion": ["core_project"]
        }
      }
    }
  ]
}
```

#### Prerequisite Types

1. **Module Prerequisites**
   ```json
   "prerequisites": ["module_id_1", "module_id_2"]
   ```

2. **XP Requirements**
   ```json
   "gamification": {
     "xp_required": 500
   }
   ```

3. **Assignment-Based**
   ```json
   "unlock_requirements": {
     "assignment_completion": ["assignment_1", "assignment_2"]
   }
   ```

4. **Score-Based**
   ```json
   "unlock_requirements": {
     "quiz_score": ["quiz_id", 0.85]
   }
   ```

### Assignment Types

#### Skill Checks
Quick assessments for specific skills:

```json
{
  "id": "vectors_skill_check",
  "name": "Vector Operations Check",
  "description": "Quick assessment of vector arithmetic",
  "points_possible": 50,
  "xp_value": 15,
  "submission_types": ["online_quiz"],
  "assignment_type": "skill_check"
}
```

#### Application Tasks
Problem-solving assignments:

```json
{
  "id": "real_world_vectors",
  "name": "Vectors in Engineering",
  "description": "Apply vector concepts to engineering problems",
  "points_possible": 100,
  "xp_value": 35,
  "submission_types": ["online_upload"],
  "assignment_type": "application"
}
```

#### Mastery Assessments
Comprehensive evaluations:

```json
{
  "id": "module_mastery",
  "name": "Linear Transformations Mastery",
  "description": "Demonstrate comprehensive understanding",
  "points_possible": 200,
  "xp_value": 100,
  "submission_types": ["online_text_entry", "online_upload"],
  "assignment_type": "mastery",
  "mastery_threshold": 0.9
}
```

## Gamification Elements

### XP System Customization

#### Base XP Values
Configure in `config/gamification.yml`:

```yaml
xp_system:
  base_rewards:
    assignment_completion: 25
    quiz_completion: 15
    discussion_post: 10
    module_completion: 50
    perfect_score: 25
    
  # Custom activity types
  custom_rewards:
    peer_review: 20
    help_forum_answer: 15
    creative_submission: 35
```

#### Bonus Multipliers

```yaml
xp_system:
  bonuses:
    early_submission:
      enabled: true
      days_early: 2
      multiplier: 1.3
      
    perfectionist:
      enabled: true
      score_threshold: 1.0
      multiplier: 1.5
      
    streak_bonus:
      enabled: true
      consecutive_days: 5
      multiplier: 1.2
      max_streak: 21
      max_multiplier: 2.0
```

#### Level Thresholds

```yaml
skill_tree:
  levels:
    beginner:
      xp_threshold: 0
      color: "#e8f5e8"
      
    intermediate:
      xp_threshold: 250
      color: "#d4f1d4"
      
    advanced:
      xp_threshold: 750
      color: "#b8e9b8"
      
    expert:
      xp_threshold: 1500
      color: "#9ce09c"
```

### Badge System Customization

#### Badge Categories

Create themed badge collections:

```json
{
  "badges": [
    {
      "id": "speed_demon",
      "name": "Speed Demon",
      "description": "Complete 5 assignments early",
      "category": "efficiency",
      "criteria": "Submit 5 assignments at least 2 days before due date",
      "xp_value": 100,
      "unlock_requirements": ["early_submission_count_5"]
    },
    {
      "id": "perfectionist",
      "name": "Perfectionist", 
      "description": "Achieve perfect scores on 3 consecutive assignments",
      "category": "excellence",
      "criteria": "Score 100% on 3 assignments in a row",
      "xp_value": 150,
      "unlock_requirements": ["perfect_streak_3"]
    }
  ]
}
```

#### Custom Badge Logic

Implement custom badge awarding logic:

```python
# In custom badge handler
def check_custom_badges(student_progress, assignment_submission):
    badges_earned = []
    
    # Collaboration badge
    if student_progress.get('peer_reviews_given', 0) >= 5:
        badges_earned.append('collaboration_champion')
    
    # Innovation badge  
    if 'creative' in assignment_submission.get('tags', []):
        badges_earned.append('innovative_thinker')
        
    return badges_earned
```

## Visual Theming

### Course Pages Styling

#### Skill Tree Visualization

Customize the skill tree appearance:

```html
<!-- Skill tree CSS customization -->
<style>
.skill-tree {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border-radius: 12px;
    padding: 20px;
}

.skill-node {
    background: rgba(255, 255, 255, 0.9);
    border: 3px solid #4CAF50;
    border-radius: 50%;
    transition: all 0.3s ease;
}

.skill-node.unlocked {
    background: #4CAF50;
    color: white;
    box-shadow: 0 0 20px rgba(76, 175, 80, 0.5);
}

.skill-node.locked {
    background: #e0e0e0;
    border-color: #bdbdbd;
    color: #757575;
}
</style>
```

#### Badge Display

Custom badge showcase:

```html
<div class="badge-showcase">
    <div class="badge-grid">
        <!-- Earned badges -->
        <div class="badge earned" data-badge="first_steps">
            <img src="badge-first-steps.png" alt="First Steps">
            <h4>First Steps</h4>
            <p>Complete your first assignment</p>
        </div>
        
        <!-- Locked badges -->
        <div class="badge locked" data-badge="speed_demon">
            <div class="badge-placeholder">🔒</div>
            <h4>Speed Demon</h4>
            <p>Complete 5 assignments early</p>
        </div>
    </div>
</div>
```

### Progress Indicators

#### XP Progress Bar

```html
<div class="xp-progress">
    <div class="xp-label">
        <span>Level 3: Intermediate</span>
        <span>750 / 1500 XP</span>
    </div>
    <div class="xp-bar">
        <div class="xp-fill" style="width: 50%"></div>
    </div>
    <div class="next-level">750 XP to Advanced</div>
</div>
```

#### Module Completion

```html
<div class="module-progress">
    <div class="module-item completed">
        <span class="icon">✅</span>
        <span class="name">Introduction</span>
        <span class="xp">+50 XP</span>
    </div>
    <div class="module-item current">
        <span class="icon">🎯</span>
        <span class="name">Vector Operations</span>
        <span class="progress">60%</span>
    </div>
    <div class="module-item locked">
        <span class="icon">🔒</span>
        <span class="name">Linear Transformations</span>
        <span class="requirement">Complete Vector Operations</span>
    </div>
</div>
```

## XP and Progression Systems

### Custom XP Calculations

#### Assignment-Based XP

```python
def calculate_assignment_xp(assignment, submission, student_progress):
    base_xp = assignment.get('xp_value', 25)
    
    # Performance multiplier
    score_ratio = submission['score'] / assignment['points_possible']
    performance_multiplier = 1.0 + (score_ratio - 0.8) * 0.5  # Bonus for scores > 80%
    
    # Early submission bonus
    early_bonus = 1.0
    if submission['submitted_early']:
        early_bonus = 1.2
    
    # Difficulty multiplier
    difficulty_multiplier = assignment.get('difficulty_multiplier', 1.0)
    
    total_xp = base_xp * performance_multiplier * early_bonus * difficulty_multiplier
    return int(total_xp)
```

#### Streak Systems

```python
def calculate_streak_bonus(student_progress):
    current_streak = student_progress.get('consecutive_days', 0)
    
    if current_streak >= 7:
        return 1.5  # 50% bonus for week streak
    elif current_streak >= 3:
        return 1.25  # 25% bonus for 3-day streak
    else:
        return 1.0  # No bonus
```

### Adaptive Difficulty

#### Dynamic XP Scaling

```python
def get_adaptive_xp_multiplier(student_performance, class_average):
    if student_performance < class_average * 0.8:
        return 1.2  # Struggling students get bonus XP
    elif student_performance > class_average * 1.2:
        return 0.9  # High performers get slightly less XP
    else:
        return 1.0  # Average performers get standard XP
```

## Badge Design

### Badge Creation Workflow

1. **Design the Badge Concept**
   - Define achievement criteria
   - Determine XP value
   - Choose category and theme

2. **Create Badge Assets**
   - Design badge image (recommended: 100x100px PNG)
   - Create locked/unlocked variants
   - Prepare description text

3. **Configure Badge Data**

```json
{
  "id": "exploration_specialist",
  "name": "Exploration Specialist",
  "description": "Discover all optional content in a module",
  "criteria": "Complete all assignments and view all supplementary materials",
  "xp_value": 75,
  "image_url": "https://your-domain.com/badges/exploration.png",
  "category": "discovery",
  "unlock_requirements": ["module_completion", "optional_content_viewed"],
  "rarity": "uncommon"
}
```

### Badge Categories

#### Achievement-Based
- **Mastery**: Skill demonstrations
- **Progress**: Milestone achievements  
- **Excellence**: Outstanding performance

#### Behavior-Based
- **Engagement**: Participation and activity
- **Collaboration**: Helping others
- **Innovation**: Creative approaches

#### Time-Based
- **Consistency**: Regular participation
- **Speed**: Quick completion
- **Endurance**: Long-term commitment

### Custom Badge Logic

```python
class BadgeEngine:
    def check_badge_eligibility(self, student_id, badge_id, student_progress):
        badge = self.get_badge(badge_id)
        requirements = badge.get('unlock_requirements', [])
        
        for requirement in requirements:
            if not self.check_requirement(student_progress, requirement):
                return False
                
        return True
    
    def award_badge(self, student_id, badge_id):
        # Record badge in Canvas gradebook
        # Update student progress
        # Send notification
        # Calculate XP reward
        pass
```

## Skill Tree Customization

### Tree Structures

#### Hierarchical Tree
Traditional branching structure:

```
        Foundation
           |
      ┌────┴────┐
   Theory    Practice
      |          |
  Advanced   Applications
```

#### Network Structure
Interconnected skills with multiple paths:

```
A ─── B ─── D
│     │     │
│     C ─── E
│           │
└─────── F ──┘
```

#### Parallel Tracks
Independent learning paths:

```
Track 1: A1 → A2 → A3 → A4
Track 2: B1 → B2 → B3 → B4
Track 3: C1 → C2 → C3 → C4
```

### Custom Unlock Requirements

#### Comprehensive Example

```json
{
  "id": "advanced_applications",
  "name": "Advanced Applications",
  "unlock_requirements": {
    "modules_completed": ["theory_foundations", "basic_practice"],
    "quiz_scores": [
      {"quiz_id": "theory_quiz", "min_score": 0.85},
      {"quiz_id": "practice_quiz", "min_score": 0.80}
    ],
    "assignment_completion": ["capstone_project"],
    "xp_threshold": 1000,
    "badge_requirements": ["theory_master", "practice_champion"],
    "time_requirement": {
      "days_in_course": 30
    },
    "peer_interaction": {
      "discussion_posts": 5,
      "peer_reviews": 3
    }
  }
}
```

## Assessment Integration

### Mastery-Based Grading

#### Configuration

```yaml
# In course_settings.yml
grading:
  scheme: "mastery_based"
  mastery_threshold: 0.85
  retake_policy: "unlimited"
  grade_calculation:
    module_mastery: 70
    final_assessment: 20
    participation: 10
```

#### Implementation

```python
def calculate_mastery_grade(student_progress, course_config):
    mastery_scores = []
    
    for module in course_config['modules']:
        module_score = calculate_module_mastery(student_progress, module)
        mastery_scores.append(module_score)
    
    # Use average of all module masteries
    overall_mastery = sum(mastery_scores) / len(mastery_scores)
    
    # Convert to letter grade
    if overall_mastery >= 0.9:
        return 'A'
    elif overall_mastery >= 0.8:
        return 'B'
    # ... etc
```

### Adaptive Assessments

#### Difficulty Adjustment

```python
def get_next_question_difficulty(student_performance, current_difficulty):
    correct_percentage = student_performance.get('recent_correct_rate', 0.5)
    
    if correct_percentage > 0.8:
        return min(current_difficulty + 1, 5)  # Increase difficulty
    elif correct_percentage < 0.6:
        return max(current_difficulty - 1, 1)  # Decrease difficulty
    else:
        return current_difficulty  # Maintain difficulty
```

## Advanced Customizations

### Custom Progression Rules

#### Subject-Specific Logic

```python
class MathProgressionEngine:
    def check_algebra_readiness(self, student_progress):
        # Must master arithmetic before algebra
        arithmetic_mastery = student_progress.get('arithmetic_mastery', 0)
        return arithmetic_mastery >= 0.85
    
    def check_calculus_readiness(self, student_progress):
        # Multiple prerequisites for calculus
        prerequisites = [
            'algebra_mastery',
            'trigonometry_mastery', 
            'function_analysis_mastery'
        ]
        
        for prereq in prerequisites:
            if student_progress.get(prereq, 0) < 0.8:
                return False
        return True
```

### Integration with External Tools

#### Learning Analytics

```python
def send_progress_to_analytics(student_id, event_type, event_data):
    analytics_data = {
        'student_id': student_id,
        'timestamp': datetime.now().isoformat(),
        'event_type': event_type,
        'course_id': COURSE_ID,
        'xp_earned': event_data.get('xp', 0),
        'skill_level': event_data.get('skill_level'),
        'module_id': event_data.get('module_id')
    }
    
    # Send to analytics platform
    analytics_client.send_event(analytics_data)
```

#### Grade Passback

```python
def sync_gamification_with_gradebook():
    """Sync XP and mastery data with Canvas gradebook"""
    for student in get_enrolled_students():
        gamification_grade = calculate_gamification_contribution(student.id)
        
        # Update custom gradebook column
        update_canvas_grade(
            student.id, 
            'gamification_points', 
            gamification_grade
        )
```

### Performance Optimization

#### Caching Strategy

```python
from functools import lru_cache
from redis import Redis

# Cache expensive calculations
@lru_cache(maxsize=1000)
def calculate_student_level(student_id):
    return expensive_level_calculation(student_id)

# Use Redis for shared cache
redis_client = Redis()

def get_cached_progress(student_id):
    cache_key = f"progress:{student_id}"
    cached_data = redis_client.get(cache_key)
    
    if cached_data:
        return json.loads(cached_data)
    else:
        progress = calculate_full_progress(student_id)
        redis_client.setex(cache_key, 3600, json.dumps(progress))  # 1 hour cache
        return progress
```

### Custom Extensions

#### Plugin Architecture

```python
class GamificationPlugin:
    def __init__(self, config):
        self.config = config
    
    def on_assignment_submit(self, student_id, assignment_id, submission_data):
        """Called when student submits assignment"""
        pass
    
    def on_badge_earned(self, student_id, badge_id):
        """Called when student earns a badge"""
        pass
    
    def on_level_up(self, student_id, new_level):
        """Called when student advances to new level"""
        pass

# Example plugin
class MotivationalPlugin(GamificationPlugin):
    def on_badge_earned(self, student_id, badge_id):
        # Send encouraging message
        send_notification(student_id, f"Congratulations on earning the {badge_id} badge! 🎉")
    
    def on_level_up(self, student_id, new_level):
        # Celebrate level advancement
        create_celebration_animation(student_id, new_level)
```

## Testing Custom Configurations

### Validation Testing

```python
def test_custom_configuration():
    # Load your custom config
    config = load_course_config('my_custom_course')
    
    # Validate structure
    validator = ConfigValidator()
    results = validator.validate_course_config(config)
    
    assert results['valid'], f"Config errors: {results['errors']}"
    
    # Test gamification logic
    test_student_progress = {'total_xp': 500}
    skill_tree = SkillTree.from_config(config)
    available_nodes = skill_tree.get_available_nodes(test_student_progress)
    
    assert len(available_nodes) > 0, "No nodes available for test student"

def test_badge_logic():
    # Test custom badge criteria
    student_progress = {
        'assignments_completed': 5,
        'perfect_scores': 2,
        'early_submissions': 3
    }
    
    badge_engine = BadgeEngine()
    eligible_badges = badge_engine.get_eligible_badges(student_progress)
    
    assert 'consistency_champion' in eligible_badges
```

---

This customization guide provides a comprehensive foundation for adapting the Canvas Course Gamification Framework to your specific needs. For additional support and examples, consult the [API Reference](api_reference.md) and [Instructor Guide](instructor_guide.md).
