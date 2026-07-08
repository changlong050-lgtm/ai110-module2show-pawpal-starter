from datetime import datetime

from pawpal_system import Owner, Pet, Task, Scheduler


def main():
    owner = Owner("Alex")

    dog = Pet("Snoopy", "Dog")
    cat = Pet("KT", "Cat")
    owner.add_pet(dog)
    owner.add_pet(cat)

    today = datetime(2026, 7, 7)
    feed = Task("Feed", 10, "medium", description="Feed breakfast", frequency="daily",
                time=today.replace(hour=8))
    walk = Task("Walk", 30, "high", description="Walk around the block", frequency="daily",
                time=today.replace(hour=9))
    vet_visit = Task("Vet Visit", 60, "low", description="Annual checkup", frequency="yearly",
                      time=today.replace(hour=14))
    grooming = Task("Grooming", 45, "medium", description="Trim nails", frequency="weekly",
                     time=today.replace(hour=14))

    owner.add_task(cat, feed)
    owner.add_task(dog, walk)
    owner.add_task(dog, vet_visit)
    owner.add_task(cat, grooming)  # same time as vet_visit -> triggers a conflict

    scheduler = Scheduler(owner)

    print("Today's Schedule")
    print("=================")
    for entry in scheduler.generate_daily_plan():
        print(entry)

    if scheduler.detect_conflicts():
        print("⚠️  Conflict detected: two or more tasks are scheduled at the same time!")
    else:
        print("No scheduling conflicts found.")


if __name__ == "__main__":
    main()
