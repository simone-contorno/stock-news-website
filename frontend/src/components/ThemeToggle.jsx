import React from 'react';
import { IconButton, Tooltip } from '@mui/material';
import Brightness4Icon from '@mui/icons-material/Brightness4'; // Moon icon for dark mode
import Brightness7Icon from '@mui/icons-material/Brightness7'; // Sun icon for light mode
import { useThemeContext } from '../contexts/ThemeContext';

const ThemeToggle = () => {
  const { mode, toggleTheme } = useThemeContext();
  
  return (
    <Tooltip title={mode === 'light' ? 'Switch to dark mode' : 'Switch to light mode'}>
      <IconButton
        onClick={toggleTheme}
        color={mode === 'light' ? 'primary' : 'inherit'}
        aria-label="toggle theme"
        sx={{
          ml: 1,
          transition: 'transform 0.3s ease-in-out',
          '&:hover': { transform: 'rotate(30deg)' },
          ...(mode === 'light' && {
            color: '#1C5D7D', // Using the dark mode primary color for better visibility in light mode
          }),
        }}
      >
        {mode === 'light' ? <Brightness4Icon /> : <Brightness7Icon />}
      </IconButton>
    </Tooltip>
  );
};

export default ThemeToggle;