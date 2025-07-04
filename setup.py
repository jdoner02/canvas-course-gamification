"""
Canvas Course Gamification Framework

A comprehensive Python framework for creating and deploying gamified courses to Canvas LMS
with automated skill trees, XP systems, and mastery-based learning progressions.
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README for long description
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

# Read requirements
requirements = (
    (this_directory / "requirements.txt").read_text(encoding="utf-8").splitlines()
)
requirements = [
    req.strip() for req in requirements if req.strip() and not req.startswith("#")
]

setup(
    name="canvas-course-gamification",
    version="1.0.0",
    description="Framework for creating gamified Canvas LMS courses with skill trees and XP systems",
    long_description=long_description,
    long_description_content_type="text/markdown",
    # Author information
    author="Canvas Course Gamification Contributors",
    author_email="your-email@example.com",
    # Project URLs
    url="https://github.com/yourusername/canvas-course-gamification",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/canvas-course-gamification/issues",
        "Source": "https://github.com/yourusername/canvas-course-gamification",
        "Documentation": "https://github.com/yourusername/canvas-course-gamification/wiki",
        "Changelog": "https://github.com/yourusername/canvas-course-gamification/blob/main/CHANGELOG.md",
    },
    # Package configuration
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    # Include non-Python files
    include_package_data=True,
    package_data={
        "": [
            "*.yml",
            "*.yaml",
            "*.json",
            "*.md",
            "*.txt",
            "config/*",
            "examples/*",
            "templates/*",
        ],
    },
    # Dependencies
    install_requires=requirements,
    # Extra dependencies for different use cases
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
            "black>=23.7.0",
            "flake8>=6.0.0",
            "mypy>=1.5.0",
            "pre-commit>=3.0.0",
        ],
        "docs": [
            "sphinx>=7.1.0",
            "sphinx-rtd-theme>=1.3.0",
            "myst-parser>=2.0.0",
        ],
        "analytics": [
            "pandas>=2.0.0",
            "matplotlib>=3.7.0",
            "seaborn>=0.12.0",
        ],
        "all": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
            "black>=23.7.0",
            "flake8>=6.0.0",
            "mypy>=1.5.0",
            "sphinx>=7.1.0",
            "sphinx-rtd-theme>=1.3.0",
            "pandas>=2.0.0",
            "matplotlib>=3.7.0",
            "seaborn>=0.12.0",
        ],
    },
    # Python version requirement
    python_requires=">=3.8",
    # PyPI classification
    classifiers=[
        # Development Status
        "Development Status :: 5 - Production/Stable",
        # Intended Audience
        "Intended Audience :: Education",
        "Intended Audience :: Developers",
        # Topic
        "Topic :: Education",
        "Topic :: Education :: Computer Aided Instruction (CAI)",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Software Development :: Libraries :: Python Modules",
        # License
        "License :: OSI Approved :: MIT License",
        # Programming Language
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        # Operating System
        "Operating System :: OS Independent",
        # Framework
        "Framework :: Flask",
        "Framework :: Django",
    ],
    # Keywords for discovery
    keywords=[
        "canvas",
        "lms",
        "gamification",
        "education",
        "elearning",
        "skill-tree",
        "xp-system",
        "badges",
        "mastery-learning",
        "instructional-design",
        "course-builder",
        "educational-technology",
    ],
    # Entry points for command-line tools
    entry_points={
        "console_scripts": [
            "canvas-gamify=src.deploy:main",
            "canvas-validate=src.validators:main",
        ],
    },
    # Project maturity
    zip_safe=False,
)
