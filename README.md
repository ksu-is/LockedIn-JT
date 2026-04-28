# LockedIn 📚
**A Simple Python Study Planner and Reminder App**

LockedIn is a command-line application that helps students organize assignments, track due dates, and receive automatic reminders — no internet or account required.

---

## Features
- **Add assignments** — store name, class, and due date
- **View assignments** — sorted by due date with days-remaining labels
- **Delete assignments** — remove completed or cancelled work
- **Auto reminders** — overdue and upcoming tasks shown at startup
- **Persistent storage** — assignments saved to `assignments.json` between sessions

---

## Requirements
- Python 3.7 or higher
- No external libraries needed (uses only the Python standard library)

---

## How to Run

```bash
python lockedin.py
```

Follow the on-screen menu to add, view, or delete assignments.

---

## File Structure

```
lockedin/
├── lockedin.py        # Main application
├── assignments.json   # Auto-created data file (do not delete)
└── README.md
```

---

## Future Plans
- Sort/filter by class or priority
- Color-coded urgency levels
- GUI version using Tkinter
- Export to CSV or PDF
