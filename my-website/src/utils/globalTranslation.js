import { translateToUrdu } from './translation';

// Global translation cache to avoid repeated API calls
const globalTranslationCache = new Map();

/**
 * Translate text using cache
 */
const translateWithCache = async (text) => {
  if (globalTranslationCache.has(text)) {
    return globalTranslationCache.get(text);
  }

  try {
    const translated = await translateToUrdu(text);
    globalTranslationCache.set(text, translated);
    return translated;
  } catch (error) {
    console.error('Global translation failed:', error);
    return text; // Return original text if translation fails
  }
};

/**
 * Check if text is likely translatable (not already Urdu)
 */
const isTranslatableText = (text) => {
  // Skip if text is empty or too short
  if (!text || text.trim().length < 2) return false;

  // Check if text contains English letters
  return /[a-zA-Z]/.test(text);
};

/**
 * Check if an element should be translated
 */
const shouldTranslateElement = (element) => {
  // Don't translate elements that are already marked as not to be translated
  if (element.dataset.noTranslate === 'true') return false;

  // Don't translate input elements, textareas, or contenteditable elements
  const tagName = element.tagName.toLowerCase();
  if (['input', 'textarea', 'select'].includes(tagName)) return false;

  // Don't translate elements with contenteditable
  if (element.contentEditable === 'true') return false;

  // Don't translate elements that are likely to be dynamic content
  if (element.classList.contains('chat-message') ||
      element.classList.contains('chat-input') ||
      element.classList.contains('chat-widget')) return false;

  return true;
};

/**
 * Translate a DOM element and its children
 */
const translateElement = async (element, targetLanguage = 'ur') => {
  if (targetLanguage === 'en') return; // No translation needed for English

  // Skip if element is already marked as translated or shouldn't be translated
  if (element.dataset.translated === 'true' || !shouldTranslateElement(element)) return;

  // Get all text nodes in the element
  const walker = document.createTreeWalker(
    element,
    NodeFilter.SHOW_TEXT,
    {
      acceptNode: (node) => {
        // Only process text nodes that contain actual content (not whitespace)
        // and whose parent element should be translated
        if (node.nodeType === Node.TEXT_NODE && node.nodeValue.trim()) {
          if (node.parentElement && shouldTranslateElement(node.parentElement)) {
            return NodeFilter.FILTER_ACCEPT;
          }
        }
        return NodeFilter.FILTER_REJECT;
      }
    }
  );

  const textNodes = [];
  let node;

  // Collect all text nodes
  while (node = walker.nextNode()) {
    textNodes.push(node);
  }

  // Translate each text node
  for (const textNode of textNodes) {
    const originalText = textNode.nodeValue.trim();

    if (originalText && isTranslatableText(originalText)) {
      try {
        const translatedText = await translateWithCache(originalText);
        if (translatedText !== originalText && translatedText) {
          // Store original text as a backup
          if (textNode.parentElement && !textNode.parentElement.dataset.originalText) {
            textNode.parentElement.dataset.originalText = originalText;
          }

          // Replace the text content
          textNode.nodeValue = textNode.nodeValue.replace(originalText, translatedText);

          // Mark the parent element as translated
          if (textNode.parentElement) {
            textNode.parentElement.dataset.translated = 'true';
          }
        }
      } catch (error) {
        console.error('Error translating text node:', error);
      }
    }
  }
};

/**
 * Global translation manager
 */
class GlobalTranslationManager {
  constructor() {
    this.isTranslating = false;
    this.targetLanguage = 'en';
    this.observer = null;
    this.periodicCheckInterval = null;
  }

