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

Describe your app in numbered steps so a reader can follow along without watching a video:

1. <!-- Describe this step -->
2. <!-- Describe this step -->
3. <!-- Describe this step -->
4. <!-- Describe this step -->
5. <!-- Add more steps as needed -->

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
