import React from 'react'
import { Box, Typography, Paper, CircularProgress, Alert, Divider } from '@mui/material'
import { Analytics as AnalyticsIcon, Lightbulb as LightbulbIcon } from '@mui/icons-material'
import './NewsSummary.css'

const NewsSummary = ({ symbol, period, isLoading = false, error = null, data = null }) => {
  return (
    <Paper
      elevation={0}
      sx={{
        p: 3,
        mb: 4,
        borderRadius: 2,
        backgroundColor: 'background.paper',
        transition: 'box-shadow 0.3s ease-in-out',
        '&:hover': {
          boxShadow: '0 4px 20px 0 rgba(0,0,0,0.1)'
        }
      }}
    >
      <Typography
        variant="h5"
        gutterBottom
        sx={{
          fontWeight: 600,
          color: 'text.primary',
          mb: 2,
          display: 'flex',
          alignItems: 'center',
          gap: 1
        }}
      >
        <AnalyticsIcon sx={{ color: 'primary.main' }} />
        AI News Analysis
      </Typography>

      {isLoading ? (
        <Box display="flex" justifyContent="center" p={4}>
          <CircularProgress />
        </Box>
      ) : error ? (
        <Alert severity="error" sx={{ mb: 2 }}>
          {error}
        </Alert>
      ) : !data ? (
        <Alert severity="info" sx={{ mb: 2 }}>
          No analysis available for this stock.
        </Alert>
      ) : (
        <Box>
          <Box>
            <Box>
              <div dangerouslySetInnerHTML={{ __html: data.formatted_text }} />
            </Box>
          </Box>
        </Box>
      )}
    </Paper>
  )
}

export default NewsSummary