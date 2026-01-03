# Tasks: Phase I - CLI Todo Manager

**Input**: Design documents from `specs/002-phase-i-cli/`
**Prerequisites**: plan.md (required), spec.md (required), data-model.md (required)
**Branch**: `002-phase-i-cli`
**Created**: 2026-01-03

**Tests**: Tests are OPTIONAL for Phase I per spec and constitution. Tasks below include test tasks marked as OPTIONAL.

**Organization**: Tasks are grouped by implementation layer (Setup, Data Layer, Service Layer, CLI Layer, Integration) to enable systematic bottom-up implementation.

## Format: `[ID] [P?] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- Include exact file paths in descriptions
- All tasks trace to spec requirements (FR-XXX) and plan sections

## Path Conventions

- **Single project**: `src/` at repository root
- **Tests**: `tests/unit/` at repository root (optional)

---

## Phase 1: Project Setup

**Purpose**: Initialize project structure and development environment

- [ ] **T001** Create project directory structure per plan section "Project Structure"
  - **Preconditions**: Repository exists
  - **Expected Output**: Directories `src/` and `tests/unit/` created
  - **Artifacts**:
    - `src/` directory (create)
    - `tests/unit/` directory (create if tests desired)
  - **Spec Reference**: N/A (infrastructure)
  - **Plan Reference**: "Project Structure" section

- [ ] **T002** Create main Python file `src/todo_cli.py` with file header and imports
  - **Preconditions**: T001 complete (src/ directory exists)
  - **Expected Output**: Empty Python file with shebang, docstring, type hints import
  - **Artifacts**:
    - `src/todo_cli.py` (create, ~10 lines)
  - **File Contents**:
    ```python
    #!/usr/bin/env python3
    """
    Phase I: CLI Todo Manager
    In-memory task management with command-line interface.
    """
    from dataclasses import dataclass
    from typing import Optional

    # Constants will be defined here
    # Classes will be defined here
    # Main entry point will be here
    ```
  - **Spec Reference**: FR-004 (in-memory storage)
  - **Plan Reference**: "Summary" - single Python script

---

## Phase 2: Data Layer (Task Model)

**Purpose**: Implement Task data model per data-model.md specification

- [ ] **T003** Define Task data model using @dataclass in `src/todo_cli.py`
  - **Preconditions**: T002 complete (todo_cli.py exists)
  - **Expected Output**: Task class with 4 fields (id, title, description, status) and type hints
  - **Artifacts**:
    - `src/todo_cli.py` (modify, add Task class ~15 lines)
  - **Implementation Details**:
    ```python
    @dataclass
    class Task:
        """Represents a single todo item."""
        id: int
        title: str
        description: str
        status: str  # "Complete" or "Incomplete"
    ```
  - **Spec Reference**:
    - Key Entities section (Task definition)
    - FR-002 (title and description fields)
    - FR-003 (ID field)
  - **Plan Reference**:
    - "Service Layer Design" section
    - data-model.md "Task" entity
  - **Validation**: Task class should have exactly 4 fields matching data-model.md

- [ ] **T004** Define status constants for task completion states in `src/todo_cli.py`
  - **Preconditions**: T003 complete (Task class exists)
  - **Expected Output**: Constants STATUS_INCOMPLETE and STATUS_COMPLETE defined
  - **Artifacts**:
    - `src/todo_cli.py` (modify, add constants ~3 lines)
  - **Implementation Details**:
    ```python
    # Constants
    STATUS_INCOMPLETE = "Incomplete"
    STATUS_COMPLETE = "Complete"
    ```
  - **Spec Reference**: Key Entities section (Status field values)
  - **Plan Reference**: data-model.md "status" field valid values
  - **Validation**: Constants match exact strings from spec

---

## Phase 3: Service Layer (TaskManager - Core Logic)

**Purpose**: Implement TaskManager class with business logic per plan section "Service Layer Design"

