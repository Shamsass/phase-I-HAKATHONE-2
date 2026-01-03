# Implementation Plan: Phase I - CLI Todo Manager

**Branch**: `002-phase-i-cli` | **Date**: 2026-01-03 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `specs/002-phase-i-cli/spec.md`

## Summary

Phase I delivers a command-line todo manager with in-memory storage. Users interact via a numbered menu system to perform CRUD operations (add, view, update, delete) and mark tasks complete/incomplete. Tasks persist only during runtime - no files or databases. The application implements clean separation between data management, business logic, and presentation layers to enable future evolution while remaining simple for Phase I scope.

**Technical Approach**: Single Python script with three logical layers - a Task data model, a TaskManager service for business logic, and a CLI interface for user interaction. In-memory storage uses a Python dictionary keyed by task ID with sequential ID generation via counter.

## Technical Context

**Language/Version**: Python 3.11+
**Primary Dependencies**: None (Python standard library only)
**Storage**: In-memory dictionary (no persistence)
**Testing**: pytest (unit tests for core logic - optional per Phase I)
**Target Platform**: Cross-platform CLI (Windows, macOS, Linux with Python 3.11+)
**Project Type**: Single console application
**Performance Goals**: Instant response for all operations (<50ms), support 100+ tasks without noticeable delay
**Constraints**: No external dependencies, no file I/O, memory-only storage, single-user session
**Scale/Scope**: Single-file Python program (~200-300 lines), 5 core operations, session-based usage

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Spec-Driven Development ✅
- [x] Approved spec.md exists with user stories and functional requirements
- [x] Plan derives only from spec - no invented features
- [x] All capabilities trace to spec requirements

### Agent Behavior Rules ✅
- [x] No manual coding - implementation through agent execution only
- [x] No feature invention beyond spec
- [x] Plan describes HOW, not inventing WHAT

### Phase Governance ✅
- [x] Phase I scope: CLI only, in-memory storage, no persistence
- [x] No Phase II+ features: No web/API, no database, no authentication, no files
- [x] Clear evolution path: data model designed for future persistence layers

### Technology Constraints ✅
- [x] Python 3.11+ (mandated backend language)
- [x] No prohibited technologies used
- [x] No frameworks required (Phase I is pre-FastAPI)
- [x] Standard library only (no external dependencies)

### Quality Standards ✅
- [x] Clean Architecture: Separation of concerns (data, logic, presentation)
- [x] Testing: Unit tests optional for Phase I (spec allows this)
- [x] Type Safety: Type hints mandatory per constitution
- [x] Code Complexity: All functions <10 cyclomatic complexity
- [x] Error Handling: Clear, actionable messages per spec FR-009, FR-010, FR-016
- [x] Input Validation: Title/description length checks per FR-011, FR-012, FR-017

**Constitution Compliance**: PASS - All gates satisfied

## Project Structure

### Documentation (this feature)

```text
specs/002-phase-i-cli/
├── spec.md              # Feature specification (completed)
├── plan.md              # This file (implementation plan)
├── data-model.md        # Phase 1 output (Task entity definition)
├── quickstart.md        # Phase 1 output (how to run the application)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
# Single project structure - Phase I uses one Python script

src/
└── todo_cli.py          # Main application (all code in single file for Phase I)

tests/                   # Optional - unit tests if desired
└── unit/
    └── test_todo_cli.py # Unit tests for TaskManager and Task logic
```

**Structure Decision**:

Phase I uses a **single Python file** (`src/todo_cli.py`) containing all code. This aligns with the simple scope and avoids premature modularization. The file internally separates concerns into three logical sections:

1. **Task Model** (data class)
2. **TaskManager Service** (business logic)
3. **CLI Interface** (user interaction loop)

This structure enables future refactoring into modules (Phase II+) without changing the logical separation. The single-file approach is justified because:
- Total code size ~200-300 lines (manageable in one file)
- No external dependencies to organize
- Simpler deployment (run one Python script)
- Clear migration path: sections become separate modules in Phase II

