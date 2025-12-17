<!-- SYNC IMPACT REPORT:
Version change: 1.0.0 → 1.1.0
Modified principles: None (new constitution created)
Added sections: All sections added
Removed sections: None
Templates requiring updates: ✅ Updated
Follow-up TODOs: None
-->
# Unified AI-Native Book with Embedded RAG Chatbot Constitution

## Core Principles

### AI/Spec-Driven Development
Entire project driven by Spec-Kit Plus specifications and Claude Code for structured, reproducible output. All development follows the spec-driven methodology with automated documentation and consistent implementation patterns.

### Modularity & Separation of Concerns
Clear separation between book content (Docusaurus), RAG indexing pipeline, backend (FastAPI), vector storage (Qdrant), session storage (Neon Postgres), and frontend chat widget. Each component operates independently with well-defined interfaces.

### Accuracy & Grounding
All chatbot responses strictly grounded in book content (full RAG) or user-selected text only. No context leakage or hallucinations outside provided text. Responses must cite relevant book chunks as evidence.

### Cost-Free & Scalable
Exclusive use of free tiers (Cohere free API, Qdrant Cloud Free, Neon Serverless Free 0.5 GiB, Render/Vercel free hosting, GitHub Pages). No paid services or upgrades allowed during development and deployment.

### Security & Privacy
Secure handling of API keys (environment variables only); minimal session storage in Neon (optional, anonymized); no user data logging beyond necessary chat history. All sensitive information stored securely and never committed to version control.

### Reproducibility
Full setup scripts, .env examples, one-click indexing, and deployment instructions for exact replication. Every aspect of the system must be reproducible by others following the documentation.

### Ethical AI
Transparent about model limitations; low temperature for factual responses; selected-text mode strictly isolated. Clear indication when responses are based on limited context versus full book knowledge.

## Tech Stack & Implementation Standards

### Tech Stack Compliance
Cohere API (free tier) for all embeddings (embed-english-v3.0) and generation (command-r or command-r-plus); FastAPI backend; Qdrant Cloud Free Tier vector DB; Neon Serverless Postgres for chat sessions/metadata; Docusaurus book deployed on GitHub Pages; React-based chat widget with text selection detection.

### Code Quality
Python code PEP8 compliant (use Black); comprehensive type hints; unit tests ≥80% coverage (pytest); React components with PropTypes or TypeScript if possible; inline comments and docstrings required for complex logic.

### Documentation
Detailed README.md covering setup, indexing, deployment, testing; FastAPI auto-generated Swagger docs; clear comments in critical sections (chunking, retrieval, selected-text handling). All APIs and interfaces must be well-documented.

### Testing Requirements
End-to-end integration tests for both modes (full-book RAG and selected-text); minimum 50 test queries dataset with expected accuracy ≥90%; error handling for API rate limits and failures. All critical paths must have test coverage.

### Performance Standards
Chunk size ~500 tokens with overlap; top-k=3 retrieval; response time <3s on free tiers; handle books up to 500 pages. All operations must perform efficiently within free tier constraints.

### Frontend Integration
Persistent chat widget in Docusaurus (fixed position); automatic detection of user text selection; clear UI indication when selected-text mode is active. User experience must be seamless and intuitive.

## Development Workflow & Constraints

### Service Limitations
Only free tiers – Cohere (≤1,000 calls/month), Qdrant Free, Neon Free, Render/Vercel free hosting; no paid upgrades allowed. All implementations must work within these constraints.

### Language & Framework Requirements
Python 3.10+ for backend/indexing; Node.js/React for Docusaurus frontend; no additional paid SDKs. All technology choices must comply with cost-free constraint.

### Deployment Specifications
Book on GitHub Pages; FastAPI backend on Render (free web service); all environment variables managed securely. Deployment must be automated and reproducible.

### Context Handling
Support MCP Context 7 (full context awareness across project phases); maintain state between book creation (Part 1) and chatbot integration (Part 2). All context must be properly managed and transferred.

### Compatibility Standards
Works in modern browsers; English primary language; graceful degradation on API limits. System must handle API failures gracefully without crashing.

## Success Criteria & Quality Assurance

### Deliverable Requirements
(1) Fully published Docusaurus book on GitHub Pages + (2) Functional embedded RAG chatbot supporting both full-book queries and selected-text-only mode. Both components must work seamlessly together.

### Accuracy Standards
≥90% correct/grounded responses on a test set of 50 queries (30 full-book, 20 selected-text); zero hallucinations outside provided context. All responses must be factually accurate and properly sourced.

### Functionality Expectations
Selected-text mode isolates response to highlighted text only; full RAG cites relevant book chunks; chat history optionally persisted via Neon. Both modes must function correctly with clear differentiation.

### Deployment Verification
Live public URL with working chat widget; backend publicly accessible (CORS enabled); successful indexing of entire book in Qdrant. All components must be accessible and functional.

### Quality Measures
Clean, PEP8-compliant code; ≥80% test coverage; complete setup/reproduction guide; passes manual code review; demo video or live walkthrough provided. All code must meet established quality standards.

### Verification Protocols
All API keys hidden; no critical bugs (crashes, leaks); rate limit handling tested; context leakage test passed (selected mode ignores full book). System must be secure and robust.

## Governance

This constitution governs all aspects of the Unified AI-Native Book with Embedded RAG Chatbot project. All development, testing, and deployment activities must comply with these principles. Amendments require explicit documentation of changes, approval from project stakeholders, and a migration plan for existing implementations. All pull requests and reviews must verify constitutional compliance before merging.

**Version**: 1.1.0 | **Ratified**: 2025-12-14 | **Last Amended**: 2025-12-14