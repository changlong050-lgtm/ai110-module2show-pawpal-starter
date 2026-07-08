import sys
import os
from datetime import datetime, timedelta

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pawpal_system import Owner, Pet, Task, Scheduler


def test_mark_complete_changes_status():
    task = Task("Walk", 30, "high", time=datetime(2026, 7, 7, 9))
    assert task.is_completed() is False

    task.mark_complete()

    assert task.is_completed() is True


def test_add_task_increases_pet_task_count():
    pet = Pet("Snoopy", "Dog")
    assert len(pet.get_tasks()) == 0

    pet.add_task(Task("Walk", 30, "high", time=datetime(2026, 7, 7, 9)))

    assert len(pet.get_tasks()) == 1


# ---- Sorting correctness ----

def test_sort_by_time_returns_chronological_order():
    owner = Owner("Alice")
    pet = Pet("Snoopy", "Dog")
    owner.add_pet(pet)
    scheduler = Scheduler(owner)

    t_noon = Task("Lunch", 15, "medium", time=datetime(2026, 7, 7, 12))
    t_morning = Task("Breakfast", 15, "medium", time=datetime(2026, 7, 7, 8))
    t_evening = Task("Dinner", 15, "medium", time=datetime(2026, 7, 7, 18))
    pet.add_task(t_noon)
    pet.add_task(t_morning)
    pet.add_task(t_evening)

    sorted_tasks = scheduler.sort_by_time(pet.get_tasks())

    assert [t.get_name() for t in sorted_tasks] == ["Breakfast", "Lunch", "Dinner"]


def test_generate_daily_plan_lists_tasks_in_order():
    owner = Owner("Alice")
    pet = Pet("Snoopy", "Dog")
    owner.add_pet(pet)
    scheduler = Scheduler(owner)

    pet.add_task(Task("Dinner", 15, "medium", time=datetime(2026, 7, 7, 18)))
    pet.add_task(Task("Breakfast", 15, "medium", time=datetime(2026, 7, 7, 8)))

    lines = scheduler.generate_daily_plan()

    breakfast_idx = next(i for i, l in enumerate(lines) if "Breakfast" in l)
    dinner_idx = next(i for i, l in enumerate(lines) if "Dinner" in l)
    assert breakfast_idx < dinner_idx


def test_sort_by_time_empty_list():
    owner = Owner("Alice")
    scheduler = Scheduler(owner)
    assert scheduler.sort_by_time([]) == []


# ---- Recurrence logic ----

def test_daily_task_complete_creates_next_day_task():
    pet = Pet("Snoopy", "Dog")
    task = Task("Walk", 30, "high", frequency="daily", time=datetime(2026, 7, 7, 9))
    pet.add_task(task)

    next_task = pet.complete_task(task)

    assert task.is_completed() is True
    assert next_task is not None
    assert next_task.get_time() == datetime(2026, 7, 8, 9)
    assert next_task.is_completed() is False
    assert next_task in pet.get_tasks()
    assert len(pet.get_tasks()) == 2


def test_weekly_task_complete_creates_next_week_task():
    pet = Pet("Snoopy", "Dog")
    task = Task("Groom", 60, "medium", frequency="weekly", time=datetime(2026, 7, 7, 9))
    pet.add_task(task)

    next_task = pet.complete_task(task)

    assert next_task.get_time() == datetime(2026, 7, 14, 9)


def test_one_time_task_complete_does_not_create_new_task():
    pet = Pet("Snoopy", "Dog")
    task = Task("Vet visit", 60, "high", frequency="", time=datetime(2026, 7, 7, 9))
    pet.add_task(task)

    next_task = pet.complete_task(task)

    assert next_task is None
    assert len(pet.get_tasks()) == 1


def test_recurring_task_frequency_case_insensitive():
    pet = Pet("Snoopy", "Dog")
    task = Task("Walk", 30, "high", frequency="Daily", time=datetime(2026, 7, 7, 9))
    pet.add_task(task)

    next_task = pet.complete_task(task)

    assert next_task is not None
    assert next_task.get_time() == datetime(2026, 7, 8, 9)


# ---- Conflict detection ----

