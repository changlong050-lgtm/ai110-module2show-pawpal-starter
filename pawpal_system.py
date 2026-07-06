class Owner:
    def __init__(self, name):
        self.name = name
        self.pets = []

    def add_pet(self, pet):
        pass

    def add_task(self, pet, task):
        pass

    def view_pets(self):
        pass


class Pet:
    def __init__(self, name, species):
        self.name = name
        self.species = species
        self.tasks = []

    def add_task(self, task):
        pass

    def get_tasks(self):
        pass


class Task:
    def __init__(self, name, duration, priority):
        self.name = name
        self.duration = duration
        self.priority = priority
        self.completed = False

    def mark_complete(self):
        pass


class Scheduler:
    def __init__(self, owner):
        self.owner = owner

    def generate_daily_plan(self):
        pass

    def sort_by_priority(self):
        pass

    def detect_conflicts(self):
        pass
