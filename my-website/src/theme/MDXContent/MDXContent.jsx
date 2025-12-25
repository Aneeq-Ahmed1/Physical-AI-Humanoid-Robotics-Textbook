import React from 'react';

// This component adds the translation functionality to all MDX content using global language context
// Since global translation handles everything, this component just provides the content
const MDXContent = ({ children }) => {
  return (
    <div>
      {children}
    </div>
  );
};

export default MDXContent;