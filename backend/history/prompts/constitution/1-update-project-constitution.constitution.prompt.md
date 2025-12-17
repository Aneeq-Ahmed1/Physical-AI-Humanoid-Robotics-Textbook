---
id: 1
title: Update Project Constitution
stage: constitution
date: 2025-12-14
surface: agent
model: Claude Sonnet 4.5
feature: none
branch: master
user: user
command: /sp.constitution
labels: [constitution, governance, ai-native-book, rag-chatbot]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
tests:
  - none
---

## Prompt

```text
Project: Unified AI-Native Book with Embedded RAG Chatbot (Full Project – Both Requirements)
Core principles:

AI/Spec-Driven Development: Entire project driven by Spec-Kit Plus specifications and Claude Code for structured, reproducible output.
Modularity & Separation of Concerns: Clear separation between book content (Docusaurus), RAG indexing pipeline, backend (FastAPI), vector storage (Qdrant), session storage (Neon Postgres), and frontend chat widget.
Accuracy & Grounding: All chatbot responses strictly grounded in book content (full RAG) or user-selected text only (no context leakage or hallucinations outside provided text).
Cost-Free & Scalable: Exclusive use of free tiers (Cohere free API, Qdrant Cloud Free, Neon Serverless Free 0.5 GiB, Render/Vercel free hosting, GitHub Pages).
Security & Privacy: Secure handling of API keys (environment variables only); minimal session storage in Neon (optional, anonymized); no user data logging beyond necessary chat history.
Reproducibility: Full setup scripts, .env examples, one-click indexing, and deployment instructions for exact replication.
Ethical AI: Transparent about model limitations; low temperature for factual responses; selected-text mode strictly isolated.

Key standards:

Tech Stack Compliance: Cohere API (free tier) for all embeddings (embed-english-v3.0) and generation (command-r or command-r-plus); FastAPI backend; Qdrant Cloud Free Tier vector DB; Neon Serverless Postgres for chat sessions/metadata; Docusaurus book deployed on GitHub Pages; React-based chat widget with text selection detection.
Code Quality: Python code PEP8 compliant (use Black); comprehensive type hints; unit tests ≥80% coverage (pytest); React components with PropTypes or TypeScript if possible; inline comments and docstrings.
Documentation: Detailed README.md covering setup, indexing, deployment, testing; FastAPI auto-generated Swagger docs; clear comments in critical sections (chunking, retrieval, selected-text handling).
Testing: End-to-end integration tests for both modes (full-book RAG and selected-text); minimum 50 test queries dataset with expected accuracy ≥90%; error handling for API rate limits and failures.
Performance: Chunk size ~500 tokens with overlap; top-k=3 retrieval; response time <3s on free tiers; handle books up to 500 pages.
Frontend Integration: Persistent chat widget in Docusaurus (fixed position); automatic detection of user text selection; clear UI indication when selected-text mode is active.

Constraints:

Services: Only free tiers – Cohere (≤1,000 calls/month), Qdrant Free, Neon Free, Render/Vercel free hosting; no paid upgrades.
Languages/Frameworks: Python 3.10+ for backend/indexing; Node.js/React for Docusaurus frontend; no additional paid SDKs.
Deployment: Book on GitHub Pages; FastAPI backend on Render (free web service); all environment variables managed securely.
Context Handling: Support MCP Context 7 (full context awareness across project phases); maintain state between book creation (Part 1) and chatbot integration (Part 2).
Time & Scope: Total implementation 20-40 hours; no external paid tools or services; all code original or properly attributed from official docs.
Compatibility: Works in modern browsers; English primary language; graceful degradation on API limits.

Success criteria:

Complete Deliverables: (1) Fully published Docusaurus book on GitHub Pages + (2) Functional embedded RAG chatbot supporting both full-book queries and selected-text-only mode.
Accuracy: ≥90% correct/grounded responses on a test set of 50 queries (30 full-book, 20 selected-text); zero hallucinations outside provided context.
Functionality: Selected-text mode isolates response to highlighted text only; full RAG cites relevant book chunks; chat history optionally persisted via Neon.
Deployment: Live public URL with working chat widget; backend publicly accessible (CORS enabled); successful indexing of entire book in Qdrant.
Quality & Reproducibility: Clean, PEP8-compliant code; ≥80% test coverage; complete setup/reproduction guide; passes manual code review; demo video or live walkthrough provided.
Verification: All API keys hidden; no critical bugs (crashes, leaks); rate limit handling tested; context leakage test passed (selected mode ignores full book).
```

## Response snapshot

Updated the project constitution file (.specify/memory/constitution.md) to reflect the requirements for the Unified AI-Native Book with Embedded RAG Chatbot project. The new constitution includes:

- Core principles: AI/Spec-Driven Development, Modularity & Separation of Concerns, Accuracy & Grounding, Cost-Free & Scalable, Security & Privacy, Reproducibility, and Ethical AI
- Tech Stack & Implementation Standards: Tech Stack Compliance, Code Quality, Documentation, Testing Requirements, Performance Standards, and Frontend Integration
- Development Workflow & Constraints: Service Limitations, Language & Framework Requirements, Deployment Specifications, Context Handling, and Compatibility Standards
- Success Criteria & Quality Assurance: Deliverable Requirements, Accuracy Standards, Functionality Expectations, Deployment Verification, Quality Measures, and Verification Protocols
- Governance section outlining constitutional oversight and amendment procedures

## Outcome

- ✅ Impact: Created comprehensive project constitution with 7 core principles and detailed standards
- 🧪 Tests: No tests required for constitution creation
- 📁 Files: Updated .specify/memory/constitution.md with new constitution content
- 🔁 Next prompts: Proceed with project implementation following the established constitution
- 🧠 Reflection: The constitution provides a solid foundation for the AI-native book project with clear guidelines for implementation

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): Not applicable
- Prompt variant (if applicable): Not applicable
- Next experiment (smallest change to try): Begin implementation of project components following the constitution