- [ ] **T005** Create TaskManager class with initialization and storage in `src/todo_cli.py`
  - **Preconditions**: T003 complete (Task model exists)
  - **Expected Output**: TaskManager class with `__init__` method, empty storage dict, ID counter
  - **Artifacts**:
    - `src/todo_cli.py` (modify, add TaskManager class skeleton ~15 lines)
  - **Implementation Details**:
    ```python
    class TaskManager:
        """Manages task storage and operations."""

        def __init__(self) -> None:
            """Initialize task manager with empty storage."""
            self._tasks: dict[int, Task] = {}
            self._next_id: int = 1
    ```
  - **Spec Reference**:
    - FR-004 (in-memory storage)
    - FR-003 (ID generation starting from 1)
  - **Plan Reference**:
    - "Service Layer Design" - Internal State
    - Phase 0 Research - "ID Generation Strategy" (sequential starting at 1)
  - **Validation**:
    - Storage is dict[int, Task]
    - ID counter starts at 1
    - No external dependencies

- [ ] **T006** Implement `add_task` method in TaskManager class
  - **Preconditions**: T005 complete (TaskManager class initialized)
  - **Expected Output**: Method that validates input, generates ID, creates Task, stores in dict
  - **Artifacts**:
    - `src/todo_cli.py` (modify, add add_task method ~25 lines)
  - **Implementation Details**:
    ```python
    def add_task(self, title: str, description: str) -> tuple[bool, str, int]:
        """Add a new task with validation.

        Returns: (success, message, task_id or 0)
        """
        # Validate title (FR-017, FR-011)
        # Validate description (FR-012)
        # Generate ID (FR-003)
        # Create Task with STATUS_INCOMPLETE
        # Store in _tasks dict
        # Return success with ID
    ```
  - **Spec Reference**:
    - FR-002 (add task with title and description)
    - FR-011 (title 1-200 chars)
    - FR-012 (description 0-1000 chars)
    - FR-017 (title not empty)
    - User Story 1 acceptance scenarios
  - **Plan Reference**:
    - "Service Layer Design" - add_task method
    - Phase 0 Research - "Input Validation Approach"
  - **Validation**:
    - Title validation: strip whitespace, check 1-200 chars
    - Description validation: check 0-1000 chars
    - Returns (True, success message, task_id) on success
    - Returns (False, error message, 0) on validation failure

- [ ] **T007** Implement `get_all_tasks` method in TaskManager class
  - **Preconditions**: T005 complete (TaskManager class initialized)
  - **Expected Output**: Method that returns all tasks as list maintaining insertion order
  - **Artifacts**:
    - `src/todo_cli.py` (modify, add get_all_tasks method ~10 lines)
  - **Implementation Details**:
    ```python
    def get_all_tasks(self) -> tuple[bool, str, list[Task]]:
        """Get all tasks in insertion order.

        Returns: (success, message, list of tasks)
        """
        # Convert dict values to list (preserves insertion order)
        # Return success with task list
    ```
  - **Spec Reference**:
    - FR-005 (display all tasks)
    - FR-013 (maintain insertion order)
    - User Story 2 acceptance scenarios
  - **Plan Reference**:
    - "Service Layer Design" - get_all_tasks method
    - Phase 0 Research - "In-Memory Storage Strategy" (dict preserves order)
  - **Validation**:
    - Returns list of Task objects
    - Order matches insertion order
    - Empty list if no tasks

- [ ] **T008** Implement `get_task` method in TaskManager class
  - **Preconditions**: T005 complete (TaskManager class initialized)
  - **Expected Output**: Method that retrieves single task by ID or returns error
  - **Artifacts**:
    - `src/todo_cli.py` (modify, add get_task method ~12 lines)
  - **Implementation Details**:
    ```python
    def get_task(self, task_id: int) -> tuple[bool, str, Optional[Task]]:
        """Get a task by ID.

        Returns: (success, message, task or None)
        """
        # Check if task_id exists in _tasks dict
        # Return (True, "", task) if found
        # Return (False, "Task ID not found. Please enter a valid ID.", None) if not found
    ```
  - **Spec Reference**:
    - FR-009 (invalid ID error message)
    - User Story 3, 4, 5 acceptance scenarios (invalid ID handling)
  - **Plan Reference**:
    - "Service Layer Design" - get_task method
    - Phase 0 Research - "Error Handling Strategy"
  - **Validation**:
    - O(1) lookup (dict access)
    - Exact error message matches spec FR-009
    - Returns None for invalid ID

