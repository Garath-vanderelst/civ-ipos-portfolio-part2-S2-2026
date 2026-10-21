import dateutil
from dateutil.parser import ParserError
from rich.errors import MarkupError
from src.task import Task
from src.file_handler import save_tasks
import dateutil.parser
from rich import print, box
from rich.console import Console
from rich.table import Table
from datetime import datetime, timedelta


def add_task(tasks, title, description, due_date):
    """
    Add a new task to the task list.

    Args:
        tasks (list): The list of existing Task objects.
        title (str): The title of the new task.
        description (str): A brief description of the task.
        due_date (str): The due date of the task in 'DD-MM-YYYY' format.

    Returns:
        bool: True if the task is added successfully, False otherwise.

    Raises:
        ValueError: If the due date is not in the correct format.

    Side Effects:
        - Saves the updated task list to a file using `save_tasks`.
    """
    # Prevent duplicate tasks
    if any(task.title == title for task in tasks):
        print("Error: A task with this title already exists.")
        return False

    # Validate due date format
    try:
        datetime.strptime(due_date, "%d-%m-%Y")
    except ValueError:
        print("Error: Invalid date format. Use DD-MM-YYYY.")
        return False

    tasks.append(Task(title, description, due_date))
    save_tasks(tasks)
    return True


def delete_task(tasks, title):
    """
    Delete a task from the task list based on its title.

    Args:
        tasks (list): The list of existing Task objects.
        title (str): The title of the task to be deleted.

    Returns:
        bool: True if the task was found and deleted, False otherwise.

    Side Effects:
        - Saves the updated task list to a file using `save_tasks`.
    """
    for task in tasks:
        if task.title == title:
            tasks.remove(task)
            save_tasks(tasks)
            return True
    return False


def list_tasks(tasks, status=None):
    """
    Display tasks in the task list, optionally filtered by status.

    Args:
        tasks (list): The list of existing Task objects.
        status (str, optional): The status to filter tasks
        by (e.g., "pending" or "completed").

    Returns:
        None

    Side Effects:
        - Prints the list of tasks to the console.
    """
    if not status:
        # If status is not set
        filtered = tasks
    else:
        # Filter tasks based on their status
        filtered = []
        for task in tasks:
            if task.status == status:
                filtered.append(task)

    if not filtered:
        print("No tasks found.")
        return

    console = Console()
    table = Table(title="Task Details", box=box.SQUARE)
    table.add_column("Title", style="white", no_wrap=True)
    table.add_column("Description", style="white", no_wrap=True)
    table.add_column("Due Date", no_wrap=True)
    table.add_column("Status", style="white", no_wrap=True)

    rich_table_data = False

    for task in filtered:
        task_date = datetime.strptime(task.due_date, "%d-%m-%Y").date()
        today = datetime.today().date()
        if task.status == "completed":
            date_style = "green"
        elif task_date < today:
            date_style = "red"
        elif task_date <= today + timedelta(days=7):
            date_style = "yellow"
        elif task_date > today + timedelta(days=7):
            date_style = "white"
        else:
            date_style = "white"

        styled_date = f"[{date_style}]{task.due_date}[/{date_style}]"

        try:
            table.add_row(task.title, task.description, styled_date, task.status)
            rich_table_data = True

        except MarkupError:

            print(f"{task.title} | {task.description} | "
            f"Due: {task.due_date} | Status: {task.status}")

    if rich_table_data:
        console.print(table)

def filter_tasks_by_status(tasks, status):
    """
    Filter tasks by their status.

    Args:
        tasks (list): The list of existing Task objects.
        status (str): The status to filter tasks by (e.g., "pending" or "completed").

    Returns:
        list: A list of Task objects that match the specified status.
    """
    return [task for task in tasks if task.status == status]

def validate_date():
    """
    Requests a due date for the item, validates it and returns it.

    Returns:
        str: The due date of the item.
    """
    while True:
        try:
            date_input = input("Due Date (DD-MM-YYYY): ")
            parsed = dateutil.parser.parse(date_input,dayfirst=True,fuzzy=True)

        except ParserError:
            print("Error: Please enter a valid date")

        else:
            return parsed.strftime("%d-%m-%Y")

