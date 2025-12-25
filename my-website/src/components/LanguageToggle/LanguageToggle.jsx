import React from 'react';
import { useLanguage } from '@site/src/contexts/LanguageContext';
import styles from './LanguageToggle.module.css';

const LanguageToggle = () => {
  const { language, toggleLanguage, loading } = useLanguage();

  return (
    <div className={styles.languageToggleContainer}>
      <button
        className={`${styles.languageToggle} ${language === 'ur' ? styles.urduActive : styles.englishActive}`}
        onClick={toggleLanguage}
        disabled={loading}
        aria-label={language === 'en' ? 'Switch to Urdu' : 'Switch to English'}
        aria-pressed={language === 'ur'}
        title={language === 'en' ? 'Switch to Urdu' : 'Switch to English'}
      >
        {loading ? (
          <span className={styles.loading}>Translating...</span>
        ) : (
          <span className={styles.languageText}>
            {language === 'en' ? 'اُردو' : 'English'}
          </span>
        )}
      </button>
    </div>
  );
};

export default LanguageToggle;