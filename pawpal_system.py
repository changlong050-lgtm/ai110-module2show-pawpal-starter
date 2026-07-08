from datetime import timedelta

class Owner:
    def __init__(self, name):
        """Create an owner with a name and an empty pet list."""
        self._name = name
        self._pets = []

    def get_name(self):
        """Return the owner's name."""
        return self._name

    def set_name(self, name):
        """Set the owner's name."""
        self._name = name

    def get_pets(self):
        """Return the owner's list of pets."""
        return self._pets

    def set_pets(self, pets):
        """Replace the owner's list of pets."""
        self._pets = pets

    def add_pet(self, pet):
        """Add a pet to the owner's pet list."""
        self._pets.append(pet)

    def add_task(self, pet, task):
        """Add a task to the given pet."""
        pet.add_task(task)

    def view_pets(self):
        """Return the owner's pets."""
        return self._pets


class Pet:
    def __init__(self, name, species):
        """Create a pet with a name, species, and an empty task list."""
        self._name = name
        self._species = species
        self._tasks = []

    def get_name(self):
        """Return the pet's name."""
        return self._name

    def set_name(self, name):
        """Set the pet's name."""
        self._name = name

    def get_species(self):
        """Return the pet's species."""
        return self._species

    def set_species(self, species):
        """Set the pet's species."""
        self._species = species

    def get_tasks(self):
        """Return the pet's list of tasks."""
        return self._tasks

    def set_tasks(self, tasks):
        """Replace the pet's list of tasks."""
        self._tasks = tasks

    def add_task(self, task):
        """Add a task to the pet's task list."""
        self._tasks.append(task)

    def complete_task(self, task):
        """Mark task done; if recurring, append the returned next-occurrence Task."""
        next_task = task.mark_complete()
        if next_task is not None:
            self._tasks.append(next_task)
        return next_task





class Task:
    def __init__(self, name, duration, priority, description="", frequency="", time=None):
        """Create task. time is a datetime (date+hour), required for recurring logic."""
        self._name = name
        self._duration = duration
        self._priority = priority
        self._description = description
        self._frequency = frequency
        self._time = time
        self._completed = False

    def get_name(self):
        """Return the task's name."""
        return self._name

    def set_name(self, name):
        """Set the task's name."""
        self._name = name

    def get_duration(self):
        """Return the task's duration in minutes."""
        return self._duration

    def set_duration(self, duration):
        """Set the task's duration in minutes."""
        self._duration = duration

    def get_priority(self):
        """Return the task's priority."""
        return self._priority

    def set_priority(self, priority):
        """Set the task's priority."""
        self._priority = priority

    def get_description(self):
        """Return the task's description."""
        return self._description

    def set_description(self, description):
        """Set the task's description."""
        self._description = description

    def get_frequency(self):
        """Return the task's frequency."""
        return self._frequency

    def set_frequency(self, frequency):
        """Set the task's frequency."""
        self._frequency = frequency

    def get_time(self):
        """Return the task's scheduled time."""
        return self._time

    def set_time(self, time):
        """Set the task's scheduled time."""
        self._time = time

    def is_completed(self):
        """Return whether the task is completed."""
        return self._completed

    def mark_complete(self):
        """Mark task done. For daily/weekly tasks, return a new Task instance for the
        next occurrence (same hour, next day/week) instead of mutating this one."""
        self._completed = True
        freq = (self._frequency or "").lower()
        if freq == "daily":
            next_time = self._time + timedelta(days=1)
        elif freq == "weekly":
            next_time = self._time + timedelta(weeks=1)
        else:
            return None
        return Task(
            self._name,
            self._duration,
            self._priority,
            description=self._description,
            frequency=self._frequency,
            time=next_time,
        )


class Scheduler:
    def __init__(self, owner):
        """Create a scheduler for the given owner."""
        self._owner = owner

    def get_owner(self):
        """Return the scheduler's owner."""
        return self._owner

    def set_owner(self, owner):
        """Set the scheduler's owner."""
        self._owner = owner

    def _all_pet_tasks(self):
        """Return a list of (pet, task) pairs across all of the owner's pets."""
        pairs = []
        for pet in self._owner.get_pets():
            for task in pet.get_tasks():
                pairs.append((pet, task))
        return pairs

    def filter_incomplete(self, tasks):
        """Return only the tasks that are not yet completed."""
        return [task for task in tasks if not task.is_completed()]

    def sort_by_time(self, tasks):
        """Return tasks sorted earliest to latest."""
        return sorted(tasks, key=lambda task: task.get_time())

    def generate_daily_plan(self):
        """Return formatted schedule lines grouped by pet, sorted by time."""
        lines = []
        for pet in self._owner.get_pets():
            tasks = self.sort_by_time(self.filter_incomplete(pet.get_tasks()))
            if not tasks:
                continue
            lines.append(f"Daily plan for {pet.get_name()} ({pet.get_species()}):")
            for task in tasks:
                lines.append(f"  At {task.get_time()}, {task.get_name()}.")
            lines.append("")
        return lines

    def sort_by_priority(self):
        """Return all tasks sorted from highest to lowest priority."""
        priority_order = {"high": 0, "medium": 1, "low": 2}
        tasks = [task for _, task in self._all_pet_tasks()]
        return sorted(
            tasks,
            key=lambda task: priority_order.get(task.get_priority().lower(), 99),
        )

    def detect_conflicts(self):
        """Return True if any two tasks share the same scheduled time."""
        tasks = [task for _, task in self._all_pet_tasks()]
        times = [task.get_time() for task in tasks if task.get_time()]
        return len(times) != len(set(times))
