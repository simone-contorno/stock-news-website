import React from 'react'
import { Box, Typography, Paper, CircularProgress, Alert, Divider } from '@mui/material'
import { Analytics as AnalyticsIcon, Lightbulb as LightbulbIcon } from '@mui/icons-material'

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
          <Box sx={{ mb: 3 }}>
            <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
              <LightbulbIcon fontSize="small" sx={{ color: 'primary.main' }} />
              Key Events Summary
            </Typography>
            <Typography variant="body1" sx={{ whiteSpace: 'pre-line' }}>
              {data.summary}
            </Typography>
          </Box>

          <Divider sx={{ my: 3 }} />

          <Box>
            <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
              <AnalyticsIcon fontSize="small" sx={{ color: 'primary.main' }} />
              Price-News Correlation Analysis
            </Typography>
            <Typography variant="body1" sx={{ whiteSpace: 'pre-line' }}>
              {data.analysis}
            </Typography>
          </Box>
        </Box>
      )}
    </Paper>
  )
}

export default NewsSummary