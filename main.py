#!/usr/bin/env python3
"""
Main entry point for the Todo CLI application.
"""
from src.todo_cli import TaskManager, CLI


def main():
    """Main function to run the CLI application."""
    task_manager = TaskManager()
    cli = CLI(task_manager)
    cli.run()


if __name__ == "__main__":
    main()
