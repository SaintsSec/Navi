import json
import click
import os
from tabulate import tabulate
import pyfiglet

command = "bullet"
use = "Bullet Journal App"


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


# Load the journal from a file
try:
    with open("journal.json", "r") as f:
        journal = json.load(f)
except FileNotFoundError:
    journal = {"Future Log": [], "Monthly Log": [],
               "Daily Log": [], "Tasks": []}
except KeyError:
    journal["Tasks"] = []

# Add a fancy header


def headerArt():
    header = pyfiglet.figlet_format("Bullet Journal", font="slant")
    click.echo(click.style(header, fg="cyan", bold=True))

# Display the tasks in each area using tabulate


def display_future_log():
    headers = ["Task", "Priority", "Completed"]
    data = [[task[key] for key in headers] for task in journal["Future Log"]]
    click.echo(tabulate(data, headers=headers, tablefmt="fancy_grid",
               numalign="center", stralign="center", showindex=True))


def display_monthly_log():
    headers = ["Task", "Priority", "Completed"]
    data = [[task[key] for key in headers] for task in journal["Monthly Log"]]
    click.echo(tabulate(data, headers=headers, tablefmt="fancy_grid",
               numalign="center", stralign="center", showindex=True))


def display_daily_log():
    headers = ["Task", "Priority", "Completed"]
    data = []
    for task in journal["Daily Log"]:
        row = []
        for key in headers:
            if key in task:
                row.append(task[key])
            else:
                row.append("")
        data.append(row)
    click.echo(tabulate(data, headers=headers, tablefmt="fancy_grid",
               numalign="center", stralign="center", showindex=True))


def display_tasks():
    headers = ["Task", "Priority", "Completed", "Area"]
    data = []
    for area, tasks in journal.items():
        if area not in ["Future Log", "Monthly Log", "Daily Log"]:
            for task in tasks:
                row = [task.get(key, "") for key in headers[:-1]]
                row.append(area)
                data.append(row)
    click.echo(click.style("\nAll Tasks", fg="cyan", bold=True))
    click.echo(click.style("=========", fg="cyan", bold=True))
    click.echo(tabulate(data, headers=headers, tablefmt="fancy_grid",
               numalign="center", stralign="center", showindex=True))


def display_tasks_by_priority():
    if "Tasks" not in journal:
        journal["Tasks"] = []
    headers = ["Task", "Priority", "Completed"]
    data = [[task[key] for key in headers]
            for task in sorted(journal["Tasks"], key=lambda x: x["Priority"])]
    click.echo(click.style("\nTasks by Priority", fg="cyan", bold=True))
    click.echo(click.style("=================", fg="cyan", bold=True))
    click.echo(tabulate(data, headers=headers, tablefmt="fancy_grid",
               numalign="center", stralign="center", showindex=True))

# Add a task to the appropriate area


def add_task():
    task_name = input("Enter task name: ")
    priority = input("Enter priority (!, !!, or !!!): ")
    area = input(
        f"Enter area ({click.style('F', bold=True)}uture Log, {click.style('M', bold=True)}onthly Log, {click.style('D', bold=True)}aily Log, {click.style('T', bold=True)}asks): ")
    if area == "":
        area = "Tasks"
    if area not in journal:
        journal[area] = []
    if "Tasks" not in journal:
        journal["Tasks"] = []
    task = {"Task": task_name, "Priority": priority, "Completed": "•"}
    journal[area].append(task)

# Edit a task in the appropriate area


