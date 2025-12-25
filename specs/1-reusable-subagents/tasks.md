---
description: "Task list for implementing reusable intelligence via Claude Subagents & Agent Skills"
---

# Tasks: Reusable Intelligence via Claude Subagents & Agent Skills

**Input**: Design documents from `/specs/1-reusable-subagents/`
**Prerequisites**: plan.md (not found), spec.md (required for user stories), research.md (not found), data-model.md (not found), contracts/ (not found)

**Tests**: The examples below include test tasks. Tests are OPTIONAL - only include them if explicitly requested in the feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Backend**: `backend/src/`, `backend/agent/`, `backend/api/`
- Paths shown below follow the existing project structure

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure for subagent architecture

- [x] T001 Create subagent directory structure in backend/agent/subagents/
- [x] T002 [P] Create skills directory structure in backend/agent/skills/
- [x] T003 [P] Create routing directory structure in backend/agent/routing/

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T004 Define base Agent class interface in backend/agent/base_agent.py
- [x] T005 [P] Create Agent skill system in backend/agent/skill_registry.py
- [x] T006 [P] Create Agent routing logic in backend/agent/agent_router.py
- [x] T007 Create evaluation framework for hallucination detection in backend/agent/evaluation.py
- [x] T008 Configure dependency injection for agent system in backend/agent/__init__.py
- [x] T009 Update main.py to initialize agent system on startup

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Book Expert Agent Access (Priority: P1) 🎯 MVP

**Goal**: Implement a Book Expert Agent that answers questions using full-book RAG capabilities

**Independent Test**: Can be fully tested by querying the agent with complex questions spanning multiple chapters and verifying the responses are well-grounded in the book content and accurate.

### Implementation for User Story 1

- [x] T010 [P] [US1] Create BookExpertAgent class in backend/agent/subagents/book_expert_agent.py
- [x] T011 [P] [US1] Create retrieve_book_chunks skill in backend/agent/skills/retrieval_skills.py
- [x] T012 [US1] Implement RAG functionality in BookExpertAgent (depends on T010, T011)
- [x] T013 [US1] Add BookExpertAgent to agent registry (depends on T005)
- [x] T014 [US1] Create API endpoint for Book Expert Agent in backend/api/subagent_endpoints.py
- [x] T015 [US1] Integrate Book Expert Agent with existing chat endpoint in backend/api/chat.py
- [x] T016 [US1] Add logging for Book Expert Agent operations

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Selected Text Reasoning (Priority: P2)

**Goal**: Implement a Selected Text Reasoner that answers questions strictly from highlighted text without pulling in external information.

**Independent Test**: Can be fully tested by providing specific text selections and verifying the agent responds only with information derived from that text, without hallucination or external context.

### Implementation for User Story 2

- [x] T017 [P] [US2] Create SelectedTextAgent class in backend/agent/subagents/selected_text_agent.py
- [x] T018 [P] [US2] Create answer_from_selected_text skill in backend/agent/skills/text_analysis_skills.py
- [x] T019 [US2] Implement strict text isolation in SelectedTextAgent (depends on T017, T018)
- [x] T020 [US2] Add SelectedTextAgent to agent registry (depends on T005)
- [x] T021 [US2] Create API endpoint for Selected Text Agent in backend/api/subagent_endpoints.py
- [x] T022 [US2] Integrate Selected Text Agent with existing chat endpoint in backend/api/chat.py
- [x] T023 [US2] Add strict isolation validation for text-only responses

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Adaptive Chapter Guidance (Priority: P3)

**Goal**: Implement a Chapter Guide Agent that explains concepts at beginner/intermediate/advanced levels.

**Independent Test**: Can be fully tested by requesting the same concept at different difficulty levels and verifying the explanations are appropriately adjusted in complexity and depth.

### Implementation for User Story 3

- [x] T024 [P] [US3] Create ChapterGuideAgent class in backend/agent/subagents/chapter_guide_agent.py
- [x] T025 [P] [US3] Create summarize_chapter skill in backend/agent/skills/chapter_skills.py
- [x] T026 [P] [US3] Create explain_like_five skill in backend/agent/skills/chapter_skills.py
- [x] T027 [US3] Implement difficulty level adaptation in ChapterGuideAgent (depends on T024-T026)
- [x] T028 [US3] Add ChapterGuideAgent to agent registry (depends on T005)
- [x] T029 [US3] Create API endpoint for Chapter Guide Agent in backend/api/subagent_endpoints.py
- [x] T030 [US3] Integrate Chapter Guide Agent with existing chat endpoint in backend/api/chat.py

**Checkpoint**: All user stories should now be independently functional

---

## Phase 6: User Story 4 - Response Quality Evaluation (Priority: P4)

**Goal**: Implement an Evaluation Agent that checks responses for hallucinations and context leakage.

**Independent Test**: Can be fully tested by providing various responses and verifying the agent correctly identifies hallucinations, context issues, and accuracy problems.

### Implementation for User Story 4

- [x] T031 [P] [US4] Create EvaluationAgent class in backend/agent/subagents/evaluation_agent.py
- [x] T032 [P] [US4] Create hallucination_detection skill in backend/agent/skills/evaluation_skills.py
- [x] T033 [US4] Implement evaluation logic in EvaluationAgent (depends on T031, T032)
- [x] T034 [US4] Add EvaluationAgent to agent registry (depends on T005)
- [x] T035 [US4] Create API endpoint for Evaluation Agent in backend/api/subagent_endpoints.py
- [x] T036 [US4] Integrate evaluation step into existing response pipeline in backend/agent/llm_agent.py

**Checkpoint**: All four subagents should now be functional and integrated

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T037 [P] Update documentation for subagent architecture in docs/subagents.md
- [ ] T038 Refactor existing chat logic to use new subagent architecture
- [x] T039 [P] Create comprehensive tests for subagent system in backend/tests/test_subagents.py
- [ ] T040 Performance optimization across all agents
- [ ] T041 Security validation of agent routing and isolation
- [ ] T042 Run validation to ensure existing chatbot continues to work

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3 → P4)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - May integrate with US1 but should be independently testable
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - May integrate with US1/US2 but should be independently testable
- **User Story 4 (P4)**: Can start after Foundational (Phase 2) - May integrate with US1/US2/US3 but should be independently testable

### Within Each User Story

- Core agent implementation before API endpoints
- Skills before agents that use them
- Agent registration before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- Different user stories can be worked on in parallel by different team members

---

## Parallel Example: User Story 1

```bash
# Launch all components for User Story 1 together:
Task: "Create BookExpertAgent class in backend/agent/subagents/book_expert_agent.py"
Task: "Create retrieve_book_chunks skill in backend/agent/skills/retrieval_skills.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Add User Story 4 → Test independently → Deploy/Demo
6. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3
   - Developer D: User Story 4
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Ensure existing chatbot functionality continues to work throughout implementation