#!/usr/bin/env python3
"""
Canvas API Integration Test Script
=================================

Interactive test script for validating Canvas API connectivity
and performing initial integration setup for Eagle Adventures 2.

Usage:
    python canvas_api_test.py

Author: AI Agent Development Team
License: MIT (Educational Use)
"""

import json
import logging
import os
import requests
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
import yaml

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class CanvasAPITester:
    """Canvas API connectivity and integration tester"""
    
    def __init__(self):
        self.config = self.load_config()
        self.session = requests.Session()
        self.setup_session()
        
    def load_config(self) -> Dict[str, Any]:
        """Load Canvas configuration from file or environment"""
        config_path = Path("config/canvas_integration.yml")
        template_path = Path("config/canvas_integration_template.yml")
        
        # Try to load actual config first
        if config_path.exists():
            with open(config_path, 'r') as f:
                config = yaml.safe_load(f)
                logger.info("Loaded Canvas configuration from config file")
        elif template_path.exists():
            logger.warning("No canvas_integration.yml found, loading template")
            with open(template_path, 'r') as f:
                config = yaml.safe_load(f)
        else:
            logger.error("No Canvas configuration file found!")
            sys.exit(1)
            
        # Override with environment variables if available
        canvas_token = os.getenv('CANVAS_API_TOKEN')
        canvas_url = os.getenv('CANVAS_BASE_URL')
        
        if canvas_token:
            config['canvas']['api_token'] = canvas_token
            logger.info("Using Canvas API token from environment")
            
        if canvas_url:
            config['canvas']['base_url'] = canvas_url
            logger.info("Using Canvas base URL from environment")
            
        return config
        
    def setup_session(self):
        """Setup requests session with Canvas authentication"""
        token = self.config['canvas']['api_token']
        
        if not token or token == "YOUR_CANVAS_API_TOKEN_HERE":
            logger.error("Canvas API token not configured!")
            logger.info("Please set CANVAS_API_TOKEN environment variable or update config file")
            sys.exit(1)
            
        self.session.headers.update({
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json',
            'User-Agent': 'Eagle Adventures 2 - Canvas Integration'
        })
        
        self.base_url = self.config['canvas']['base_url'].rstrip('/')
        logger.info(f"Canvas API configured for: {self.base_url}")
        
    def test_connection(self) -> bool:
        """Test basic Canvas API connectivity"""
        logger.info("Testing Canvas API connectivity...")
        
        try:
            url = f"{self.base_url}/api/v1/users/self"
            response = self.session.get(url)
            response.raise_for_status()
            
            user_info = response.json()
            logger.info(f"✅ Connected successfully as: {user_info.get('name', 'Unknown')}")
            logger.info(f"   User ID: {user_info.get('id')}")
            logger.info(f"   Email: {user_info.get('email', 'Not provided')}")
            return True
            
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Canvas API connection failed: {e}")
            return False
            
    def list_courses(self) -> List[Dict[str, Any]]:
        """List accessible courses"""
        logger.info("Fetching accessible courses...")
        
        try:
            url = f"{self.base_url}/api/v1/courses"
            params = {
                'enrollment_type': 'teacher',
                'state': 'available',
                'per_page': 50
            }
            
            response = self.session.get(url, params=params)
            response.raise_for_status()
            
            courses = response.json()
            logger.info(f"Found {len(courses)} courses where you have teacher access:")
            
            for course in courses:
                logger.info(f"  - {course.get('name')} (ID: {course.get('id')})")
                
            return courses
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to fetch courses: {e}")
            return []
            
    def analyze_course(self, course_id: int) -> Dict[str, Any]:
        """Analyze a specific course for gamification potential"""
        logger.info(f"Analyzing course {course_id} for gamification integration...")
        
        analysis = {
            'course_id': course_id,
            'assignments': [],
            'modules': [],
            'students': [],
            'gradebook_columns': []
        }
        
        try:
            # Get course info
            course_url = f"{self.base_url}/api/v1/courses/{course_id}"
            course_response = self.session.get(course_url)
            course_response.raise_for_status()
            course_info = course_response.json()
            
            analysis['course_info'] = course_info
            logger.info(f"Course: {course_info.get('name')}")
            
            # Get assignments
            assignments_url = f"{self.base_url}/api/v1/courses/{course_id}/assignments"
            assignments_response = self.session.get(assignments_url)
            assignments_response.raise_for_status()
            assignments = assignments_response.json()
            
            analysis['assignments'] = assignments
            logger.info(f"Found {len(assignments)} assignments")
            
            # Analyze assignment types for XP mapping
            assignment_types = {}
            total_points = 0
            
            for assignment in assignments:
                assignment_group = assignment.get('assignment_group_id', 'unknown')
                points = assignment.get('points_possible', 0) or 0
                total_points += points
                
                if assignment_group not in assignment_types:
                    assignment_types[assignment_group] = {
                        'count': 0,
                        'total_points': 0,
                        'assignments': []
                    }
                    
                assignment_types[assignment_group]['count'] += 1
                assignment_types[assignment_group]['total_points'] += points
                assignment_types[assignment_group]['assignments'].append(assignment['name'])
                
            logger.info(f"Total points available: {total_points}")
            logger.info("Assignment distribution:")
            for group_id, data in assignment_types.items():
                logger.info(f"  Group {group_id}: {data['count']} assignments, {data['total_points']} points")
                
            # Get modules
            modules_url = f"{self.base_url}/api/v1/courses/{course_id}/modules"
            modules_response = self.session.get(modules_url)
            if modules_response.status_code == 200:
                modules = modules_response.json()
                analysis['modules'] = modules
                logger.info(f"Found {len(modules)} modules")
            
            # Get student count
            students_url = f"{self.base_url}/api/v1/courses/{course_id}/users"
            params = {'enrollment_type': 'student'}
            students_response = self.session.get(students_url, params=params)
            if students_response.status_code == 200:
                students = students_response.json()
                analysis['students'] = students
                logger.info(f"Found {len(students)} enrolled students")
                
            return analysis
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to analyze course {course_id}: {e}")
            return analysis
            
    def create_xp_gradebook_column(self, course_id: int) -> Optional[int]:
        """Create a custom gradebook column for XP tracking"""
        logger.info(f"Creating XP gradebook column for course {course_id}...")
        
        try:
            url = f"{self.base_url}/api/v1/courses/{course_id}/custom_gradebook_columns"
            
            column_data = {
                'column': {
                    'title': 'Eagle Adventures XP',
                    'position': 1,
                    'hidden': False,
                    'teacher_notes': 'Gamification XP points earned through Eagle Adventures 2'
                }
            }
            
            response = self.session.post(url, json=column_data)
            response.raise_for_status()
            
            column_info = response.json()
            column_id = column_info.get('id')
            
            logger.info(f"✅ Created XP column with ID: {column_id}")
            return column_id
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to create XP column: {e}")
            return None
            
    def update_student_xp(self, course_id: int, column_id: int, student_id: int, xp_value: int) -> bool:
        """Update a student's XP in the gradebook"""
        logger.info(f"Updating XP for student {student_id}: {xp_value} points")
        
        try:
            url = f"{self.base_url}/api/v1/courses/{course_id}/custom_gradebook_columns/{column_id}/data/{student_id}"
            
            data = {
                'column_data': {
                    'content': str(xp_value)
                }
            }
            
            response = self.session.put(url, json=data)
            response.raise_for_status()
            
            logger.info(f"✅ Updated student {student_id} XP to {xp_value}")
            return True
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to update student XP: {e}")
            return False
            
    def run_integration_test(self):
        """Run complete integration test"""
        logger.info("🚀 Starting Canvas API Integration Test")
        logger.info("=" * 50)
        
        # Step 1: Test connection
        if not self.test_connection():
            return False
            
        # Step 2: List courses
        courses = self.list_courses()
        if not courses:
            logger.warning("No courses found - you may need teacher access")
            return False
            
        # Step 3: Analyze first course (or let user select)
        if len(courses) == 1:
            selected_course = courses[0]
        else:
            logger.info("\nSelect a course for integration testing:")
            for i, course in enumerate(courses):
                print(f"{i+1}. {course.get('name')} (ID: {course.get('id')})")
                
            try:
                choice = int(input("\nEnter course number: ")) - 1
                if 0 <= choice < len(courses):
                    selected_course = courses[choice]
                else:
                    logger.error("Invalid selection")
                    return False
            except (ValueError, KeyboardInterrupt):
                logger.info("Test cancelled by user")
                return False
                
        course_id = selected_course['id']
        logger.info(f"\n🎯 Testing integration with: {selected_course['name']}")
        
        # Step 4: Analyze course
        analysis = self.analyze_course(course_id)
        
        # Step 5: Test XP column creation (optional)
        create_xp = input("\nCreate XP gradebook column? (y/n): ").lower().startswith('y')
        if create_xp:
            column_id = self.create_xp_gradebook_column(course_id)
            if column_id and analysis['students']:
                # Test updating first student's XP
                student = analysis['students'][0]
                test_xp = 100
                logger.info(f"Testing XP update for student: {student.get('name')}")
                self.update_student_xp(course_id, column_id, student['id'], test_xp)
                
        logger.info("\n✅ Canvas API Integration Test Complete!")
        logger.info("The Eagle Adventures 2 platform is ready for Canvas deployment.")
        
        return True


def main():
    """Main test function"""
    print("🎮 Eagle Adventures 2 - Canvas API Integration Test")
    print("="*55)
    print()
    
    # Check for API token
    if not os.getenv('CANVAS_API_TOKEN') and not Path('config/canvas_integration.yml').exists():
        print("⚠️  Canvas API token not found!")
        print("Please either:")
        print("1. Set CANVAS_API_TOKEN environment variable, or")
        print("2. Copy config/canvas_integration_template.yml to config/canvas_integration.yml")
        print("   and update with your Canvas API credentials")
        print()
        return
        
    try:
        tester = CanvasAPITester()
        success = tester.run_integration_test()
        
        if success:
            print("\n🎉 Integration test successful!")
            print("Next steps:")
            print("1. Update config/canvas_integration.yml with your course ID")
            print("2. Run: python -m src.canvas_integration.live_connector")
            print("3. Begin gamified learning with your students!")
        else:
            print("\n❌ Integration test failed.")
            print("Please check your Canvas API credentials and permissions.")
            
    except KeyboardInterrupt:
        print("\n\nTest cancelled by user.")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        

if __name__ == "__main__":
    main()
