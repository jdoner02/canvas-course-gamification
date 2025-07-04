#!/usr/bin/env python3
"""
Find pages with table accessibility issues
"""

import json


def find_table_pages():
    with open("examples/linear_algebra/pages.json", "r") as f:
        data = json.load(f)

    for i, page in enumerate(data["pages"]):
        if "<table" in page.get("body", ""):
            print(f"Page {i}: {page.get('title', 'Unknown title')}")
            # Check if table has proper header structure
            body = page.get("body", "")
            if "<th>" not in body:
                print(f"  ❌ Table without proper headers found")
            else:
                print(f"  ✅ Table has headers")


if __name__ == "__main__":
    find_table_pages()
