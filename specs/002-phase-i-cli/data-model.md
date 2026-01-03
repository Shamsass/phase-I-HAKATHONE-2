# Data Model: Phase I - CLI Todo Manager

**Feature**: Phase I - CLI Todo Manager
**Created**: 2026-01-03
**Status**: Final

## Overview

Phase I has a single entity: **Task**. This document defines the Task entity structure, validation rules, and state transitions.

## Entities

### Task

Represents a single todo item that a user needs to track during an application session.

#### Fields

| Field       | Type   | Constraints                      | Default      | Mutable | Description                                    |
|-------------|--------|----------------------------------|--------------|---------|------------------------------------------------|
| id          | int    | Unique, >0, auto-generated       | N/A          | No      | Unique identifier assigned on creation         |
| title       | str    | 1-200 characters, required       | N/A          | Yes     | Brief description of what needs to be done     |
| description | str    | 0-1000 characters, optional      | "" (empty)   | Yes     | Detailed information about the task            |
| status      | str    | "Complete" or "Incomplete" only  | "Incomplete" | Yes     | Current completion state of the task           |

#### Field Details

**id** (Unique Identifier)
- **Type**: Positive integer (int > 0)
- **Generation**: Auto-assigned sequentially starting from 1
- **Uniqueness**: Guaranteed unique within session - never reused even after deletion (per spec Assumption 6)
- **Mutability**: Immutable after creation (read-only)
- **Purpose**: Enables users to reference specific tasks for update/delete/mark operations

**title** (Task Name)
- **Type**: String (str)
- **Constraints**:
  - Minimum length: 1 character (cannot be empty - FR-017)
  - Maximum length: 200 characters (FR-011)
  - Leading/trailing whitespace: Allowed (user may want formatting)
- **Required**: Yes (must be provided during creation and cannot be set to empty during update)
- **Purpose**: Primary description of what user needs to do

**description** (Task Details)
- **Type**: String (str)
- **Constraints**:
  - Minimum length: 0 characters (empty is valid - description is optional)
  - Maximum length: 1000 characters (FR-012)
- **Required**: No (can be empty string)
- **Default**: Empty string ("") if not provided
- **Purpose**: Additional context or notes about the task

**status** (Completion State)
- **Type**: String enum (str with restricted values)
- **Valid Values**:
  - "Complete": Task has been finished
  - "Incomplete": Task is pending (default state)
- **Default**: "Incomplete" when task is created
- **Transitions**: Can toggle between Complete ↔ Incomplete any number of times
- **Purpose**: Tracks whether user has completed the task

#### Validation Rules

Validation is enforced by the TaskManager service layer before any operation.

**Creation (Add Task)**:
1. Title must not be empty after stripping whitespace
2. Title must not exceed 200 characters
3. Description must not exceed 1000 characters (if provided)
4. Status automatically set to "Incomplete" (user cannot specify)

**Update (Modify Task)**:
1. At least one field (title or description) must be updated
2. If updating title: must not be empty, must not exceed 200 characters
3. If updating description: must not exceed 1000 characters
4. Status cannot be updated via update operation (use mark_complete/mark_incomplete instead)

**Status Transition (Mark Complete/Incomplete)**:
1. Task ID must exist
2. No validation on status value itself (operation sets it directly)

**Deletion**:
1. Task ID must exist
2. No other validation (any task can be deleted)

#### State Transitions

```
                     [add_task]
                         ↓
                  ┌──────────────┐
                  │  Incomplete  │ ← [mark_incomplete]
                  └──────────────┘
                         ↓
                  [mark_complete]
                         ↓
                  ┌──────────────┐
                  │   Complete   │ ← [mark_incomplete]
                  └──────────────┘
                         ↓
                  [mark_complete]
                         ↓
                  (cycle repeats)

Note: [update_task] and [delete_task] can occur at any state
```

**Valid Transitions**:
- New Task → Incomplete (automatic on creation)
- Incomplete → Complete (via mark_complete operation)
- Complete → Incomplete (via mark_incomplete operation)
- Any State → Deleted (via delete_task operation)

**Invalid Transitions**: None - all operations are allowed from any state

#### Example Instances

**Minimal Task** (optional fields empty):
```python
Task(
    id=1,
    title="Buy milk",
    description="",
    status="Incomplete"
)
```

**Full Task** (all fields populated):
```python
Task(
    id=2,
    title="Complete project report",
    description="Include Q4 metrics, team feedback, and future roadmap. Due Friday.",
    status="Incomplete"
)
```

**Completed Task**:
```python
Task(
    id=3,
    title="Review PR #42",
    description="Check for security issues and test coverage",
    status="Complete"
)
```

## Relationships

Phase I has no relationships - there is only one entity (Task) with no associations to other entities.

**Future Phases** (not implemented in Phase I):
- Phase II: Task → User (many-to-one) - each task belongs to a user
- Phase III: Task → Tags (many-to-many) - tasks can have multiple tags
- Phase III: Task → AIContext (one-to-many) - tasks have AI-generated suggestions

These relationships are explicitly OUT OF SCOPE for Phase I per the specification.

## Storage Implementation

**Phase I: In-Memory Dictionary**

```python
# Internal storage structure in TaskManager class
_tasks: dict[int, Task] = {}
_next_id: int = 1

# Example state after adding 3 tasks:
{
    1: Task(id=1, title="Buy groceries", description="Milk, eggs", status="Incomplete"),
    2: Task(id=2, title="Write report", description="", status="Complete"),
    3: Task(id=3, title="Call dentist", description="Schedule cleaning", status="Incomplete")
}
```

**Key Properties**:
- O(1) lookup by ID (dictionary key)
- Insertion order preserved (Python 3.7+ guarantee)
- Memory-only (no persistence - tasks lost on exit)

**ID Generation**:
```python
def _generate_next_id(self) -> int:
    """Generate next sequential task ID."""
    task_id = self._next_id
    self._next_id += 1
    return task_id
```

## Data Constraints Summary

| Constraint Type      | Rule                                           | Enforced By      |
|----------------------|------------------------------------------------|------------------|
| Uniqueness           | Task IDs must be unique                        | TaskManager      |
| ID Sequential        | IDs assigned sequentially starting from 1      | TaskManager      |
| ID Immutability      | Task ID cannot change after creation           | Task (dataclass) |
| Title Required       | Title cannot be empty                          | TaskManager      |
| Title Length         | Title: 1-200 characters                        | TaskManager      |
| Description Length   | Description: 0-1000 characters                 | TaskManager      |
| Status Values        | Status must be "Complete" or "Incomplete"      | TaskManager      |
| No Duplicates        | Multiple tasks can have same title/description | N/A (allowed)    |

## Evolution Notes

**Phase I → Phase II Migration**:

When migrating to Phase II (database persistence), the Task entity will evolve:

1. **Add Fields**:
   - `created_at: datetime` - timestamp of creation
   - `updated_at: datetime` - timestamp of last modification
   - `user_id: int` - foreign key to user table

2. **Change Storage**:
   - From: Python dict in memory
   - To: SQLModel table with PostgreSQL backend

3. **Preserve Fields**:
   - All Phase I fields (id, title, description, status) remain unchanged
   - Validation rules remain the same

4. **Migration Strategy**:
   - TaskManager interface stays the same (methods unchanged)
   - Internal implementation switches from dict to database queries
   - Tests written in Phase I should pass in Phase II (same behavior)

This design ensures clean evolution without breaking Phase I logic.
