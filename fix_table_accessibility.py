#!/usr/bin/env python3
"""
Fix all table accessibility issues by making them more explicit
"""

import json
import re


def fix_table_accessibility():
    with open("examples/linear_algebra/pages.json", "r") as f:
        data = json.load(f)

    for i, page in enumerate(data["pages"]):
        body = page.get("body", "")

        # Find and fix all tables
        if "<table" in body:
            print(f"Fixing tables in page {i}: {page.get('title', 'Unknown')}")

            # For the span table, ensure it has proper accessibility
            if "span-table" in body:
                body = re.sub(
                    r"<table class='span-table'><thead><tr><th>([^<]+)</th><th>([^<]+)</th><th>([^<]+)</th></tr></thead><tbody>(.*?)</tbody></table>",
                    r'<table class="span-table" role="table" aria-label="Vector span visualization table"><caption>Table showing the relationship between number of vectors and their span in ℝ³</caption><thead><tr><th scope="col">\1</th><th scope="col">\2</th><th scope="col">\3</th></tr></thead><tbody>\4</tbody></table>',
                    body,
                    flags=re.DOTALL,
                )

            # For the elimination example table
            if "elimination-example" in body:
                body = re.sub(
                    r"<table><thead><tr><th>([^<]+)</th><th>([^<]+)</th><th>([^<]+)</th></tr></thead><tbody>(.*?)</tbody></table>",
                    r'<table role="table" aria-label="Linear system to matrix transformation example"><caption>Example showing conversion from system of equations to augmented matrix form</caption><thead><tr><th scope="col">\1</th><th scope="col">\2</th><th scope="col">\3</th></tr></thead><tbody>\4</tbody></table>',
                    body,
                    flags=re.DOTALL,
                )

            page["body"] = body

    # Write back to file
    with open("examples/linear_algebra/pages.json", "w") as f:
        json.dump(data, f, indent=2)

    print("Fixed table accessibility issues")


if __name__ == "__main__":
    fix_table_accessibility()
