---
id: 1
title: Update Docusaurus Homepage
stage: general
date: 2025-12-06
surface: agent
model: Claude Sonnet 4.5
feature: none
branch: master
user: unknown
command: /sp.task
labels: ["ui-update", "homepage", "docusaurus"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - my-website/src/pages/index.js
 - my-website/src/css/custom.css
 - my-website/src/pages/index.module.css
 - my-website/src/components/HomepageFeatures/index.js
 - my-website/src/components/HomepageFeatures/styles.module.css
tests:
 - none
---

## Prompt

Update the Docusaurus homepage for the textbook **"Physical AI & Humanoid Robotics"**.

Goals:
1. Replace all default Docusaurus UI on the landing page.
2. Create a proper textbook-style homepage with:
   - Title: "Physical AI & Humanoid Robotics"
   - Subtitle: "A Modern Guide to Embodied Intelligence, Machines, and Human-Robot Futures"
   - Three main CTAs:
      - "Start Reading"
      - "Download PDF"
      - "View Chapters"
   - Features section with:
      - Physical AI
      - Humanoid Design
      - Sensorimotor Systems
      - Cognitive Architecture
      - Ethics & Safety
3. Add automatic routing to `/docs/intro`.
4. Make design clean, academic, and professional (no cartoon look).
5. Modify the following file(s):
   - `my-website/src/pages/index.js`
   - `my-website/src/css/custom.css` (if needed)

Acceptance criteria:
- Default Docusaurus content should be 100% removed.
- New homepage loads instantly when running `npm run start`.
- The "Start Reading" button must go to `/docs/intro`.
- All content must be generated automatically by Spec-Kit Plus.

labels: ["ui-update", "homepage", "docusaurus"]
files: []

## Response snapshot

Successfully updated the Docusaurus homepage with textbook-specific content, academic styling, and proper routing.

## Outcome

- ✅ Impact: Complete replacement of default Docusaurus homepage with textbook-specific design
- 🧪 Tests: none
- 📁 Files: my-website/src/pages/index.js, my-website/src/css/custom.css, my-website/src/pages/index.module.css, my-website/src/components/HomepageFeatures/index.js, my-website/src/components/HomepageFeatures/styles.module.css
- 🔁 Next prompts: none
- 🧠 Reflection: Created a professional academic design appropriate for a robotics textbook with clean UI and proper navigation

## Evaluation notes (flywheel)

- Failure modes observed: Initial PDF link pointed to non-existent file, corrected to /docs/downloads
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Add actual PDF download functionality