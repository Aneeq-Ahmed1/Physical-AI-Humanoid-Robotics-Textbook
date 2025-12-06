---
id: 0001
title: AI-Native Software Development Book Constitution
stage: constitution
date: 2025-12-05
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: master
user: user
command: /sp.constitution
labels: [constitution]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - CLAUDE.md
  - .specify/memory/constitution.md
tests:
  - null
---

## Prompt

Project: AI-Native Software Development Book
Stack: Claude Code + Spec-Kit Plus + Docusaurus + GitHub Pages + Context7 MCP

Purpose:
Produce an academically rigorous book on AI-native software development, using Spec-Kit Plus for workflow automation and Context7 MCP for advanced retrieval/grounded facts.

Principles:
- Accuracy: Claims must be verified using primary/authoritative sources via Context7 MCP or academic search.
- Rigor: At least 50% peer-reviewed references.
- Clarity: Written for a computer-science academic audience.
- Reproducibility: All claims must be traceable with APA citations.
- Originality: Zero-plagiarism tolerance.

Standards:
- APA-style citations (in-text + reference list).
- Writing level: Flesch-Kincaid grade 10–12.
- No fabricated sources, data, or citations.
- Peer-reviewed sources preferred (ACM, IEEE, Springer, Elsevier, ArXiv).

Constraints:
- Total word count: 5,000–7,000.
- Minimum 15 credible sources (≥50% peer-reviewed).
- Output: Docusaurus site + PDF with embedded citations.
- Must deploy cleanly on GitHub Pages.

MCP Rules:
- Use Context7 MCP for fact-checking, reference lookup, and verifying technical claims.
- Do not generate unsupported statements; defer to MCP search when uncertain.
- Maintain full citation traceability for all facts retrieved via MCP.

Deliverables:
1. Complete book via Spec-Kit Plus (all 5 phases).
2. Docusaurus project with structured chapters.
3. Live GitHub Pages deployment.
4. Final PDF with citations.
5. All facts cross-verified through Context7 MCP.

Success Criteria:
- All claims verified & cited.
- Zero plagiarism.
- Accurate APA references.
- Clean Docusaurus build + live deployment.
- Ready for academic review.

End.

## Response snapshot

Recorded Prompt History Record (PHR) for the constitution. ID: 0001, Path: history/prompts/constitution/0001-ai-native-software-development-book-constitution.constitution.prompt.md, Stage: constitution, Title: AI-Native Software Development Book Constitution.

## Outcome

- ✅ Impact: Constitution defined and recorded.
- 🧪 Tests: No tests performed for constitution definition.
- 📁 Files: CLAUDE.md and .specify/memory/constitution.md reviewed.
- 🔁 Next prompts: Proceed with next development phase (e.g., /sp.specify).
- 🧠 Reflection: Successfully recorded the project constitution and agent guidelines. Confirmed adherence to PHR creation mandate.

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A