- [ ] **T009** Implement `update_task` method in TaskManager class
  - **Preconditions**: T008 complete (get_task method exists)
  - **Expected Output**: Method that updates task title/description with validation
  - **Artifacts**:
    - `src/todo_cli.py` (modify, add update_task method ~30 lines)
  - **Implementation Details**:
    ```python
    def update_task(
        self, task_id: int, title: Optional[str], description: Optional[str]
    ) -> tuple[bool, str]:
        """Update task title and/or description.

        Returns: (success, message)
        """
        # Check task exists (use get_task)
        # Validate new title if provided (FR-011, FR-017)
        # Validate new description if provided (FR-012)
        # Update task fields (mutate in place)
        # Return success message
    ```
  - **Spec Reference**:
    - FR-007 (update task title/description)
    - FR-009 (invalid ID error)
    - FR-011, FR-012, FR-017 (validation rules)
    - User Story 4 acceptance scenarios
  - **Plan Reference**:
    - "Service Layer Design" - update_task method
    - Phase 0 Research - "Input Validation Approach"
  - **Validation**:
    - Can update title only, description only, or both
    - Validation rules same as add_task
    - Original fields preserved if not updating
    - Status field not affected

- [ ] **T010** Implement `delete_task` method in TaskManager class
  - **Preconditions**: T008 complete (get_task method exists)
  - **Expected Output**: Method that removes task from storage by ID
  - **Artifacts**:
    - `src/todo_cli.py` (modify, add delete_task method ~12 lines)
  - **Implementation Details**:
    ```python
    def delete_task(self, task_id: int) -> tuple[bool, str]:
        """Delete a task by ID.

        Returns: (success, message)
        """
        # Check task exists
        # Remove from _tasks dict using del or pop
        # Return success message with task_id
    ```
  - **Spec Reference**:
    - FR-008 (delete task by ID)
    - FR-009 (invalid ID error)
    - User Story 5 acceptance scenarios
  - **Plan Reference**: "Service Layer Design" - delete_task method
  - **Validation**:
    - Task removed from dict
    - Remaining tasks unchanged
    - IDs not reused (spec Assumption 6)

- [ ] **T011** Implement `mark_complete` method in TaskManager class
  - **Preconditions**: T008 complete (get_task method exists)
  - **Expected Output**: Method that sets task status to "Complete"
  - **Artifacts**:
    - `src/todo_cli.py` (modify, add mark_complete method ~12 lines)
  - **Implementation Details**:
    ```python
    def mark_complete(self, task_id: int) -> tuple[bool, str]:
        """Mark a task as complete.

        Returns: (success, message)
        """
        # Check task exists
        # Set task.status = STATUS_COMPLETE
        # Return success message
    ```
  - **Spec Reference**:
    - FR-006 (mark task complete)
    - FR-009 (invalid ID error)
    - User Story 3 acceptance scenario 1
  - **Plan Reference**: "Service Layer Design" - mark_complete method
  - **Validation**:
    - Status changes to "Complete"
    - Title/description unchanged
    - Can be called on already-complete task (idempotent)

- [ ] **T012** Implement `mark_incomplete` method in TaskManager class
  - **Preconditions**: T008 complete (get_task method exists)
  - **Expected Output**: Method that sets task status to "Incomplete"
  - **Artifacts**:
    - `src/todo_cli.py` (modify, add mark_incomplete method ~12 lines)
  - **Implementation Details**:
    ```python
    def mark_incomplete(self, task_id: int) -> tuple[bool, str]:
        """Mark a task as incomplete.

        Returns: (success, message)
        """
        # Check task exists
        # Set task.status = STATUS_INCOMPLETE
        # Return success message
    ```
  - **Spec Reference**:
    - FR-006 (mark task incomplete)
    - FR-009 (invalid ID error)
    - User Story 3 acceptance scenario 2
  - **Plan Reference**: "Service Layer Design" - mark_incomplete method
  - **Validation**:
    - Status changes to "Incomplete"
    - Can toggle back and forth with mark_complete

---

## Phase 4: CLI Layer (User Interface)

**Purpose**: Implement CLI class for user interaction per plan section "CLI Layer Design"

- [ ] **T013** Create CLI class with initialization in `src/todo_cli.py`
  - **Preconditions**: T012 complete (TaskManager fully implemented)
  - **Expected Output**: CLI class with constructor accepting TaskManager instance
  - **Artifacts**:
    - `src/todo_cli.py` (modify, add CLI class ~10 lines)
  - **Implementation Details**:
    ```python
    class CLI:
        """Command-line interface for todo manager."""

        def __init__(self, task_manager: TaskManager) -> None:
            """Initialize CLI with task manager."""
            self.task_manager = task_manager
    ```
  - **Spec Reference**: FR-001 (text-based menu interface)
  - **Plan Reference**:
    - "CLI Layer Design" section
    - Architecture Decision AD-5 (validation in service layer)
  - **Validation**: CLI depends on TaskManager (separation of concerns)

