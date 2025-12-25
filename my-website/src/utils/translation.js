// Translation utility functions

// Cache for translated content to avoid repeated API calls
const translationCache = new Map();

/**
 * Translate content from English to Urdu using LLM API
 * @param {string} content - The content to translate
 * @returns {Promise<string>} - Translated content
 */
export const translateToUrdu = async (content) => {
  // Check cache first
  if (translationCache.has(content)) {
    return translationCache.get(content);
  }

  try {
    const response = await callLLMApi(content);

    // Cache the result
    translationCache.set(content, response);

    return response;
  } catch (error) {
    console.error('Translation API error:', error);
    throw new Error(`Translation failed: ${error.message}`);
  }
};

/**
 * Call the LLM API for translation
 * @param {string} content - Content to translate
 * @returns {Promise<string>} - Translated content
 */
const callLLMApi = async (content) => {
  try {
    // Call the backend translation service
    const response = await fetch('/api/translate', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        text: content,
        targetLanguage: 'ur',
        sourceLanguage: 'en'
      })
    });

    if (!response.ok) {
      throw new Error(`Translation API error: ${response.status} - ${response.statusText}`);
    }

    const result = await response.json();
    return result.translatedText;
  } catch (error) {
    console.error('Translation API call failed:', error);
    throw error; // Re-throw to be handled by calling function
  }
};

/**
 * Check if content is already cached
 * @param {string} content - Content to check
 * @returns {boolean} - Whether content is cached
 */
export const isContentCached = (content) => {
  return translationCache.has(content);
};

/**
 * Clear the translation cache
 */
export const clearTranslationCache = () => {
  translationCache.clear();
};

/**
 * Get cached translation
 * @param {string} content - Content to get from cache
 * @returns {string|null} - Cached translation or null
 */
export const getCachedTranslation = (content) => {
  return translationCache.get(content) || null;
};

/**
 * Get the global translation cache for debugging purposes
 */
export const getTranslationCache = () => {
  return translationCache;
};