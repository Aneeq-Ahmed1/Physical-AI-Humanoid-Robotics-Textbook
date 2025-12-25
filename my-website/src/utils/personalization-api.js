/** API utility functions for content personalization */

// Get API base URL - adjust as needed for your deployment
const getApiBaseUrl = () => {
  if (typeof window !== 'undefined' && window.CHATBOT_API_URL) {
    return `${window.CHATBOT_API_URL}/api`;
  }
  // Check for REACT_APP_API_URL in browser environment (for builds)
  if (typeof process !== 'undefined' && process.env && process.env.REACT_APP_API_URL) {
    return `${process.env.REACT_APP_API_URL}/api`;
  }
  // Fallback to local backend during development
  return 'http://localhost:8000/api';
};

const API_BASE_URL = getApiBaseUrl();

/**
 * Personalize content based on difficulty level
 * @param {string} session_id - The session ID
 * @param {string} chapter_content - The content of the chapter to personalize
 * @param {string} difficulty_level - The difficulty level ('beginner', 'intermediate', 'advanced')
 * @param {string} chapter_id - The ID of the chapter
 * @param {number} reading_position - The current reading position
 * @returns {Promise<Object>} - The personalized content response
 */
export const personalizeContent = async (session_id, chapter_content, difficulty_level, chapter_id, reading_position = 0) => {
  try {
    const response = await fetch(`${API_BASE_URL}/personalize`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        session_id,
        chapter_content,
        difficulty_level,
        chapter_id,
        reading_position
      }),
    });

    if (!response.ok) {
      // Handle different error statuses
      if (response.status === 400) {
        const errorData = await response.json();
        throw new Error(`Invalid request: ${errorData.detail || 'Bad request'}`);
      } else if (response.status === 404) {
        throw new Error('Personalization service not found');
      } else if (response.status >= 500) {
        throw new Error('Personalization service is temporarily unavailable');
      } else {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
    }

    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Error personalizing content:', error);

    // Check if it's a network error
    if (error instanceof TypeError && error.message.includes('fetch')) {
      throw new Error('Unable to connect to personalization service. Please check your connection.');
    }

    throw error;
  }
};

/**
 * Toggle back to original content
 * @param {string} session_id - The session ID
 * @returns {Promise<Object>} - The original content response
 */
export const toggleOriginalContent = async (session_id) => {
  try {
    const response = await fetch(`${API_BASE_URL}/toggle-original`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        session_id
      }),
    });

    if (!response.ok) {
      // Handle different error statuses
      if (response.status === 400) {
        const errorData = await response.json();
        throw new Error(`Invalid request: ${errorData.detail || 'Bad request'}`);
      } else if (response.status === 404) {
        throw new Error('Personalization session not found');
      } else if (response.status >= 500) {
        throw new Error('Personalization service is temporarily unavailable');
      } else {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
    }

    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Error getting original content:', error);

    // Check if it's a network error
    if (error instanceof TypeError && error.message.includes('fetch')) {
      throw new Error('Unable to connect to personalization service. Please check your connection.');
    }

    throw error;
  }
};

/**
 * Change difficulty level mid-session
 * @param {string} session_id - The session ID
 * @param {string} chapter_content - The content of the chapter to personalize
 * @param {string} difficulty_level - The new difficulty level
 * @param {string} chapter_id - The ID of the chapter
 * @param {number} reading_position - The current reading position
 * @returns {Promise<Object>} - The updated personalized content response
 */
export const changeDifficultyLevel = async (session_id, chapter_content, difficulty_level, chapter_id, reading_position = 0) => {
  try {
    const response = await fetch(`${API_BASE_URL}/change-difficulty`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        session_id,
        chapter_content,
        difficulty_level,
        chapter_id,
        reading_position
      }),
    });

    if (!response.ok) {
      // Handle different error statuses
      if (response.status === 400) {
        const errorData = await response.json();
        throw new Error(`Invalid request: ${errorData.detail || 'Bad request'}`);
      } else if (response.status === 404) {
        throw new Error('Personalization session not found');
      } else if (response.status >= 500) {
        throw new Error('Personalization service is temporarily unavailable');
      } else {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
    }

    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Error changing difficulty level:', error);

    // Check if it's a network error
    if (error instanceof TypeError && error.message.includes('fetch')) {
      throw new Error('Unable to connect to personalization service. Please check your connection.');
    }

    throw error;
  }
};

/**
 * Clear personalization session
 * @param {string} session_id - The session ID to clear
 * @returns {Promise<Object>} - The response from the server
 */
export const clearPersonalizationSession = async (session_id) => {
  try {
    const response = await fetch(`${API_BASE_URL}/personalization/session/${session_id}`, {
      method: 'DELETE',
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Error clearing personalization session:', error);
    throw error;
  }
};