- [ ] **T014** Implement `display_menu` method in CLI class
  - **Preconditions**: T013 complete (CLI class initialized)
  - **Expected Output**: Method that prints menu with 7 numbered options
  - **Artifacts**:
    - `src/todo_cli.py` (modify, add display_menu method ~15 lines)
  - **Implementation Details**:
    ```python
    def display_menu(self) -> None:
        """Display main menu options."""
        print("\n=== Todo Manager ===")
        print("1. Add Task")
        print("2. View All Tasks")
        print("3. Mark Task Complete")
        print("4. Mark Task Incomplete")
        print("5. Update Task")
        print("6. Delete Task")
        print("7. Exit")
    ```
  - **Spec Reference**:
    - FR-001 (numbered menu options)
    - Plan section "Menu Options"
  - **Plan Reference**: "CLI Layer Design" - Menu Options
  - **Validation**: Exact menu text matches plan section

- [ ] **T015** Implement `handle_add_task` method in CLI class
  - **Preconditions**: T014 complete (display_menu exists)
  - **Expected Output**: Method that prompts for title/description, calls add_task, displays result
  - **Artifacts**:
    - `src/todo_cli.py` (modify, add handle_add_task method ~20 lines)
  - **Implementation Details**:
    ```python
    def handle_add_task(self) -> None:
        """Handle add task menu option."""
        print("\n--- Add Task ---")
        title = input("Enter task title: ")
        description = input("Enter task description (optional, press Enter to skip): ")

        success, message, task_id = self.task_manager.add_task(title, description)
        if success:
            print(f"Task added successfully with ID {task_id}")
        else:
            print(f"Error: {message}")
    ```
  - **Spec Reference**:
    - FR-002 (add task with title and description)
    - User Story 1 "Add Task Flow"
    - User Story 1 acceptance scenarios
  - **Plan Reference**: "CLI Layer Design" - Add Task Flow
  - **Validation**:
    - Prompts match plan exactly
    - Description is optional (can be empty)
    - Success message includes task ID

- [ ] **T016** Implement `handle_view_tasks` method in CLI class
  - **Preconditions**: T014 complete (display_menu exists)
  - **Expected Output**: Method that displays all tasks in table format or empty message
  - **Artifacts**:
    - `src/todo_cli.py` (modify, add handle_view_tasks method ~25 lines)
  - **Implementation Details**:
    ```python
    def handle_view_tasks(self) -> None:
        """Handle view all tasks menu option."""
        print("\n--- All Tasks ---")
        success, message, tasks = self.task_manager.get_all_tasks()

        if not tasks:
            print("No tasks found. Add a task to get started.")
            return

        # Print table header
        print(f"{'ID':<5} | {'Title':<30} | {'Description':<40} | {'Status':<12}")
        print("-" * 95)

        # Print each task
        for task in tasks:
            # Truncate long fields for display
            # Format: ID | Title | Description | Status
    ```
  - **Spec Reference**:
    - FR-005 (display all tasks with details)
    - FR-010 (empty list message - exact text)
    - User Story 2 acceptance scenarios
  - **Plan Reference**: "CLI Layer Design" - View All Tasks Flow
  - **Validation**:
    - Empty message matches spec FR-010 exactly
    - Table shows ID, Title, Description, Status
    - Tasks display in insertion order (FR-013)

- [ ] **T017** Implement `handle_mark_complete` method in CLI class
  - **Preconditions**: T014 complete (display_menu exists)
  - **Expected Output**: Method that prompts for ID, calls mark_complete, displays result
  - **Artifacts**:
    - `src/todo_cli.py` (modify, add handle_mark_complete method ~18 lines)
  - **Implementation Details**:
    ```python
    def handle_mark_complete(self) -> None:
        """Handle mark task complete menu option."""
        print("\n--- Mark Task Complete ---")
        try:
            task_id = int(input("Enter task ID to mark complete: "))
        except ValueError:
            print("Error: Please enter a valid numeric ID.")
            return

        success, message = self.task_manager.mark_complete(task_id)
        if success:
            print(f"Task {task_id} marked as complete.")
        else:
            print(f"Error: {message}")
    ```
  - **Spec Reference**:
    - FR-006 (mark complete by ID)
    - FR-009 (invalid ID error)
    - Edge case: non-numeric input handling
    - User Story 3 acceptance scenarios
  - **Plan Reference**: "CLI Layer Design" - Mark Complete Flow
  - **Validation**:
    - Handles non-numeric input gracefully
    - Success message includes task ID
    - Error message from service layer displayed

