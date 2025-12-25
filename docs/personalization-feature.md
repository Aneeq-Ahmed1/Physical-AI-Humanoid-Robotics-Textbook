# Chapter Content Personalization Feature

## Overview
The Chapter Content Personalization feature allows logged-in users to adapt textbook content to their preferred skill level (beginner, intermediate, advanced). The system dynamically rewrites content in real-time while preserving the original text for later reference.

## Features

### Skill Level Selection
- Users can select from three difficulty levels:
  - **Beginner**: Simplified explanations with analogies
  - **Intermediate**: Technical details with context
  - **Advanced**: Deep technical analysis

### Content Personalization
- Real-time content transformation based on selected difficulty
- Preserves original content for reference
- Maintains user's reading position during transformations

### Session Management
- Personalization settings persist throughout a session
- Sessions automatically expire after 1 hour of inactivity
- Automatic cleanup of expired sessions

## Technical Architecture

### Frontend Components
- **PersonalizationButton**: UI component for difficulty selection
- **DocItem/Content**: Docusaurus theme override for content replacement
- **API utilities**: Communication with backend services

### Backend Services
- **Chapter Guide Agent**: Processes content with difficulty-appropriate explanations
- **Personalization API**: Endpoints for content transformation
- **Session Cache**: In-memory storage for personalization sessions

### API Endpoints
- `POST /api/personalization/personalize` - Transform content to difficulty level
- `POST /api/personalization/change-difficulty` - Change difficulty mid-session
- `POST /api/personalization/toggle-original` - Return to original content
- `DELETE /api/personalization/session/{session_id}` - Clear session

## User Experience

1. User clicks "Personalize Content" button on any chapter page
2. Selects preferred difficulty level (beginner, intermediate, advanced)
3. Content is transformed in real-time while preserving reading position
4. User can switch difficulty levels or return to original content at any time

## Analytics
The feature includes analytics tracking for:
- Content personalization events
- Difficulty level switches
- Original content toggles
- Content refresh actions

## Error Handling
- Graceful degradation when personalization service is unavailable
- Network error detection and user feedback
- Fallback to original content if transformation fails

## Security & Privacy
- Session-based personalization without permanent user data storage
- No personal information collected beyond session management
- All transformations happen server-side for security