from pawpal_system import Owner, Pet, Task, Scheduler


def main():
    owner = Owner("Alex")

    dog = Pet("Snoopy", "Dog")
    cat = Pet("KT", "Cat")
    owner.add_pet(dog)
    owner.add_pet(cat)

    feed = Task("Feed", 10, "medium", description="Feed breakfast", frequency="daily", time="8 AM")
    walk = Task("Walk", 30, "high", description="Walk around the block", frequency="daily", time="9 AM")
    vet_visit = Task("Vet Visit", 60, "low", description="Annual checkup", frequency="yearly", time="2 PM")

    owner.add_task(cat, feed)
    owner.add_task(dog, walk)
    owner.add_task(dog, vet_visit)

    scheduler = Scheduler(owner)

    print("Today's Schedule")
    print("=================")
    for entry in scheduler.generate_daily_plan():
        print(entry)


if __name__ == "__main__":
    main()
