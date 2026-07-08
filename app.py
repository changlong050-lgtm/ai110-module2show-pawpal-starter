from datetime import datetime

import streamlit as st

from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

st.subheader("Quick Demo Inputs (UI only)")
# ORIGINAL (no persistence across refresh, no backend wiring):
# owner_name = st.text_input("Owner name", value="Jordan")
# pet_name = st.text_input("Pet name", value="Mochi")
# species = st.selectbox("Species", ["dog", "cat", "other"])
owner_name = st.text_input("Owner name", value="Jordan", key="owner_name")
pet_name = st.text_input("Pet name", value="Mochi", key="pet_name")
species = st.selectbox("Species", ["dog", "cat", "other"], key="species")

# NEW: keep one Owner object per distinct owner name, each with its own
# pets-by-name dict, in session_state.
# BUG FIX: a single shared Owner object was being renamed via set_name whenever
# the "Owner name" field changed, so a new name silently inherited the previous
# owner's pets (same root cause as the earlier Pet bug). Same fix pattern: look
# up/create by name instead of mutating the shared object.
if "owners_by_name" not in st.session_state:
    st.session_state.owners_by_name = {}

if owner_name not in st.session_state.owners_by_name:
    st.session_state.owners_by_name[owner_name] = {
        "owner": Owner(owner_name),
        "pets_by_name": {},
    }

owner_record = st.session_state.owners_by_name[owner_name]
owner = owner_record["owner"]
pets_by_name = owner_record["pets_by_name"]

if pet_name not in pets_by_name:
    new_pet = Pet(pet_name, species)
    pets_by_name[pet_name] = new_pet
    owner.add_pet(new_pet)

pet = pets_by_name[pet_name]
pet.set_species(species)

st.markdown("### Tasks")
st.caption("Add a few tasks. In your final version, these should feed into your scheduler.")

# ORIGINAL (tasks stored as plain dicts, not backed by Task/Pet classes):
# if "tasks" not in st.session_state:
#     st.session_state.tasks = []
#
# col1, col2, col3 = st.columns(3)
# with col1:
#     task_title = st.text_input("Task title", value="Morning walk")
# with col2:
#     duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
# with col3:
#     priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)
#
# if st.button("Add task"):
#     st.session_state.tasks.append(
#         {"title": task_title, "duration_minutes": int(duration), "priority": priority}
#     )
#
# if st.session_state.tasks:
#     st.write("Current tasks:")
#     st.table(st.session_state.tasks)
# else:
#     st.info("No tasks yet. Add one above.")

col1, col2, col3, col4 = st.columns(4)
with col1:
    task_title = st.text_input("Task title", value="Morning walk", key="task_title")
with col2:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20, key="duration")
with col3:
    priority = st.selectbox("Priority", ["low", "medium", "high"], index=2, key="priority")
with col4:
    task_time_str = st.text_input("Time (YYYY-MM-DD HH:MM)", value="2026-07-07 08:00", key="task_time")

frequency = st.selectbox("Frequency", ["once", "daily", "weekly"], key="frequency")

if st.button("Add task"):
    task_time = datetime.strptime(task_time_str, "%Y-%m-%d %H:%M")
    task = Task(task_title, int(duration), priority, frequency=frequency, time=task_time)
    owner.add_task(pet, task)

if pet.get_tasks():
    st.write("Current tasks:")
    st.table(
        [
            {
                "title": t.get_name(),
                "duration_minutes": t.get_duration(),
                "priority": t.get_priority(),
                "time": t.get_time(),
                "completed": t.is_completed(),
            }
            for t in pet.get_tasks()
        ]
    )
else:
    st.info("No tasks yet. Add one above.")

st.divider()

st.subheader("Build Schedule")

# ORIGINAL (placeholder, no scheduling logic wired up):
# st.caption("This button should call your scheduling logic once you implement it.")
#
# if st.button("Generate schedule"):
#     st.warning(
#         "Not implemented yet. Next step: create your scheduling logic (classes/functions) and call it here."
#     )
#     st.markdown(
#         """
# Suggested approach:
# 1. Design your UML (draft).
# 2. Create class stubs (no logic).
# 3. Implement scheduling behavior.
# 4. Connect your scheduler here and display results.
# """
#     )

if st.button("Generate schedule"):
    scheduler = Scheduler(owner)
    plan_lines = scheduler.generate_daily_plan()
    if plan_lines:
        st.markdown("\n".join(f"- {line}" if line else "" for line in plan_lines))
    else:
        st.info("No pending tasks to schedule.")

    if scheduler.detect_conflicts():
        st.warning("Conflict detected: two or more tasks share the same time.")

    st.write("Tasks by priority:")
    st.table(
        [
            {"title": t.get_name(), "priority": t.get_priority(), "time": t.get_time()}
            for t in scheduler.sort_by_priority()
        ]
    )
