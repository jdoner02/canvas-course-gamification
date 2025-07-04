# Faculty Onboarding Guide - Level 2: "Copy-Paste Pro Speed Run"

## Quick Setup for Technical Faculty ⚡

This guide is for faculty comfortable with basic technical concepts who want to rapidly deploy a gamified linear algebra course with advanced customization options.

---

## Speed Run Checklist ✅

### Phase 1: Environment Setup (5 minutes)
```bash
# Clone the repository
git clone https://github.com/jdoner02/canvas-course-gamification.git
cd canvas-course-gamification

# Install dependencies
npm install
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your Canvas API credentials
```

### Phase 2: Canvas Integration (3 minutes)
```bash
# Configure Canvas API
export CANVAS_API_URL="https://yourinstitution.instructure.com"
export CANVAS_API_TOKEN="your_api_token_here"

# Test connection
python scripts/canvas_integration/test_connection.py

# Import course structure
python scripts/canvas_integration/import_course.py --course-id YOUR_COURSE_ID
```

### Phase 3: Student Roster Import (2 minutes)
```bash
# Download student CSV from Canvas
# Upload using the import script
python scripts/student_management/import_roster.py --file students.csv --course-id YOUR_COURSE_ID

# Verify import
python scripts/student_management/verify_import.py
```

### Phase 4: Content Processing (5 minutes)
```bash
# If you have YouTube content
python scripts/content_processing/youtube_processor.py --playlist-id YOUR_PLAYLIST_ID

# Process syllabus and materials
python scripts/content_processing/syllabus_parser.py --file syllabus.pdf

# Generate skill tree
python scripts/content_processing/skill_tree_generator.py --subject linear_algebra
```

### Phase 5: Launch System (1 minute)
```bash
# Build and deploy
npm run build
npm run deploy

# Launch monitoring dashboard
python scripts/monitoring/dashboard.py --port 8080

# Send student welcome emails
python scripts/communication/send_welcome.py --course-id YOUR_COURSE_ID
```

**Total Setup Time: ~16 minutes**

---

## Advanced Customization Options

### Skill Tree Modification
```yaml
# config/custom_skill_tree.yml
linear_algebra:
  vector_operations:
    vector_basics:
      xp_requirement: 100
      prerequisites: []
      specialization_bonuses:
        engineer: 1.25
        data_scientist: 1.0
    vector_arithmetic:
      xp_requirement: 150
      prerequisites: ["vector_basics"]
      unlock_abilities: ["vector_boost"]
```

### Pet System Configuration
```yaml
# config/pet_settings.yml
companion_system:
  adoption_cost: 100
  evolution_requirements:
    hatchling:
      days: 7
      care_average: 60
      learning_consistency: 0.3
  species_abilities:
    vector_sprite:
      evolution_bonus: "vector_operations"
      special_ability: "dimensional_insight"
```

### Gamification Parameters
```yaml
# config/gamification.yml
experience_system:
  homework_completion: 50
  quiz_perfect_score: 100
  class_participation: 25
  peer_helping: 75
  daily_login: 10
  
difficulty_scaling:
  engineer_track:
    computational_focus: 1.2
    application_emphasis: 1.5
  pure_math_track:
    proof_focus: 1.4
    abstraction_level: 1.3
```

---

## AI Agent Prompts for Rapid Customization

### Content Generation
```
"Generate 20 vector addition problems with increasing difficulty for engineering students, focusing on real-world applications like force vectors and displacement. Include both 2D and 3D examples with visual representations."
```

### Quest Line Creation
```
"Create a 5-part quest series introducing eigenvalues and eigenvectors. Each quest should build on the previous, include both computational and conceptual elements, and culminate in a collaborative 'boss battle' problem requiring team coordination."
```

### Assessment Design
```
"Design an adaptive assessment for matrix operations that adjusts difficulty based on student performance. Include immediate feedback, partial credit for method, and personalized hint systems based on common error patterns."
```

### Analytics Dashboard Customization
```
"Create a custom analytics view showing correlation between pet care consistency and homework completion rates. Include predictive indicators for students at risk of disengagement."
```