- [ ] **T018** Implement `handle_mark_incomplete` method in CLI class
  - **Preconditions**: T014 complete (display_menu exists)
  - **Expected Output**: Method that prompts for ID, calls mark_incomplete, displays result
  - **Artifacts**:
    - `src/todo_cli.py` (modify, add handle_mark_incomplete method ~18 lines)
  - **Implementation Details**:
    ```python
    def handle_mark_incomplete(self) -> None:
        """Handle mark task incomplete menu option."""
        print("\n--- Mark Task Incomplete ---")
        try:
            task_id = int(input("Enter task ID to mark incomplete: "))
        except ValueError:
            print("Error: Please enter a valid numeric ID.")
            return

        success, message = self.task_manager.mark_incomplete(task_id)
        if success:
            print(f"Task {task_id} marked as incomplete.")
        else:
            print(f"Error: {message}")
    ```
  - **Spec Reference**:
    - FR-006 (mark incomplete by ID)
    - FR-009 (invalid ID error)
    - User Story 3 acceptance scenario 2
  - **Plan Reference**: "CLI Layer Design" - Mark Incomplete Flow
  - **Validation**: Similar to T017 but for incomplete status

- [ ] **T019** Implement `handle_update_task` method in CLI class
  - **Preconditions**: T014 complete (display_menu exists)
  - **Expected Output**: Method that prompts for ID and new values, calls update_task
  - **Artifacts**:
    - `src/todo_cli.py` (modify, add handle_update_task method ~30 lines)
  - **Implementation Details**:
    ```python
    def handle_update_task(self) -> None:
        """Handle update task menu option."""
        print("\n--- Update Task ---")
        try:
            task_id = int(input("Enter task ID to update: "))
        except ValueError:
            print("Error: Please enter a valid numeric ID.")
            return

        # Get current task to show existing values
        success, msg, task = self.task_manager.get_task(task_id)
        if not success:
            print(f"Error: {msg}")
            return

        print(f"Current: {task.title} | {task.description}")
        new_title = input("Enter new title (or press Enter to keep current): ")
        new_desc = input("Enter new description (or press Enter to keep current): ")

        # Call update_task with None for unchanged fields
    ```
  - **Spec Reference**:
    - FR-007 (update title/description)
    - FR-009 (invalid ID error)
    - User Story 4 acceptance scenarios
  - **Plan Reference**: "CLI Layer Design" - Update Task Flow
  - **Validation**:
    - Shows current values before update
    - Allows updating title only, description only, or both
    - Empty input means keep current value

- [ ] **T020** Implement `handle_delete_task` method in CLI class
  - **Preconditions**: T014 complete (display_menu exists)
  - **Expected Output**: Method that prompts for ID, calls delete_task, displays result
  - **Artifacts**:
    - `src/todo_cli.py` (modify, add handle_delete_task method ~18 lines)
  - **Implementation Details**:
    ```python
    def handle_delete_task(self) -> None:
        """Handle delete task menu option."""
        print("\n--- Delete Task ---")
        try:
            task_id = int(input("Enter task ID to delete: "))
        except ValueError:
            print("Error: Please enter a valid numeric ID.")
            return

        success, message = self.task_manager.delete_task(task_id)
        if success:
            print(f"Task {task_id} deleted successfully.")
        else:
            print(f"Error: {message}")
    ```
  - **Spec Reference**:
    - FR-008 (delete task by ID)
    - FR-009 (invalid ID error)
    - User Story 5 acceptance scenarios
  - **Plan Reference**: "CLI Layer Design" - Delete Task Flow
  - **Validation**: Non-numeric input handled gracefully