def test_detect_conflicts_true_when_duplicate_times():
    owner = Owner("Alice")
    pet = Pet("Snoopy", "Dog")
    owner.add_pet(pet)
    scheduler = Scheduler(owner)

    pet.add_task(Task("Walk", 30, "high", time=datetime(2026, 7, 7, 9)))
    pet.add_task(Task("Feed", 15, "medium", time=datetime(2026, 7, 7, 9)))

    assert scheduler.detect_conflicts() is True


def test_detect_conflicts_false_when_times_unique():
    owner = Owner("Alice")
    pet = Pet("Snoopy", "Dog")
    owner.add_pet(pet)
    scheduler = Scheduler(owner)

    pet.add_task(Task("Walk", 30, "high", time=datetime(2026, 7, 7, 9)))
    pet.add_task(Task("Feed", 15, "medium", time=datetime(2026, 7, 7, 10)))

    assert scheduler.detect_conflicts() is False


def test_detect_conflicts_across_multiple_pets():
    owner = Owner("Alice")
    pet1 = Pet("Snoopy", "Dog")
    pet2 = Pet("Whiskers", "Cat")
    owner.add_pet(pet1)
    owner.add_pet(pet2)
    scheduler = Scheduler(owner)

    pet1.add_task(Task("Walk", 30, "high", time=datetime(2026, 7, 7, 9)))
    pet2.add_task(Task("Feed", 15, "medium", time=datetime(2026, 7, 7, 9)))

    assert scheduler.detect_conflicts() is True


def test_detect_conflicts_no_tasks():
    owner = Owner("Alice")
    scheduler = Scheduler(owner)
    assert scheduler.detect_conflicts() is False


def test_detect_conflicts_ignores_tasks_without_time():
    owner = Owner("Alice")
    pet = Pet("Snoopy", "Dog")
    owner.add_pet(pet)
    scheduler = Scheduler(owner)

    pet.add_task(Task("Walk", 30, "high", time=None))
    pet.add_task(Task("Feed", 15, "medium", time=None))

    assert scheduler.detect_conflicts() is False


# ---- Edge cases ----

def test_filter_incomplete_excludes_completed_tasks():
    owner = Owner("Alice")
    pet = Pet("Snoopy", "Dog")
    owner.add_pet(pet)
    scheduler = Scheduler(owner)

    done_task = Task("Walk", 30, "high", time=datetime(2026, 7, 7, 9))
    done_task.mark_complete()
    pending_task = Task("Feed", 15, "medium", time=datetime(2026, 7, 7, 10))
    pet.add_task(done_task)
    pet.add_task(pending_task)

    incomplete = scheduler.filter_incomplete(pet.get_tasks())

    assert incomplete == [pending_task]


def test_generate_daily_plan_skips_pets_with_no_incomplete_tasks():
    owner = Owner("Alice")
    pet_no_tasks = Pet("Idle", "Cat")
    pet_with_task = Pet("Snoopy", "Dog")
    owner.add_pet(pet_no_tasks)
    owner.add_pet(pet_with_task)
    scheduler = Scheduler(owner)

    pet_with_task.add_task(Task("Walk", 30, "high", time=datetime(2026, 7, 7, 9)))

    lines = scheduler.generate_daily_plan()

    assert not any("Idle" in line for line in lines)
    assert any("Snoopy" in line for line in lines)


def test_owner_add_pet_and_view_pets():
    owner = Owner("Alice")
    pet = Pet("Snoopy", "Dog")

    owner.add_pet(pet)

    assert owner.view_pets() == [pet]


def test_task_getters_and_setters():
    task = Task("Walk", 30, "high", description="Morning walk", frequency="daily",
                time=datetime(2026, 7, 7, 9))

    task.set_name("Run")
    task.set_duration(45)
    task.set_priority("low")
    task.set_description("Evening run")
    task.set_frequency("weekly")
    new_time = datetime(2026, 7, 8, 10)
    task.set_time(new_time)

    assert task.get_name() == "Run"
    assert task.get_duration() == 45
    assert task.get_priority() == "low"
    assert task.get_description() == "Evening run"
    assert task.get_frequency() == "weekly"
    assert task.get_time() == new_time
