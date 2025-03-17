import React from 'react';
import { Box, Typography, Paper, Alert } from '@mui/material';
import { ErrorOutline as ErrorIcon } from '@mui/icons-material';

/**
 * ErrorMessage Component
 * 
 * A component for displaying network error messages with a suggestion to reload the page.
 * Used in the dashboard to show connection errors with improved UX.
 * 
 * Features:
 * - Professional network error message component
 * - Customizable title and message
 * 
 * @param {string} [props.title="Network Error"] - The error title
 * @param {string} [props.message="Unable to establish connection with the server."] - The error message
 */
const ErrorMessage = ({
  title = "Network Error",
  message = "Unable to establish connection with the server."
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
        icon={<ErrorIcon fontSize="large" sx={{ fontSize: 36 }} />}
        sx={{
          mb: 2,
          width: '100%',
          '& .MuiAlert-message': {
            width: '100%'
          }
        }}
      >
        <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center', width: '100%' }}>
          <Typography variant="h5" component="div" gutterBottom fontWeight="500">
            {title}
          </Typography>
          <Typography variant="body1" color="text.secondary" paragraph>
            {message}
          </Typography>
          <Typography variant="body2" color="primary" sx={{ mt: 2, fontWeight: 500 }}>
            Please try reloading the page.
          </Typography>
        </Box>
      </Alert>
    </Paper>
  );
};

export default ErrorMessage;