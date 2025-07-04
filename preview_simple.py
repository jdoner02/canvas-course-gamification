#!/usr/bin/env python3
"""
Simple preview generator script
"""

import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from src.preview_generator import PreviewGenerator


def main():
    if len(sys.argv) != 3:
        print("Usage: python preview_simple.py <data_path> <output_path>")
        sys.exit(1)

    data_path = sys.argv[1]
    output_path = sys.argv[2]

    print(f"Generating preview: {data_path} -> {output_path}")

    generator = PreviewGenerator(data_path, output_path)
    generator.load_course_data()
    generator.generate_preview()

    print(f"Preview generated: {output_path}")


if __name__ == "__main__":
    main()
