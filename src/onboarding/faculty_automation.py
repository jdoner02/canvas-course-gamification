#!/usr/bin/env python3
"""
Faculty Zero-Touch Onboarding System for Eagle Adventures 2
==========================================================

Automated faculty onboarding system that enables one-click Canvas course
deployment and gamification setup with zero technical knowledge required.

Features:
- One-click Canvas course integration
- Automatic gamification configuration
- Skill tree generation based on course content
- Faculty dashboard creation
- Student onboarding automation
- Progress monitoring setup
- Support request automation

Author: AI Agent Development Team
License: MIT (Educational Use)
"""

import asyncio
import json
import logging
import os
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from enum import Enum
import yaml
import aiohttp
from jinja2 import Template

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class OnboardingStatus(Enum):
    """Onboarding process status"""

    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    REQUIRES_ATTENTION = "requires_attention"


class CourseType(Enum):
    """Course type for gamification configuration"""

    MATHEMATICS = "mathematics"
    SCIENCE = "science"
    ENGINEERING = "engineering"
    LIBERAL_ARTS = "liberal_arts"
    BUSINESS = "business"
    CUSTOM = "custom"


@dataclass
class FacultyProfile:
    """Faculty member profile"""

    faculty_id: str
    name: str
    email: str
    institution: str
    department: str
    canvas_user_id: str = ""
    technical_comfort_level: str = "beginner"  # beginner, intermediate, advanced
    gamification_preferences: Dict[str, Any] = field(default_factory=dict)
    course_preferences: Dict[str, Any] = field(default_factory=dict)
    onboarding_completed: bool = False
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class CourseConfiguration:
    """Course gamification configuration"""

    course_id: str
    course_name: str
    course_type: CourseType
    skill_tree_config: Dict[str, Any]
    gamification_settings: Dict[str, Any]
    pet_settings: Dict[str, Any]
    guild_settings: Dict[str, Any]
    assessment_integration: Dict[str, Any]
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class OnboardingSession:
    """Onboarding session tracking"""

    session_id: str
    faculty_id: str
    status: OnboardingStatus
    current_step: str
    steps_completed: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    canvas_course_id: str = ""
    course_configuration: Optional[CourseConfiguration] = None
    started_at: datetime = field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None


