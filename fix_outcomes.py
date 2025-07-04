#!/usr/bin/env python3
"""
Quick script to add title fields to outcomes
"""

import json
import sys


def fix_outcomes(file_path):
    with open(file_path, "r") as f:
        data = json.load(f)

    # Add title field to each outcome (copy from name field)
    for outcome in data["outcomes"]:
        if "name" in outcome and "title" not in outcome:
            outcome["title"] = outcome["name"]

    # Write back to file
    with open(file_path, "w") as f:
        json.dump(data, f, indent=2)

    print(f"Fixed {len(data['outcomes'])} outcomes in {file_path}")


if __name__ == "__main__":
    fix_outcomes("examples/linear_algebra/outcomes.json")
