#!/usr/bin/env python3
"""
Test runner script for Canvas Course Gamification
"""

import subprocess
import sys
import os
from pathlib import Path


def run_command(cmd, description):
    """Run a command and report results"""
    print(f"\n{'='*60}")
    print(f"Running: {description}")
    print(f"Command: {' '.join(cmd)}")
    print("=" * 60)

    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.stdout:
        print("STDOUT:")
        print(result.stdout)

    if result.stderr:
        print("STDERR:")
        print(result.stderr)

    if result.returncode == 0:
        print(f"✅ {description} completed successfully")
    else:
        print(f"❌ {description} failed with return code {result.returncode}")

    return result.returncode == 0


def main():
    """Main test runner"""
    # Ensure we're in the project root
    project_root = Path(__file__).parent
    os.chdir(project_root)

    print("Canvas Course Gamification Test Suite")
    print("=" * 60)

    # Check if virtual environment is activated
    if hasattr(sys, "real_prefix") or (
        hasattr(sys, "base_prefix") and sys.base_prefix != sys.prefix
    ):
        print("✅ Virtual environment detected")
    else:
        print("⚠️  Virtual environment not detected")
        if input("Continue anyway? (y/N): ").lower() != "y":
            return 1

    all_passed = True

    # Install/update dependencies
    print("\n🔧 Installing dependencies...")
    if not run_command(
        [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"],
        "Installing dependencies",
    ):
        print("❌ Failed to install dependencies")
        return 1

    # Run code formatting check
    print("\n🎨 Checking code formatting...")
    if not run_command(
        ["python", "-m", "black", "--check", "src/", "tests/"], "Code formatting check"
    ):
        print("⚠️  Code formatting issues found. Run 'black src/ tests/' to fix.")
        all_passed = False

    # Run linting
    print("\n🔍 Running linting...")
    if not run_command(["python", "-m", "flake8", "src/", "tests/"], "Linting check"):
        print("⚠️  Linting issues found")
        all_passed = False

    # Run type checking
    print("\n🔬 Running type checking...")
    if not run_command(["python", "-m", "mypy", "src/"], "Type checking"):
        print("⚠️  Type checking issues found")
        all_passed = False

    # Run unit tests
    print("\n🧪 Running unit tests...")
    if not run_command(
        [
            "python",
            "-m",
            "pytest",
            "tests/unit/",
            "-v",
            "--cov=src",
            "--cov-report=term-missing",
        ],
        "Unit tests",
    ):
        all_passed = False

    # Run integration tests
    print("\n🔗 Running integration tests...")
    if not run_command(
        ["python", "-m", "pytest", "tests/integration/", "-v"], "Integration tests"
    ):
        all_passed = False

    # Validate MATH231 data specifically
    print("\n📊 Validating MATH231 course data...")
    if not run_command(
        ["python", "-m", "src.cli", "validate", "data/math231"],
        "MATH231 data validation",
    ):
        all_passed = False

    # Generate test coverage report
    print("\n📈 Generating coverage report...")
    run_command(["python", "-m", "coverage", "html"], "Coverage report generation")

    # Final summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)

    if all_passed:
        print("🎉 All tests passed!")
        print("✅ Code is ready for deployment")
        return 0
    else:
        print("❌ Some tests failed")
        print("🔧 Please fix the issues before deployment")
        return 1


if __name__ == "__main__":
    sys.exit(main())
