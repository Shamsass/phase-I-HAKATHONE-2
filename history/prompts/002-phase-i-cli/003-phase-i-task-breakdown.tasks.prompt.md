---
id: 003
title: Phase I Task Breakdown Creation
stage: tasks
date: 2026-01-03
surface: agent
model: claude-sonnet-4-5-20250929
feature: 002-phase-i-cli
branch: 002-phase-i-cli
user: Shamsass
command: /sp.tasks
labels: ["tasks", "implementation", "phase-i", "cli", "breakdown"]
links:
  spec: specs/002-phase-i-cli/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/002-phase-i-cli/tasks.md
tests:
  - null
---

## Prompt

Break the Phase I technical plan into atomic implementation tasks.

Each task must include:
- Task ID
- Clear description
- Preconditions
- Expected output
- Artifacts to be created or modified
- Explicit references to the Phase I specification and plan sections

Tasks must cover:
1. Task data model and in-memory storage
2. CLI menu and application loop
3. Add task functionality
4. View task list functionality
5. Update task functionality
6. Delete task functionality
7. Mark task complete/incomplete
8. Input validation and error handling
9. Application startup and exit flow

Rules:
- Tasks must be small, testable, and sequential
- Do NOT introduce new features
- Do NOT include future phases
- Tasks must be sufficient to fully implement Phase I

## Response snapshot

Created comprehensive task breakdown with 26 tasks (22 required + 4 optional tests) organized into 6 phases.

**Task Organization**:

1. **Phase 1: Project Setup** (2 tasks)
   - T001: Create directory structure (src/, tests/unit/)
   - T002: Create main Python file with imports

2. **Phase 2: Data Layer** (2 tasks)
   - T003: Define Task @dataclass with 4 fields (id, title, description, status)
   - T004: Define status constants (STATUS_INCOMPLETE, STATUS_COMPLETE)

3. **Phase 3: Service Layer - TaskManager** (8 tasks)
   - T005: Initialize TaskManager with storage dict and ID counter
   - T006: Implement add_task with validation (FR-002, FR-011, FR-012, FR-017)
   - T007: Implement get_all_tasks preserving insertion order (FR-005, FR-013)
   - T008: Implement get_task with error handling (FR-009)
   - T009: Implement update_task with validation (FR-007)
   - T010: Implement delete_task (FR-008)
   - T011: Implement mark_complete (FR-006)
   - T012: Implement mark_incomplete (FR-006)

4. **Phase 4: CLI Layer** (9 tasks)
   - T013: Create CLI class with TaskManager dependency
   - T014: Implement display_menu with 7 options (FR-001)
   - T015: Implement handle_add_task (User Story 1)
   - T016: Implement handle_view_tasks with table formatting (User Story 2, FR-010)
   - T017: Implement handle_mark_complete with input validation (User Story 3)
   - T018: Implement handle_mark_incomplete (User Story 3)
   - T019: Implement handle_update_task showing current values (User Story 4)
   - T020: Implement handle_delete_task (User Story 5)
   - T021: Implement run() method with menu loop (FR-015, FR-016)

5. **Phase 5: Entry Point** (1 task)
   - T022: Implement main() function and __main__ block

6. **Phase 6: Testing - OPTIONAL** (4 tasks)
   - T023: Create test file with fixtures
   - T024: Test add_task validations
   - T025: Test retrieval and status changes
   - T026: Test update and delete operations

**Task Details**:

Each task includes:
- **Preconditions**: What must be complete before starting
- **Expected Output**: Specific deliverable
- **Artifacts**: Exact file paths and approximate line counts
- **Implementation Details**: Code snippets or pseudocode
- **Spec References**: Exact FR-XXX requirements and user stories
- **Plan References**: Specific plan sections and architecture decisions
- **Validation Criteria**: How to verify task completion

**Traceability**:
- All 17 functional requirements (FR-001 to FR-017) mapped to tasks
- All 5 user stories (US1-US5) covered with acceptance scenarios
- All edge cases from spec addressed (non-numeric input, empty list, invalid ID)
- Error messages use exact text from spec (FR-009, FR-010, FR-016)

**Execution Strategy**:

**Sequential Path** (single developer):
Setup (T001-T002) → Data (T003-T004) → Service Core (T005-T008) → Service Operations (T009-T012) → CLI Core (T013-T014) → CLI Handlers (T015-T020) → Entry (T021-T022) → Optional Tests (T023-T026)

**Parallel Opportunities**:
- Phase 3: T009-T012 (service methods) - different methods, no interdependencies
- Phase 4: T015-T020 (CLI handlers) - different handlers, no interdependencies
- Phase 6: T023-T026 (tests) - independent test suites

**Estimated Code Size**:
- Phase 1: ~10 lines
- Phase 2: ~20 lines
- Phase 3: ~120 lines
- Phase 4: ~150 lines
- Phase 5: ~10 lines
- Phase 6: ~80 lines (optional)
- **Total**: ~310 lines (230 without tests) - matches plan estimate

**Key Design Decisions Reflected**:
- Single file architecture (src/todo_cli.py)
- 3-layer separation (Task → TaskManager → CLI)
- Return tuple error handling (success, message, data)
- Service layer validation (not CLI layer)
- Dictionary storage with O(1) lookups
- Sequential ID generation starting at 1

**Constitution Compliance**:
- ✅ All tasks trace to approved spec (no invented features)
- ✅ Type hints mandated in implementation details
- ✅ Error messages use exact spec text
- ✅ Clean architecture enforced (data → logic → presentation)
- ✅ No Phase II+ features (no persistence, no web/API)

## Outcome

- ✅ Impact: Complete implementation roadmap with 26 atomic tasks. Each task is independently testable and traceable to spec requirements. Ready for implementation phase.
- 🧪 Tests: 4 optional test tasks (T023-T026) covering TaskManager business logic per constitution allowance for Phase I
- 📁 Files: tasks.md created (~500 lines) with full task definitions, dependencies, and execution strategy
- 🔁 Next prompts: `/sp.implement` to execute tasks; User approval of task breakdown; Begin implementation starting with T001
- 🧠 Reflection: Task breakdown successfully maps all 17 functional requirements to 22 implementation tasks. Parallel opportunities identified (Phase 3: 4 tasks, Phase 4: 6 tasks). Sequential dependencies clear. Estimated 230-310 lines matches plan. Tests optional per Phase I spec.

## Evaluation notes (flywheel)

- Failure modes observed: None - all spec requirements mapped to tasks, no ambiguities
- Graders run and results (PASS/FAIL): PASS - All FR-XXX requirements covered, all user stories addressable, traceability complete
- Prompt variant (if applicable): Standard /sp.tasks workflow with phase-by-phase organization
- Next experiment (smallest change to try): Monitor implementation - verify task granularity is appropriate (not too small/large). Track if parallel opportunities used effectively.
