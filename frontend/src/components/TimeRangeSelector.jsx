import React from 'react'
import { ToggleButtonGroup, ToggleButton, Box } from '@mui/material'

const TimeRangeSelector = ({ selectedPeriod, onPeriodChange }) => {
  const periods = [
    { value: '7d', label: '1 Week' },
    { value: '1mo', label: '1 Month' },
    { value: '1y', label: '1 Year' },
    { value: '3y', label: '3 Years' },
    { value: '5y', label: '5 Years' },
    { value: 'max', label: 'Max' }
  ]

  return (
    <Box sx={{ mb: 3 }}>
      <ToggleButtonGroup
        value={selectedPeriod}
        exclusive
        onChange={(e, value) => value && onPeriodChange(value)}
        aria-label="time period"
        sx={{
          '& .MuiToggleButton-root': {
            border: '1px solid',
            borderColor: 'divider',
            px: 2,
            py: 0.75,
            color: 'text.secondary',
            fontSize: '0.875rem',
            fontWeight: 500,
            transition: 'all 0.2s ease-in-out',
            '&:hover': {
              backgroundColor: 'action.hover',
              borderColor: 'primary.main',
            },
            '&.Mui-selected': {
              backgroundColor: 'primary.main',
              color: 'common.white',
              '&:hover': {
                backgroundColor: 'primary.dark',
              },
            },
          },
        }}
      >
        {periods.map(period => (
          <ToggleButton
            key={period.value}
            value={period.value}
            aria-label={period.label}
          >
            {period.label}
          </ToggleButton>
        ))}
      </ToggleButtonGroup>
    </Box>
  )
}

export default TimeRangeSelector