## Complexity Tracking

No constitution violations - this section is not applicable.

---

## Phase 0: Research & Technical Decisions

### Research Areas

Since Phase I has no external dependencies and uses only Python standard library, research focuses on design patterns and best practices for the constrained environment.

#### 1. In-Memory Storage Strategy

**Decision**: Use Python dictionary (`dict[int, Task]`) keyed by task ID

**Rationale**:
- O(1) lookups by ID for all operations (view, update, delete, mark complete)
- Maintains insertion order (Python 3.7+ guarantee) per FR-013
- Simple counter variable for ID generation starting at 1
- Native Python - no imports required

**Alternatives Considered**:
- List storage: O(n) lookups by ID, requires linear search - rejected for performance
- Named tuple storage: Immutable, complicates updates - rejected for mutability needs
- OrderedDict: Redundant in Python 3.7+ where dict preserves order - rejected as unnecessary

#### 2. ID Generation Strategy

**Decision**: Sequential integer counter starting at 1, never reused per spec Assumption 6

**Rationale**:
- Simple to implement: `self.next_id += 1`
- Meets FR-003 requirement (unique numeric ID, sequential)
- Aligns with spec Assumption 6 (IDs never reused even after deletion)
- User-friendly (IDs are predictable: 1, 2, 3, ...)

**Alternatives Considered**:
- UUID: Overkill for single-user in-memory app, less user-friendly - rejected
- Reuse deleted IDs: Contradicts spec Assumption 6 - rejected
- Hash-based IDs: Unpredictable for users, unnecessary - rejected

#### 3. CLI Menu Flow Pattern

**Decision**: Infinite loop with switch-case (match-case in Python 3.10+) for menu dispatch

**Rationale**:
- Meets FR-015 (loop until exit chosen)
- Clear mapping: menu choice → function call
- Easy error handling for invalid choices (FR-016)
- Standard CLI pattern users expect

**Control Flow**:
```
START → Display Menu → Get User Choice → Validate Choice
         ↑                                      ↓
         └──────────── Execute Action ←─────────┘
                             ↓
                        [Exit chosen?]
                          Yes → END
```

#### 4. Error Handling Strategy

**Decision**: Return error messages as strings from service layer, display in CLI layer

**Rationale**:
- Clear separation: service logic doesn't know about console output
- Enables future reuse: web API could return same error messages as JSON
- Meets FR-009 (invalid ID errors), FR-010 (empty list messages), FR-016 (invalid menu choice)

**Error Categories**:
- Invalid Task ID: "Task ID not found. Please enter a valid ID."
- Empty Task List: "No tasks found. Add a task to get started."
- Invalid Menu Choice: "Invalid choice. Please select a number from the menu."
- Validation Errors: "Title cannot be empty." / "Title exceeds 200 characters." / "Description exceeds 1000 characters."

#### 5. Input Validation Approach

**Decision**: Validate at service layer (TaskManager), not CLI layer

**Rationale**:
- Business rules belong in business logic, not presentation
- Service layer enforces FR-011 (title 1-200 chars), FR-012 (description 0-1000 chars), FR-017 (title not empty)
- CLI layer handles I/O and user feedback only

**Validation Points**:
- Add Task: title length, description length
- Update Task: title length (if updating title), description length (if updating description), task ID existence
- Mark Complete/Incomplete: task ID existence
- Delete Task: task ID existence

---

## Phase 1: Design & Contracts

### Data Model

See [data-model.md](./data-model.md) for complete entity definition.

**Summary**: Single entity `Task` with fields:
- `id`: int (unique, auto-generated, immutable)
- `title`: str (1-200 chars, required)
- `description`: str (0-1000 chars, optional)
- `status`: str ("Complete" or "Incomplete", defaults to "Incomplete")

### Service Layer Design

**TaskManager Class** - Business logic for task operations

**Responsibilities**:
- Maintain in-memory task storage (dict)
- Generate unique task IDs
- Validate inputs (title/description lengths)
- Execute CRUD operations
- Enforce business rules (no empty titles, ID uniqueness)

