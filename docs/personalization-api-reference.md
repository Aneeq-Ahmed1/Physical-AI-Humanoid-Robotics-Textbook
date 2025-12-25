# Personalization API Reference

## Overview
The Personalization API provides endpoints for dynamically adapting textbook content to different difficulty levels (beginner, intermediate, advanced) based on user preferences.

## Base URL
All endpoints are prefixed with `/api/personalization`

## Authentication
No authentication required - sessions are managed client-side via session IDs

## Endpoints

### POST /api/personalization/personalize

Personalize chapter content based on the selected difficulty level.

#### Request
```json
{
  "session_id": "string",
  "chapter_content": "string",
  "difficulty_level": "string",
  "chapter_id": "string",
  "reading_position": "integer (optional, default: 0)"
}
```

**Parameters:**
- `session_id`: Unique identifier for the personalization session
- `chapter_content`: The original chapter content to be personalized
- `difficulty_level`: Difficulty level - "beginner", "intermediate", or "advanced"
- `chapter_id`: Identifier for the chapter being personalized
- `reading_position`: Current reading position in the chapter (optional)

#### Response
```json
{
  "session_id": "string",
  "personalized_content": "string",
  "difficulty_level": "string",
  "chapter_id": "string",
  "timestamp": "string"
}
```

**Response Fields:**
- `session_id`: The session ID (same as input)
- `personalized_content`: The content transformed to the requested difficulty level
- `difficulty_level`: The difficulty level applied
- `chapter_id`: The chapter ID (same as input)
- `timestamp`: ISO 8601 timestamp of the response

#### Example Request
```json
{
  "session_id": "sess_12345",
  "chapter_content": "# Introduction to Robotics\nRobots are machines...",
  "difficulty_level": "beginner",
  "chapter_id": "intro-robotics"
}
```

#### Example Response
```json
{
  "session_id": "sess_12345",
  "personalized_content": "BEGINNER LEVEL EXPLANATION:\n\nThink of robots like advanced toys...",
  "difficulty_level": "beginner",
  "chapter_id": "intro-robotics",
  "timestamp": "2025-12-22T10:30:45.123456"
}
```

#### Error Responses
- `400 Bad Request`: Invalid difficulty level or missing required fields
- `500 Internal Server Error`: Processing error

---

### POST /api/personalization/change-difficulty

Change the difficulty level for an existing session and return new personalized content.

#### Request
```json
{
  "session_id": "string",
  "chapter_content": "string",
  "difficulty_level": "string",
  "chapter_id": "string",
  "reading_position": "integer (optional, default: 0)"
}
```

**Parameters:**
- `session_id`: Session ID to update
- `chapter_content`: The original chapter content (used for re-processing)
- `difficulty_level`: New difficulty level - "beginner", "intermediate", or "advanced"
- `chapter_id`: Chapter identifier
- `reading_position`: Updated reading position (optional)

#### Response
Same as `/personalize` endpoint

#### Example Request
```json
{
  "session_id": "sess_12345",
  "chapter_content": "# Introduction to Robotics\nRobots are machines...",
  "difficulty_level": "advanced",
  "chapter_id": "intro-robotics",
  "reading_position": 150
}
```

#### Error Responses
- `400 Bad Request`: Invalid difficulty level
- `404 Not Found`: Session not found
- `500 Internal Server Error`: Processing error

---

### POST /api/personalization/toggle-original

Toggle back to the original chapter content for a session.

#### Request
```json
{
  "session_id": "string"
}
```

**Parameters:**
- `session_id`: Session ID to retrieve original content for

#### Response
```json
{
  "session_id": "string",
  "original_content": "string",
  "timestamp": "string"
}
```

**Response Fields:**
- `session_id`: The session ID (same as input)
- `original_content`: The original chapter content as it was before personalization
- `timestamp`: ISO 8601 timestamp of the response

#### Example Request
```json
{
  "session_id": "sess_12345"
}
```

#### Example Response
```json
{
  "session_id": "sess_12345",
  "original_content": "# Introduction to Robotics\nRobots are machines...",
  "timestamp": "2025-12-22T10:35:22.789012"
}
```

#### Error Responses
- `404 Not Found`: Session not found
- `500 Internal Server Error`: Processing error

---

### DELETE /api/personalization/session/{session_id}

Clear a personalization session from the cache.

#### Path Parameters
- `session_id`: The session ID to clear

#### Response
```json
{
  "message": "string",
  "session_id": "string"
}
```

**Response Fields:**
- `message`: Confirmation message
- `session_id`: The session ID that was cleared

#### Example Response
```json
{
  "message": "Session cleared successfully",
  "session_id": "sess_12345"
}
```

#### Error Responses
- `404 Not Found`: Session not found
- `500 Internal Server Error`: Processing error

## Data Models

### PersonalizationSession
```typescript
interface PersonalizationSession {
  session_id: string;
  difficulty_level: string; // "beginner" | "intermediate" | "advanced"
  original_content: string;
  personalized_content: string;
  chapter_id: string;
  created_at: number; // Unix timestamp
  last_accessed: number; // Unix timestamp
  reading_position: number;
}
```

### PersonalizationPreferences
```typescript
interface PersonalizationPreferences {
  difficulty_level: "beginner" | "intermediate" | "advanced";
  reading_position: number;
  preferred_format?: string; // "text", "visual", "audio", etc.
  content_focus?: string; // Specific topic focus if any
}
```

## Error Codes

| Status Code | Error Type | Description |
|-------------|------------|-------------|
| 400 | `invalid_difficulty` | Invalid difficulty level provided |
| 400 | `missing_required_field` | Required field missing from request |
| 404 | `session_not_found` | Personalization session does not exist |
| 500 | `processing_error` | Internal error during content processing |

## Session Management

- Sessions automatically expire after 1 hour of inactivity (configurable)
- Session cleanup occurs periodically (approximately 1 in 10 requests triggers cleanup)
- Session data is stored in-memory with thread-safe access
- Session IDs should be generated client-side using UUIDs

## Implementation Notes

- The Chapter Guide Agent processes content with appropriate difficulty level
- Content transformations are cached per session to avoid re-processing
- Original content is preserved in the session for toggle functionality
- Reading position is maintained across difficulty changes