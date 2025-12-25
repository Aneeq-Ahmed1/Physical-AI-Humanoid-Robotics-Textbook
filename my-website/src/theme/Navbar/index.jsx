import React from 'react';
import OriginalNavbar from '@theme-original/Navbar';
import LanguageToggle from '@site/src/components/LanguageToggle/LanguageToggle';
import { useLanguage } from '@site/src/contexts/LanguageContext';

const Navbar = (props) => {
  const { loading } = useLanguage();

  return (
    <div style={{ position: 'relative' }}>
      <OriginalNavbar {...props} />
      <div style={{
        position: 'absolute',
        right: '160px', // Adjusted to make space for GitHub button (typically ~60px width + some margin)
        top: '50%',
        transform: 'translateY(-50%)',
        zIndex: 1000
      }}>
        {!loading && <LanguageToggle />}
      </div>
    </div>
  );
};

export default Navbar;