import React, { useState, useEffect } from 'react';
import { useLanguage } from '@site/src/contexts/LanguageContext';

/**
 * A component that automatically translates text content based on the current language
 */
const TranslationWrapper = ({ children, fallback = null }) => {
  const { language, translateUI, loading } = useLanguage();
  const [translatedText, setTranslatedText] = useState(null);

  useEffect(() => {
    const translateContent = async () => {
      if (language === 'ur' && children) {
        try {
          // Convert children to string if it's not already
          const textToTranslate = typeof children === 'string' ? children : String(children);
          const translated = await translateUI(textToTranslate);
          setTranslatedText(translated);
        } catch (error) {
          console.error('Translation error:', error);
          setTranslatedText(fallback || children);
        }
      } else {
        setTranslatedText(children);
      }
    };

    if (children) {
      translateContent();
    }
  }, [children, language, translateUI, fallback]);

  if (loading && language === 'ur') {
    return <span>Translating...</span>;
  }

  return <span>{translatedText || fallback || children}</span>;
};

export default TranslationWrapper;