  async translatePage(language = 'ur') {
    if (this.isTranslating) return;

    this.isTranslating = true;
    this.targetLanguage = language;

    try {
      if (language === 'ur') {
        // Wait for content to be loaded
        await this.waitForContent();

        // Multiple translation passes to catch all content
        for (let i = 0; i < 3; i++) {
          await translateElement(document.body, language);
          await this.delay(300); // Brief delay between passes
        }

        // Set up mutation observer to catch dynamically added content
        this.setupMutationObserver();

        // Set up periodic checks for content that might load later
        this.startPeriodicTranslation();
      } else {
        // Reset translation state when switching back to English
        this.cleanupTranslation();
        // Clear periodic checks
        if (this.periodicCheckInterval) {
          clearInterval(this.periodicCheckInterval);
          this.periodicCheckInterval = null;
        }
      }
    } catch (error) {
      console.error('Global translation error:', error);
    } finally {
      this.isTranslating = false;
    }
  }

  // Start periodic translation checks for content that loads later
  startPeriodicTranslation() {
    if (this.periodicCheckInterval) {
      clearInterval(this.periodicCheckInterval);
    }

    // Check every 2 seconds for new content to translate
    this.periodicCheckInterval = setInterval(() => {
      if (this.targetLanguage === 'ur') {
        translateElement(document.body, 'ur');
      }
    }, 2000);
  }

  // Add delay utility function
  delay(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }

  // Wait for content to be loaded before translation
  waitForContent() {
    return new Promise((resolve) => {
      // Check if content is already loaded
      if (document.readyState === 'complete' ||
          (document.readyState !== 'loading' && !document.documentElement.doScroll)) {
        resolve();
      } else {
        // Wait for DOM content to be loaded
        if (document.addEventListener) {
          document.addEventListener('DOMContentLoaded', () => resolve());
        } else {
          // Fallback for older browsers
          const timer = setInterval(() => {
            if (document.readyState !== 'loading') {
              clearInterval(timer);
              resolve();
            }
          }, 10);
        }
      }
    });
  }

  setupMutationObserver() {
    if (this.observer) {
      this.observer.disconnect();
    }

    this.observer = new MutationObserver((mutations) => {
      mutations.forEach((mutation) => {
        if (mutation.type === 'childList') {
          mutation.addedNodes.forEach(async (node) => {
            if (node.nodeType === Node.ELEMENT_NODE) {
              // Translate the new element if the language is Urdu
              if (this.targetLanguage === 'ur') {
                await translateElement(node, this.targetLanguage);
              }
            }
          });
        }
      });
    });

    // Observe the entire document body
    this.observer.observe(document.body, {
      childList: true,
      subtree: true
    });
  }

  cleanupTranslation() {
    // Clear periodic checks
    if (this.periodicCheckInterval) {
      clearInterval(this.periodicCheckInterval);
      this.periodicCheckInterval = null;
    }

    // Restore original text content for elements that were translated
    const translatedElements = document.querySelectorAll('[data-translated="true"]');
    translatedElements.forEach(el => {
      // Restore original text if available and element should be translated
      if (el.dataset.originalText && shouldTranslateElement(el)) {
        // Find text nodes that contain the translated text and restore original
        const walker = document.createTreeWalker(
          el,
          NodeFilter.SHOW_TEXT,
          null
        );

        let node;
        while (node = walker.nextNode()) {
          if (node.nodeValue && el.dataset.originalText) {
            // Replace the translated text with original text
            const translatedText = node.nodeValue.trim();
            // Only replace if the current text matches what we translated
            if (translatedText && translatedText !== el.dataset.originalText) {
              node.nodeValue = node.nodeValue.replace(translatedText, el.dataset.originalText);
            }
          }
        }

        // Remove the original text backup
        delete el.dataset.originalText;
      }

      // Remove the translation mark
      delete el.dataset.translated;
    });

    // Disconnect mutation observer
    if (this.observer) {
      this.observer.disconnect();
      this.observer = null;
    }
  }

  // Method to translate specific content
  async translateContent(content, targetLanguage = 'ur') {
    if (targetLanguage === 'en' || !content) return content;

    if (typeof content === 'string') {
      if (isTranslatableText(content)) {
        return await translateWithCache(content);
      }
      return content;
    }

    return content;
  }
}

// Create a singleton instance
export const globalTranslationManager = new GlobalTranslationManager();

// Function to translate text directly
export const translateText = async (text, targetLanguage = 'ur') => {
  return await globalTranslationManager.translateContent(text, targetLanguage);
};