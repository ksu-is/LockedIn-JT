"""
LockedIn - A Simple Python Study Planner and Reminder App
A command-line tool for students to manage assignments and due dates.
"""

import json
import os
from datetime import datetime, date


DATA_FILE = "assignments.json"


def load_assignments():
    """Load assignments from the JSON file. Returns empty list if file doesn't exist."""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []


def save_assignments(assignments):
    """Save the current list of assignments to the JSON file."""
    with open(DATA_FILE, "w") as f:
        json.dump(assignments, f, indent=2)


def add_assignment(assignments):
    """Prompt the user to add a new assignment."""
    print("\n--- Add New Assignment ---")
    name = input("Assignment name: ").strip()
    if not name:
        print("Assignment name cannot be empty.")
        return

    class_name = input("Class name: ").strip()
    if not class_name:
        print("Class name cannot be empty.")
        return

    due_date_str = input("Due date (YYYY-MM-DD): ").strip()
    try:
        due_date = datetime.strptime(due_date_str, "%Y-%m-%d").date()
    except ValueError:
        print("Invalid date format. Please use YYYY-MM-DD (e.g. 2025-05-15).")
        return

    assignment = {
        "name": name,
        "class": class_name,
        "due_date": due_date_str,
        "added_on": str(date.today())
    }
    assignments.append(assignment)
    save_assignments(assignments)
    print(f"\n✓ Added: '{name}' for {class_name}, due {due_date_str}.")