- [ ] **T021** Implement `run` method in CLI class (main application loop)
  - **Preconditions**: T014-T020 complete (all handler methods exist)
  - **Expected Output**: Infinite loop that displays menu, gets choice, dispatches to handlers
  - **Artifacts**:
    - `src/todo_cli.py` (modify, add run method ~40 lines)
  - **Implementation Details**:
    ```python
    def run(self) -> None:
        """Run the main application loop."""
        print("Welcome to Todo Manager!")

        while True:
            self.display_menu()
            choice = input("\nSelect an option: ").strip()

            if choice == "1":
                self.handle_add_task()
            elif choice == "2":
                self.handle_view_tasks()
            elif choice == "3":
                self.handle_mark_complete()
            elif choice == "4":
                self.handle_mark_incomplete()
            elif choice == "5":
                self.handle_update_task()
            elif choice == "6":
                self.handle_delete_task()
            elif choice == "7":
                print("Goodbye! (Note: All tasks will be lost)")
                break
            else:
                print("Invalid choice. Please select a number from the menu.")
    ```
  - **Spec Reference**:
    - FR-001 (menu interface)
    - FR-014 (exit gracefully)
    - FR-015 (loop until exit)
    - FR-016 (invalid menu choice error - exact text)
  - **Plan Reference**:
    - Phase 0 Research - "CLI Menu Flow Pattern"
    - "CLI Layer Design" - Exit Flow
  - **Validation**:
    - Loop continues until choice 7
    - Invalid choice shows exact error from FR-016
    - Exit message warns about data loss

---

## Phase 5: Application Entry Point

**Purpose**: Create main entry point to start application

- [ ] **T022** Implement `main()` function and `if __name__ == "__main__"` block in `src/todo_cli.py`
  - **Preconditions**: T021 complete (CLI.run method exists)
  - **Expected Output**: Entry point that creates TaskManager, CLI, and starts application
  - **Artifacts**:
    - `src/todo_cli.py` (modify, add main function ~10 lines)
  - **Implementation Details**:
    ```python
    def main() -> None:
        """Application entry point."""
        task_manager = TaskManager()
        cli = CLI(task_manager)
        cli.run()


    if __name__ == "__main__":
        main()
    ```
  - **Spec Reference**: FR-014 (provide way to exit - implies way to start)
  - **Plan Reference**: "Summary" - single Python script
  - **Validation**:
    - Can run with `python src/todo_cli.py`
    - No command-line arguments required
    - Clean exit on choice 7

---

## Phase 6: Testing (OPTIONAL)

**Purpose**: Unit tests for TaskManager business logic (optional per Phase I spec)

**NOTE**: These tasks are OPTIONAL. Phase I spec states "Unit tests for core logic (optional integration tests)" and constitution allows optional tests for Phase I.

- [ ] **T023 [OPTIONAL]** Create test file `tests/unit/test_todo_cli.py` with imports and fixtures
  - **Preconditions**: T012 complete (TaskManager implemented), tests/unit/ directory exists
  - **Expected Output**: Test file with pytest imports and TaskManager fixture
  - **Artifacts**:
    - `tests/unit/test_todo_cli.py` (create, ~15 lines)
  - **Spec Reference**: Testing requirements (optional for Phase I)
  - **Plan Reference**: "Technical Context" - pytest for testing

- [ ] **T024 [OPTIONAL]** Write unit tests for `add_task` method validations
  - **Preconditions**: T023 complete
  - **Expected Output**: Tests for title validation (empty, too long), description validation
  - **Artifacts**:
    - `tests/unit/test_todo_cli.py` (modify, add ~30 lines)
  - **Test Cases**:
    - Test empty title rejected
    - Test title >200 chars rejected
    - Test description >1000 chars rejected
    - Test valid task added successfully
    - Test ID generation increments
  - **Spec Reference**: FR-011, FR-012, FR-017

- [ ] **T025 [OPTIONAL]** Write unit tests for task retrieval and status changes
  - **Preconditions**: T023 complete
  - **Expected Output**: Tests for get_task, get_all_tasks, mark complete/incomplete
  - **Artifacts**:
    - `tests/unit/test_todo_cli.py` (modify, add ~25 lines)
  - **Test Cases**:
    - Test get_task returns correct task
    - Test get_task returns error for invalid ID
    - Test get_all_tasks preserves order
    - Test mark_complete changes status
    - Test mark_incomplete toggles status back
  - **Spec Reference**: FR-005, FR-006, FR-009, FR-013

