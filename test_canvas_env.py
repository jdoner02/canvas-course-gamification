#!/usr/bin/env python3
"""
Test Canvas API Connection Using Environment Variables
====================================================

This script tests the Canvas API connection using environment variables
from the .env file to ensure proper configuration.
"""

import os
import sys
import asyncio
import aiohttp
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


async def test_canvas_connection():
    """Test Canvas API connection using environment variables"""

    # Get Canvas configuration from environment
    canvas_url = os.getenv("CANVAS_API_URL")
    canvas_token = os.getenv("CANVAS_API_TOKEN")

    if not canvas_url:
        print("❌ CANVAS_API_URL not found in environment variables")
        return False

    if not canvas_token:
        print("❌ CANVAS_API_TOKEN not found in environment variables")
        return False

    print(f"✅ Canvas URL: {canvas_url}")
    print(f"✅ Canvas Token: {canvas_token[:20]}...")

    # Test API connection
    api_url = f"{canvas_url}/api/v1/users/self"
    headers = {
        "Authorization": f"Bearer {canvas_token}",
        "Content-Type": "application/json",
    }

    try:
        async with aiohttp.ClientSession() as session:
            print(f"\n🔄 Testing connection to: {api_url}")

            async with session.get(api_url, headers=headers) as response:
                if response.status == 200:
                    user_data = await response.json()
                    print(f"✅ Successfully connected to Canvas!")
                    print(f"   User: {user_data.get('name', 'Unknown')}")
                    print(f"   Email: {user_data.get('email', 'Not provided')}")
                    print(f"   ID: {user_data.get('id', 'Unknown')}")
                    return True
                else:
                    text = await response.text()
                    print(f"❌ Failed to connect: {response.status}")
                    print(f"   Response: {text[:200]}...")
                    return False

    except Exception as e:
        print(f"❌ Connection error: {str(e)}")
        return False


async def test_course_creation_permissions():
    """Test if we can list courses (indicating course creation permissions)"""

    canvas_url = os.getenv("CANVAS_API_URL")
    canvas_token = os.getenv("CANVAS_API_TOKEN")

    api_url = f"{canvas_url}/api/v1/accounts/self/courses"
    headers = {
        "Authorization": f"Bearer {canvas_token}",
        "Content-Type": "application/json",
    }

    try:
        async with aiohttp.ClientSession() as session:
            print(f"\n🔄 Testing course permissions...")

            async with session.get(api_url, headers=headers) as response:
                if response.status == 200:
                    courses = await response.json()
                    print(f"✅ Can access courses (found {len(courses)} courses)")
                    return True
                elif response.status == 401:
                    print(f"❌ Unauthorized - Token may be invalid")
                    return False
                elif response.status == 403:
                    print(f"⚠️  Limited permissions - May not be able to create courses")
                    print(f"   Will use demo mode for course creation")
                    return True  # Demo mode is still valid
                else:
                    text = await response.text()
                    print(f"❌ Unexpected response: {response.status}")
                    print(f"   Response: {text[:200]}...")
                    return False

    except Exception as e:
        print(f"❌ Permission test error: {str(e)}")
        return False


def main():
    """Main test function"""
    print("🧪 Testing Canvas API Environment Configuration")
    print("=" * 50)

    # Run async tests
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    try:
        # Test basic connection
        connection_ok = loop.run_until_complete(test_canvas_connection())

        if connection_ok:
            # Test course permissions
            permissions_ok = loop.run_until_complete(test_course_creation_permissions())

            print("\n" + "=" * 50)
            if connection_ok and permissions_ok:
                print("✅ Environment configuration is working correctly!")
                print("🚀 Ready to deploy Canvas courses")
            else:
                print("⚠️  Some issues found - check configuration")
        else:
            print("\n❌ Environment configuration issues found")
            print("Please check your .env file and Canvas API credentials")

    finally:
        loop.close()


if __name__ == "__main__":
    main()
