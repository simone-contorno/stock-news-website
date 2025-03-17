import React from 'react';
import { Box, Typography, Paper, Alert, List, ListItem, ListItemIcon } from '@mui/material';
import { ErrorOutline as ErrorIcon, FiberManualRecord as BulletIcon } from '@mui/icons-material';

/**
 * ErrorMessage Component
 * 
 * A component for displaying network error messages with a suggestion to reload the page
 * and multiple troubleshooting options. Used to show connection errors with improved UX.
 * 
 * Features:
 * - Professional network error message component with bullet points
 * - Customizable title and message
 * - Comprehensive troubleshooting guidance in an easy-to-read format
 * 
 * @param {string} [props.title="Network Error"] - The error title
 * @param {string} [props.message="Unable to establish connection with the server. This could be due to network issues, script blockers, or server-side problems."] - The error message
 */
const ErrorMessage = ({
  title = "Network Error",
  message = "Unable to establish connection with the server. This could be due to network issues, script blockers, or server-side problems."
}) => {
  return (
    <Paper
      elevation={3}
      sx={{
        p: 4,
        my: 3,
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        textAlign: 'center',
        borderRadius: 2,
        border: 1,
        borderColor: 'error.light',
        maxWidth: '600px',
        mx: 'auto'
      }}
    >
      <Alert
        severity="error"
        icon={false}
        sx={{
          mb: 2,
          width: '100%',
          '& .MuiAlert-message': {
            width: '100%'
          }
        }}
      >
        <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center', width: '100%' }}>
          <ErrorIcon fontSize="large" sx={{ fontSize: 36, color: 'error.main', mb: 2 }} />
          <Typography variant="h5" component="div" gutterBottom fontWeight="500">
            {title}
          </Typography>
          <Typography variant="body1" color="text.secondary" paragraph>
            {message}
          </Typography>
          
          <List sx={{ width: '100%', textAlign: 'left', py: 0 }}>
            <ListItem sx={{ py: 0.5 }}>
              <ListItemIcon sx={{ minWidth: 28 }}>
                <BulletIcon sx={{ fontSize: 10, color: 'primary.main' }} />
              </ListItemIcon>
              <Typography variant="body2" color="text.secondary">
                Check your internet connection
              </Typography>
            </ListItem>
            <ListItem sx={{ py: 0.5 }}>
              <ListItemIcon sx={{ minWidth: 28 }}>
                <BulletIcon sx={{ fontSize: 10, color: 'primary.main' }} />
              </ListItemIcon>
              <Typography variant="body2" color="text.secondary">
                Disable any script blockers or ad blockers
              </Typography>
            </ListItem>
          </List>
          
          <Typography variant="body2" color="primary" sx={{ mt: 2, fontWeight: 500 }}>
            Please try reloading the page.
          </Typography>
        </Box>
      </Alert>
    </Paper>
  );
};

export default ErrorMessage;