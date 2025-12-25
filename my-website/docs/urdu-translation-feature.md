---
sidebar_position: 100
title: Urdu Translation Feature
---

# Urdu Translation Feature Documentation

## Overview
The Urdu Translation feature allows logged-in users to dynamically translate individual book chapters from English to Urdu using an LLM-powered translation service. The feature provides a toggle button at the beginning of each chapter that enables users to switch between English and Urdu content without affecting the original content or the existing RAG chatbot functionality.

## Features

### 1. Translation Toggle Button
- A "Translate to Urdu" button appears at the top of each chapter for authenticated users
- The button provides clear visual feedback about the current language state
- Includes accessibility features (aria labels, keyboard navigation)

### 2. Dynamic Translation
- Content is translated on-demand using an LLM API
- Translation happens client-side with backend API support
- Caching mechanism prevents repeated API calls for the same content

### 3. Content Preservation
- Original English content is always preserved
- Users can seamlessly switch between English and Urdu versions
- Formatting, code snippets, and diagrams are maintained during translation

### 4. Error Handling
- Graceful fallback to English content if translation fails
- Loading indicators during translation process
- Error boundaries to prevent page crashes

## Technical Implementation

### Frontend Components
- `TranslationToggle.jsx`: Main component that manages language state and toggling
- `TranslationErrorBoundary.jsx`: Error boundary to catch translation errors
- CSS module for styling and visual feedback

### Utility Functions
- `translation.js`: Handles API calls and caching
- `contentExtractor.js`: Extracts and preserves content formatting

### Backend API
- `/api/translate`: Translation endpoint that interfaces with LLM service
- Built with FastAPI and follows existing project patterns

## Usage
1. Navigate to any chapter in the textbook
2. If logged in, you'll see the "Translate to Urdu" button at the top
3. Click the button to translate the content to Urdu
4. Click again to switch back to English

## Constraints
- Translation is available only to authenticated users
- Original RAG chatbot functionality remains unchanged
- No modifications to vector store, ingestion, or retrieval logic