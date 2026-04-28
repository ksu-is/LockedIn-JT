# LockedIn — Project Roadmap

_Last updated: Sprint 2_

---

## Sprint 1 — Planning & Setup ✅

- [x] Write project description and proposal (LockedIn PDF)
- [x] Define key features: Add, View, Delete, Reminders, Save Data
- [x] Identify target audience (high school/college students)
- [x] Research similar projects (GitHub to-do apps, W3Schools file handling)
- [x] Set up GitHub repository in course organization
- [x] Create initial `README.md` with project overview

---

## Sprint 2 — Core Development (IN PROGRESS)

### Core Features
- [x] Set up project folder structure (`lockedin/`)
- [x] Create `lockedin.py` main application file
- [x] Implement `main()` loop with menu system
- [x] Implement `add_assignment()` — accepts name, class, due date with input validation
- [x] Implement `view_assignments()` — sorted by due date with days-remaining labels
- [x] Implement `delete_assignment()` — remove by selecting from numbered list
- [x] Implement `show_reminders()` — auto-displays overdue + due-within-3-days on startup
- [x] Implement `save_assignments()` / `load_assignments()` — JSON file persistence
- [ ] Test all features manually with sample data
- [ ] Fix any bugs found during testing

### Git Commits (Target: 6+ meaningful commits)
- [x] Commit 1: "Initial project setup — added lockedin.py skeleton with main menu loop and placeholder functions"
- [x] Commit 2: "Implemented add_assignment() with input validation for name, class, and due date format"
- [x] Commit 3: "Implemented view_assignments() with due-date sorting and days-remaining status labels"
- [x] Commit 4: "Implemented delete_assignment() allowing users to remove completed assignments by number"
- [x] Commit 5: "Added show_reminders() to auto-display overdue and upcoming assignments at startup"
- [x] Commit 6: "Added JSON file persistence via load_assignments() and save_assignments() — data now survives between sessions"
- [ ] Commit 7: "Bug fixes and edge case handling from manual testing"
- [ ] Commit 8: "Updated README.md with full usage instructions and file structure"

### Documentation
- [x] Write `README.md` with features, requirements, and how-to-run instructions
- [ ] Add inline code comments to all functions in `lockedin.py`
- [ ] Update `projectroadmap.md` to reflect Sprint 2 progress (this file)

---

## Sprint 3 — Stretch Goals & Polish (PLANNED)

- [ ] Add input to mark assignment as "complete" without deleting it
- [ ] Filter/view assignments by class name
- [ ] Sort assignments by priority (High / Medium / Low) set by user
- [ ] Add color output using `colorama` library (green = fine, yellow = soon, red = overdue)
- [ ] Explore Tkinter GUI version
- [ ] Write unit tests for core functions

---

## Emerging Tasks (added during development)

- [ ] Handle edge case: user enters past date when adding assignment — warn but allow
- [ ] Handle edge case: duplicate assignment names in same class
- [ ] Consider adding an "edit assignment" option (change due date)

---

## Known Issues / Bugs

- None identified yet — will update after manual testing in Sprint 2

---

## Notes

> The `assignments.json` file is auto-created on first run. It should be added to `.gitignore` so personal assignment data isn't committed to the shared repo.