---

## API Integration Examples

### Student Progress Tracking
```python
from gamification_engine import PlayerProfileManager

# Initialize system
manager = PlayerProfileManager()

# Award XP for custom activity
result = manager.award_xp(
    student_id="student_123",
    skill_id="matrix_operations", 
    xp_amount=150,
    source="custom_lab_exercise"
)

# Check for level ups and achievements
if result['levels_gained'] > 0:
    send_celebration_notification(student_id, result)
```

### Pet System Integration
```python
from gamification_engine.pets import PetCompanionSystem

pet_system = PetCompanionSystem()

# Update learning consistency from Canvas analytics
consistency_score = calculate_weekly_consistency(student_id)
evolution_result = pet_system.update_learning_consistency(
    student_id, consistency_score
)

if evolution_result:
    send_evolution_notification(student_id, evolution_result)
```

### Custom Event Creation
```python
from gamification_engine.events import EventManager

event_manager = EventManager()

# Create weekly challenge
challenge = event_manager.create_challenge(
    name="Matrix Determinant Speed Run",
    description="Calculate determinants as fast as possible",
    duration_hours=168,  # One week
    difficulty="medium",
    rewards={"xp": 200, "rare_pet_food": 5}
)
```

---

## Advanced Analytics Integration

### Custom Metrics Dashboard
```python
# scripts/analytics/custom_dashboard.py
from analytics_engine import LearningAnalytics

analytics = LearningAnalytics()

# Student engagement patterns
engagement_data = analytics.get_engagement_patterns(
    course_id="MATH231",
    time_range="last_30_days",
    group_by="specialization"
)

# Predictive modeling
at_risk_students = analytics.predict_at_risk_students(
    model="gradient_boosting",
    features=["login_frequency", "homework_completion", "pet_care"],
    threshold=0.7
)

# Social network analysis
collaboration_networks = analytics.analyze_study_groups(
    course_id="MATH231",
    include_peer_tutoring=True
)
```

### Research Data Export
```python
# Export data for educational research
research_data = analytics.export_research_dataset(
    course_id="MATH231",
    anonymize=True,
    include_temporal_data=True,
    format="csv"
)

# Generate automated research reports
report = analytics.generate_research_report(
    template="educational_effectiveness",
    comparison_baseline="traditional_course_data.csv"
)
```

---

## Deployment Configurations

### Production Environment
```yaml
# docker-compose.production.yml
version: '3.8'
services:
  gamification_engine:
    image: mathgamification/engine:latest
    environment:
      - NODE_ENV=production
      - CANVAS_API_URL=${CANVAS_API_URL}
      - DATABASE_URL=${DATABASE_URL}
    ports:
      - "80:8080"
  
  analytics_service:
    image: mathgamification/analytics:latest
    environment:
      - REDIS_URL=${REDIS_URL}
      - MONGODB_URL=${MONGODB_URL}
    ports:
      - "8081:8080"
```

### Kubernetes Deployment
```yaml
# k8s/gamification-deployment.yml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: gamification-engine
spec:
  replicas: 3
  selector:
    matchLabels:
      app: gamification-engine
  template:
    metadata:
      labels:
        app: gamification-engine
    spec:
      containers:
      - name: engine
        image: mathgamification/engine:latest
        ports:
        - containerPort: 8080
        env:
        - name: CANVAS_API_URL
          valueFrom:
            secretKeyRef:
              name: canvas-credentials
              key: api-url
```

---

## Automated Workflow Scripts

### Daily Maintenance
```bash
#!/bin/bash
# scripts/maintenance/daily_tasks.sh

# Update pet status for all students
python scripts/pets/daily_update.py

# Generate engagement reports
python scripts/analytics/daily_report.py --email-faculty

# Process new YouTube content
python scripts/content/auto_process_new_videos.py

# Clean up old temporary files
python scripts/maintenance/cleanup.py --days 7
```

### Weekly Analytics
```bash
#!/bin/bash
# scripts/analytics/weekly_report.sh

# Generate comprehensive learning analytics
python scripts/analytics/weekly_deep_dive.py --course-id ALL

# Update predictive models
python scripts/ml/retrain_models.py --model engagement_prediction

# Send faculty dashboard updates
python scripts/communication/faculty_weekly_update.py
```

