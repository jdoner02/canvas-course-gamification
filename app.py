#!/usr/bin/env python3
"""
Linear Algebra Course Builder - Web Application
===============================================

Flask web application for faculty to create customized linear algebra courses
with Canvas integration, public student join links, and automated workflows.

Features:
- Faculty course customization form
- Real-time course creation and deployment
- Public student enrollment portal
- Course export and management dashboard
- Automated GitHub workflow integration

Author: AI Agent Education Team
License: MIT (Educational Use)
"""

import os
import json
import logging
import asyncio
from datetime import datetime, timedelta
from flask import (
    Flask,
    render_template,
    request,
    jsonify,
    redirect,
    url_for,
    flash,
    send_file,
)
from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    TextAreaField,
    SelectField,
    BooleanField,
    IntegerField,
    SubmitField,
)
from wtforms.validators import DataRequired, Email, Length, NumberRange
from werkzeug.utils import secure_filename
import sqlite3
import uuid
from pathlib import Path

# Load environment variables
from dotenv import load_dotenv

load_dotenv()

# Import our course template system
from src.course_templates.linear_algebra_template import (
    LinearAlgebraTemplateManager,
    LinearAlgebraCourse,
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Validate required environment variables
required_env_vars = ["CANVAS_API_TOKEN", "CANVAS_API_URL"]
missing_vars = [var for var in required_env_vars if not os.getenv(var)]
if missing_vars:
    logger.error(f"Missing required environment variables: {', '.join(missing_vars)}")
    logger.error(
        "Please check your .env file and ensure all Canvas API credentials are set."
    )

# Flask app configuration
app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get(
    "FLASK_SECRET_KEY", "dev-key-change-in-production"
)
app.config["UPLOAD_FOLDER"] = "uploads"
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024  # 16MB max file upload

# Ensure upload directory exists
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)


class CourseCreationForm(FlaskForm):
    """Form for faculty to create customized linear algebra courses"""

    # Faculty Information
    instructor_name = StringField(
        "Your Name", validators=[DataRequired(), Length(min=2, max=100)]
    )
    instructor_email = StringField("Your Email", validators=[DataRequired(), Email()])
    institution = StringField(
        "Institution/Organization", validators=[DataRequired(), Length(min=2, max=200)]
    )

    # Course Configuration
    course_name = StringField(
        "Course Name",
        default="Linear Algebra with Applications",
        validators=[DataRequired(), Length(min=5, max=100)],
    )
    course_code = StringField("Course Code (optional)", validators=[Length(max=20)])
    semester = StringField(
        "Semester/Term",
        default="Fall 2024",
        validators=[DataRequired(), Length(min=3, max=50)],
    )

    # Course Customization
    focus_area = SelectField(
        "Primary Focus Area",
        choices=[
            ("foundations", "Mathematical Foundations"),
            ("applications", "Real-World Applications"),
            ("computational", "Computational Methods"),
            ("theoretical", "Theoretical Emphasis"),
            ("engineering", "Engineering Applications"),
            ("data_science", "Data Science Applications"),
        ],
        validators=[DataRequired()],
    )

    difficulty_level = SelectField(
        "Difficulty Level",
        choices=[
            ("introductory", "Introductory (100-200 level)"),
            ("intermediate", "Intermediate (200-300 level)"),
            ("advanced", "Advanced (300-400 level)"),
            ("graduate", "Graduate Level"),
        ],
        validators=[DataRequired()],
    )

    # Learning Preferences
    include_gamification = BooleanField(
        "Enable Skill Trees & Gamification", default=True
    )
    include_visualizations = BooleanField(
        "Include Interactive Visualizations", default=True
    )
    include_applications = BooleanField(
        "Emphasize Real-World Applications", default=True
    )
    include_proofs = BooleanField("Include Mathematical Proofs", default=False)

    # Course Structure
    estimated_duration = SelectField(
        "Course Duration",
        choices=[
            ("8_weeks", "8 Weeks"),
            ("12_weeks", "12 Weeks (Semester)"),
            ("16_weeks", "16 Weeks (Full Semester)"),
            ("self_paced", "Self-Paced"),
        ],
        default="12_weeks",
        validators=[DataRequired()],
    )

    weekly_hours = IntegerField(
        "Expected Weekly Study Hours",
        default=6,
        validators=[DataRequired(), NumberRange(min=1, max=20)],
    )

    # Additional Customization
    special_topics = TextAreaField(
        "Special Topics or Emphasis Areas (optional)",
        render_kw={
            "placeholder": "e.g., Machine Learning Applications, Computer Graphics, Engineering Mechanics"
        },
    )

    additional_notes = TextAreaField(
        "Additional Customization Notes (optional)",
        render_kw={
            "placeholder": "Any specific requirements or preferences for your course"
        },
    )

    # Deployment Options
    enable_public_enrollment = BooleanField(
        "Enable Public Student Enrollment", default=True
    )
    course_visibility = SelectField(
        "Course Visibility",
        choices=[
            ("public", "Public (Anyone can join with link)"),
            ("institution", "Institution Only"),
            ("invite_only", "Invite Only"),
        ],
        default="public",
        validators=[DataRequired()],
    )

    submit = SubmitField("Create Linear Algebra Course")


