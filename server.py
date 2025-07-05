#!/usr/bin/env python3
"""
Linear Algebra Course Builder - Production Server
================================================

Production-ready server with proper configuration, logging, and error handling.
"""

import os
import sys
import logging
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from app import app


def setup_production_logging():
    """Configure production logging"""
    log_level = os.environ.get("LOG_LEVEL", "INFO").upper()

    # Create logs directory
    log_dir = project_root / "logs"
    log_dir.mkdir(exist_ok=True)

    # Configure logging
    logging.basicConfig(
        level=getattr(logging, log_level),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(log_dir / "app.log"),
            logging.StreamHandler(sys.stdout),
        ],
    )

    # Set up specific loggers
    werkzeug_logger = logging.getLogger("werkzeug")
    werkzeug_logger.setLevel(logging.WARNING)

    app_logger = logging.getLogger("linear_algebra_builder")
    app_logger.setLevel(getattr(logging, log_level))

    return app_logger


def validate_environment():
    """Validate required environment variables"""
    required_vars = ["CANVAS_API_TOKEN", "CANVAS_API_URL", "FLASK_SECRET_KEY"]

    missing_vars = []
    for var in required_vars:
        if not os.environ.get(var):
            missing_vars.append(var)

    if missing_vars:
        print(f"❌ Missing required environment variables: {', '.join(missing_vars)}")
        print("Please set these variables in your .env file or environment.")
        sys.exit(1)

    # Check for encryption key file
    key_path = project_root / "config" / ".privacy_encryption_key"
    if not key_path.exists():
        print("❌ Missing encryption key file: config/.privacy_encryption_key")
        print("This file is required for secure operation.")
        sys.exit(1)

    print("✅ Environment validation passed")


def main():
    """Main application entry point"""
    logger = setup_production_logging()
    logger.info("Starting Linear Algebra Course Builder...")

    # Validate environment
    try:
        validate_environment()
    except Exception as e:
        logger.error(f"Environment validation failed: {e}")
        sys.exit(1)

    # Initialize the application
    try:
        from src.course_templates.linear_algebra_template import (
            LinearAlgebraTemplateManager,
        )

        manager = LinearAlgebraTemplateManager()
        logger.info("✅ Course template manager initialized successfully")
    except Exception as e:
        logger.error(f"❌ Failed to initialize course manager: {e}")
        sys.exit(1)

    # Configure Flask app for production
    app.config.update(
        DEBUG=os.environ.get("DEBUG", "false").lower() == "true",
        SECRET_KEY=os.environ.get("FLASK_SECRET_KEY"),
        WTF_CSRF_ENABLED=True,
        WTF_CSRF_TIME_LIMIT=3600,  # 1 hour
        MAX_CONTENT_LENGTH=16 * 1024 * 1024,  # 16MB
        SESSION_COOKIE_SECURE=os.environ.get("HTTPS_ENABLED", "false").lower()
        == "true",
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE="Lax",
    )

    # Get host and port
    host = os.environ.get("HOST", "0.0.0.0")
    port = int(os.environ.get("PORT", 5000))

    logger.info(f"🚀 Starting server on {host}:{port}")
    logger.info(f"🔗 Access URL: http://{host}:{port}")

    # Run the application
    app.run(host=host, port=port, debug=app.config["DEBUG"], threaded=True)


if __name__ == "__main__":
    main()
