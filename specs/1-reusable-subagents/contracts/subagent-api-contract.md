# API Contract: Subagent System

## Base Path
`/api/subagent`

## Endpoints

### 1. Route Request to Appropriate Agent
**POST** `/api/subagent`

#### Description
Intelligently routes the request to the most appropriate subagent based on content analysis and user context.

#### Request
```json
{
  "query": "string - The user's question or request",
  "user_context": {
    "user_id": "string - Optional user identifier",
    "difficulty_preference": "enum - beginner|intermediate|advanced",
    "previous_interactions": "array - Previous conversation context"
  },
  "metadata": {
    "source": "string - Source of the request (web, mobile, etc.)",
    "timestamp": "string - ISO 8601 timestamp"
  }
}
```

#### Response
```json
{
  "request_id": "string - Unique identifier for this request",
  "agent_used": "string - Name of the agent that processed the request",
  "response": "string - The agent's response",
  "confidence": "number - Confidence score (0-1)",
  "sources": "array - List of sources used by the agent",
  "evaluation": {
    "quality_score": "number - Quality assessment (0-1)",
    "issues": "array - List of any detected issues (hallucinations, etc.)"
  },
  "timestamp": "string - ISO 8601 timestamp"
}
```

#### Status Codes
- 200: Success
- 400: Invalid request format
- 429: Rate limit exceeded
- 500: Internal server error

### 2. Book Expert Agent
**POST** `/api/subagent/book-expert`

#### Description
Direct access to the Book Expert Agent for questions requiring full-book RAG capabilities.

#### Request
```json
{
  "query": "string - Question requiring comprehensive book knowledge",
  "context": "enum - full_book|chapter_specific|section_specific",
  "include_sources": "boolean - Whether to include source citations (default: true)"
}
```

#### Response
```json
{
  "request_id": "string",
  "response": "string - Comprehensive answer based on book content",
  "sources": "array - List of book sections/chapters referenced",
  "confidence": "number - Confidence in the response (0-1)"
}
```

### 3. Selected Text Reasoner
**POST** `/api/subagent/selected-text`

#### Description
Direct access to the Selected Text Reasoner for analysis of specific text selections.

#### Request
```json
{
  "selected_text": "string - The specific text to analyze",
  "analysis_type": "enum - summary|analysis|explanation|question",
  "context_isolation": "boolean - Ensure no external context is used (default: true)"
}
```

#### Response
```json
{
  "request_id": "string",
  "response": "string - Analysis based only on the provided text",
  "text_used": "string - The text that was analyzed",
  "analysis_metadata": {
    "length": "number - Length of analyzed text",
    "complexity": "string - Estimated complexity level"
  }
}
```

### 4. Chapter Guide Agent
**POST** `/api/subagent/chapter-guide`

#### Description
Direct access to the Chapter Guide Agent for explanations at different difficulty levels.

#### Request
```json
{
  "topic": "string - The concept or topic to explain",
  "chapter": "string - Optional specific chapter reference",
  "difficulty": "enum - beginner|intermediate|advanced",
  "include_examples": "boolean - Whether to include examples (default: true)"
}
```

#### Response
```json
{
  "request_id": "string",
  "response": "string - Explanation tailored to the difficulty level",
  "difficulty_level": "string - The difficulty level used",
  "key_points": "array - Key points covered in the explanation",
  "examples": "array - Examples provided (if requested)"
}
```

### 5. Evaluation Agent
**POST** `/api/subagent/evaluate`

#### Description
Direct access to the Evaluation Agent for checking response quality.

#### Request
```json
{
  "response_to_evaluate": "string - The response to evaluate",
  "original_query": "string - The original query that generated the response",
  "expected_context": "string - Expected context for the response"
}
```

#### Response
```json
{
  "request_id": "string",
  "quality_score": "number - Overall quality score (0-1)",
  "issues": [
    {
      "type": "enum - hallucination|context_leakage|factual_error|other",
      "description": "string - Description of the issue",
      "severity": "enum - low|medium|high"
    }
  ],
  "suggestions": "array - Suggestions for improvement",
  "confidence_in_evaluation": "number - Confidence in the evaluation (0-1)"
}
```

## Common Error Response
```json
{
  "error": {
    "code": "string - Error code",
    "message": "string - Human-readable error message",
    "details": "object - Additional error details"
  }
}
```

## Authentication
All endpoints require a valid API key in the `Authorization` header:
```
Authorization: Bearer <api_key>
```

## Rate Limiting
- 100 requests per minute per API key
- 1000 requests per hour per API key