@app.route("/")
def index():
    """Main landing page"""
    return render_template("index.html")


@app.route("/create-course", methods=["GET", "POST"])
def create_course():
    """Course creation form and processing"""
    form = CourseCreationForm()

    if form.validate_on_submit():
        try:
            # Create course instance from form data
            course_data = {
                "course_id": str(uuid.uuid4()),
                "course_name": form.course_name.data,
                "instructor_name": form.instructor_name.data,
                "instructor_email": form.instructor_email.data,
                "institution": form.institution.data,
                "course_code": form.course_code.data,
                "semester": form.semester.data,
                "focus_area": form.focus_area.data,
                "difficulty_level": form.difficulty_level.data,
                "include_gamification": form.include_gamification.data,
                "include_visualizations": form.include_visualizations.data,
                "include_applications": form.include_applications.data,
                "include_proofs": form.include_proofs.data,
                "estimated_duration": form.estimated_duration.data,
                "weekly_hours": form.weekly_hours.data,
                "special_topics": form.special_topics.data,
                "additional_notes": form.additional_notes.data,
                "enable_public_enrollment": form.enable_public_enrollment.data,
                "course_visibility": form.course_visibility.data,
                "created_date": datetime.now().isoformat(),
                "status": "creating",
            }

            # Initialize course manager and create course
            manager = LinearAlgebraTemplateManager()

            # Run the async course creation
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                course_result = loop.run_until_complete(
                    manager.create_course_from_template(course_data)
                )
                flash(
                    f'Course "{course_data["course_name"]}" created successfully!',
                    "success",
                )
                return redirect(
                    url_for("course_dashboard", course_id=course_data["course_id"])
                )
            finally:
                loop.close()

        except Exception as e:
            logger.error(f"Error creating course: {str(e)}")
            flash(f"Error creating course: {str(e)}", "error")

    return render_template("create_course.html", form=form)


@app.route("/course/<course_id>")
def course_dashboard(course_id):
    """Course management dashboard for faculty"""
    try:
        manager = LinearAlgebraTemplateManager()

        # Get course details
        conn = sqlite3.connect(manager.db_path)
        course_data = conn.execute(
            "SELECT * FROM courses WHERE course_id = ?", (course_id,)
        ).fetchone()

        if not course_data:
            flash("Course not found", "error")
            return redirect(url_for("index"))

        # Get enrollment statistics
        enrollment_count = conn.execute(
            "SELECT COUNT(*) FROM enrollments WHERE course_id = ?", (course_id,)
        ).fetchone()[0]

        # Get export history
        exports = conn.execute(
            "SELECT * FROM exports WHERE course_id = ? ORDER BY created_date DESC",
            (course_id,),
        ).fetchall()

        conn.close()

        # Convert to dict for template
        course_info = {
            "course_id": course_data[0],
            "course_name": course_data[1],
            "instructor_name": course_data[2],
            "instructor_email": course_data[3],
            "canvas_course_id": course_data[4],
            "join_code": course_data[5],
            "join_url": course_data[6],
            "canvas_url": course_data[7],
            "status": course_data[8],
            "created_date": course_data[9],
            "cleanup_date": course_data[10],
            "enrollment_count": enrollment_count,
            "exports": exports,
        }

        return render_template("course_dashboard.html", course=course_info)

    except Exception as e:
        logger.error(f"Error loading course dashboard: {str(e)}")
        flash(f"Error loading course: {str(e)}", "error")
        return redirect(url_for("index"))


@app.route("/join")
def student_portal():
    """Public student enrollment portal"""
    return render_template("student_portal.html")


@app.route("/join/<join_code>")
def join_course(join_code):
    """Student course enrollment via join code"""
    try:
        manager = LinearAlgebraTemplateManager()

        # Find course by join code
        conn = sqlite3.connect(manager.db_path)
        course_data = conn.execute(
            "SELECT * FROM courses WHERE join_code = ?", (join_code,)
        ).fetchone()

        if not course_data:
            flash("Invalid join code", "error")
            return redirect(url_for("student_portal"))

        course_info = {
            "course_id": course_data[0],
            "course_name": course_data[1],
            "instructor_name": course_data[2],
            "canvas_url": course_data[7],
            "join_code": course_data[5],
        }

        conn.close()
        return render_template("join_course.html", course=course_info)

    except Exception as e:
        logger.error(f"Error joining course: {str(e)}")
        flash(f"Error joining course: {str(e)}", "error")
        return redirect(url_for("student_portal"))