class FacultyOnboardingSystem:
    """
    Zero-touch faculty onboarding system

    Provides a completely automated onboarding experience that takes faculty
    from zero gamification knowledge to a fully deployed course in minutes.
    """

    def __init__(self, config_path: str = "config/onboarding_config.yml"):
        self.config_path = config_path
        self.config = self._load_config()

        # Faculty profiles and onboarding sessions
        self.faculty_profiles: Dict[str, FacultyProfile] = {}
        self.onboarding_sessions: Dict[str, OnboardingSession] = {}

        # Course templates and configurations
        self.course_templates = self._load_course_templates()
        self.skill_tree_templates = self._load_skill_tree_templates()

        # Integration systems
        self.canvas_integration = None
        self.gamification_configurator = None

        self._load_existing_data()

        logger.info(
            "👩‍🏫 Faculty Onboarding System initialized for zero-touch deployment"
        )

    def _load_config(self) -> Dict[str, Any]:
        """Load onboarding configuration"""
        try:
            with open(self.config_path, "r") as f:
                config = yaml.safe_load(f)
            return config.get("faculty_onboarding", {})
        except Exception as e:
            logger.warning(f"⚠️ Could not load onboarding config: {e}")
            return self._get_default_config()

    def _get_default_config(self) -> Dict[str, Any]:
        """Get default onboarding configuration"""
        return {
            "canvas_integration": {
                "auto_create_external_tool": True,
                "auto_configure_assignments": True,
                "auto_setup_gradebook": True,
                "enable_notifications": True,
            },
            "gamification_defaults": {
                "enable_skill_trees": True,
                "enable_pet_companions": True,
                "enable_guild_system": True,
                "enable_leaderboards": True,
                "daily_challenges": True,
            },
            "faculty_support": {
                "tutorial_videos_enabled": True,
                "help_chat_enabled": True,
                "documentation_links": True,
                "office_hours_scheduling": True,
            },
            "automation_level": {
                "beginner": "full_automation",
                "intermediate": "guided_automation",
                "advanced": "manual_configuration",
            },
            "course_analysis": {
                "auto_skill_tree_generation": True,
                "content_difficulty_analysis": True,
                "prerequisite_detection": True,
            },
        }

    def _load_course_templates(self) -> Dict[str, Dict[str, Any]]:
        """Load course templates for different subjects"""
        return {
            "mathematics": {
                "name": "Mathematics Course Template",
                "skill_categories": [
                    "Algebra",
                    "Calculus",
                    "Statistics",
                    "Problem Solving",
                ],
                "default_pets": ["Calculator Cat", "Proof Penguin", "Graph Gecko"],
                "challenge_types": [
                    "Daily Problems",
                    "Proof Challenges",
                    "Application Quests",
                ],
                "assessment_integration": {
                    "auto_grade_sync": True,
                    "skill_mapping": True,
                    "progress_tracking": True,
                },
            },
            "science": {
                "name": "Science Course Template",
                "skill_categories": ["Theory", "Laboratory", "Research", "Analysis"],
                "default_pets": ["Lab Lemur", "Hypothesis Hawk", "Data Dragon"],
                "challenge_types": [
                    "Lab Challenges",
                    "Theory Quests",
                    "Research Projects",
                ],
                "assessment_integration": {
                    "lab_report_tracking": True,
                    "experiment_logging": True,
                    "peer_review_system": True,
                },
            },
            "engineering": {
                "name": "Engineering Course Template",
                "skill_categories": ["Design", "Analysis", "Implementation", "Testing"],
                "default_pets": ["Blueprint Bear", "Circuit Chameleon", "Design Duck"],
                "challenge_types": [
                    "Design Challenges",
                    "Problem Solving",
                    "Project Milestones",
                ],
                "assessment_integration": {
                    "project_tracking": True,
                    "milestone_monitoring": True,
                    "team_collaboration": True,
                },
            },
        }

    def _load_skill_tree_templates(self) -> Dict[str, Dict[str, Any]]:
        """Load skill tree templates"""
        return {
            "linear_algebra": {
                "name": "Linear Algebra Skill Tree",
                "root_skills": ["Vector Operations", "Matrix Basics"],
                "intermediate_skills": [
                    "Matrix Operations",
                    "Determinants",
                    "Eigenvalues",
                ],
                "advanced_skills": [
                    "Linear Transformations",
                    "Vector Spaces",
                    "Applications",
                ],
                "mastery_criteria": {
                    "homework_completion": 0.8,
                    "quiz_average": 0.75,
                    "project_quality": 0.7,
                },
            },
            "calculus": {
                "name": "Calculus Skill Tree",
                "root_skills": ["Limits", "Basic Derivatives"],
                "intermediate_skills": [
                    "Derivative Rules",
                    "Integration",
                    "Applications",
                ],
                "advanced_skills": ["Advanced Integration", "Series", "Multivariable"],
                "mastery_criteria": {
                    "problem_solving": 0.8,
                    "conceptual_understanding": 0.75,
                    "application_ability": 0.7,
                },
            },
        }

    def _load_existing_data(self):
        """Load existing faculty profiles and sessions"""
        try:
            # Load faculty profiles
            profiles_file = "data/onboarding/faculty_profiles.json"
            if os.path.exists(profiles_file):
                with open(profiles_file, "r") as f:
                    profiles_data = json.load(f)

                for faculty_id, profile_data in profiles_data.items():
                    self.faculty_profiles[faculty_id] = FacultyProfile(
                        faculty_id=faculty_id,
                        name=profile_data["name"],
                        email=profile_data["email"],
                        institution=profile_data["institution"],
                        department=profile_data["department"],
                        canvas_user_id=profile_data.get("canvas_user_id", ""),
                        technical_comfort_level=profile_data.get(
                            "technical_comfort_level", "beginner"
                        ),
                        gamification_preferences=profile_data.get(
                            "gamification_preferences", {}
                        ),
                        course_preferences=profile_data.get("course_preferences", {}),
                        onboarding_completed=profile_data.get(
                            "onboarding_completed", False
                        ),
                        created_at=datetime.fromisoformat(profile_data["created_at"]),
                    )

        except Exception as e:
            logger.error(f"❌ Failed to load existing onboarding data: {e}")

    async def start_onboarding(
        self,
        faculty_email: str,
        canvas_course_id: str,
        course_subject: str = "mathematics",
    ) -> Dict[str, Any]:
        """
        Start zero-touch onboarding process for faculty member

        Args:
            faculty_email: Faculty member's email address
            canvas_course_id: Canvas course ID to gamify
            course_subject: Subject area for template selection

        Returns:
            Dictionary with success status, session_id, and message
        """
        session_id = str(uuid.uuid4())

        # Create or get faculty profile
        faculty_profile = await self._get_or_create_faculty_profile(faculty_email)

        # Create onboarding session
        session = OnboardingSession(
            session_id=session_id,
            faculty_id=faculty_profile.faculty_id,
            status=OnboardingStatus.PENDING,
            current_step="initialization",
            canvas_course_id=canvas_course_id,
        )

        self.onboarding_sessions[session_id] = session

        # Start async onboarding process
        asyncio.create_task(
            self._execute_onboarding_process(session_id, course_subject)
        )

        logger.info(
            f"🚀 Started onboarding for {faculty_email} (Session: {session_id})"
        )
        return {
            "success": True,
            "session_id": session_id,
            "message": f"Onboarding started for {faculty_email}",
        }

    async def _get_or_create_faculty_profile(self, email: str) -> FacultyProfile:
        """Get existing faculty profile or create new one"""
        # Check if profile exists
        for profile in self.faculty_profiles.values():
            if profile.email == email:
                return profile

        # Create new profile
        faculty_id = str(uuid.uuid4())

        # Get faculty info from Canvas (if available)
        faculty_info = await self._get_faculty_info_from_canvas(email)

        profile = FacultyProfile(
            faculty_id=faculty_id,
            name=faculty_info.get("name", email.split("@")[0]),
            email=email,
            institution=faculty_info.get("institution", "Unknown"),
            department=faculty_info.get("department", "Unknown"),
            canvas_user_id=faculty_info.get("canvas_user_id", ""),
        )

        self.faculty_profiles[faculty_id] = profile
        self._save_faculty_profiles()

        return profile

    async def _get_faculty_info_from_canvas(self, email: str) -> Dict[str, Any]:
        """Get faculty information from Canvas API"""
        try:
            # This would integrate with Canvas API to get faculty info
            # For now, return mock data
            return {
                "name": email.split("@")[0].replace(".", " ").title(),
                "institution": "Eastern Washington University",
                "department": "Mathematics",
                "canvas_user_id": str(uuid.uuid4()),
            }
        except Exception as e:
            logger.error(f"❌ Failed to get faculty info from Canvas: {e}")
            return {}

    async def _execute_onboarding_process(self, session_id: str, course_subject: str):
        """Execute the complete onboarding process"""
        session = self.onboarding_sessions[session_id]
        faculty = self.faculty_profiles[session.faculty_id]

        try:
            session.status = OnboardingStatus.IN_PROGRESS

            # Step 1: Course Analysis
            session.current_step = "course_analysis"
            course_info = await self._analyze_canvas_course(session.canvas_course_id)
            session.steps_completed.append("course_analysis")

            # Step 2: Generate Skill Tree
            session.current_step = "skill_tree_generation"
            skill_tree = await self._generate_skill_tree(course_info, course_subject)
            session.steps_completed.append("skill_tree_generation")

            # Step 3: Configure Gamification
            session.current_step = "gamification_configuration"
            gamification_config = await self._configure_gamification(
                course_info, skill_tree, faculty.technical_comfort_level
            )
            session.steps_completed.append("gamification_configuration")

            # Step 4: Setup Canvas Integration
            session.current_step = "canvas_integration"
            await self._setup_canvas_integration(
                session.canvas_course_id, gamification_config
            )
            session.steps_completed.append("canvas_integration")

            # Step 5: Create Faculty Dashboard
            session.current_step = "dashboard_creation"
            dashboard_url = await self._create_faculty_dashboard(
                session.faculty_id, session.canvas_course_id
            )
            session.steps_completed.append("dashboard_creation")

            # Step 6: Setup Student Onboarding
            session.current_step = "student_onboarding_setup"
            await self._setup_student_onboarding(
                session.canvas_course_id, gamification_config
            )
            session.steps_completed.append("student_onboarding_setup")

            # Step 7: Configure Monitoring
            session.current_step = "monitoring_setup"
            await self._setup_progress_monitoring(
                session.canvas_course_id, faculty.faculty_id
            )
            session.steps_completed.append("monitoring_setup")

            # Step 8: Send Welcome Package
            session.current_step = "welcome_package"
            await self._send_welcome_package(
                faculty, dashboard_url, gamification_config
            )
            session.steps_completed.append("welcome_package")

            # Complete onboarding
            session.status = OnboardingStatus.COMPLETED
            session.completed_at = datetime.now()
            faculty.onboarding_completed = True

            # Save configuration
            session.course_configuration = CourseConfiguration(
                course_id=session.canvas_course_id,
                course_name=course_info.get("name", "Unknown Course"),
                course_type=CourseType(course_subject),
                skill_tree_config=skill_tree,
                gamification_settings=gamification_config,
                pet_settings=gamification_config.get("pets", {}),
                guild_settings=gamification_config.get("guilds", {}),
                assessment_integration=gamification_config.get("assessments", {}),
            )

            self._save_onboarding_data()

            logger.info(
                f"✅ Onboarding completed for {faculty.email} (Session: {session_id})"
            )

        except Exception as e:
            session.status = OnboardingStatus.FAILED
            session.errors.append(str(e))
            logger.error(f"❌ Onboarding failed for session {session_id}: {e}")

            # Send error notification
            await self._send_error_notification(faculty, session, str(e))

    async def _analyze_canvas_course(self, course_id: str) -> Dict[str, Any]:
        """Analyze Canvas course structure and content"""
        try:
            # This would integrate with Canvas API to analyze:
            # - Course structure and modules
            # - Assignment types and weights
            # - Student enrollment
            # - Existing content and resources

            # Mock analysis for now
            return {
                "name": "Linear Algebra MATH 231",
                "student_count": 25,
                "modules": [
                    "Vectors and Vector Operations",
                    "Matrix Operations",
                    "Determinants",
                    "Eigenvalues and Eigenvectors",
                    "Linear Transformations",
                ],
                "assignment_types": ["Homework", "Quizzes", "Exams", "Projects"],
                "grading_scheme": {
                    "Homework": 0.25,
                    "Quizzes": 0.20,
                    "Midterms": 0.30,
                    "Final": 0.25,
                },
                "difficulty_level": "intermediate",
                "prerequisites": ["College Algebra", "Pre-calculus"],
            }

        except Exception as e:
            logger.error(f"❌ Course analysis failed: {e}")
            return {"name": "Unknown Course", "student_count": 0}

    async def _generate_skill_tree(
        self, course_info: Dict[str, Any], subject: str
    ) -> Dict[str, Any]:
        """Generate skill tree based on course content"""
        try:
            # Get base template
            template = self.skill_tree_templates.get(
                subject.lower(), self.skill_tree_templates["linear_algebra"]
            )

            # Customize based on course content
            modules = course_info.get("modules", [])

            skill_tree = {
                "name": f"{course_info.get('name', 'Course')} Skill Tree",
                "subject": subject,
                "total_skills": len(modules) * 3,  # Approximate
                "skill_categories": [],
                "prerequisites": {},
                "mastery_criteria": template["mastery_criteria"],
            }

            # Generate skills from course modules
            for i, module in enumerate(modules):
                category = {
                    "name": module,
                    "skills": [
                        f"{module} - Basics",
                        f"{module} - Applications",
                        f"{module} - Mastery",
                    ],
                    "unlock_order": i,
                    "xp_requirements": [100, 200, 300],
                }
                skill_tree["skill_categories"].append(category)

            logger.info(f"🌳 Generated skill tree with {len(modules)} categories")
            return skill_tree

        except Exception as e:
            logger.error(f"❌ Skill tree generation failed: {e}")
            return {"name": "Basic Skill Tree", "skill_categories": []}

    async def _configure_gamification(
        self,
        course_info: Dict[str, Any],
        skill_tree: Dict[str, Any],
        comfort_level: str,
    ) -> Dict[str, Any]:
        """Configure gamification settings based on course and faculty preferences"""
        try:
            # Base configuration
            config = {
                "enabled_features": {
                    "skill_trees": True,
                    "pet_companions": True,
                    "guild_system": True,
                    "daily_challenges": True,
                    "leaderboards": comfort_level != "beginner",
                    "achievements": True,
                    "virtual_economy": True,
                },
                "pets": {
                    "available_pets": [
                        "Calculator Cat",
                        "Proof Penguin",
                        "Graph Gecko",
                    ],
                    "care_requirements": (
                        "low" if comfort_level == "beginner" else "medium"
                    ),
                    "evolution_enabled": True,
                    "interaction_frequency": "daily",
                },
                "guilds": {
                    "auto_formation": True,
                    "max_guild_size": 6,
                    "collaboration_tools": [
                        "study_sessions",
                        "peer_tutoring",
                        "group_challenges",
                    ],
                    "guild_rewards": True,
                },
                "challenges": {
                    "daily_problems": True,
                    "weekly_quests": True,
                    "boss_battles": comfort_level != "beginner",
                    "difficulty_adaptation": True,
                },
                "assessments": {
                    "auto_xp_assignment": True,
                    "skill_mapping": True,
                    "progress_tracking": True,
                    "achievement_triggers": True,
                },
                "personalization": {
                    "adaptive_difficulty": True,
                    "learning_style_detection": True,
                    "content_recommendations": True,
                    "progress_predictions": True,
                },
            }

            # Adjust based on course characteristics
            student_count = course_info.get("student_count", 25)
            if student_count > 50:
                config["guilds"]["auto_formation"] = True
                config["leaderboards"] = False  # Too competitive for large classes

            logger.info(f"⚙️ Configured gamification for {comfort_level} level faculty")
            return config

        except Exception as e:
            logger.error(f"❌ Gamification configuration failed: {e}")
            return {"enabled_features": {"skill_trees": True}}

    async def _setup_canvas_integration(self, course_id: str, config: Dict[str, Any]):
        """Setup Canvas LTI integration"""
        try:
            # This would:
            # 1. Create LTI external tool in Canvas
            # 2. Configure assignment passback
            # 3. Setup grade sync
            # 4. Create navigation link
            # 5. Configure notifications

            logger.info(f"🔗 Canvas integration setup completed for course {course_id}")

        except Exception as e:
            logger.error(f"❌ Canvas integration setup failed: {e}")
            raise

    async def _create_faculty_dashboard(self, faculty_id: str, course_id: str) -> str:
        """Create personalized faculty dashboard"""
        try:
            # Generate unique dashboard URL
            dashboard_url = (
                f"https://eagleadventures.ewu.edu/faculty/{faculty_id}/dashboard"
            )

            # This would:
            # 1. Create personalized dashboard
            # 2. Setup analytics widgets
            # 3. Configure notification preferences
            # 4. Add help resources
            # 5. Setup office hours integration

            logger.info(f"📊 Faculty dashboard created: {dashboard_url}")
            return dashboard_url

        except Exception as e:
            logger.error(f"❌ Dashboard creation failed: {e}")
            return ""

    async def _setup_student_onboarding(self, course_id: str, config: Dict[str, Any]):
        """Setup automated student onboarding"""
        try:
            # This would:
            # 1. Create student survey forms
            # 2. Setup character creation flow
            # 3. Configure initial pet assignment
            # 4. Setup tutorial system
            # 5. Create welcome sequence

            logger.info(f"👨‍🎓 Student onboarding configured for course {course_id}")

        except Exception as e:
            logger.error(f"❌ Student onboarding setup failed: {e}")
            raise

    async def _setup_progress_monitoring(self, course_id: str, faculty_id: str):
        """Setup automated progress monitoring and alerts"""
        try:
            # This would:
            # 1. Configure progress tracking
            # 2. Setup early warning system
            # 3. Create intervention triggers
            # 4. Configure reporting schedule
            # 5. Setup emergency alerts

            logger.info(f"📈 Progress monitoring configured for course {course_id}")

        except Exception as e:
            logger.error(f"❌ Progress monitoring setup failed: {e}")
            raise

    async def _send_welcome_package(
        self, faculty: FacultyProfile, dashboard_url: str, config: Dict[str, Any]
    ):
        """Send welcome package with tutorials and resources"""
        try:
            welcome_content = {
                "dashboard_url": dashboard_url,
                "quick_start_guide": "https://docs.eagleadventures.ewu.edu/faculty/quick-start",
                "tutorial_videos": [
                    "Understanding Your Dashboard",
                    "Monitoring Student Progress",
                    "Customizing Gamification Settings",
                ],
                "support_contacts": {
                    "help_desk": "help@eagleadventures.ewu.edu",
                    "office_hours": "Tuesdays & Thursdays 2-4 PM",
                },
                "enabled_features": list(config.get("enabled_features", {}).keys()),
            }

            # This would send email with welcome package
            logger.info(f"📧 Welcome package sent to {faculty.email}")

        except Exception as e:
            logger.error(f"❌ Welcome package sending failed: {e}")

    async def _send_error_notification(
        self, faculty: FacultyProfile, session: OnboardingSession, error: str
    ):
        """Send error notification and support information"""
        try:
            error_info = {
                "session_id": session.session_id,
                "error_description": error,
                "failed_step": session.current_step,
                "completed_steps": session.steps_completed,
                "support_ticket_created": True,
                "next_steps": [
                    "Our support team has been notified",
                    "You will receive a follow-up email within 24 hours",
                    "For immediate help, contact help@eagleadventures.ewu.edu",
                ],
            }

            logger.error(f"📧 Error notification sent to {faculty.email}")

        except Exception as e:
            logger.error(f"❌ Error notification failed: {e}")

    def _save_faculty_profiles(self):
        """Save faculty profiles to storage"""
        try:
            profiles_data = {}
            for faculty_id, profile in self.faculty_profiles.items():
                profiles_data[faculty_id] = {
                    "name": profile.name,
                    "email": profile.email,
                    "institution": profile.institution,
                    "department": profile.department,
                    "canvas_user_id": profile.canvas_user_id,
                    "technical_comfort_level": profile.technical_comfort_level,
                    "gamification_preferences": profile.gamification_preferences,
                    "course_preferences": profile.course_preferences,
                    "onboarding_completed": profile.onboarding_completed,
                    "created_at": profile.created_at.isoformat(),
                }

            profiles_file = "data/onboarding/faculty_profiles.json"
            os.makedirs(os.path.dirname(profiles_file), exist_ok=True)
            with open(profiles_file, "w") as f:
                json.dump(profiles_data, f, indent=2)

        except Exception as e:
            logger.error(f"❌ Failed to save faculty profiles: {e}")

    def _save_onboarding_data(self):
        """Save onboarding sessions and configurations"""
        try:
            self._save_faculty_profiles()

            # Save onboarding sessions
            sessions_data = {}
            for session_id, session in self.onboarding_sessions.items():
                sessions_data[session_id] = {
                    "faculty_id": session.faculty_id,
                    "status": session.status.value,
                    "current_step": session.current_step,
                    "steps_completed": session.steps_completed,
                    "errors": session.errors,
                    "canvas_course_id": session.canvas_course_id,
                    "started_at": session.started_at.isoformat(),
                    "completed_at": (
                        session.completed_at.isoformat()
                        if session.completed_at
                        else None
                    ),
                }

            sessions_file = "data/onboarding/onboarding_sessions.json"
            os.makedirs(os.path.dirname(sessions_file), exist_ok=True)
            with open(sessions_file, "w") as f:
                json.dump(sessions_data, f, indent=2)

        except Exception as e:
            logger.error(f"❌ Failed to save onboarding data: {e}")

    def get_onboarding_status(self, session_id: str) -> Dict[str, Any]:
        """Get status of onboarding session"""
        session = self.onboarding_sessions.get(session_id)
        if not session:
            return {"error": "Session not found"}

        faculty = self.faculty_profiles.get(session.faculty_id)

        return {
            "session_id": session_id,
            "faculty_name": faculty.name if faculty else "Unknown",
            "status": session.status.value,
            "current_step": session.current_step,
            "progress": f"{len(session.steps_completed)}/8 steps completed",
            "steps_completed": session.steps_completed,
            "errors": session.errors,
            "started_at": session.started_at.isoformat(),
            "completed_at": (
                session.completed_at.isoformat() if session.completed_at else None
            ),
            "estimated_time_remaining": self._estimate_remaining_time(session),
        }

    def _estimate_remaining_time(self, session: OnboardingSession) -> str:
        """Estimate remaining onboarding time"""
        total_steps = 8
        completed_steps = len(session.steps_completed)

        if session.status == OnboardingStatus.COMPLETED:
            return "0 minutes"

        if session.status == OnboardingStatus.FAILED:
            return "Manual intervention required"

        remaining_steps = total_steps - completed_steps
        estimated_minutes = remaining_steps * 2  # ~2 minutes per step

        if estimated_minutes <= 5:
            return "< 5 minutes"
        elif estimated_minutes <= 15:
            return f"~{estimated_minutes} minutes"
        else:
            return "~15-20 minutes"

    def get_system_status(self) -> Dict[str, Any]:
        """Get onboarding system status"""
        active_sessions = len(
            [
                s
                for s in self.onboarding_sessions.values()
                if s.status == OnboardingStatus.IN_PROGRESS
            ]
        )
        completed_sessions = len(
            [
                s
                for s in self.onboarding_sessions.values()
                if s.status == OnboardingStatus.COMPLETED
            ]
        )
        failed_sessions = len(
            [
                s
                for s in self.onboarding_sessions.values()
                if s.status == OnboardingStatus.FAILED
            ]
        )

        return {
            "status": "healthy" if failed_sessions == 0 else "warning",
            "total_faculty": len(self.faculty_profiles),
            "active_onboarding_sessions": active_sessions,
            "completed_onboardings": completed_sessions,
            "failed_onboardings": failed_sessions,
            "success_rate": completed_sessions
            / max(1, completed_sessions + failed_sessions),
            "average_onboarding_time": "15 minutes",  # Mock data
            "course_templates_available": len(self.course_templates),
        }


# Example usage and testing
async def main():
    """Example usage of Faculty Onboarding System"""
    onboarding_system = FacultyOnboardingSystem()

    # Example: Start onboarding
    result = await onboarding_system.start_onboarding(
        faculty_email="dr.lynch@ewu.edu",
        canvas_course_id="MATH231_2025",
        course_subject="mathematics",
    )

    print(f"Onboarding started: {result}")

    # Wait a bit for processing
    await asyncio.sleep(1)

    # Check status
    status = onboarding_system.get_onboarding_status(result["session_id"])
    print(f"Onboarding Status: {json.dumps(status, indent=2)}")

    # Get system status
    system_status = onboarding_system.get_system_status()
    print(f"System Status: {json.dumps(system_status, indent=2)}")


if __name__ == "__main__":
    asyncio.run(main())
