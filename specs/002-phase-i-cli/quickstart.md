# Quickstart Guide: Phase I - CLI Todo Manager

**Version**: Phase I (In-Memory CLI)
**Last Updated**: 2026-01-03

## Prerequisites

- Python 3.11 or higher installed
- Terminal/Command Prompt access
- Text editor (optional, for viewing source)

## Installation

**No installation required!** Phase I is a single Python script with no external dependencies.

### Quick Check: Verify Python Version

```bash
python --version
# Should show: Python 3.11.x or higher
```

If you see Python 2.x or 3.10 or lower, install Python 3.11+ from [python.org](https://www.python.org/downloads/).

## Running the Application

### Step 1: Navigate to Project Directory

```bash
cd path/to/phase-i-cli
```

### Step 2: Run the Script

```bash
python src/todo_cli.py
```

You should see the main menu:

```
=== Todo Manager ===
1. Add Task
2. View All Tasks
3. Mark Task Complete
4. Mark Task Incomplete
5. Update Task
6. Delete Task
7. Exit
Select an option: _
```

## Basic Usage

### Adding Your First Task

1. From the main menu, enter `1` and press Enter
2. Enter a task title (e.g., "Buy groceries")
3. Enter a description (optional - press Enter to skip)
4. You'll see: "Task added successfully with ID 1"

**Example**:
```
Select an option: 1
Enter task title: Buy groceries
Enter task description (optional, press Enter to skip): Milk, eggs, bread
Task added successfully with ID 1
```

### Viewing Your Tasks

1. From the main menu, enter `2` and press Enter
2. You'll see all your tasks in a table format

**Example Output**:
```
ID | Title           | Description         | Status
---|-----------------|--------------------|------------
1  | Buy groceries   | Milk, eggs, bread  | Incomplete
```

### Marking a Task Complete

1. From the main menu, enter `3` and press Enter
2. Enter the task ID (e.g., `1`)
3. You'll see: "Task 1 marked as complete."

**Example**:
```
Select an option: 3
Enter task ID to mark complete: 1
Task 1 marked as complete.
```

### Updating a Task

1. From the main menu, enter `5` and press Enter
2. Enter the task ID you want to update
3. Enter a new title (or press Enter to keep current)
4. Enter a new description (or press Enter to keep current)

**Example**:
```
Select an option: 5
Enter task ID to update: 1
Current task: Buy groceries | Milk, eggs, bread
Enter new title (or press Enter to keep current): Buy groceries and pharmacy
Enter new description (or press Enter to keep current): Milk, eggs, bread, aspirin
Task 1 updated successfully.
```

### Deleting a Task

1. From the main menu, enter `6` and press Enter
2. Enter the task ID you want to delete

**Example**:
```
Select an option: 6
Enter task ID to delete: 1
Task 1 deleted successfully.
```

### Exiting the Application

1. From the main menu, enter `7` and press Enter
2. You'll see: "Goodbye! (Note: All tasks will be lost)"
3. The application closes

**⚠️ Important**: All tasks are stored in memory only. When you exit, all tasks are permanently lost. This is expected behavior for Phase I.

## Common Workflows

### Daily Task Management

**Morning**: Start your day
```bash
python src/todo_cli.py
# Add tasks: 1 → Enter details
# View tasks: 2 → Check your list
```

**During Day**: Mark tasks as you complete them
```bash
# Mark complete: 3 → Enter task ID
# View progress: 2 → See what's done
```

**Evening**: Review and clean up
```bash
# View all: 2 → See completed tasks
# Delete old tasks: 6 → Remove ID
# Exit: 7 → End session
```

### Weekly Planning

```bash
# 1. Add all tasks for the week
Select option 1 → "Finish project report"
Select option 1 → "Review team PRs"
Select option 1 → "Prepare presentation"

# 2. View full list
Select option 2 → See all tasks

# 3. Work through tasks during week
Select option 3 → Mark tasks complete as finished

# 4. Friday review
Select option 2 → Check what's done vs. pending
```

## Tips & Best Practices

### Writing Good Task Titles

✅ **Good** (specific, actionable):
- "Buy groceries for dinner party"
- "Review PR #42 for security issues"
- "Call dentist to schedule cleaning"

❌ **Poor** (vague, non-actionable):
- "Stuff"
- "Things to do"
- "Work"

### Using Descriptions Effectively

- **Short tasks**: Leave description empty
  - Title: "Buy milk" (description not needed)

- **Complex tasks**: Add details in description
  - Title: "Prepare presentation"
  - Description: "Include Q4 metrics, demo video, and roadmap slide. Aim for 15 minutes."

- **Tasks with dependencies**: Note requirements
  - Title: "Deploy website"
  - Description: "Requires: tests passing, manager approval, Friday 5 PM window"

### Managing Your Task List

**Keep it focused**:
- Don't add more than 10-15 tasks per session
- Delete completed tasks regularly
- Update tasks as requirements change

**Use IDs efficiently**:
- Note task IDs you'll need frequently
- IDs never change (even if you delete other tasks)
- IDs never reuse - ID 1 is always ID 1

## Troubleshooting

### "Command not found: python"

**macOS/Linux**: Try `python3` instead of `python`
```bash
python3 src/todo_cli.py
```

### "No such file or directory: src/todo_cli.py"

You're not in the correct directory. Navigate to the project root:
```bash
cd path/to/phase-i-cli
ls  # Should show "src" folder
```

### "Invalid choice. Please select a number from the menu."

You entered something other than 1-7. Enter only the option number.

### "Task ID not found. Please enter a valid ID."

The task ID you entered doesn't exist. Possible reasons:
- Task was already deleted
- You mistyped the ID
- Task was never created

**Solution**: Enter `2` to view all tasks and see valid IDs.

### "Title cannot be empty."

You pressed Enter without typing a title. Task titles are required.

**Solution**: Enter at least 1 character for the title.

### "Title exceeds 200 characters."

Your title is too long (maximum 200 characters).

**Solution**: Shorten the title or move details to the description field.

## Limitations (Phase I)

**⚠️ Be aware of these Phase I constraints:**

1. **No Persistence**: Tasks are lost when you exit the application
2. **Single User**: Only one person can use the application at a time
3. **No Search**: You must manually scan the list to find tasks
4. **No Categories**: All tasks are in one flat list
5. **No Due Dates**: Cannot set or track deadlines
6. **No Priority**: All tasks have equal importance
7. **No Undo**: Deleted tasks cannot be recovered

**Future Phases** will add:
- Phase II: Web interface, database persistence, multi-user support
- Phase III: AI-powered task suggestions and natural language input
- Phase IV+: Advanced features like categories, priorities, search, etc.

## Getting Help

### View This Guide

```bash
# In your terminal
cat specs/002-phase-i-cli/quickstart.md
```

### View Feature Specification

```bash
# In your terminal
cat specs/002-phase-i-cli/spec.md
```

### Report Issues

If you encounter bugs or have questions:
1. Check this quickstart guide first
2. Review the specification (spec.md)
3. Check the implementation plan (plan.md)

## Next Steps

Once you're comfortable with the CLI:

1. **Read the spec**: `specs/002-phase-i-cli/spec.md` for detailed requirements
2. **Read the plan**: `specs/002-phase-i-cli/plan.md` for technical details
3. **Review the code**: `src/todo_cli.py` to understand implementation
4. **Run tests** (if available): `pytest tests/unit/` to see how it's tested

## Example Session

Here's a complete example session from start to finish:

```
$ python src/todo_cli.py

=== Todo Manager ===
1. Add Task
2. View All Tasks
3. Mark Task Complete
4. Mark Task Incomplete
5. Update Task
6. Delete Task
7. Exit
Select an option: 1
Enter task title: Buy groceries
Enter task description (optional, press Enter to skip): Milk, eggs, bread
Task added successfully with ID 1

Select an option: 1
Enter task title: Finish project report
Enter task description (optional, press Enter to skip):
Task added successfully with ID 2

Select an option: 2
ID | Title                  | Description        | Status
---|------------------------|--------------------|------------
1  | Buy groceries          | Milk, eggs, bread  | Incomplete
2  | Finish project report  |                    | Incomplete

Select an option: 3
Enter task ID to mark complete: 1
Task 1 marked as complete.

Select an option: 2
ID | Title                  | Description        | Status
---|------------------------|--------------------|------------
1  | Buy groceries          | Milk, eggs, bread  | Complete
2  | Finish project report  |                    | Incomplete

Select an option: 7
Goodbye! (Note: All tasks will be lost)
```

---

**Happy task managing! 🎯**
