import React, { useState, useEffect, useRef } from 'react';
import TranslationErrorBoundary from './TranslationErrorBoundary';
import { extractContentWithFormatting, restoreFormatting, preserveOriginalContent, restoreOriginalContent } from '@site/src/utils/contentExtractor';
import { translateToUrdu, isContentCached, getCachedTranslation } from '@site/src/utils/translation';
import styles from './TranslationToggle.module.css';

const TranslationToggle = ({ children }) => {
  const [languageMode, setLanguageMode] = useState('en'); // 'en' or 'ur'
  const [translatedContent, setTranslatedContent] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const contentRef = useRef(null);
  const contentKey = useRef(null); // Unique key for this content

  // Preserve original content on initial render
  useEffect(() => {
    if (!contentKey.current) {
      contentKey.current = `content-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
      preserveOriginalContent(children, contentKey.current);
    }
  }, [children]);

  // Extract original content from children
  const extractContent = () => {
    // Use the content extractor utility to get text content while preserving formatting info
    return extractContentWithFormatting(children);
  };

  // Toggle between English and Urdu
  const toggleLanguage = async () => {
    if (languageMode === 'en') {
      setIsLoading(true);
      setError(null);

      try {
        const contentData = extractContent();
        let translated;

        // Check if content is already cached
        if (isContentCached(contentData.text)) {
          translated = getCachedTranslation(contentData.text);
        } else {
          // Call the translation API
          translated = await translateToUrdu(contentData.text);
        }

        // Restore formatting to translated content
        const formattedTranslated = restoreFormatting(translated, contentData.formattingInfo);
        setTranslatedContent(formattedTranslated);
        setLanguageMode('ur');
      } catch (err) {
        setError('Translation failed. Please try again.');
        console.error('Translation error:', err);
      } finally {
        setIsLoading(false);
      }
    } else {
      // When switching back to English, clear the translated content to show original
      setTranslatedContent(null);
      setLanguageMode('en');
    }
  };

  return (
    <TranslationErrorBoundary>
      <div className={styles.translationContainer}>
        <div className={styles.controls}>
          <button
            className={`${styles.toggleButton} ${languageMode === 'ur' ? styles.urduActive : styles.englishActive}`}
            onClick={toggleLanguage}
            disabled={isLoading}
            aria-label={languageMode === 'en' ? 'Translate to Urdu' : 'Switch back to English'}
            aria-pressed={languageMode === 'ur'}
          >
            {isLoading ? (
              <span className={styles.loadingSpinner}>Translating...</span>
            ) : (
              <>
                <span className={styles.buttonText}>
                  {languageMode === 'en' ? '.Translate to Urdu' : '.Translate to English'}
                </span>
                <span className={`${styles.languageIndicator} ${languageMode === 'en' ? styles.englishIndicator : styles.urduIndicator}`}>
                  {languageMode}
                </span>
              </>
            )}
          </button>
          {error && <div className={styles.error}>{error}</div>}
        </div>

        <div className={styles.content}>
          {languageMode === 'ur' && translatedContent ? translatedContent :
            // When in English mode, ensure we're showing the original content
            children}
        </div>
      </div>
    </TranslationErrorBoundary>
  );
};

export default TranslationToggle;