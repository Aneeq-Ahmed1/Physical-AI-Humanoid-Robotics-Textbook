# Data Model: Humanoid Robotics Textbook with Embedded Agentic RAG Chatbot

## Core Entities

### 1. Chat Session
- **Description**: Represents a user's conversation with the agent, including history and context
- **Fields**:
  - `session_id` (string): Unique identifier for the chat session
  - `user_id` (string, optional): Anonymous identifier for the user (if tracking)
  - `created_at` (datetime): Timestamp when session was created
  - `updated_at` (datetime): Timestamp when session was last updated
  - `expires_at` (datetime): When the session expires (24-hour timeout as specified)
  - `messages` (array): List of message objects in the conversation

### 2. Message
- **Description**: A single message in the chat conversation
- **Fields**:
  - `message_id` (string): Unique identifier for the message
  - `session_id` (string): Reference to the parent chat session
  - `role` (string): "user" or "assistant"
  - `content` (string): The actual message content
  - `timestamp` (datetime): When the message was created
  - `citations` (array, optional): List of source citations for assistant responses
  - `selected_text` (string, optional): Text that was selected when the message was sent

### 3. Book Content Chunk
- **Description**: A chunk of the textbook content stored in the vector database
- **Fields**:
  - `chunk_id` (string): Unique identifier for the chunk
  - `text` (string): The actual text content of the chunk
  - `source_file` (string): Original source file name in the book
  - `chunk_index` (integer): Sequential index of this chunk in the source file
  - `vector` (array): Embedding vector for similarity search
  - `metadata` (object): Additional metadata like page number, section, etc.

### 4. Retrieved Document
- **Description**: A document retrieved from the vector database as context
- **Fields**:
  - `document_id` (string): Unique identifier for the retrieved document
  - `text` (string): The text content of the retrieved chunk
  - `source_file` (string): Source file name where the chunk came from
  - `chunk_index` (integer): Index of the chunk in the source file
  - `similarity_score` (float): Similarity score from vector search
  - `page_number` (integer, optional): Page number if available in source

## Relationships

### Chat Session → Message
- One-to-Many relationship
- A chat session contains multiple messages in chronological order

### Message → Retrieved Document
- Many-to-Many relationship (via citations)
- A message can cite multiple retrieved documents as sources
- Retrieved documents can be cited by multiple messages

## Validation Rules

### Chat Session
- `session_id` must be unique
- `expires_at` must be 24 hours after `created_at`
- Session should be cleaned up after expiration

### Message
- `role` must be either "user" or "assistant"
- `content` must not be empty
- `timestamp` must be current or past time

### Book Content Chunk
- `chunk_id` must be unique
- `text` must have a minimum length (e.g., 50 characters)
- `vector` must have the correct dimension (768 for Gemini embedding-001)

## State Transitions

### Chat Session States
1. **Active**: New session created, ready for messages
2. **Inactive**: Session exists but no recent activity
3. **Expired**: Session has exceeded 24-hour timeout, eligible for cleanup

## API Considerations

The data model supports:
- Session management with automatic expiration
- Conversation history preservation
- Proper citation tracking for RAG responses
- Efficient retrieval of book content chunks
- Selection-based query handling