import React, { createContext, useContext, useState, useEffect } from 'react';
import { translateToUrdu, isContentCached, getCachedTranslation } from '@site/src/utils/translation';
import { extractContentWithFormatting, restoreFormatting } from '@site/src/utils/contentExtractor';
import { globalTranslationManager } from '@site/src/utils/globalTranslation';

// Create the language context
const LanguageContext = createContext();

// Custom hook to use the language context
export const useLanguage = () => {
  const context = useContext(LanguageContext);
  if (!context) {
    throw new Error('useLanguage must be used within a LanguageProvider');
  }
  return context;
};

// Language provider component
export const LanguageProvider = ({ children }) => {
  const [language, setLanguage] = useState('en'); // 'en' for English, 'ur' for Urdu
  const [loading, setLoading] = useState(false);

  // Toggle language and apply global translation
  const toggleLanguage = async () => {
    const newLanguage = language === 'en' ? 'ur' : 'en';
    setLanguage(newLanguage);

    // Apply global translation to the entire page
    await globalTranslationManager.translatePage(newLanguage);
  };

  // Get current language
  const getCurrentLanguage = () => {
    return language;
  };

  // Value object to provide to consumers
  const value = {
    language,
    loading,
    toggleLanguage,
    getCurrentLanguage,
    isUrdu: language === 'ur',
    isEnglish: language === 'en'
  };

  // Apply global translation when language changes
  useEffect(() => {
    globalTranslationManager.translatePage(language);
  }, [language]);

  return (
    <LanguageContext.Provider value={value}>
      {children}
    </LanguageContext.Provider>
  );
};