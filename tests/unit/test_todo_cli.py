import unittest
from unittest.mock import patch, call
from io import StringIO
import sys

from src.todo_cli import TaskManager, CLI, Task


class TestCLI(unittest.TestCase):
    def setUp(self):
        """Set up a new TaskManager and CLI for each test."""
        self.task_manager = TaskManager()
        self.cli = CLI(self.task_manager)

    def test_add_task_ui(self):
        """Test the 'Add Task' UI flow."""
        with patch("builtins.input", side_effect=["Test Title", "Test Description"]):
            with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
                self.cli.add_task_ui()
                self.assertIn("Task added successfully.", mock_stdout.getvalue())
        
        _, _, tasks = self.task_manager.get_all_tasks()
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0].title, "Test Title")
        self.assertEqual(tasks[0].description, "Test Description")

    def test_list_tasks_ui_no_tasks(self):
        """Test listing tasks when there are no tasks."""
        with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            self.cli.list_tasks_ui()
            self.assertIn("No tasks found.", mock_stdout.getvalue())

    def test_list_tasks_ui_with_tasks(self):
        """Test listing tasks when there are tasks."""
        self.task_manager.add_task("Task 1", "Desc 1")
        self.task_manager.add_task("Task 2", "Desc 2")
        with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            self.cli.list_tasks_ui()
            output = mock_stdout.getvalue()
            self.assertIn("ID: 1, Title: Task 1", output)
            self.assertIn("ID: 2, Title: Task 2", output)

    def test_update_task_ui(self):
        """Test the 'Update Task' UI flow."""
        _, _, task_id = self.task_manager.add_task("Old Title", "Old Desc")
        with patch("builtins.input", side_effect=[str(task_id), "New Title", "New Desc"]):
            with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
                self.cli.update_task_ui()
                self.assertIn("Task updated successfully.", mock_stdout.getvalue())
        
        _, _, task = self.task_manager.get_task(task_id)
        self.assertEqual(task.title, "New Title")
        self.assertEqual(task.description, "New Desc")

    def test_delete_task_ui(self):
        """Test the 'Delete Task' UI flow."""
        _, _, task_id = self.task_manager.add_task("To Be Deleted", "None")
        with patch("builtins.input", side_effect=[str(task_id)]):
            with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
                self.cli.delete_task_ui()
                self.assertIn(f"Task {task_id} deleted successfully.", mock_stdout.getvalue())
        
        success, _, _ = self.task_manager.get_task(task_id)
        self.assertFalse(success)

    def test_mark_complete_ui(self):
        """Test the 'Mark Task as Complete' UI flow."""
        _, _, task_id = self.task_manager.add_task("Incomplete Task", "None")
        with patch("builtins.input", side_effect=[str(task_id)]):
            with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
                self.cli.mark_complete_ui()
                self.assertIn(f"Task {task_id} marked as complete.", mock_stdout.getvalue())

        _, _, task = self.task_manager.get_task(task_id)
        self.assertEqual(task.status, "Complete")

    def test_mark_incomplete_ui(self):
        """Test the 'Mark Task as Incomplete' UI flow."""
        _, _, task_id = self.task_manager.add_task("Complete Task", "None")
        self.task_manager.mark_complete(task_id)
        with patch("builtins.input", side_effect=[str(task_id)]):
            with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
                self.cli.mark_incomplete_ui()
                self.assertIn(f"Task {task_id} marked as incomplete.", mock_stdout.getvalue())

        _, _, task = self.task_manager.get_task(task_id)
        self.assertEqual(task.status, "Incomplete")



if __name__ == "__main__":
    unittest.main()