**Public Methods** (return tuple: (success: bool, message: str, data: optional)):
- `add_task(title: str, description: str) -> tuple[bool, str, int]`
- `get_all_tasks() -> tuple[bool, str, list[Task]]`
- `get_task(task_id: int) -> tuple[bool, str, Task | None]`
- `update_task(task_id: int, title: str | None, description: str | None) -> tuple[bool, str]`
- `delete_task(task_id: int) -> tuple[bool, str]`
- `mark_complete(task_id: int) -> tuple[bool, str]`
- `mark_incomplete(task_id: int) -> tuple[bool, str]`

**Internal State**:
- `_tasks: dict[int, Task]` - storage dictionary
- `_next_id: int` - counter for ID generation (starts at 1)

### CLI Layer Design

**CLI Class** - User interaction and display

**Responsibilities**:
- Display menu and prompt user
- Parse user input
- Call TaskManager methods
- Format and display results/errors
- Handle input validation (numeric menu choices, non-empty input where required)

**Menu Options** (FR-001):
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

**Interaction Flows**:

1. **Add Task Flow**:
   - Prompt: "Enter task title: "
   - Read title
   - Prompt: "Enter task description (optional, press Enter to skip): "
   - Read description
   - Call `task_manager.add_task(title, description)`
   - Display success: "Task added successfully with ID {id}" OR error message

2. **View All Tasks Flow**:
   - Call `task_manager.get_all_tasks()`
   - If empty: Display "No tasks found. Add a task to get started."
   - If has tasks: Display formatted table:
     ```
     ID | Title                  | Description           | Status
     ---|-----------------------|----------------------|------------
     1  | Buy groceries         | Milk, eggs, bread    | Incomplete
     2  | Finish project report |                      | Complete
     ```

3. **Mark Complete Flow**:
   - Prompt: "Enter task ID to mark complete: "
   - Read task_id (validate numeric input)
   - Call `task_manager.mark_complete(task_id)`
   - Display success: "Task {id} marked as complete." OR error message

4. **Mark Incomplete Flow**:
   - Prompt: "Enter task ID to mark incomplete: "
   - Read task_id (validate numeric input)
   - Call `task_manager.mark_incomplete(task_id)`
   - Display success: "Task {id} marked as incomplete." OR error message

5. **Update Task Flow**:
   - Prompt: "Enter task ID to update: "
   - Read task_id (validate numeric input)
   - Get current task to show existing values
   - Prompt: "Enter new title (or press Enter to keep current): "
   - Read new_title
   - Prompt: "Enter new description (or press Enter to keep current): "
   - Read new_description
   - Call `task_manager.update_task(task_id, new_title or None, new_description or None)`
   - Display success: "Task {id} updated successfully." OR error message

6. **Delete Task Flow**:
   - Prompt: "Enter task ID to delete: "
   - Read task_id (validate numeric input)
   - Call `task_manager.delete_task(task_id)`
   - Display success: "Task {id} deleted successfully." OR error message

7. **Exit Flow**:
   - Display: "Goodbye! (Note: All tasks will be lost)"
   - Exit program cleanly

### No External Contracts

Phase I has no APIs, web endpoints, or external interfaces. The contract is the CLI menu interface itself, documented above. Future phases will extract the TaskManager service layer behind REST APIs.

### Quickstart Guide

See [quickstart.md](./quickstart.md) for user-facing instructions.

**Developer Quick Commands**:
```bash
# Run application
python src/todo_cli.py

# Run tests (if implemented)
pytest tests/unit/

# Type check
mypy src/todo_cli.py --strict

# Lint
black src/todo_cli.py --check
```

---

## Architecture Decisions

### AD-1: Single File vs. Multiple Modules

**Context**: Phase I is simple (5 operations, ~200-300 lines). Should we split into modules now or keep as single file?

**Decision**: Single file (`src/todo_cli.py`)

