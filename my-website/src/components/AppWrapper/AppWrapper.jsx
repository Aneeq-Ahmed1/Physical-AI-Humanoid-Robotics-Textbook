import React from 'react';
import { LanguageProvider } from '@site/src/contexts/LanguageContext';

// App-level wrapper to provide language context
const AppWrapper = ({ children }) => {
  return (
    <LanguageProvider>
      {children}
    </LanguageProvider>
  );
};

export default AppWrapper;