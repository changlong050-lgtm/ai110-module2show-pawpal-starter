# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.


## 🖥️ Sample Output

Paste a sample of your app's CLI or Streamlit output here so a reader can see what a generated plan looks like:

```
Today's Schedule
=================
Daily plan for Snoopy (Dog):
  At 2 PM, Vet Visit.
  At 9 AM, Walk.

Daily plan for KT (Cat):
  At 8 AM, Feed.
```

## 🧪 Testing PawPal+

### Run Tests

```bash
# Run the full test suite:
python -m pytest
```

### What We Test

Our test suite covers four main areas:

1. **Sorting Correctness** — Tasks are ordered chronologically by time, even when added out of order. Edge cases include empty task lists.

2. **Recurrence Logic** — Daily and weekly tasks automatically create new instances when marked complete, with the correct due date (24 hours or 7 days later). One-time tasks don't generate follow-ups.

3. **Conflict Detection** — The system identifies scheduling conflicts when two tasks share the same time, even across different pets. Tasks without times are handled safely.

4. **Edge Cases** — Incomplete task filtering, pets with no pending tasks, owner-pet relationships, and getter/setter validation.

### Test Results
================================================== test session starts ===================================================
platform win32 -- Python 3.14.5, pytest-9.0.3, pluggy-1.6.0
rootdir: C:\Users\at252\OneDrive\Documents\ai110-module2show-pawpal-starter
plugins: anyio-4.13.0
collected 18 items
tests\test_pawpal.py ..................                                                                             [100%]
=================================================== 18 passed in 0.08s ===================================================

### Confidence Level

⭐⭐⭐⭐ (4 stars) — The system handles core scheduling logic and edge cases reliably.


## 📐 Smarter Scheduling

> Fill in once you've implemented scheduling logic.

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | | e.g., by priority, duration |
| Filtering | | e.g., skip tasks if time runs out |
| Conflict handling | | e.g., overlapping time slots |
| Recurring tasks | | e.g., daily vs. weekly |

## 📸 Demo Walkthrough

### Main features

- Add an owner and one or more pets.
- Add tasks to a pet (name, duration, priority, description, frequency, time).
- Generate a sorted daily plan across all pets.
- Detect scheduling conflicts (two tasks at the same time).
- Mark a task complete — recurring tasks (daily/weekly) automatically create their next occurrence.

### Example workflow

1. Create an owner (`Owner("Alex")`) and add a pet (`Pet("Snoopy", "Dog")`).
2. Add a task to that pet, e.g. a daily "Walk" at 9 AM (`owner.add_task(dog, walk)`).
3. Add a second pet with a task scheduled at the same time as an existing task, to see conflict detection in action.
4. Create a `Scheduler(owner)` and call `generate_daily_plan()` to view today's schedule.
5. Call `detect_conflicts()` to check for overlapping tasks before finalizing the plan.
6. Mark a recurring task complete (`pet.complete_task(task)`) and confirm a new Task for the next day/week appears in the pet's task list.

### Key Scheduler behaviors shown

- **Sorting** — `sort_by_time()` orders each pet's tasks earliest to latest before display.
- **Filtering** — `filter_incomplete()` drops finished tasks out of the daily plan.
- **Conflict warnings** — `detect_conflicts()` returns `True` when two tasks (even across different pets) share the same time, e.g. "Vet Visit" and "Grooming" both at 2 PM.
- **Recurrence** — `mark_complete()` on a daily/weekly task returns a new `Task` instance one day/week later; one-time tasks return `None`.

### Sample CLI output (from `main.py`)

```
Today's Schedule
=================
Daily plan for Snoopy (Dog):
  At 2026-07-07 09:00:00, Walk.
  At 2026-07-07 14:00:00, Vet Visit.

Daily plan for KT (Cat):
  At 2026-07-07 08:00:00, Feed.
  At 2026-07-07 14:00:00, Grooming.

⚠️  Conflict detected: two or more tasks are scheduled at the same time!
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
