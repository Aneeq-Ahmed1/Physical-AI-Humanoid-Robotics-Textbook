import React from 'react';
import OriginalDocSidebar from '@theme-original/DocSidebar';

// Component to render sidebar with global language context
const DocSidebar = (props) => {
  return (
    <OriginalDocSidebar {...props} />
  );
};

export default DocSidebar;