def edit_task():
    task_name = input("Enter task name: ")
    current_area = input(
        f"Enter current area ({click.style('F', bold=True)}uture Log, {click.style('M', bold=True)}onthly Log, {click.style('D', bold=True)}aily Log, {click.style('T', bold=True)}asks): ")
    if current_area not in journal:
        click.echo(click.style(
            f"{current_area} area does not exist", fg="red"))
        return
    for task in journal[current_area]:
        if task["Task"] == task_name:
            new_task_name = input("Enter new task name: ")
            new_priority = input("Enter new priority (!, !!, or !!!): ")
            new_area = input(
                f"Enter new area ({click.style('F', bold=True)}uture Log, {click.style('M', bold=True)}onthly Log, {click.style('D', bold=True)}aily Log, {click.style('T', bold=True)}asks): ")
            if new_area == "":
                new_area = "Tasks"
            if new_area not in journal:
                journal[new_area] = []
            task["Task"] = new_task_name
            task["Priority"] = new_priority
            journal[new_area].append(task)
            journal[current_area].remove(task)
            break
    else:
        click.echo(click.style(
            f"{task_name} not found in {current_area}", fg="red"))

# Delete a task from the appropriate area


def delete_task():
    task_name = input("Enter task name: ")
    area = input(
        f"Enter area ({click.style('F', bold=True)}uture Log, {click.style('M', bold=True)}onthly Log, {click.style('D', bold=True)}aily Log, {click.style('T', bold=True)}asks): ")
    if area not in journal:
        click.echo(click.style(f"{area} area does not exist", fg="red"))
        return
    for task in journal[area]:
        if task["Task"] == task_name:
            journal[area].remove(task)
            break
    else:
        click.echo(click.style(f"{task_name} not found in {area}", fg="red"))


def complete_task():
    task_name = input("Enter task name: ")
    area = input(
        f"Enter area ({click.style('F', bold=True)}uture Log, {click.style('M', bold=True)}onthly Log, {click.style('D', bold=True)}aily Log, {click.style('T', bold=True)}asks): ")
    if area not in journal:
        click.echo(click.style(f"{area} area does not exist", fg="red"))
        return
    for task in journal[area]:
        if task["Task"] == task_name:
            task["Completed"] = "X"
            break
    else:
        click.echo(click.style(f"{task_name} not found in {area}", fg="red"))


def display_completed_tasks():
    headers = ["Task", "Priority", "Area"]
    data = []
    for area, tasks in journal.items():
        if area not in ["Future Log", "Monthly Log", "Daily Log"]:
            for task in tasks:
                if task["Completed"] == "X":
                    row = [task[key] for key in headers[:-1]]
                    row.append(area)
                    data.append(row)
    click.echo(tabulate(data, headers=headers, tablefmt="fancy_grid",
               numalign="center", stralign="center", showindex=True))

# Save the journal to a file


def save_journal():
    with open("journal.json", "w") as f:
        json.dump(journal, f)

# Main loop


def run():
    clear_screen()
    headerArt()
    display_tasks()
    while True:
        click.echo(click.style("Menu: ", fg="cyan", bold=True), nl=False)
        click.echo(click.style("\n[1] Add task ", fg="yellow"), nl=False)
        click.echo(click.style("[2] Edit task ", fg="yellow"), nl=False)
        click.echo(click.style("[3] Delete task ", fg="yellow"), nl=False)
        click.echo(click.style("[4] Display tasks ", fg="yellow"), nl=False)
        click.echo(click.style(
            "\n[5] Mark task as completed ", fg="yellow"), nl=False)
        click.echo(click.style(
            "[6] Display completed tasks ", fg="yellow"), nl=False)
        click.echo(click.style(
            "\n[7] Display tasks by priority ", fg="yellow"), nl=False)
        click.echo(click.style("[8] Save journal ", fg="yellow"), nl=False)
        click.echo(click.style("[9] Exit", fg="yellow"))
        choice = input(click.style("\nEnter choice number: ", fg="cyan"))
        if choice == "1":
            add_task()
        elif choice == "2":
            edit_task()
        elif choice == "3":
            delete_task()
        elif choice == "4":
            display_tasks()
        elif choice == "5":
            complete_task()
        elif choice == "6":
            display_completed_tasks()
        elif choice == "7":
            display_tasks_by_priority()
        elif choice == "8":
            save_journal()
        elif choice == "9":
            break
        else:
            click.echo(click.style("Invalid choice", fg="red", bold=True))


if __name__ == "__main__":
    run()
