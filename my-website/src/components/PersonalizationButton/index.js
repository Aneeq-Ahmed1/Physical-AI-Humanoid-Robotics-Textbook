import React, { useState } from 'react';
import DifficultySelector from './DifficultySelector';
import './PersonalizationButton.css';

const PersonalizationButton = ({
  onPersonalize,
  onToggleOriginal,
  isPersonalized,
  currentDifficulty = 'intermediate',
  isLoading = false
}) => {
  const [isOpen, setIsOpen] = useState(false);
  const [selectedLevel, setSelectedLevel] = useState(currentDifficulty);

  const handleLevelSelect = (level) => {
    setSelectedLevel(level);
    if (onPersonalize) {
      onPersonalize(level);
    }
  };

  const toggleMenu = () => {
    setIsOpen(!isOpen);
  };

  const handleToggleOriginal = () => {
    if (onToggleOriginal) {
      onToggleOriginal();
    }
  };

  return (
    <div className="personalization-container">
      <button
        className={`personalization-toggle-btn ${isLoading ? 'loading' : ''}`}
        onClick={toggleMenu}
        aria-label="Content personalization options"
        disabled={isLoading}
      >
        {isLoading ? (
          <span className="loading-content">🔄 Processing...</span>
        ) : (
          <span>
            {isPersonalized ? `🎓 ${currentDifficulty.charAt(0).toUpperCase() + currentDifficulty.slice(1)}` : '🎓 Personalize Content'}
          </span>
        )}
      </button>

      {isOpen && !isLoading && (
        <div className="personalization-dropdown">
          {isPersonalized ? (
            <>
              <DifficultySelector
                onSelect={handleLevelSelect}
                selectedLevel={selectedLevel}
              />
              <button
                className="original-content-btn"
                onClick={handleToggleOriginal}
              >
                View Original Content
              </button>
            </>
          ) : (
            <DifficultySelector
              onSelect={handleLevelSelect}
              selectedLevel={selectedLevel}
            />
          )}
        </div>
      )}
    </div>
  );
};

export default PersonalizationButton;