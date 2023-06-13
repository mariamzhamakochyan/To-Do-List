from datetime import datetime, timedelta

tasks = []

def add_task():
    task = input("Enter a new task: ")
    deadline = input("Enter the task deadline (YYYY-MM-DD HH:MM): ")
    deadline = datetime.strptime(deadline, "%Y-%m-%d %H:%M")
    tasks.append({"task": task, "deadline": deadline, "completed": False})
    print("Task added successfully!")

def delete_task():
    view_tasks()
    if not tasks:
        return

    task_number = int(input("Enter the task number to delete: "))
    if task_number <= 0 or task_number > len(tasks):
        print("Invalid task number.")
    else:
        removed_task = tasks.pop(task_number - 1)
        print(f"Task '{removed_task['task']}' removed successfully!")

def modify_task():
    view_tasks()
    if not tasks:
        return

    task_number = int(input("Enter the task number to modify: "))
    if task_number <= 0 or task_number > len(tasks):
        print("Invalid task number.")
    else:
        task = tasks[task_number - 1]
        new_task = input("Enter the new task: ")
        task["task"] = new_task
        print("Task modified successfully!")

def mark_task_as_completed():
    view_tasks()
    if not tasks:
        return

    task_number = int(input("Enter the task number to mark as completed: "))
    if task_number <= 0 or task_number > len(tasks):
        print("Invalid task number.")
    else:
        task = tasks[task_number - 1]
        if not task["completed"]:
            task["completed"] = True
            print("Task marked as completed!")
        else:
            print("Task is already marked as completed.")

def view_tasks():
    if not tasks:
        print("No tasks in the list.")
    else:
        print("Tasks:")
        for index, task in enumerate(tasks):
            status = "[completed]" if task["completed"] else "[incomplete]"
            deadline = task["deadline"]
            time_remaining = deadline - datetime.now()
            if time_remaining < timedelta(days=1) and not task["completed"]:
                if time_remaining < timedelta(hours=1):
                    print(f"{index+1}. {status} {task['task']} (Deadline approaching! Less than an hour remaining)")
                else:
                    print(f"{index+1}. {status} {task['task']} (Deadline tomorrow!)")
            else:
                print(f"{index+1}. {status} {task['task']}")

def show_task_stats():
    total_tasks = len(tasks)
    completed_tasks = sum(task["completed"] for task in tasks)
    uncompleted_tasks = total_tasks - completed_tasks
    print(f"Total tasks: {total_tasks}")
    print(f"Completed tasks: {completed_tasks}")
    print(f"Uncompleted tasks: {uncompleted_tasks}")

def check_deadline_approaching():
    for task in tasks:
        if not task["completed"]:
            time_remaining = task["deadline"] - datetime.now()
            if time_remaining < timedelta(hours=1) and time_remaining > timedelta():
                print(f"Task '{task['task']}' deadline is approaching! Less than an hour remaining.")

def main():
    while True:
        print("\n       ~To-Do List~        ")
        print("1. Add Task")
        print("2. View Tasks")
        print("3. Modify Task")
        print("4. Delete Task")
        print("5. Mark Task as Completed")
        print("6. Show Task Statistics")
        print("7. Check Deadline Approaching")
        print("8. Exit")
        choice = input("Enter your choice (1-8): ")

        if choice == "1":
            add_task()
        elif choice == "2":
            view_tasks()
        elif choice == "3":
            modify_task()
        elif choice == "4":
            delete_task()
        elif choice == "5":
            mark_task_as_completed()
        elif choice == "6":
            show_task_stats()
        elif choice == "7":
            check_deadline_approaching()
        elif choice == "8":
            print("Exit!")
            break
        else:
            print("Try again.")

if __name__ == "__main__":
    main()
