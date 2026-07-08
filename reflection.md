# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

I will have 4 classes: owner, pet, task, and scheduler. 
Owener can view pets, add tasks. 
Pet owns the task, so it has the method, add task, get task, update task, delete task. 
For the task class, it will has the attribute completed, name, duration, priority, and a method mark_complete. 
Class scheduler, store a reference to the owner. Then it can get all the owner's pets and their tasks to schedule. and the method: generate daily plan() 

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

1/ I was trying to walk through my thoughts with AI, and it asked me """So the scheduler needs access to the tasks, right? Does your diagram show a direct connection from scheduler to task, or does it go through pet?"""
For my current diagram, scheduler has no arrow pointing to the task.  But after second think, I understand the secheduler can have access to the tasks, through the train from owner, pet to tasks. the scheduler knows which owner it's managing for, the owner has multiple pets, each pet has multiple tasks with duration and priority, and the scheduler accesses those tasks by following that chain—owner to pet to task. That way we don't need a direct scheduler-to-task connection, which keeps things cleaner. So I haven't made change to my uml diagram.

2/ for task class, I add description, and frequency attributes, time. after reading the phase 2 insturction. 
 
 question: how should the Scheduler retrieve all tasks from the Owner's pets?
3/ I add contractors and getters and setters for every class,
so that scheduler can have access to the owner and then get the pet and task. scheduler stores owner in its constructor, then uses owner's getter to access pets, then uses pet's getter to access tasks
4/ change the duration attribute to time, so that the scheduler can sort the plan 
5/ I am very confuesd about if the scheduler is for user or for pet. 
My guess is that one scheduler handles all pets for one owner.

At first, I didn't read the app.py and I didn't run the code to see the page. After seeing the page, the project is more clear.

6/ At first, my time attribute in the task class only shows the hour. Later I changed it to be including the year, date and the hour, so I can handle recurring task.


---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?



**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?
Tradeoff: in my scheduler, detect_conflicts compare exact get_time() match, not overlap with duration. Two task start 08:00 and 08:15, dur 30min each will be overlapped, but no flag since times are different.

I detect conflict only using the time because this is a small, personal pet-care scheduler with just a handful of tasks per day, entered manually by the owner. An exact-time-match check is simple and fast (just look for duplicates in a list), and it catches the most common real mistake — accidentally scheduling two tasks for the same slot. Real interval-overlap detection would require sorting tasks by start time and comparing each task's end time against the next one's start time, which is more correct but adds complexity that isn't worth it for this scale of app

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
