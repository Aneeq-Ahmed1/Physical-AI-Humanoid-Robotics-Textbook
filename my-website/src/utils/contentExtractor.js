import React from 'react';

// Content extraction utility functions

/**
 * Extract text content from React nodes
 * @param {React.ReactNode|string} content - The content to extract from
 * @returns {string} - Extracted text content
 */
export const extractTextContent = (content) => {
  if (typeof content === 'string') {
    return content;
  }

  if (typeof content === 'number') {
    return content.toString();
  }

  if (React.isValidElement(content)) {
    return extractFromReactElement(content);
  }

  if (Array.isArray(content)) {
    return content.map(extractTextContent).join(' ');
  }

  if (content && typeof content === 'object') {
    // Handle objects that might have a text-like property
    if (content.props && content.props.children) {
      return extractTextContent(content.props.children);
    }
  }

  return String(content || '');
};

/**
 * Helper function to extract text from React elements
 * @param {React.ReactNode} element - React element to extract from
 * @returns {string} - Extracted text
 */
const extractFromReactElement = (element) => {
  if (typeof element === 'string' || typeof element === 'number') {
    return element.toString();
  }

  if (React.isValidElement(element)) {
    const { props, type } = element;
    if (props && props.children) {
      if (Array.isArray(props.children)) {
        return props.children.map(extractFromReactElement).join(' ');
      } else {
        return extractFromReactElement(props.children);
      }
    }
  }

  return '';
};

/**
 * Preserve formatting while extracting content
 * @param {React.ReactNode|string} content - Content to process
 * @returns {Object} - Object containing text content and formatting info
 */
export const extractContentWithFormatting = (content) => {
  const text = extractTextContent(content);

  // Basic detection of content types
  const hasCodeBlocks = /```[\s\S]*?```|`[^`]*`|<code[\s\S]*?<\/code>/g.test(text);
  const hasHeadings = /^#{1,6}\s.*$/gm.test(text);
  const hasLists = /^[\s\t]*(?:[*+-]|\d+\.)\s/gm.test(text);
  const hasBold = /\*\*.*?\*\*|__.*?__/g.test(text);
  const hasItalic = /\*.*?\*|_.*?_/g.test(text);

  return {
    text,
    formattingInfo: {
      hasCodeBlocks,
      hasHeadings,
      hasLists,
      hasBold,
      hasItalic,
      originalContent: content
    }
  };
};

/**
 * Restore formatting to translated content
 * @param {string} translatedText - The translated text
 * @param {Object} formattingInfo - Original formatting information
 * @returns {string} - Content with formatting restored
 */
export const restoreFormatting = (translatedText, formattingInfo) => {
  // In a real implementation, this would reconstruct the original structure
  // For now, we return the translated text
  return translatedText;
};

// Store original content for each element to ensure preservation
const originalContentMap = new Map();

/**
 * Preserve original content before translation
 * @param {React.ReactNode} content - Original content to preserve
 * @param {string} key - Unique key for this content
 * @returns {string} - String representation of original content
 */
export const preserveOriginalContent = (content, key) => {
  originalContentMap.set(key, content);
  return key;
};

/**
 * Restore original content
 * @param {string} key - Key for the content to restore
 * @returns {React.ReactNode} - Original content
 */
export const restoreOriginalContent = (key) => {
  return originalContentMap.get(key) || null;
};

/**
 * Clear preserved content
 * @param {string} key - Key for the content to clear
 */
export const clearPreservedContent = (key) => {
  originalContentMap.delete(key);
};

/**
 * Get all preserved content
 * @returns {Map} - Map of all preserved content
 */
export const getAllPreservedContent = () => {
  return originalContentMap;
};