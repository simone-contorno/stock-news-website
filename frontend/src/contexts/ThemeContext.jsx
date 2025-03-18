import React, { createContext, useState, useContext, useEffect } from 'react';
import { createTheme, ThemeProvider as MuiThemeProvider } from '@mui/material/styles';

// Create light and dark theme configurations
const getTheme = (mode) => createTheme({
  palette: {
    mode,
    ...(mode === 'light' 
      ? {
        // Light mode colors
        primary: {
          main: '#0B3954',  // Deep navy blue
          light: '#1C5D7D',
          dark: '#082940',
        },
        secondary: {
          main: '#1B998B',  // Professional teal
          light: '#34B5A5',
          dark: '#147D71',
        },
        background: {
          default: '#F8F9FA',
          paper: '#FFFFFF',
        },
        text: {
          primary: '#1A1A1A',
          secondary: '#4A4A4A',
        },
      } 
      : {
        // Dark mode colors
        primary: {
          main: '#1C5D7D',  // Lighter blue for dark mode
          light: '#2A7EA3',
          dark: '#0B3954',
        },
        secondary: {
          main: '#34B5A5',  // Brighter teal for dark mode
          light: '#4DCBBB',
          dark: '#1B998B',
        },
        background: {
          default: '#121212',
          paper: '#1E1E1E',
        },
        text: {
          primary: '#FFFFFF',
          secondary: '#B0B0B0',
        },
      }),
  },
  typography: {
    fontFamily: '"Inter", "Roboto", "Helvetica", "Arial", sans-serif',
    h1: {
      fontSize: '2.5rem',
      fontWeight: 600,
      letterSpacing: '-0.01562em',
    },
    h2: {
      fontSize: '2rem',
      fontWeight: 500,
      letterSpacing: '-0.00833em',
    },
    h3: {
      fontSize: '1.75rem',
      fontWeight: 500,
      letterSpacing: '0em',
    },
    subtitle1: {
      fontSize: '1rem',
      fontWeight: 400,
      letterSpacing: '0.00938em',
    },
    body1: {
      fontSize: '1rem',
      letterSpacing: '0.00938em',
    },
  },
  shape: {
    borderRadius: 8,
  },
  components: {
    MuiCssBaseline: {
      styleOverrides: {
        body: {
          margin: 0,
          padding: 0,
        },
      },
    },
    MuiButton: {
      styleOverrides: {
        root: {
          textTransform: 'none',
          borderRadius: 8,
          padding: '8px 16px',
        },
      },
    },
    MuiCard: {
      styleOverrides: {
        root: {
          borderRadius: 12,
          boxShadow: '0 2px 12px 0 rgba(0,0,0,0.05)',
          transition: 'box-shadow 0.3s ease-in-out',
          '&:hover': {
            boxShadow: '0 4px 20px 0 rgba(0,0,0,0.1)',
          },
        },
      },
    },
    MuiPaper: {
      styleOverrides: {
        root: {
          transition: 'box-shadow 0.3s ease-in-out',
        },
      },
    },
  },
});

// Create the context
const ThemeContext = createContext();

// Custom hook to use the theme context
export const useThemeContext = () => useContext(ThemeContext);

// Theme provider component
export const ThemeProvider = ({ children }) => {
  // Check if there's a saved theme preference in localStorage
  const savedTheme = localStorage.getItem('themeMode');
  const [mode, setMode] = useState(savedTheme || 'light');
  
  // Generate the theme based on current mode
  const theme = React.useMemo(() => getTheme(mode), [mode]);
  
  // Toggle between light and dark mode
  const toggleTheme = () => {
    const newMode = mode === 'light' ? 'dark' : 'light';
    setMode(newMode);
    localStorage.setItem('themeMode', newMode);
  };

  // Effect to sync with system preference if no saved preference
  useEffect(() => {
    if (!savedTheme) {
      const prefersDarkMode = window.matchMedia('(prefers-color-scheme: dark)').matches;
      setMode(prefersDarkMode ? 'dark' : 'light');
    }
  }, [savedTheme]);

  return (
    <ThemeContext.Provider value={{ mode, toggleTheme }}>
      <MuiThemeProvider theme={theme}>
        {children}
      </MuiThemeProvider>
    </ThemeContext.Provider>
  );
};