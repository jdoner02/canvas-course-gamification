#!/usr/bin/env python3
"""
Production Startup Script with Environment Validation
====================================================

This script validates environment configuration before starting the
Flask application to ensure proper Canvas API integration.
"""

import os
import sys
import asyncio
from dotenv import load_dotenv


def validate_environment():
    """Validate required environment variables"""
    print("🔍 Validating environment configuration...")

    # Load environment variables
    load_dotenv()

    # Required variables
    required_vars = {
        "CANVAS_API_URL": "Canvas API base URL",
        "CANVAS_API_TOKEN": "Canvas API authentication token",
        "FLASK_SECRET_KEY": "Flask application secret key",
    }

    # Optional but recommended variables
    optional_vars = {
        "DEBUG": "Debug mode flag",
        "LOG_LEVEL": "Logging level",
        "HOST": "Server host address",
        "PORT": "Server port number",
    }

    # Check required variables
    missing_required = []
    for var, description in required_vars.items():
        value = os.getenv(var)
        if not value:
            missing_required.append(f"  ❌ {var}: {description}")
        else:
            # Mask sensitive values
            if "TOKEN" in var or "SECRET" in var:
                display_value = value[:10] + "..." if len(value) > 10 else "***"
            else:
                display_value = value
            print(f"  ✅ {var}: {display_value}")

    # Check optional variables
    print(f"\n📋 Optional configuration:")
    for var, description in optional_vars.items():
        value = os.getenv(var)
        if value:
            print(f"  ✅ {var}: {value}")
        else:
            print(f"  ⚪ {var}: Not set (using default)")

    # Report missing required variables
    if missing_required:
        print(f"\n❌ Missing required environment variables:")
        for missing in missing_required:
            print(missing)
        print(
            f"\nPlease check your .env file and ensure all required variables are set."
        )
        return False

    print(f"\n✅ Environment validation successful!")
    return True


async def test_canvas_connection():
    """Quick test of Canvas API connection"""
    print(f"\n🔄 Testing Canvas API connection...")

    try:
        import aiohttp

        canvas_url = os.getenv("CANVAS_API_URL")
        canvas_token = os.getenv("CANVAS_API_TOKEN")

        api_url = f"{canvas_url}/api/v1/users/self"
        headers = {
            "Authorization": f"Bearer {canvas_token}",
            "Content-Type": "application/json",
        }

        async with aiohttp.ClientSession() as session:
            async with session.get(api_url, headers=headers) as response:
                if response.status == 200:
                    user_data = await response.json()
                    print(f"  ✅ Connected as: {user_data.get('name', 'Unknown User')}")
                    return True
                else:
                    print(
                        f"  ⚠️  Connection issue (status {response.status}) - Demo mode will be used"
                    )
                    return True  # Demo mode is acceptable

    except Exception as e:
        print(f"  ⚠️  Connection test failed: {str(e)} - Demo mode will be used")
        return True  # Demo mode is acceptable


def start_application():
    """Start the Flask application"""
    print(f"\n🚀 Starting Flask application...")

    # Import and configure Flask app
    from app import app

    # Get configuration from environment
    host = os.getenv("HOST", "127.0.0.1")
    port = int(os.getenv("PORT", 5000))
    debug = os.getenv("DEBUG", "false").lower() == "true"

    print(f"  🌐 Server: http://{host}:{port}")
    print(f"  🐛 Debug mode: {debug}")
    print(f"  📁 Upload folder: {app.config.get('UPLOAD_FOLDER', 'uploads')}")

    # Start the application
    try:
        app.run(host=host, port=port, debug=debug)
    except KeyboardInterrupt:
        print(f"\n👋 Application stopped by user")
    except Exception as e:
        print(f"\n❌ Application error: {str(e)}")
        sys.exit(1)


def main():
    """Main startup function"""
    print("🎓 Linear Algebra Course Builder - Production Startup")
    print("=" * 60)

    # Validate environment
    if not validate_environment():
        print(f"\n❌ Environment validation failed. Please fix issues and try again.")
        sys.exit(1)

    # Test Canvas connection
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        canvas_ok = loop.run_until_complete(test_canvas_connection())
        if not canvas_ok:
            print(f"\n⚠️  Canvas connection issues detected - proceeding with demo mode")
    finally:
        loop.close()

    # Start application
    start_application()


if __name__ == "__main__":
    main()
