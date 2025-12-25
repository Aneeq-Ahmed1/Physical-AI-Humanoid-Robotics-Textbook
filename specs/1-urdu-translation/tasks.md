# Tasks: Urdu Translation for Book Chapters

**Input**: Design documents from `/specs/1-urdu-translation/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: No explicit tests requested in feature specification, so test tasks are not included.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `backend/src/`, `my-website/src/`
- Paths adjusted based on plan.md structure

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Create translation toggle component directory structure in my-website/src/components/TranslationToggle/
- [x] T002 [P] Set up translation utility functions directory in my-website/src/utils/

---
## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T003 Create TranslationToggle component in my-website/src/components/TranslationToggle/TranslationToggle.jsx
- [x] T004 [P] Create translation utility functions in my-website/src/utils/translation.js
- [x] T005 [P] Create content extraction utility in my-website/src/utils/contentExtractor.js
- [x] T006 Create CSS module for translation toggle in my-website/src/components/TranslationToggle/TranslationToggle.module.css
- [x] T007 Update Docusaurus theme wrapper to support translation in my-website/src/theme/MDXContent/Wrapper.jsx

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---
## Phase 3: User Story 1 - Translate Individual Chapters to Urdu (Priority: P1) 🎯 MVP

**Goal**: Allow logged-in users to translate individual book chapters from English to Urdu with toggle functionality

**Independent Test**: Can be fully tested by clicking the translate button and verifying the content is displayed in Urdu, while ensuring the original English content can be restored.

### Implementation for User Story 1

- [x] T008 [P] [US1] Implement language state management in TranslationToggle component
- [x] T009 [US1] Implement content extraction functionality in contentExtractor.js
- [x] T010 [US1] Implement LLM translation API call in translation.js
- [x] T011 [US1] Add translation caching mechanism in translation.js
- [x] T012 [US1] Implement rendering logic for Urdu/English toggle
- [x] T013 [US1] Add loading indicator during translation process
- [x] T014 [US1] Implement error handling and fallback to English

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---
## Phase 4: User Story 2 - Accessible Translation Controls (Priority: P1)

**Goal**: Provide easily accessible and visible translation controls with clear visual indicators of language state

**Independent Test**: Can be fully tested by verifying the button placement, visibility, and visual feedback about current language state.

### Implementation for User Story 2

- [x] T015 [P] [US2] Style translation toggle button with clear visual indicators in TranslationToggle.module.css
- [x] T016 [US2] Position translation button at the beginning of each chapter in TranslationToggle.jsx
- [x] T017 [US2] Add authentication check to show button only to logged-in users
- [x] T018 [US2] Implement visual feedback for current language state (English/Urdu)
- [x] T019 [US2] Add accessibility features (aria labels, keyboard navigation) to translation button

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---
## Phase 5: User Story 3 - Preserve Original Content (Priority: P2)

**Goal**: Ensure original English content is perfectly preserved without modifications or loss of formatting when toggling between languages

**Independent Test**: Can be fully tested by translating to Urdu, then back to English, and verifying the content matches the original.

### Implementation for User Story 3

- [x] T020 [P] [US3] Implement content preservation mechanism to store original English content
- [x] T021 [US3] Ensure formatting, code snippets, and diagrams are preserved during translation
- [x] T022 [US3] Test content restoration after multiple language toggles
- [x] T023 [US3] Verify no permanent modifications to original content during translation process

**Checkpoint**: All user stories should now be independently functional

---
## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [x] T024 [P] Update documentation to explain the Urdu translation feature
- [x] T025 Add error boundaries to prevent translation errors from breaking the page
- [ ] T026 [P] Add performance monitoring for translation API calls
- [x] T027 Ensure translation feature works across multiple chapters
- [ ] T028 Verify no regression in existing RAG chatbot functionality
- [ ] T029 Test translation feature with different chapter lengths and content types

---
## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - May integrate with US1 but should be independently testable
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - May integrate with US1/US2 but should be independently testable

### Within Each User Story

- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- Different user stories can be worked on in parallel by different team members

---
## Parallel Example: User Story 1

```bash
# Launch all foundational tasks together:
Task: "Create TranslationToggle component in my-website/src/components/TranslationToggle/TranslationToggle.jsx"
Task: "Create translation utility functions in my-website/src/utils/translation.js"
Task: "Create content extraction utility in my-website/src/utils/contentExtractor.js"
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
5. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3
3. Stories complete and integrate independently

---
## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify functionality after each task or logical group
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence