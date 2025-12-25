import React from 'react';

const DifficultySelector = ({ onSelect, selectedLevel }) => {
  const difficultyLevels = [
    { value: 'beginner', label: 'Beginner', description: 'Simple explanations with analogies' },
    { value: 'intermediate', label: 'Intermediate', description: 'Technical details with context' },
    { value: 'advanced', label: 'Advanced', description: 'Deep technical analysis' }
  ];

  return (
    <div className="difficulty-selector">
      <h4>Choose Difficulty Level</h4>
      <div className="difficulty-options">
        {difficultyLevels.map((level) => (
          <button
            key={level.value}
            className={`difficulty-option ${selectedLevel === level.value ? 'selected' : ''}`}
            onClick={() => onSelect(level.value)}
          >
            <div className="difficulty-header">
              <span className="difficulty-label">{level.label}</span>
            </div>
            <div className="difficulty-description">
              {level.description}
            </div>
          </button>
        ))}
      </div>
    </div>
  );
};

export default DifficultySelector;