- [ ] **T026 [OPTIONAL]** Write unit tests for update and delete operations
  - **Preconditions**: T023 complete
  - **Expected Output**: Tests for update_task and delete_task edge cases
  - **Artifacts**:
    - `tests/unit/test_todo_cli.py` (modify, add ~25 lines)
  - **Test Cases**:
    - Test update title only
    - Test update description only
    - Test update both fields
    - Test update validates new values
    - Test delete removes task
    - Test delete with invalid ID fails
  - **Spec Reference**: FR-007, FR-008, FR-009

---

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 1 (Setup)**: No dependencies - can start immediately
- **Phase 2 (Data Layer)**: Depends on Phase 1 completion
- **Phase 3 (Service Layer)**: Depends on Phase 2 completion
- **Phase 4 (CLI Layer)**: Depends on Phase 3 completion
- **Phase 5 (Entry Point)**: Depends on Phase 4 completion
- **Phase 6 (Testing)**: OPTIONAL - can be done anytime after Phase 3

### Task Dependencies Within Phases

**Phase 1 (Setup)**:
- T002 depends on T001

**Phase 2 (Data Layer)**:
- T003 depends on T002
- T004 depends on T003

**Phase 3 (Service Layer)**:
- T005 depends on T003 (needs Task model)
- T006, T007 depend on T005 (needs TaskManager skeleton)
- T008 depends on T005
- T009, T010, T011, T012 depend on T008 (need get_task helper)

**Phase 4 (CLI Layer)**:
- T013 depends on T012 (needs complete TaskManager)
- T014 depends on T013
- T015-T020 depend on T014 (need display_menu)
- T021 depends on T015-T020 (needs all handlers)

**Phase 5 (Entry Point)**:
- T022 depends on T021 (needs CLI.run)

**Phase 6 (Testing - OPTIONAL)**:
- T023-T026 depend on T012 (need TaskManager implemented)
- Can be done in parallel with each other

### Parallel Opportunities

**Within Phase 3** (after T008 complete):
- T009, T010, T011, T012 can run in parallel (different methods, no interdependencies)

**Within Phase 4** (after T014 complete):
- T015, T016, T017, T018, T019, T020 can run in parallel (different handler methods)

**Phase 6** (optional tests):
- T023, T024, T025, T026 can run in parallel if multiple developers

### Sequential Execution (Single Developer)

Recommended order for single-developer implementation:

1. **Setup**: T001 → T002
2. **Data**: T003 → T004
3. **Service Core**: T005 → T006 → T007 → T008
4. **Service Operations**: T009 → T010 → T011 → T012 (or in parallel)
5. **CLI Core**: T013 → T014
6. **CLI Handlers**: T015 → T016 → T017 → T018 → T019 → T020 (or in parallel)
7. **Entry**: T021 → T022
8. **Test (optional)**: T023 → T024 → T025 → T026

**Estimated LOC per Phase**:
- Phase 1: ~10 lines
- Phase 2: ~20 lines
- Phase 3: ~120 lines
- Phase 4: ~150 lines
- Phase 5: ~10 lines
- Phase 6: ~80 lines (optional)
- **Total**: ~310 lines (or ~230 without tests)

---

## Validation Checklist

After completing all tasks, verify:

- [ ] All 17 functional requirements (FR-001 through FR-017) implemented
- [ ] All 5 user stories testable via CLI interaction
- [ ] All edge cases from spec handled (non-numeric input, empty list, invalid ID, etc.)
- [ ] Error messages match spec exactly (FR-009, FR-010, FR-016)
- [ ] Type hints present on all functions (constitution requirement)
- [ ] No external dependencies (only Python standard library)
- [ ] Single file ~200-300 lines (matches plan estimate)
- [ ] Application runs with `python src/todo_cli.py`
- [ ] Exit gracefully with choice 7
- [ ] Success criteria from spec met (SC-001 through SC-007)

---

## Notes

- All tasks trace to spec requirements (FR-XXX) and plan sections
- No invented features - all functionality from approved spec
- Error messages use exact text from spec where specified
- Type hints mandatory per constitution Quality Standards
- Tests are optional but recommended for Phase I
- Single file keeps implementation simple while maintaining clean separation
- Each task is independently testable and reviewable
- Commit after each task or logical grouping for traceability
