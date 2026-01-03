#!/usr/bin/env python3
"""
Phase I: CLI Todo Manager
In-memory task management with command-line interface.
"""
from dataclasses import dataclass
from typing import Optional


# Constants
STATUS_INCOMPLETE = "Incomplete"
STATUS_COMPLETE = "Complete"

# Classes will be defined here
# Main entry point will be here

@dataclass
class Task:
    """Represents a single todo item."""
    id: int
    title: str
    description: str
    status: str  # "Complete" or "Incomplete"


class TaskManager:
    """Manages task storage and operations."""

    def __init__(self) -> None:
        """Initialize task manager with empty storage."""
        self._tasks: dict[int, Task] = {}
        self._next_id: int = 1

    def add_task(self, title: str, description: str) -> tuple[bool, str, int]:
        """Add a new task with validation.

        Returns: (success, message, task_id or 0)
        """
        # Validate title (FR-017, FR-011)
        stripped_title = title.strip()
        if not stripped_title:
            return False, "Title cannot be empty.", 0

        if len(stripped_title) > 200:
            return False, "Title must be 200 characters or less.", 0

        # Validate description (FR-012)
        if len(description) > 1000:
            return False, "Description must be 1000 characters or less.", 0

        # Generate ID (FR-003)
        task_id = self._next_id
        self._next_id += 1

        # Create Task with STATUS_INCOMPLETE
        task = Task(
            id=task_id,
            title=stripped_title,
            description=description,
            status=STATUS_INCOMPLETE
        )

        # Store in _tasks dict
        self._tasks[task_id] = task

        # Return success with ID
        return True, "Task added successfully.", task_id

    def get_all_tasks(self) -> tuple[bool, str, list[Task]]:
        """Get all tasks in insertion order.

        Returns: (success, message, list of tasks)
        """
        # Convert dict values to list (preserves insertion order)
        tasks = list(self._tasks.values())

        # Return success with task list
        return True, "Tasks retrieved successfully.", tasks

    def get_task(self, task_id: int) -> tuple[bool, str, Optional[Task]]:
        """Get a task by ID.

        Returns: (success, message, task or None)
        """
        # Check if task_id exists in _tasks dict
        if task_id in self._tasks:
            # Return (True, "", task) if found
            return True, "", self._tasks[task_id]
        else:
            # Return (False, "Task ID not found. Please enter a valid ID.", None) if not found
            return False, "Task ID not found. Please enter a valid ID.", None

    def update_task(
        self, task_id: int, title: Optional[str], description: Optional[str]
    ) -> tuple[bool, str]:
        """Update task title and/or description.

        Returns: (success, message)
        """
        # Check task exists (use get_task)
        success, msg, task = self.get_task(task_id)
        if not success:
            return False, msg

        # Validate new title if provided (FR-011, FR-017)
        if title is not None:
            stripped_title = title.strip()
            if not stripped_title:
                return False, "Title cannot be empty."

            if len(stripped_title) > 200:
                return False, "Title must be 200 characters or less."

            # Update task title
            task.title = stripped_title

        # Validate new description if provided (FR-012)
        if description is not None:
            if len(description) > 1000:
                return False, "Description must be 1000 characters or less."

            # Update task description
            task.description = description

        # Return success message
        return True, "Task updated successfully."

    def delete_task(self, task_id: int) -> tuple[bool, str]:
        """Delete a task by ID.

        Returns: (success, message)
        """
        # Check task exists
        if task_id not in self._tasks:
            return False, "Task ID not found. Please enter a valid ID."

        # Remove from _tasks dict using del or pop
        del self._tasks[task_id]

        # Return success message with task_id
        return True, f"Task {task_id} deleted successfully."

    def mark_complete(self, task_id: int) -> tuple[bool, str]:
        """Mark a task as complete.

        Returns: (success, message)
        """
        # Check task exists
        success, msg, task = self.get_task(task_id)
        if not success:
            return False, msg

        # Set task.status = STATUS_COMPLETE
        task.status = STATUS_COMPLETE

        # Return success message
        return True, f"Task {task_id} marked as complete."

    def mark_incomplete(self, task_id: int) -> tuple[bool, str]:
        """Mark a task as incomplete.

        Returns: (success, message)
        """
        # Check task exists
        success, msg, task = self.get_task(task_id)
        if not success:
            return False, msg

        # Set task.status = STATUS_INCOMPLETE
        task.status = STATUS_INCOMPLETE

        # Return success message
        return True, f"Task {task_id} marked as incomplete."


