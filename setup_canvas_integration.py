#!/usr/bin/env python3
"""
Canvas Integration Setup Wizard
===============================

Interactive setup wizard for connecting Eagle Adventures 2
with Canvas LMS courses. Guides faculty through the complete
integration process step-by-step.

Usage:
    python setup_canvas_integration.py

Author: AI Agent Development Team
License: MIT (Educational Use)
"""

import json
import logging
import os
import shutil
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
import yaml

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class CanvasIntegrationWizard:
    """Interactive Canvas integration setup wizard"""
    
    def __init__(self):
        self.config = {}
        self.canvas_info = {}
        
    def welcome(self):
        """Display welcome message and overview"""
        print("\n" + "🎮 " + "="*60)
        print("  EAGLE ADVENTURES 2 - CANVAS INTEGRATION WIZARD")
        print("="*62)
        print("\nWelcome! This wizard will help you connect your Canvas course")
        print("with the Eagle Adventures 2 gamification platform.")
        print("\n📋 What this wizard will do:")
        print("   ✓ Configure Canvas API connectivity")
        print("   ✓ Set up your course for gamification")
        print("   ✓ Create XP tracking in Canvas gradebook")
        print("   ✓ Map assignments to skill progression")
        print("   ✓ Test the complete integration")
        print("\n⏱️  Estimated time: 10-15 minutes")
        print("\n" + "-"*62)
        
        proceed = input("\nReady to begin? (y/n): ").lower().startswith('y')
        if not proceed:
            print("Setup cancelled. Run again when you're ready!")
            sys.exit(0)
            
    def collect_canvas_credentials(self):
        """Collect Canvas API credentials from user"""
        print("\n📡 STEP 1: Canvas API Configuration")
        print("-" * 40)
        
        print("\nFirst, we need your Canvas API credentials.")
        print("📖 How to get your Canvas API token:")
        print("   1. Log into your Canvas account")
        print("   2. Go to Account → Settings")
        print("   3. Scroll to 'Approved Integrations'")
        print("   4. Click '+ New Access Token'")
        print("   5. Enter purpose: 'Eagle Adventures 2 Integration'")
        print("   6. Copy the generated token")
        
        # Get Canvas URL
        print("\n🌐 Canvas Instance URL")
        default_url = "https://canvas.ewu.edu"
        canvas_url = input(f"Enter your Canvas URL [{default_url}]: ").strip()
        if not canvas_url:
            canvas_url = default_url
            
        # Ensure URL format
        if not canvas_url.startswith('http'):
            canvas_url = f"https://{canvas_url}"
        canvas_url = canvas_url.rstrip('/')
        
        # Get API token
        print("\n🔑 Canvas API Token")
        api_token = input("Enter your Canvas API token: ").strip()
        
        if not api_token:
            print("❌ API token is required for integration.")
            sys.exit(1)
            
        self.canvas_info = {
            'base_url': canvas_url,
            'api_token': api_token
        }
        
        print(f"✅ Canvas configured: {canvas_url}")
        
    def test_canvas_connection(self):
        """Test Canvas API connectivity"""
        print("\n🔍 STEP 2: Testing Canvas Connection")
        print("-" * 42)
        
        print("Testing Canvas API connectivity...")
        
        # Import and use our test script
        try:
            import requests
            
            session = requests.Session()
            session.headers.update({
                'Authorization': f'Bearer {self.canvas_info["api_token"]}',
                'Content-Type': 'application/json'
            })
            
            url = f"{self.canvas_info['base_url']}/api/v1/users/self"
            response = session.get(url)
            response.raise_for_status()
            
            user_info = response.json()
            print(f"✅ Connected successfully!")
            print(f"   👤 User: {user_info.get('name', 'Unknown')}")
            print(f"   📧 Email: {user_info.get('email', 'Not provided')}")
            
            self.canvas_info['user_info'] = user_info
            return True
            
        except Exception as e:
            print(f"❌ Connection failed: {e}")
            print("\nPlease check:")
            print("   • Canvas URL is correct")
            print("   • API token is valid and active")
            print("   • You have sufficient permissions")
            return False
            
    def select_course(self):
        """Let user select which course to integrate"""
        print("\n📚 STEP 3: Course Selection")
        print("-" * 30)
        
        print("Fetching your Canvas courses...")
        
        try:
            import requests
            
            session = requests.Session()
            session.headers.update({
                'Authorization': f'Bearer {self.canvas_info["api_token"]}',
                'Content-Type': 'application/json'
            })
            
            url = f"{self.canvas_info['base_url']}/api/v1/courses"
            params = {
                'enrollment_type': 'teacher',
                'state': 'available',
                'per_page': 50
            }
            
            response = session.get(url, params=params)
            response.raise_for_status()
            courses = response.json()
            
            if not courses:
                print("❌ No courses found where you have teacher access.")
                return False
                
            print(f"\nFound {len(courses)} courses:")
            for i, course in enumerate(courses):
                enrollment_count = course.get('total_students', 'Unknown')
                print(f"   {i+1}. {course.get('name')} (ID: {course.get('id')}, Students: {enrollment_count})")
                
            # Get user selection
            while True:
                try:
                    choice = input(f"\nSelect course (1-{len(courses)}): ")
                    choice_idx = int(choice) - 1
                    
                    if 0 <= choice_idx < len(courses):
                        selected_course = courses[choice_idx]
                        break
                    else:
                        print(f"Please enter a number between 1 and {len(courses)}")
                        
                except ValueError:
                    print("Please enter a valid number")
                    
            self.canvas_info['selected_course'] = selected_course
            print(f"✅ Selected: {selected_course['name']}")
            return True
            
        except Exception as e:
            print(f"❌ Failed to fetch courses: {e}")
            return False
            
    def configure_gamification_settings(self):
        """Configure gamification settings for the course"""
        print("\n🎮 STEP 4: Gamification Configuration")
        print("-" * 44)
        
        course_name = self.canvas_info['selected_course']['name']
        print(f"Configuring gamification for: {course_name}")
        
        # XP Settings
        print("\n⚡ XP (Experience Points) Settings")
        
        default_homework_xp = 25
        homework_xp = input(f"XP per homework assignment [{default_homework_xp}]: ")
        homework_xp = int(homework_xp) if homework_xp.isdigit() else default_homework_xp
        
        default_quiz_xp = 50
        quiz_xp = input(f"XP per quiz [{default_quiz_xp}]: ")
        quiz_xp = int(quiz_xp) if quiz_xp.isdigit() else default_quiz_xp
        
        default_exam_xp = 100
        exam_xp = input(f"XP per exam [{default_exam_xp}]: ")
        exam_xp = int(exam_xp) if exam_xp.isdigit() else default_exam_xp
        
        # Badge Settings
        print("\n🏆 Badge and Achievement Settings")
        enable_badges = input("Enable achievement badges? (y/n) [y]: ").lower()
        enable_badges = not enable_badges.startswith('n')
        
        enable_leaderboard = input("Enable class leaderboard? (y/n) [y]: ").lower()
        enable_leaderboard = not enable_leaderboard.startswith('n')
        
        # Skill Tree Settings
        print("\n🌳 Skill Tree Settings")
        skill_tree_theme = input("Course theme [Mathematical Adventure]: ").strip()
        if not skill_tree_theme:
            skill_tree_theme = "Mathematical Adventure"
            
        self.config = {
            'canvas': {
                'base_url': self.canvas_info['base_url'],
                'api_token': self.canvas_info['api_token'],
                'course_id': self.canvas_info['selected_course']['id'],
                'course_name': self.canvas_info['selected_course']['name']
            },
            'gamification': {
                'xp_values': {
                    'homework': homework_xp,
                    'quiz': quiz_xp,
                    'exam': exam_xp,
                    'participation': 10,
                    'bonus': 5
                },
                'features': {
                    'badges_enabled': enable_badges,
                    'leaderboard_enabled': enable_leaderboard,
                    'skill_tree_enabled': True
                },
                'theme': {
                    'name': skill_tree_theme,
                    'style': 'academic_adventure'
                }
            },
            'privacy': {
                'ferpa_compliant': True,
                'anonymous_leaderboard': True,
                'data_retention_days': 365
            }
        }
        
        print("✅ Gamification settings configured!")
        
    def create_xp_gradebook_column(self):
        """Create XP tracking column in Canvas gradebook"""
        print("\n📊 STEP 5: Gradebook Integration")
        print("-" * 36)
        
        print("Creating XP tracking column in Canvas gradebook...")
        
        try:
            import requests
            
            session = requests.Session()
            session.headers.update({
                'Authorization': f'Bearer {self.canvas_info["api_token"]}',
                'Content-Type': 'application/json'
            })
            
            course_id = self.canvas_info['selected_course']['id']
            url = f"{self.canvas_info['base_url']}/api/v1/courses/{course_id}/custom_gradebook_columns"
            
            column_data = {
                'column': {
                    'title': 'Eagle Adventures XP',
                    'position': 1,
                    'hidden': False,
                    'teacher_notes': 'Experience points earned through gamified learning activities'
                }
            }
            
            response = session.post(url, json=column_data)
            response.raise_for_status()
            
            column_info = response.json()
            self.config['canvas']['xp_column_id'] = column_info.get('id')
            
            print("✅ XP gradebook column created successfully!")
            print(f"   Column ID: {column_info.get('id')}")
            
            return True
            
        except Exception as e:
            print(f"❌ Failed to create gradebook column: {e}")
            print("You can create this manually later if needed.")
            return False
            
    def save_configuration(self):
        """Save configuration to file"""
        print("\n💾 STEP 6: Saving Configuration")
        print("-" * 34)
        
        # Ensure config directory exists
        config_dir = Path("config")
        config_dir.mkdir(exist_ok=True)
        
        # Save main configuration
        config_file = config_dir / "canvas_integration.yml"
        with open(config_file, 'w') as f:
            yaml.dump(self.config, f, default_flow_style=False, indent=2)
            
        print(f"✅ Configuration saved to: {config_file}")
        
        # Create backup of template if it doesn't exist
        template_file = config_dir / "canvas_integration_template.yml"
        if not template_file.exists():
            shutil.copy(config_file, template_file)
            
        # Save deployment info
        deployment_info = {
            'setup_date': datetime.now().isoformat(),
            'setup_user': self.canvas_info['user_info']['name'],
            'course_info': self.canvas_info['selected_course'],
            'integration_status': 'configured'
        }
        
        deployment_file = config_dir / "deployment_info.json"
        with open(deployment_file, 'w') as f:
            json.dump(deployment_info, f, indent=2)
            
        print(f"✅ Deployment info saved to: {deployment_file}")
        
    def run_final_test(self):
        """Run final integration test"""
        print("\n🧪 STEP 7: Final Integration Test")
        print("-" * 36)
        
        print("Running final integration test...")
        
        try:
            # Test Canvas API connectivity
            import requests
            
            session = requests.Session()
            session.headers.update({
                'Authorization': f'Bearer {self.canvas_info["api_token"]}',
                'Content-Type': 'application/json'
            })
            
            course_id = self.canvas_info['selected_course']['id']
            
            # Test 1: Get course info
            course_url = f"{self.canvas_info['base_url']}/api/v1/courses/{course_id}"
            response = session.get(course_url)
            response.raise_for_status()
            print("   ✓ Course access confirmed")
            
            # Test 2: Get assignments
            assignments_url = f"{self.canvas_info['base_url']}/api/v1/courses/{course_id}/assignments"
            response = session.get(assignments_url)
            response.raise_for_status()
            assignments = response.json()
            print(f"   ✓ Found {len(assignments)} assignments for XP mapping")
            
            # Test 3: Verify XP column
            if 'xp_column_id' in self.config['canvas']:
                columns_url = f"{self.canvas_info['base_url']}/api/v1/courses/{course_id}/custom_gradebook_columns"
                response = session.get(columns_url)
                response.raise_for_status()
                print("   ✓ XP gradebook column accessible")
                
            print("\n✅ All integration tests passed!")
            return True
            
        except Exception as e:
            print(f"❌ Integration test failed: {e}")
            return False
            
    def show_next_steps(self):
        """Show next steps for faculty"""
        print("\n🎉 INTEGRATION COMPLETE!")
        print("="*50)
        
        print("\n📋 Next Steps:")
        print("1. 🚀 Start the gamification engine:")
        print("   python -m src.canvas_integration.live_connector")
        print()
        print("2. 📊 Generate course preview:")
        print("   python -m src.preview_generator data/math231 output/preview.html")
        print()
        print("3. 👥 Onboard your students:")
        print("   python -m src.onboarding.student_automation")
        print()
        print("4. 📈 Monitor progress:")
        print("   python -m src.analytics.privacy_respecting_analytics")
        print()
        
        print("🎮 Your Eagle Adventures 2 gamified course is ready!")
        print("\n📧 Need help? Check docs/ or contact support.")
        
        # Save quick start commands
        commands_file = Path("CANVAS_INTEGRATION_COMMANDS.txt")
        with open(commands_file, 'w') as f:
            f.write("Eagle Adventures 2 - Canvas Integration Commands\n")
            f.write("=" * 50 + "\n\n")
            f.write("Start gamification engine:\n")
            f.write("python -m src.canvas_integration.live_connector\n\n")
            f.write("Generate course preview:\n")
            f.write("python -m src.preview_generator data/math231 output/preview.html\n\n")
            f.write("Run system health check:\n")
            f.write("python test_comprehensive_systems.py\n\n")
            f.write("Access demo portal:\n")
            f.write("python -m src.public.demo_portal\n\n")
            
        print(f"💾 Quick reference saved to: {commands_file}")
        
    def run_setup_wizard(self):
        """Run the complete setup wizard"""
        try:
            self.welcome()
            self.collect_canvas_credentials()
            
            if not self.test_canvas_connection():
                print("❌ Setup failed at connection test.")
                return False
                
            if not self.select_course():
                print("❌ Setup failed at course selection.")
                return False
                
            self.configure_gamification_settings()
            self.create_xp_gradebook_column()
            self.save_configuration()
            
            if self.run_final_test():
                self.show_next_steps()
                return True
            else:
                print("⚠️  Setup completed with warnings. Check configuration.")
                return False
                
        except KeyboardInterrupt:
            print("\n\n⏹️  Setup cancelled by user.")
            return False
        except Exception as e:
            print(f"\n❌ Setup failed with error: {e}")
            logger.exception("Setup wizard error")
            return False


def main():
    """Main setup function"""
    wizard = CanvasIntegrationWizard()
    success = wizard.run_setup_wizard()
    
    if success:
        print("\n🎊 Welcome to the future of education!")
    else:
        print("\n🔧 Setup incomplete. Please try again or check the logs.")
        

if __name__ == "__main__":
    main()
