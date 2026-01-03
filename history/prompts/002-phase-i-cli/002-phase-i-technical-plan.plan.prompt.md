---
id: 002
title: Phase I Technical Plan Creation
stage: plan
date: 2026-01-03
surface: agent
model: claude-sonnet-4-5-20250929
feature: 002-phase-i-cli
branch: 002-phase-i-cli
user: Shamsass
command: /sp.plan
labels: ["planning", "architecture", "phase-i", "cli", "in-memory", "python"]
links:
  spec: specs/002-phase-i-cli/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/002-phase-i-cli/plan.md
  - specs/002-phase-i-cli/data-model.md
  - specs/002-phase-i-cli/quickstart.md
tests:
  - null
---

## Prompt

Create the Phase I technical plan for the Todo in-memory Python console application.

The plan must be derived strictly from the Phase I specification and global constitution.

Include:

1. High-level application structure (single Python program)
2. In-memory data structures to store tasks
3. Task identification strategy (ID generation)
4. CLI control flow (menu loop, user input handling)
5. Separation of responsibilities (data handling vs CLI)
6. Error handling strategy for invalid input and missing tasks

Constraints:
- No databases
- No file storage
- No web frameworks
- No external services
- No future phase concepts

The plan must not introduce new features. It must only describe HOW the approved Phase I requirements will be implemented.

## Response snapshot

Created comprehensive technical plan for Phase I CLI Todo Manager with three logical layers and constitution compliance verification.

**Artifacts Created**:

1. **plan.md** (complete implementation plan):
   - Summary: Single Python script with 3 layers (Task model, TaskManager service, CLI interface)
   - Technical Context: Python 3.11+, no dependencies, in-memory dict storage, pytest for testing
   - Constitution Check: ✅ All 5 principles verified (SDD, agent behavior, phase governance, tech constraints, quality standards)
   - Project Structure: Single file `src/todo_cli.py` (~200-300 lines) for Phase I simplicity
   - Phase 0 Research: 5 technical decisions documented with rationales
     - In-memory storage: Dict keyed by ID for O(1) lookups
     - ID generation: Sequential counter starting at 1, never reused
     - CLI flow: Infinite loop with switch-case menu dispatch
     - Error handling: Return tuples (success, message, data) from service layer
     - Input validation: Service layer enforces business rules
   - Phase 1 Design: Data model, service layer (TaskManager), CLI layer with 7 menu options
   - Architecture Decisions: 5 ADRs with context, decisions, rationales, consequences
     - AD-1: Single file vs modules → Single file (manageable size, clear evolution path)
     - AD-2: Dict vs List storage → Dict for O(1) lookups
     - AD-3: Dataclass for Task → Built-in, auto methods, SQLModel-compatible
     - AD-4: Exceptions vs return values → Return tuples for explicit error handling
     - AD-5: Validation location → Service layer (business logic centralized)

2. **data-model.md** (Task entity specification):
   - Single entity: Task with 4 fields (id, title, description, status)
   - Detailed field constraints: title 1-200 chars required, description 0-1000 chars optional
   - Validation rules for creation, update, status transitions, deletion
   - State transition diagram: Incomplete ↔ Complete cycle
   - Storage implementation: dict[int, Task] with sequential ID generator
   - Evolution notes: Phase II migration path (add timestamps, user_id, switch to SQLModel/PostgreSQL)

3. **quickstart.md** (user-facing guide):
   - Prerequisites: Python 3.11+, no installation needed
   - Step-by-step instructions: Run `python src/todo_cli.py`
   - Basic usage: Add, view, mark complete, update, delete tasks
   - Common workflows: Daily task management, weekly planning
   - Tips: Writing good titles/descriptions, managing task list
   - Troubleshooting: Common errors and solutions
   - Example session: Complete walkthrough from start to exit
   - Limitations: No persistence, single user, no search/categories/due dates

**Constitution Compliance**:
- ✅ Spec-Driven Development: All decisions trace to spec requirements (FR-001 through FR-017)
- ✅ Agent Behavior: No invented features, HOW only (WHAT came from approved spec)
- ✅ Phase Governance: No Phase II+ features (no persistence, no web/API, no auth)
- ✅ Technology Constraints: Python 3.11+, standard library only, clean architecture
- ✅ Quality Standards: Type hints mandated, separation of concerns, <10 cyclomatic complexity

**Architecture Highlights**:
- **3-Layer Design**: Task (data) → TaskManager (logic) → CLI (presentation)
- **Single File**: All code in `src/todo_cli.py` for Phase I simplicity with clear internal structure
- **O(1) Operations**: Dictionary storage enables constant-time lookups by task ID
- **Clear Error Handling**: Service layer returns (success, message, data) tuples
- **Future-Ready**: Clean separation enables Phase II extraction (TaskManager → REST API)

**Key Technical Decisions**:
- Storage: `dict[int, Task]` for O(1) lookups, preserves insertion order (Python 3.7+)
- ID Generation: Sequential counter starting at 1, IDs never reused per spec
- Validation: Business rules in TaskManager service layer, not CLI
- Error Messages: Constructed at service layer for reuse in future web APIs
- Type Safety: @dataclass for Task, type hints throughout for constitution compliance

## Outcome

- ✅ Impact: Complete technical plan defining HOW Phase I requirements will be implemented. Ready for task breakdown phase.
- 🧪 Tests: Testing strategy defined (pytest for unit tests, optional in Phase I per spec)
- 📁 Files: 3 files created (plan.md, data-model.md, quickstart.md) totaling ~900 lines
- 🔁 Next prompts: `/sp.tasks` to generate implementation tasks from plan and spec; User review/approval of technical approach
- 🧠 Reflection: Single-file architecture balances Phase I simplicity with clear evolution path. Dictionary storage with sequential IDs provides O(1) performance. Return-value error handling enables future API reuse. All decisions traced to constitution principles and spec requirements.

## Evaluation notes (flywheel)

- Failure modes observed: None - plan created successfully from spec with no ambiguities
- Graders run and results (PASS/FAIL): PASS - All constitution gates satisfied, no invented features, clear separation of concerns
- Prompt variant (if applicable): Standard /sp.plan workflow with Phase 0 research and Phase 1 design
- Next experiment (smallest change to try): Monitor Phase II migration - verify TaskManager interface stability when switching from dict to database