class CLI:
    """Command-line interface for todo manager."""

    def __init__(self, task_manager: TaskManager) -> None:
        """Initialize CLI with task manager."""
        self.task_manager = task_manager

    def run(self):
        """Display the main menu and handle user input."""
        while True:
            self.show_menu()
            choice = input("Enter your choice: ").strip()
            if choice == "1":
                self.add_task_ui()
            elif choice == "2":
                self.list_tasks_ui()
            elif choice == "3":
                self.update_task_ui()
            elif choice == "4":
                self.delete_task_ui()
            elif choice == "5":
                self.mark_complete_ui()
            elif choice == "6":
                self.mark_incomplete_ui()
            elif choice == "7":
                print("Exiting...")
                break
            else:
                print("Invalid choice. Please try again.")

    def show_menu(self):
        """Display the main menu options."""
        print("\n--- Todo Manager ---")
        print("1. Add Task")
        print("2. List Tasks")
        print("3. Update Task")
        print("4. Delete Task")
        print("5. Mark Task as Complete")
        print("6. Mark Task as Incomplete")
        print("7. Exit")

    def add_task_ui(self):
        """Handle the 'Add Task' UI flow."""
        print("\n--- Add Task ---")
        title = input("Enter title: ")
        description = input("Enter description: ")
        success, message, _ = self.task_manager.add_task(title, description)
        print(message)

    def list_tasks_ui(self):
        """Handle the 'List Tasks' UI flow."""
        print("\n--- All Tasks ---")
        _, _, tasks = self.task_manager.get_all_tasks()
        if not tasks:
            print("No tasks found.")
        else:
            for task in tasks:
                print(
                    f"ID: {task.id}, Title: {task.title}, "
                    f"Description: {task.description}, Status: {task.status}"
                )

    def update_task_ui(self):
        """Handle the 'Update Task' UI flow."""
        print("\n--- Update Task ---")
        try:
            task_id = int(input("Enter task ID to update: "))
            title = input("Enter new title (or press Enter to skip): ")
            description = input(
                "Enter new description (or press Enter to skip): "
            )
            success, message = self.task_manager.update_task(
                task_id,
                title if title else None,
                description if description else None,
            )
            print(message)
        except ValueError:
            print("Invalid ID. Please enter a number.")

    def delete_task_ui(self):
        """Handle the 'Delete Task' UI flow."""
        print("\n--- Delete Task ---")
        try:
            task_id = int(input("Enter task ID to delete: "))
            success, message = self.task_manager.delete_task(task_id)
            print(message)
        except ValueError:
            print("Invalid ID. Please enter a number.")

    def mark_complete_ui(self):
        """Handle the 'Mark Task as Complete' UI flow."""
        print("\n--- Mark Task as Complete ---")
        try:
            task_id = int(input("Enter task ID to mark as complete: "))
            success, message = self.task_manager.mark_complete(task_id)
            print(message)
        except ValueError:
            print("Invalid ID. Please enter a number.")

    def mark_incomplete_ui(self):
        """Handle the 'Mark Task as Incomplete' UI flow."""
        print("\n--- Mark Task as Incomplete ---")
        try:
            task_id = int(input("Enter task ID to mark as incomplete: "))
            success, message = self.task_manager.mark_incomplete(task_id)
            print(message)
        except ValueError:
            print("Invalid ID. Please enter a number.")