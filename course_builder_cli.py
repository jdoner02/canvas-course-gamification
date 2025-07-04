#!/usr/bin/env python3
"""
Course Builder CLI - Entry point script
Makes the CLI tool easily accessible
"""

import os
import sys
from pathlib import Path

# Add src to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Import and run the CLI
if __name__ == "__main__":
    # Set up environment
    os.environ['PYTHONPATH'] = str(project_root)
    
    # Import and run CLI
    from src.cli import cli
    cli()