**Rationale**:
- Total code size manageable in one file
- No external dependencies to organize
- Simpler for users to understand and run
- Clear internal structure (Task model → TaskManager service → CLI interface) enables easy extraction to modules in Phase II
- Avoids premature optimization (YAGNI principle per constitution)

**Consequences**:
- ✅ Easier to review and understand as single artifact
- ✅ Simpler deployment (one file to copy/run)
- ✅ Clear migration path for Phase II (sections become modules)
- ⚠️ Must maintain disciplined internal organization (comments separating sections)
- ⚠️ If code grows >500 lines, should reconsider (not expected for Phase I)

### AD-2: Dictionary vs. List for Task Storage

**Context**: Need in-memory storage supporting O(1) lookup by ID for operations.

**Decision**: Dictionary (`dict[int, Task]`) keyed by task ID

**Rationale**:
- O(1) lookups for get/update/delete operations
- Python 3.7+ guarantees insertion order (meets FR-013)
- Simple ID generation with counter variable
- Standard Python pattern for key-value storage

**Consequences**:
- ✅ Fast lookups by ID (constant time)
- ✅ Maintains insertion order automatically
- ✅ Easy to understand and implement
- ⚠️ Slightly more memory than list (minimal impact for <1000 tasks)
- ⚠️ Must track next_id separately (solved with counter variable)

### AD-3: Type Hints and Data Classes

**Context**: Constitution mandates type hints. Should we use dataclasses, NamedTuple, or plain class for Task?

**Decision**: Use `@dataclass` for Task model

**Rationale**:
- Automatic `__init__`, `__repr__`, `__eq__` methods
- Immutable option with `frozen=True` not needed (tasks are mutable)
- Built-in to Python 3.7+ (no external dependencies)
- Clear type hints for all fields
- Future-compatible with SQLModel (Phase II) which uses similar syntax

**Consequences**:
- ✅ Less boilerplate code
- ✅ Automatic string representation for debugging
- ✅ Type safety enforced at runtime with type checkers
- ✅ Easy migration to SQLModel in Phase II (similar field syntax)
- ⚠️ Slightly more imports than plain class (dataclasses module)

### AD-4: Error Handling: Exceptions vs. Return Values

**Context**: How should TaskManager methods signal errors (invalid ID, validation failures)?

**Decision**: Return tuple `(success: bool, message: str, data: optional)`

**Rationale**:
- Explicit error handling at call site (no hidden control flow)
- Service layer doesn't need to know about exception types
- Easy to test (check return values)
- CLI layer gets actionable messages to display
- Avoids exception handling overhead for expected errors (invalid ID is not exceptional)

**Consequences**:
- ✅ Clear success/failure semantics
- ✅ Error messages constructed at service layer (business logic)
- ✅ CLI layer just displays messages (no error interpretation logic)
- ✅ Easy to add logging/metrics (check success boolean)
- ⚠️ Callers must check success flag (but this is explicit and good)
- ⚠️ Slightly more verbose than raising exceptions

### AD-5: Input Validation Location

**Context**: Where should validation happen - CLI layer (presentation) or TaskManager (business logic)?

**Decision**: Validation in TaskManager service layer

**Rationale**:
- Business rules belong in business logic, not presentation
- Enables reuse in Phase II (web API will use same TaskManager)
- Single source of truth for validation rules
- CLI layer handles only I/O and formatting

**Consequences**:
- ✅ Business rules centralized
- ✅ Future APIs get same validation automatically
- ✅ Easier to test (test service layer, not CLI interaction)
- ⚠️ CLI must handle validation errors gracefully (display messages)
- ⚠️ Cannot provide real-time feedback before service call (acceptable tradeoff)

---

## Phase 2: Implementation Readiness

This plan document is now complete. The next step is to run `/sp.tasks` to generate the task breakdown from this plan and the spec.

**Artifacts Produced**:
- [x] plan.md (this file)
- [x] data-model.md (Task entity definition)
- [x] quickstart.md (how to run application)

**Ready for**:
- `/sp.tasks` command to generate tasks.md
- User review and approval of technical approach

**No Clarifications Needed**: All technical decisions resolved with justifications.