@app.route("/api/enroll", methods=["POST"])
def api_enroll_student():
    """API endpoint for student enrollment"""
    try:
        data = request.get_json()
        course_id = data.get("course_id")
        student_email = data.get("student_email")
        student_name = data.get("student_name")

        if not all([course_id, student_email, student_name]):
            return jsonify({"error": "Missing required fields"}), 400

        manager = LinearAlgebraTemplateManager()

        # Run async enrollment
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            success = loop.run_until_complete(
                manager.enroll_student(course_id, student_email, student_name)
            )

            if success:
                return jsonify({"success": True, "message": "Enrolled successfully!"})
            else:
                return jsonify({"error": "Enrollment failed"}), 500

        finally:
            loop.close()

    except Exception as e:
        logger.error(f"Error in API enrollment: {str(e)}")
        return jsonify({"error": str(e)}), 500


@app.route("/api/export/<course_id>")
def api_export_course(course_id):
    """API endpoint to export course as Canvas cartridge"""
    try:
        manager = LinearAlgebraTemplateManager()

        # Run async export
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            export_path = loop.run_until_complete(manager.export_course(course_id))

            if export_path and os.path.exists(export_path):
                return send_file(
                    export_path,
                    as_attachment=True,
                    download_name=f"linear_algebra_course_{course_id}.imscc",
                )
            else:
                return jsonify({"error": "Export failed"}), 500

        finally:
            loop.close()

    except Exception as e:
        logger.error(f"Error exporting course: {str(e)}")
        return jsonify({"error": str(e)}), 500


@app.route("/api/courses")
def api_list_courses():
    """API endpoint to list all courses"""
    try:
        manager = LinearAlgebraTemplateManager()
        conn = sqlite3.connect(manager.db_path)

        courses = conn.execute(
            """
            SELECT course_id, course_name, instructor_name, status, created_date,
                   (SELECT COUNT(*) FROM enrollments WHERE enrollments.course_id = courses.course_id) as enrollment_count
            FROM courses 
            ORDER BY created_date DESC
        """
        ).fetchall()

        conn.close()

        course_list = []
        for course in courses:
            course_list.append(
                {
                    "course_id": course[0],
                    "course_name": course[1],
                    "instructor_name": course[2],
                    "status": course[3],
                    "created_date": course[4],
                    "enrollment_count": course[5],
                }
            )

        return jsonify(course_list)

    except Exception as e:
        logger.error(f"Error listing courses: {str(e)}")
        return jsonify({"error": str(e)}), 500


@app.route("/admin")
def admin_dashboard():
    """Administrative dashboard for course management"""
    try:
        manager = LinearAlgebraTemplateManager()
        conn = sqlite3.connect(manager.db_path)

        # Get course statistics
        total_courses = conn.execute("SELECT COUNT(*) FROM courses").fetchone()[0]
        active_courses = conn.execute(
            "SELECT COUNT(*) FROM courses WHERE status = 'active'"
        ).fetchone()[0]
        total_enrollments = conn.execute("SELECT COUNT(*) FROM enrollments").fetchone()[
            0
        ]

        # Get recent courses
        recent_courses = conn.execute(
            """
            SELECT course_id, course_name, instructor_name, status, created_date,
                   (SELECT COUNT(*) FROM enrollments WHERE enrollments.course_id = courses.course_id) as enrollment_count
            FROM courses 
            ORDER BY created_date DESC 
            LIMIT 10
        """
        ).fetchall()

        conn.close()

        stats = {
            "total_courses": total_courses,
            "active_courses": active_courses,
            "total_enrollments": total_enrollments,
            "recent_courses": recent_courses,
        }

        return render_template("admin_dashboard.html", stats=stats)

    except Exception as e:
        logger.error(f"Error loading admin dashboard: {str(e)}")
        flash(f"Error loading dashboard: {str(e)}", "error")
        return redirect(url_for("index"))


@app.route("/api/cleanup")
def api_cleanup_courses():
    """API endpoint to run course cleanup (7-day deletion)"""
    try:
        manager = LinearAlgebraTemplateManager()

        # Run async cleanup
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            cleaned_courses = loop.run_until_complete(manager.cleanup_expired_courses())
            return jsonify(
                {
                    "success": True,
                    "cleaned_courses": cleaned_courses,
                    "message": f"Cleaned up {len(cleaned_courses)} expired courses",
                }
            )
        finally:
            loop.close()

    except Exception as e:
        logger.error(f"Error during cleanup: {str(e)}")
        return jsonify({"error": str(e)}), 500


@app.errorhandler(404)
def not_found(error):
    return render_template("404.html"), 404


@app.errorhandler(500)
def internal_error(error):
    return render_template("500.html"), 500


if __name__ == "__main__":
    # Initialize database on startup
    try:
        manager = LinearAlgebraTemplateManager()
        logger.info("Linear Algebra Course Builder started successfully")
    except Exception as e:
        logger.error(f"Failed to initialize application: {str(e)}")
        exit(1)

    # Run Flask app
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000)),
        debug=os.environ.get("DEBUG", "false").lower() == "true",
    )
