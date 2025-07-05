#!/usr/bin/env python3
"""
Canvas Course Gamification Framework
Main entry point for the application.
"""

import sys
import os
from pathlib import Path

# Add src to path for imports
project_root = Path(__file__).parent
src_path = project_root / "src"
sys.path.insert(0, str(src_path))


def main():
    """Main application entry point."""
    import typer
    from src.cli import app

    # Run the CLI application
    app()


if __name__ == "__main__":
    main()
