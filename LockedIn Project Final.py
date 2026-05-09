"""
LockedIn - A Simple Python Study Planner and Reminder App
Sprint 3: Added mark-complete, filter by class, priority levels, and color output.
"""

import json
import os
from datetime import datetime, date

try:
    from colorama import init, Fore, Style
    init(autoreset=True)
    COLOR = True
except ImportError:
    COLOR = False

DATA_FILE = "assignments.json"
PRIORITIES = {"1": "High", "2": "Medium", "3": "Low"}
PRIORITY_ORDER = {"High": 0, "Medium": 1, "Low": 2}

def red(s):    return (Fore.RED + s + Style.RESET_ALL) if COLOR else s
def yellow(s): return (Fore.YELLOW + s + Style.RESET_ALL) if COLOR else s
def green(s):  return (Fore.GREEN + s + Style.RESET_ALL) if COLOR else s
def cyan(s):   return (Fore.CYAN + s + Style.RESET_ALL) if COLOR else s
def bold(s):   return (Style.BRIGHT + s + Style.RESET_ALL) if COLOR else s

def load_assignments():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []

def save_assignments(assignments):
    with open(DATA_FILE, "w") as f:
        json.dump(assignments, f, indent=2)

def add_assignment(assignments):
    print(bold("\n--- Add New Assignment ---"))
    name = input("Assignment name: ").strip()
    if not name:
        print(red("Assignment name cannot be empty.")); return
    class_name = input("Class name: ").strip()
    if not class_name:
        print(red("Class name cannot be empty.")); return
    due_date_str = input("Due date (YYYY-MM-DD): ").strip()
    try:
        due_date = datetime.strptime(due_date_str, "%Y-%m-%d").date()
    except ValueError:
        print(red("Invalid date format. Use YYYY-MM-DD.")); return
    if due_date < date.today():
        confirm = input(yellow("Warning: that date is in the past. Add anyway? (y/n): "))
        if confirm.lower() != "y":
            print("Cancelled."); return
    print("Priority: 1=High  2=Medium  3=Low")
    priority = PRIORITIES.get(input("Choose priority (1/2/3, default=2): ").strip() or "2", "Medium")
    assignment = {"name": name, "class": class_name, "due_date": due_date_str,
                  "priority": priority, "completed": False, "added_on": str(date.today())}
    assignments.append(assignment)
    save_assignments(assignments)
    print(green(f"\n✓ Added: '{name}' for {class_name}, due {due_date_str} [{priority} priority]."))

def _days_label(days_left):
    if days_left < 0:   return red(f"[OVERDUE {abs(days_left)}d]")
    elif days_left == 0: return red("[DUE TODAY]")
    elif days_left == 1: return yellow("[DUE TOMORROW]")
    elif days_left <= 3: return yellow(f"[Due in {days_left} days]")
    else:                return green(f"({days_left} days left)")

def view_assignments(assignments, filter_class=None, show_completed=False):
    print(bold("\n--- Your Assignments ---"))
    filtered = [a for a in assignments if not a.get("completed", False) or show_completed]
    if filter_class:
        filtered = [a for a in filtered if a["class"].lower() == filter_class.lower()]
    if not filtered:
        print("No assignments to display."); return
    sorted_a = sorted(filtered, key=lambda x: (x.get("completed", False), x["due_date"],
                                                PRIORITY_ORDER.get(x.get("priority","Medium"),1)))
    today = date.today()
    for i, a in enumerate(sorted_a, start=1):
        due = datetime.strptime(a["due_date"], "%Y-%m-%d").date()
        days_left = (due - today).days
        done_mark = green("✓ DONE  ") if a.get("completed") else ""
        plabel = {"High": red("[HIGH]"), "Medium": yellow("[MED]"), "Low": cyan("[LOW]")}.get(a.get("priority","Medium"),"")
        print(f"\n  {i}. {bold(a['name'])} {done_mark}{plabel}")
        print(f"     Class : {a['class']}")
        print(f"     Due   : {a['due_date']}  {_days_label(days_left)}")

