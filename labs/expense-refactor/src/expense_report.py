"""Expense Report — starter code.

This script works. It reads transactions.csv, categorizes the rows,
and prints a report showing per-category totals.

It also has all of its logic crammed into one big main() function with
hard-coded filenames, a hard-coded category dict, and print() statements
woven into the calculations.

Your job is to refactor this code IN PLACE, by moving the right logic
into the four helper shapes below, in response to the change requests in
the README. Keep everything in this one file.

When you're done, the script should produce the SAME output (TOTAL = $613.87)
on the original inputs — the change requests should not change observable
behavior on the starting CSV.

DO NOT add any external libraries. Standard library only.
"""

import json
from pathlib import Path
import csv
from io import StringIO

# -----------------------------------------------------------------------------
# TODO Part 1 — fill these in. (See README "Part 1 — Add JSON support".)
# -----------------------------------------------------------------------------

def parse_csv(text: str) -> list[dict]:
    rows = []
    reader = csv.DictReader(StringIO(text))

    for row in reader:
        if (
            not row
            or row.get("date") is None
            or row.get("vendor") is None
            or row.get("amount") is None
            or row.get("note") is None
        ):
            continue

        rows.append({
            "date": row["date"],
            "vendor": row["vendor"],
            "amount": float(row["amount"]),
            "note": row["note"],
        })

    return rows


def parse_json(text: str) -> list[dict]:
    data = json.loads(text)

    rows = []
    for row in data:
        rows.append({
            "date": row["date"],
            "vendor": row["vendor"],
            "amount": float(row["amount"]),
            "note": row["note"],
        })

    return rows


# -----------------------------------------------------------------------------
# TODO Part 2 — fill this in. (See README "Part 2 — Configurable categories".)
# -----------------------------------------------------------------------------

def categorize(vendor: str, categories: dict) -> str:
    vendor_upper = vendor.upper()

    for category, keywords in categories.items():
        for keyword in keywords:
            if keyword.upper() in vendor_upper:
                return category

    return "other"

# -----------------------------------------------------------------------------
# TODO Part 3 — fill this in. (See README "Part 3 — A pure pipeline".)
# -----------------------------------------------------------------------------

def build_report(rows: list[dict], categories: dict) -> dict:
    totals = {}

    for row in rows:
        category = categorize(row["vendor"], categories)
        totals[category] = totals.get(category, 0.0) + float(row["amount"])

    return totals
# -----------------------------------------------------------------------------
# main() — I/O lives here. Once Parts 1-3 are done, this should shrink to
# just the I/O glue: read files, call parse_*, call build_report, print.
# Right now it has everything inline.
# -----------------------------------------------------------------------------

def main():
    with open("data/transactions.csv") as f:
        rows = parse_csv(f.read())

    with open("data/categories.json") as f:
        categories = json.load(f)

    totals = build_report(rows, categories)

    print("=== Expense Report ===")
    for cat, total in sorted(totals.items()):
        print(f"  {cat:<15} ${total:>8.2f}")
    print(f"  {'TOTAL':<15} ${sum(totals.values()):>8.2f}")

if __name__ == "__main__":
    main()