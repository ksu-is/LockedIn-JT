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


def view_assignments(assignments):
    """Display all current assignments sorted by due date."""
    print("\n--- Your Assignments ---")
    if not assignments:
        print("No assignments yet. Add one to get started!")
        return

    sorted_assignments = sorted(assignments, key=lambda x: x["due_date"])
    today = date.today()

    for i, a in enumerate(sorted_assignments, start=1):
        due = datetime.strptime(a["due_date"], "%Y-%m-%d").date()
        days_left = (due - today).days

        if days_left < 0:
            status = "  [OVERDUE]"
        elif days_left == 0:
            status = "  [DUE TODAY]"
        elif days_left == 1:
            status = "  [DUE TOMORROW]"
        elif days_left <= 3:
            status = f"  [Due in {days_left} days]"
        else:
            status = f"  ({days_left} days left)"

        print(f"\n  {i}. {a['name']}")
        print(f"     Class : {a['class']}")
        print(f"     Due   : {a['due_date']}{status}")


def delete_assignment(assignments):
    """Let the user remove a completed or unwanted assignment."""
    view_assignments(assignments)
    if not assignments:
        return

    print("\n--- Delete Assignment ---")
    try:
        choice = int(input("Enter the number of the assignment to delete (0 to cancel): "))
    except ValueError:
        print("Please enter a valid number.")
        return

    sorted_assignments = sorted(assignments, key=lambda x: x["due_date"])

    if choice == 0:
        print("Cancelled.")
        return
    elif 1 <= choice <= len(sorted_assignments):
        removed = sorted_assignments[choice - 1]
        assignments.remove(removed)
        save_assignments(assignments)
        print(f"\n✓ Deleted: '{removed['name']}' ({removed['class']})")
    else:
        print("Invalid selection.")


def show_reminders(assignments):
    """Show urgent reminders for assignments due today or within 3 days."""
    today = date.today()
    urgent = []
    overdue = []

    for a in assignments:
        due = datetime.strptime(a["due_date"], "%Y-%m-%d").date()
        days_left = (due - today).days
        if days_left < 0:
            overdue.append((a, days_left))
        elif days_left <= 3:
            urgent.append((a, days_left))

    if not urgent and not overdue:
        return  # No reminders needed, stay quiet

    print("\n" + "=" * 40)
    print("  REMINDERS")
    print("=" * 40)

    for a, days in overdue:
        print(f"  OVERDUE ({abs(days)}d ago): {a['name']} — {a['class']}")

    for a, days in urgent:
        if days == 0:
            print(f"  DUE TODAY: {a['name']} — {a['class']}")
        elif days == 1:
            print(f"  DUE TOMORROW: {a['name']} — {a['class']}")
        else:
            print(f"  Due in {days} days: {a['name']} — {a['class']}")

    print("=" * 40)


def print_menu():
    """Print the main menu options."""
    print("\n=============================")
    print("       L O C K E D I N       ")
    print("   Your Study Planner App    ")
    print("=============================")
    print("  1. View Assignments")
    print("  2. Add Assignment")
    print("  3. Delete Assignment")
    print("  4. Exit")
    print("=============================")


def main():
    """Main loop for the LockedIn application."""
    print("\nWelcome to LockedIn!")
    assignments = load_assignments()

    # Show reminders automatically on startup
    show_reminders(assignments)

    while True:
        print_menu()
        choice = input("Choose an option (1-4): ").strip()

        if choice == "1":
            view_assignments(assignments)
        elif choice == "2":
            add_assignment(assignments)
        elif choice == "3":
            delete_assignment(assignments)
        elif choice == "4":
            print("\nGoodbye! Stay locked in. 📚\n")
            break
        else:
            print("Invalid choice. Please enter 1, 2, 3, or 4.")


if __name__ == "__main__":
    main()