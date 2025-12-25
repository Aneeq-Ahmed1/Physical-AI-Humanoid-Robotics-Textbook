import React, { useState, useEffect, useRef } from 'react';
import { useDoc } from '@docusaurus/plugin-content-docs/client';
import { useLocation } from '@docusaurus/router';
import PersonalizationButton from '@site/src/components/PersonalizationButton';
import { personalizeContent, toggleOriginalContent, changeDifficultyLevel } from '@site/src/utils/personalization-api';
import analytics from '@site/src/utils/analytics';

// Docusaurus default DocContent component
import OriginalDocContent from '@theme-original/DocItem/Content';

export default function DocItemContent(props) {
  const { content } = props;
  const { metadata } = useDoc();
  const location = useLocation();
  const [personalizedContent, setPersonalizedContent] = useState(null);
  const [isPersonalized, setIsPersonalized] = useState(false);
  const [currentDifficulty, setCurrentDifficulty] = useState('intermediate');
  const [isLoading, setIsLoading] = useState(false);
  const [sessionId, setSessionId] = useState(null);
  const contentRef = useRef(null);

  // Generate session ID if not exists
  useEffect(() => {
    if (!sessionId) {
      const id = `session_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
      setSessionId(id);
    }
  }, [sessionId]);

  // Extract original content from props
  const getOriginalContent = () => {
    // Get the content from the markdown content
    if (contentRef.current) {
      return contentRef.current.innerHTML;
    }
    return document.querySelector('.markdown')?.innerHTML || '';
  };

  const handlePersonalize = async (difficultyLevel) => {
    if (!sessionId) return;

    // Save current scroll position
    const currentScrollPosition = window.scrollY;

    setIsLoading(true);
    try {
      // Get current content (either original or currently personalized)
      let currentContent = getOriginalContent();

      // If we have personalized content, use that as the base
      if (isPersonalized && personalizedContent) {
        currentContent = personalizedContent;
      } else {
        // Otherwise, extract from the DOM
        const markdownElement = document.querySelector('.markdown');
        currentContent = markdownElement ? markdownElement.innerHTML : '';
      }

      let response;
      // If difficulty is changing from an existing personalized state, use changeDifficultyLevel API
      if (isPersonalized) {
        response = await changeDifficultyLevel(
          sessionId,
          currentContent,
          difficultyLevel,
          metadata.id,
          currentScrollPosition
        );
        setPersonalizedContent(response.personalized_content);
        setCurrentDifficulty(response.difficulty_level);

        // Track difficulty switch
        analytics.trackDifficultySwitch(sessionId, currentDifficulty, difficultyLevel, metadata.id);
      } else {
        // Otherwise, use the standard personalization API
        response = await personalizeContent(
          sessionId,
          currentContent,
          difficultyLevel,
          metadata.id,
          currentScrollPosition
        );
        setPersonalizedContent(response.personalized_content);
        setIsPersonalized(true);
        setCurrentDifficulty(difficultyLevel);

        // Track initial personalization
        analytics.trackPersonalization(sessionId, difficultyLevel, metadata.id, currentScrollPosition);
      }

      // Track content refresh
      analytics.trackContentRefresh(sessionId, difficultyLevel, response.personalized_content.length, metadata.id);

      // Restore scroll position after content is updated
      setTimeout(() => {
        window.scrollTo(0, currentScrollPosition);
      }, 100);
    } catch (error) {
      console.error('Error personalizing content:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleToggleOriginal = async () => {
    if (!sessionId) return;

    // Save current scroll position
    const currentScrollPosition = window.scrollY;

    setIsLoading(true);
    try {
      const response = await toggleOriginalContent(sessionId);
      setPersonalizedContent(response.original_content);
      setIsPersonalized(false);

      // Track toggle to original
      analytics.trackToggleOriginal(sessionId, metadata.id);

      // Restore scroll position after content is updated
      setTimeout(() => {
        window.scrollTo(0, currentScrollPosition);
      }, 100);
    } catch (error) {
      console.error('Error toggling to original content:', error);

      // Fallback: if API fails, just reset to non-personalized state
      setPersonalizedContent(null);
      setIsPersonalized(false);

      // Restore scroll position even if API fails
      setTimeout(() => {
        window.scrollTo(0, currentScrollPosition);
      }, 100);
    } finally {
      setIsLoading(false);
    }
  };

  // Update content when personalized content changes
  useEffect(() => {
    if (personalizedContent && isPersonalized) {
      const markdownElement = document.querySelector('.markdown');
      if (markdownElement) {
        markdownElement.innerHTML = personalizedContent;
      }
    }
  }, [personalizedContent, isPersonalized]);

  // Render loading state if needed
  if (isLoading) {
    return (
      <div className="doc-content-wrapper">
        <div className="personalization-loading">
          <div className="loading-spinner">🔄</div>
          <p>Personalizing content...</p>
        </div>
        <OriginalDocContent {...props} />
      </div>
    );
  }

  return (
    <div className="doc-content-wrapper">
      <div className="personalization-header">
        <PersonalizationButton
          onPersonalize={handlePersonalize}
          onToggleOriginal={handleToggleOriginal}
          isPersonalized={isPersonalized}
          currentDifficulty={currentDifficulty}
          isLoading={isLoading}
        />
        {isPersonalized && (
          <span className="difficulty-indicator">
            Level: {currentDifficulty.charAt(0).toUpperCase() + currentDifficulty.slice(1)}
          </span>
        )}
      </div>

      <OriginalDocContent {...props} />

      <div ref={contentRef} style={{ display: 'none' }}>
        {React.Children.map(props.children, child => child)}
      </div>
    </div>
  );
}