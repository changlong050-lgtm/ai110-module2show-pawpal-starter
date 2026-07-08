# PawPal+ Project Reflection

## 1. System Design

### a. Initial Design

I designed four classes: Owner, Pet, Task, and Scheduler. The Owner can view pets and add tasks. The Pet owns tasks and has methods to add, get, update, and delete them. The Task class has attributes for completion status, name, duration, priority, and a mark_complete() method. The Scheduler stores a reference to the Owner, allowing it to access all the owner's pets and their tasks for scheduling. Its main method is generate_daily_plan().

### b. Design Changes

Yes, my design changed during implementation:

1. **Task relationships**: Initially, I wasn't sure if the Scheduler needed a direct connection to Task. An AI assistant asked, "Does the scheduler need to access tasks directly, or through the pet?" This made me realize the Scheduler can access tasks through the chain: Owner → Pet → Task. This keeps the design cleaner without unnecessary direct connections.

2. **Task attributes**: After reading Phase 2 instructions, I added `description`, `frequency`, and `time` attributes to the Task class.

3. **Constructors and accessors**: I added constructors and getter/setter methods to every class so the Scheduler can navigate: Owner → (get pets) → Pet → (get tasks) → Task.

4. **Time attribute**: I changed from just storing the hour to storing the full datetime (year, month, day, hour) to handle recurring tasks properly.

5. **Scheduler scope**: I was confused about whether the Scheduler manages one pet or all pets. After running the app and seeing the UI, I realized one Scheduler handles all pets for one Owner.

---

## 2. Scheduling Logic and Tradeoffs

### a. Constraints and Priorities

My scheduler considers time and task completion status. Time is the most important constraint because it's clear and intuitive—users should complete tasks in chronological order.

### b. Tradeoffs

**Tradeoff**: My conflict detection uses exact time matching, not duration overlap. Two tasks at 08:00 and 08:15 (each 30 minutes) would overlap in reality but won't be flagged as conflicting.

**Why it's reasonable**: This is a small, personal pet-care scheduler with just a handful of daily tasks entered manually by the owner. An exact-time-match check is simple, fast, and catches the most common mistake—scheduling two tasks for the same time slot. Real interval-overlap detection would require sorting tasks and comparing end times, adding complexity that isn't justified for this scale.

---

## 3. AI Collaboration

### a. How You Used AI

I used AI as a programming assistant to help me understand project instructions and explain logic I didn't understand. When designing classes, I discussed which attributes to include and where to place them. I also used AI to help generate tests and debug code. **The most helpful prompts were specific ones** — like asking AI to do something in a specific file using specific context, rather than vague requests.

### b. Judgment and Verification

I rejected several AI suggestions when they didn't match what I asked for:
- When I asked for a `.docx` file, it generated `.md` instead (likely due to previous chat history)
- When I asked for Mermaid.js code, it generated a visual diagram instead of the text code
- When I asked to generate tests in an existing file, it created a new file instead

**I accept AI suggestions only when they match my exact requirements.**

---

---

## 4. Testing and Verification

**a. What you tested**

I wrote 18 pytest tests covering four areas:

- **Sorting correctness** — `sort_by_time()` returns tasks in chronological order regardless of insertion order, `generate_daily_plan()` lists tasks earliest-to-latest, and an empty task list doesn't crash. This matters because the daily plan is the app's core output — if ordering is wrong, the whole schedule is misleading.
- **Recurrence logic** — completing a daily task creates a new task exactly 24 hours later, a weekly task 7 days later, a one-time task creates no follow-up, and frequency matching is case-insensitive ("Daily" vs "daily"). This is the trickiest logic in the system (it returns a new `Task` instead of mutating the old one), so it needed the most direct coverage.
- **Conflict detection** — flags two tasks at the same time (same pet and across different pets), doesn't flag unique times, returns `False` with no tasks, and safely ignores tasks with `time=None`. Conflicts are the main safety check protecting the owner from double-booking, so both true and false cases needed verification.
- **Edge cases** — completed tasks are filtered out of the plan, pets with no pending tasks are skipped in the output, owner-pet relationships work, and every Task getter/setter round-trips correctly.

Each test isolates one behavior so a failure points directly at the broken method rather than requiring me to debug the whole pipeline.

**b. Confidence**

I'm fairly confident (4/5 stars) — all 18 tests pass and they cover the core scheduling paths I actually use in `main.py`. The main gap is that conflict detection uses exact time-equality, not duration/interval overlap (documented as a known tradeoff above), so it won't catch two tasks that partially overlap.

With more time I'd test:
- Duration-based overlap detection (e.g., a 30-minute task starting at 8:00 and another starting at 8:15).
- Tasks with malformed or missing `frequency` values combined with a recurring `time` already in the past.
- Multiple recurring tasks completed in sequence across several days, to confirm chained next-occurrence generation stays correct.
- Large numbers of tasks/pets, to sanity-check `generate_daily_plan()` and `detect_conflicts()` don't degrade unexpectedly.

---

## 5. Reflection

### a. What Went Well

I'm most satisfied with the design of my classes. I clearly understood the logic, created an initial design, and then polished the class attributes and methods as I worked through each phase. This iterative approach helped me build a solid foundation.

### b. What You Would Improve

If I had another iteration, I would read the entire project carefully before starting, which would have saved me a lot of time understanding the requirements. Initially, I only read the project instructions without examining the code. I discovered that running Streamlit to see the UI while developing was very helpful, and I would do that earlier next time.

### c. Key Takeaway

I learned that I must understand the project logic myself first before asking AI to implement it. I need to be aware of each step I'm taking rather than blindly following AI-generated code—I should control the AI, not the other way around. I also learned to better use AI as a guide to walk through projects. When starting a new project, I should read the entire project structure first to understand it. System design is hard to start—figuring out all the classes, attributes, and methods upfront is challenging. It's very helpful to create an initial UML draft and design, then work on it iteratively, polishing and filling in missing attributes and methods as you progress through each phase.

---