def mark_complete(assignments):
    active = [a for a in assignments if not a.get("completed", False)]
    if not active:
        print("No active assignments to mark complete."); return
    print(bold("\n--- Mark Assignment Complete ---"))
    sorted_active = sorted(active, key=lambda x: x["due_date"])
    today = date.today()
    for i, a in enumerate(sorted_active, start=1):
        due = datetime.strptime(a["due_date"], "%Y-%m-%d").date()
        print(f"  {i}. {a['name']} ({a['class']}) — {_days_label((due-today).days)}")
    try:
        choice = int(input("\nEnter number to mark complete (0 to cancel): "))
    except ValueError:
        print(red("Invalid input.")); return
    if choice == 0:
        print("Cancelled."); return
    elif 1 <= choice <= len(sorted_active):
        target = sorted_active[choice - 1]
        for a in assignments:
            if a["name"]==target["name"] and a["class"]==target["class"] and a["due_date"]==target["due_date"]:
                a["completed"] = True; break
        save_assignments(assignments)
        print(green(f"\n✓ Marked complete: '{target['name']}' ({target['class']})"))
    else:
        print(red("Invalid selection."))

def filter_by_class(assignments):
    classes = sorted(set(a["class"] for a in assignments if not a.get("completed", False)))
    if not classes:
        print("No active assignments to filter."); return
    print(bold("\n--- Filter by Class ---"))
    for i, c in enumerate(classes, start=1):
        print(f"  {i}. {c}")
    try:
        choice = int(input("\nSelect class number (0 to cancel): "))
    except ValueError:
        print(red("Invalid input.")); return
    if choice == 0:
        print("Cancelled.")
    elif 1 <= choice <= len(classes):
        view_assignments(assignments, filter_class=classes[choice - 1])
    else:
        print(red("Invalid selection."))

def delete_assignment(assignments):
    print(bold("\n--- Delete Assignment ---"))
    sorted_all = sorted(assignments, key=lambda x: x["due_date"])
    if not sorted_all:
        print("No assignments to delete."); return
    today = date.today()
    for i, a in enumerate(sorted_all, start=1):
        due = datetime.strptime(a["due_date"], "%Y-%m-%d").date()
        done = green(" [DONE]") if a.get("completed") else ""
        print(f"  {i}. {a['name']} ({a['class']}) — {_days_label((due-today).days)}{done}")
    try:
        choice = int(input("\nEnter number to delete (0 to cancel): "))
    except ValueError:
        print(red("Please enter a valid number.")); return
    if choice == 0:
        print("Cancelled.")
    elif 1 <= choice <= len(sorted_all):
        removed = sorted_all[choice - 1]
        assignments.remove(removed)
        save_assignments(assignments)
        print(green(f"\n✓ Deleted: '{removed['name']}' ({removed['class']})"))
    else:
        print(red("Invalid selection."))

def show_reminders(assignments):
    today = date.today()
    urgent, overdue = [], []
    for a in assignments:
        if a.get("completed"): continue
        due = datetime.strptime(a["due_date"], "%Y-%m-%d").date()
        days_left = (due - today).days
        if days_left < 0:    overdue.append((a, days_left))
        elif days_left <= 3: urgent.append((a, days_left))
    if not urgent and not overdue: return
    print("\n" + bold("=" * 44))
    print(bold("             REMINDERS"))
    print(bold("=" * 44))
    for a, days in overdue:
        print(red(f"  OVERDUE ({abs(days)}d ago): {a['name']} — {a['class']}"))
    for a, days in urgent:
        if days == 0:   print(red(f"  DUE TODAY:    {a['name']} — {a['class']}"))
        elif days == 1: print(yellow(f"  DUE TOMORROW: {a['name']} — {a['class']}"))
        else:           print(yellow(f"  Due in {days} days: {a['name']} — {a['class']}"))
    print(bold("=" * 44))

def print_menu():
    print(bold("\n================================"))
    print(bold("        L O C K E D I N        "))
    print(bold("================================"))
    print("  1. View All Assignments")
    print("  2. Add Assignment")
    print("  3. Mark Assignment Complete")
    print("  4. Filter Assignments by Class")
    print("  5. Delete Assignment")
    print("  6. View Completed Assignments")
    print("  7. Exit")
    print(bold("================================"))

def main():
    print(bold("\nWelcome to LockedIn! 📚"))
    if not COLOR:
        print("(Tip: install colorama for colored output: pip install colorama)")
    assignments = load_assignments()
    show_reminders(assignments)
    while True:
        print_menu()
        choice = input("Choose an option (1-7): ").strip()
        if   choice == "1": view_assignments(assignments)
        elif choice == "2": add_assignment(assignments)
        elif choice == "3": mark_complete(assignments)
        elif choice == "4": filter_by_class(assignments)
        elif choice == "5": delete_assignment(assignments)
        elif choice == "6": view_assignments(assignments, show_completed=True)
        elif choice == "7": print(green("\nGoodbye! Stay locked in. 📚\n")); break
        else: print(red("Invalid choice. Please enter 1–7."))

if __name__ == "__main__":
    main()
