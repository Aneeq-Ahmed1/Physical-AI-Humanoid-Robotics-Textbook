import React from 'react';
import { LanguageProvider } from '@site/src/contexts/LanguageContext';
import ChatWidget from '@site/src/components/ChatWidget';

// Root component to wrap the entire application with language context
const Root = ({ children }) => {
  return (
    <LanguageProvider>
      {children}
      <ChatWidget />
    </LanguageProvider>
  );
};

export default Root;