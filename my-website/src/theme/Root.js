import React from 'react';
import ChatWidget from '@site/src/components/ChatWidget';

function Root({ children }) {
  return (
    <>
      {children}
      <ChatWidget />
    </>
  );
}

export default Root;