---

## Integration with External Tools

### Learning Management Systems
```python
# integrations/lms_connector.py
class CanvasConnector:
    def sync_grades(self, course_id):
        # Sync gamification points to Canvas gradebook
        students = self.get_enrolled_students(course_id)
        for student in students:
            xp_points = self.gamification.get_total_xp(student.id)
            canvas_grade = self.convert_xp_to_grade(xp_points)
            self.canvas_api.update_grade(student.id, canvas_grade)
    
    def import_assignments(self, course_id):
        # Convert Canvas assignments to gamification quests
        assignments = self.canvas_api.get_assignments(course_id)
        for assignment in assignments:
            quest = self.create_quest_from_assignment(assignment)
            self.gamification.add_quest(quest)
```

### Student Information Systems
```python
# integrations/sis_connector.py
class SISConnector:
    def sync_student_data(self):
        # Import student majors for specialization assignment
        students = self.sis_api.get_student_data()
        for student in students:
            specialization = self.map_major_to_specialization(student.major)
            self.gamification.set_student_specialization(
                student.id, specialization
            )
```

---

## Troubleshooting Quick Fixes

### Common Issues and Solutions

#### API Connection Problems
```bash
# Test Canvas API connectivity
curl -H "Authorization: Bearer $CANVAS_API_TOKEN" \
     "$CANVAS_API_URL/api/v1/courses"

# Reset API credentials
python scripts/setup/reset_api_credentials.py
```

#### Database Sync Issues
```bash
# Reset student progress (use carefully!)
python scripts/database/reset_student_progress.py --student-id STUDENT_ID

# Backup and restore
python scripts/database/backup.py --output backup_$(date +%Y%m%d).sql
python scripts/database/restore.py --input backup_file.sql
```

#### Performance Optimization
```bash
# Enable Redis caching
redis-server --daemonize yes
python scripts/optimization/enable_caching.py

# Database indexing
python scripts/database/optimize_indexes.py

# Asset compression
npm run optimize-assets
```

---

## Monitoring and Alerts

### System Health Monitoring
```yaml
# monitoring/alerts.yml
alerts:
  low_engagement:
    condition: "daily_active_users < 70%"
    action: "email_faculty_intervention_needed"
  
  api_errors:
    condition: "error_rate > 5%"
    action: "page_technical_team"
  
  pet_abandonment:
    condition: "pet_happiness < 30% for 3_days"
    action: "send_care_reminder"
```

### Performance Metrics
```python
# monitoring/metrics.py
from prometheus_client import Counter, Histogram, Gauge

# Track key metrics
student_logins = Counter('student_logins_total', 'Total student logins')
quest_completions = Counter('quest_completions_total', 'Completed quests')
response_time = Histogram('response_time_seconds', 'Response time')
active_students = Gauge('active_students', 'Currently active students')
```

---

## Getting Advanced Support

### Technical Support Channels
- **GitHub Issues:** Bug reports and feature requests
- **Slack Channel:** Real-time technical discussion
- **Video Consultations:** Complex integration support
- **Code Review:** Custom modification assistance

### Advanced Training Resources
- **API Documentation:** Complete reference with examples
- **Architecture Deep Dive:** System design and scalability
- **Research Integration:** Academic study design support
- **Custom Development:** Institutional-specific modifications

### Community Contributions
- **Plugin Development:** Extend system functionality
- **Content Sharing:** Exchange quests and activities
- **Research Collaboration:** Multi-institutional studies
- **Open Source Contributions:** Core system improvements

---

## Contact Information for Technical Faculty

- **Technical Documentation:** docs@mathgamification.edu
- **API Support:** api@mathgamification.edu  
- **DevOps Assistance:** devops@mathgamification.edu
- **Research Collaboration:** research@mathgamification.edu
- **Emergency Technical Support:** +1-555-MATH-911

**Ready to dive deeper?** Check out the PhD-level developer documentation for advanced customization and research integration options.
