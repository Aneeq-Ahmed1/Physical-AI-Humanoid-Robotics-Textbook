# Implementation Plan: Reusable Intelligence via Claude Subagents & Agent Skills

**Branch**: `1-reusable-subagents` | **Date**: 2025-12-20 | **Spec**: [specs/1-reusable-subagents/spec.md](../spec.md)
**Input**: Feature specification from `/specs/1-reusable-subagents/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Implement a subagent architecture that enables reusable intelligence through specialized Claude agents (Book Expert, Selected Text Reasoner, Chapter Guide, Evaluation Agent) with a skill-based system and routing logic. This will allow users to access different types of AI assistance tailored to their specific needs while maintaining a consistent, modular architecture that supports future extensions.

## Technical Context

**Language/Version**: Python 3.11 (existing project uses Python/Flask backend)
**Primary Dependencies**: Anthropic Claude API, existing backend dependencies (Flask, etc.), Pydantic for data validation
**Storage**: N/A (no new storage - uses existing book content and session state)
**Testing**: pytest for unit/integration tests, existing test framework
**Target Platform**: Linux server (existing backend deployment)
**Project Type**: Web application backend (extends existing backend architecture)
**Performance Goals**: <500ms response time for agent queries, handle 100 concurrent users
**Constraints**: <200ms p95 latency for core agent operations, maintain existing chatbot functionality
**Scale/Scope**: 4 specialized agents, 7+ reusable skills, support for 10k+ daily interactions

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

Based on the Physical AI & Humanoid Robotics Textbook Project Constitution:
- ✅ Interdisciplinary Collaboration: The subagent architecture enables different AI specializations to work together
- ✅ Ethical AI Development: Evaluation agent will check for hallucinations and context leakage, ensuring transparency
- ✅ Robustness & Safety Engineering: Modular architecture with proper error handling and isolation between agents
- ✅ Human-Robot Interaction Design: Agents provide intuitive, natural interaction for different user needs
- ✅ Continuous Learning & Adaptation: Architecture designed to support adding new agents and skills over time

## Project Structure

### Documentation (this feature)

```text
specs/[###-feature]/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (extends existing backend structure)

```text
backend/
├── agent/
│   ├── __init__.py
│   ├── base_agent.py                    # Base Agent class interface
│   ├── agent_router.py                  # Agent routing logic
│   ├── skill_registry.py                # Agent skill system
│   ├── evaluation.py                    # Evaluation framework for hallucination detection
│   ├── subagents/
│   │   ├── __init__.py
│   │   ├── book_expert_agent.py         # Book Expert Agent
│   │   ├── selected_text_agent.py       # Selected Text Reasoner
│   │   ├── chapter_guide_agent.py       # Chapter Guide Agent
│   │   └── evaluation_agent.py          # Evaluation Agent
│   └── skills/
│       ├── __init__.py
│       ├── retrieval_skills.py          # retrieve_book_chunks skill
│       ├── text_analysis_skills.py      # answer_from_selected_text skill
│       ├── chapter_skills.py            # summarize_chapter, explain_like_five skills
│       └── evaluation_skills.py         # hallucination_detection skill
├── api/
│   ├── subagent_endpoints.py            # API endpoints for subagents
│   └── chat.py                          # Integration with existing chat endpoint
└── tests/
    └── test_subagents.py                # Tests for subagent system
```

**Structure Decision**: Extends existing backend architecture with new agent/ directory following modular design principles. New subagents and skills are isolated in their own directories to maintain clear separation of concerns while integrating with existing API and test structures.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| N/A | N/A | N/A |
