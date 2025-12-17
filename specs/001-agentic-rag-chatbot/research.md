# Research Summary: Humanoid Robotics Textbook with Embedded Agentic RAG Chatbot

## Overview
This research document captures the technical decisions and approaches for implementing an agentic RAG chatbot for the Humanoid Robotics textbook using Google Gemini API instead of Cohere as originally specified.

## Technology Decisions

### 1. LLM and API Selection
- **Decision**: Use Google Gemini API instead of Cohere API
- **Rationale**: User specifically requested Google Gemini API (free tier via Google AI Studio) instead of Cohere. Gemini offers strong function calling capabilities suitable for the agentic behavior required.
- **Alternatives considered**:
  - Cohere Command-R (original spec): Good RAG capabilities but switching to meet user requirements
  - OpenAI GPT: Would require different payment model, Gemini free tier is sufficient
  - Anthropic Claude: Similar payment model concerns

### 2. Backend Framework
- **Decision**: FastAPI for the backend
- **Rationale**: FastAPI provides excellent support for async operations, automatic API documentation, and works well with Python-based ML/AI tools. It's lightweight and perfect for the free tier deployment on Render.
- **Alternatives considered**:
  - Flask: More familiar but less performant for async operations
  - Express.js: Would require switching to Node.js ecosystem

### 3. Vector Database
- **Decision**: Continue using Qdrant Cloud Free Tier
- **Rationale**: Already specified in original requirements and works well with Python embeddings. No need to change from original spec.
- **API Details**:
  - Endpoint: https://6a02f705-256d-4d8a-9fb8-45e16c7df3ad.us-east4-0.gcp.cloud.qdrant.io
  - API Key: Provided in user requirements

### 4. Session Storage
- **Decision**: Neon Serverless Postgres for chat sessions
- **Rationale**: Free tier meets requirements, serverless means no maintenance, and integrates well with Python backend.
- **Connection**: postgresql://neondb_owner:npg_5dtYkfFo1ENp@ep-gentle-river-a4da4s3u-pooler.us-east-1.aws.neon.tech/neondb

### 5. Frontend Integration
- **Decision**: Docusaurus with @chatscope/chat-ui-kit-react
- **Rationale**: Docusaurus is already set up for the textbook, and chatscope provides a clean UI for chat interfaces. Perfect for embedding the chatbot widget.

## Architecture Approach

### Agentic Behavior Implementation
The agent will use Google Gemini's function calling capabilities to decide between two primary tools:
1. `retrieve_from_book` - For full-book RAG queries
2. `answer_from_selected_text` - For selected-text-only mode

### Text Selection Detection
The frontend will implement a global selection listener that detects when users highlight text in the textbook and store it for the next query.

### Rate Limiting Strategy
With Gemini free tier ~15 RPM, the system will implement queuing and graceful degradation when rate limits are hit.

## Implementation Challenges & Solutions

### Challenge 1: Context Switching Between Modes
- **Issue**: Ensuring zero context leakage between full-book RAG and selected-text modes
- **Solution**: Clear state management in the agent to use only the selected_text when provided, ignoring any full-book retrieval

### Challenge 2: Book Content Chunking and Embedding
- **Issue**: Properly chunking book content for effective retrieval
- **Solution**: Using RecursiveCharacterTextSplitter with ~500 token chunks and 50-token overlap, then embedding with Gemini's embedding-001 model

### Challenge 3: Citations and Grounding
- **Issue**: Providing proper citations to book content as required by the spec
- **Solution**: The retrieval tool will return source_file and chunk_index metadata that can be formatted into proper citations

## Dependencies

### Backend Dependencies:
- fastapi: Web framework
- uvicorn: ASGI server
- google-generativeai: Gemini API client
- qdrant-client: Vector database client
- psycopg2-binary: Postgres adapter
- python-dotenv: Environment variable management
- pydantic: Data validation

### Frontend Dependencies:
- @chatscope/chat-ui-kit-react: Chat UI components
- Docusaurus: Book hosting platform

## API Design Considerations

The backend will expose:
1. `/tools/retrieve_book` - Embeds query, searches Qdrant, returns formatted documents
2. `/tools/answer_from_selected` - Directly uses provided selected_text
3. `/chat` - Main endpoint handling the Gemini function calling loop with chat history

## Deployment Strategy

- Book: GitHub Pages (Docusaurus)
- Backend: Render free tier
- Vector DB: Qdrant Cloud Free
- Session Storage: Neon Serverless Postgres

All components stay within free tier constraints as required by the constitution.