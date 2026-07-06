import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pawpal_system import Pet, Task


def test_mark_complete_changes_status():
    task = Task("Walk", 30, "high", time="9 AM")
    assert task.is_completed() is False

    task.mark_complete()

    assert task.is_completed() is True


def test_add_task_increases_pet_task_count():
    pet = Pet("Snoopy", "Dog")
    assert len(pet.get_tasks()) == 0

    pet.add_task(Task("Walk", 30, "high", time="9 AM"))

    assert len(pet.get_tasks()) == 1
