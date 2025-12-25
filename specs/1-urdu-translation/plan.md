# Implementation Plan: Urdu Translation for Book Chapters

**Branch**: `1-urdu-translation` | **Date**: 2025-12-23 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/[1-urdu-translation]/spec.md`

## Summary

Implement a chapter-level Urdu translation feature that allows logged-in users to translate individual book chapters from English to Urdu using an LLM. The system will provide a "Translate to Urdu" button at the beginning of each chapter, dynamically translate content while preserving formatting, and allow users to toggle between languages without affecting the existing RAG chatbot functionality.

## Technical Context

**Language/Version**: JavaScript/TypeScript, Python 3.11 for backend services
**Primary Dependencies**: Docusaurus, React, FastAPI, existing LLM API integration
**Storage**: N/A (client-side state management with caching)
**Testing**: Jest for frontend, pytest for backend
**Target Platform**: Web (GitHub Pages deployment)
**Project Type**: Web application with frontend (Docusaurus) and backend (FastAPI)
**Performance Goals**: Translation completes under 10 seconds for 95% of chapters
**Constraints**: Must not break existing RAG chatbot, embeddings, or ingestion pipeline
**Scale/Scope**: Individual chapter translation on demand

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

The implementation will follow the existing architecture patterns for the Docusaurus-based textbook and FastAPI backend. Since this feature adds functionality at the UI layer without modifying core systems, it aligns with the project constitution's principles of incremental enhancement.

## Project Structure

### Documentation (this feature)
```text
specs/1-urdu-translation/
├── plan.md              # This file (/sp.plan command output)
├── spec.md              # Feature specification
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
my-website/
├── src/
│   ├── components/
│   │   └── TranslationToggle/
│   │       ├── TranslationToggle.jsx
│   │       └── TranslationToggle.module.css
│   ├── utils/
│   │   ├── translation.js
│   │   └── contentExtractor.js
│   └── theme/
│       └── MDXContent/
│           └── Wrapper.jsx
backend/
├── src/
│   └── api/
│       └── translation.py    # Optional backend translation endpoint
```

**Structure Decision**: The feature will be implemented primarily in the Docusaurus frontend with potential backend support for translation services. The existing backend architecture (FastAPI) will remain unchanged except for potential new translation endpoints if needed.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| New translation state management | Required to track language mode per chapter | Using URL parameters would be less flexible and harder to maintain |