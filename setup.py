#!/usr/bin/env python3
"""
Setup script for Canvas Course Gamification Framework.
"""

import os
import sys
import subprocess
from pathlib import Path


def check_python_version():
    """Check if Python version is 3.8 or higher."""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required.")
        print(f"Current version: {sys.version}")
        sys.exit(1)
    print(f"✅ Python {sys.version.split()[0]} detected")


def install_dependencies():
    """Install project dependencies."""
    print("📦 Installing dependencies...")
    try:
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"]
        )
        print("✅ Dependencies installed successfully")
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies")
        sys.exit(1)


def setup_environment():
    """Set up environment file."""
    env_example = Path(".env.example")
    env_file = Path(".env")

    if not env_file.exists() and env_example.exists():
        print("📝 Creating .env file from template...")
        env_file.write_text(env_example.read_text())
        print("✅ .env file created. Please edit it with your Canvas credentials.")
    elif env_file.exists():
        print("✅ .env file already exists")
    else:
        print("⚠️ No .env.example template found")


def main():
    """Run the setup process."""
    print("🚀 Setting up Canvas Course Gamification Framework\n")

    check_python_version()
    install_dependencies()
    setup_environment()

    print("\n🎉 Setup complete!")
    print("\n📋 Next steps:")
    print("1. Edit .env file with your Canvas API credentials")
    print("2. Run: python main.py --help")
    print("3. Check out examples/ directory for sample courses")


if __name__ == "__main__":
    main()
