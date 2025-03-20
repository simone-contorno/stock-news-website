import React, { useState, useEffect, useRef } from 'react'
import { ToggleButtonGroup, ToggleButton, Box, useMediaQuery, useTheme, IconButton } from '@mui/material'
import KeyboardArrowLeftIcon from '@mui/icons-material/KeyboardArrowLeft'
import KeyboardArrowRightIcon from '@mui/icons-material/KeyboardArrowRight'

const TimeRangeSelector = ({ selectedPeriod, onPeriodChange }) => {
  const theme = useTheme()
  const isMobile = useMediaQuery(theme.breakpoints.down('sm'))
  const isTablet = useMediaQuery(theme.breakpoints.down('md'))
  const scrollContainerRef = useRef(null)
  const [scrollable, setScrollable] = useState(false)
  const [showLeftArrow, setShowLeftArrow] = useState(false)
  const [showRightArrow, setShowRightArrow] = useState(false)
  const [isTouchDevice, setIsTouchDevice] = useState(false)
  
  const periods = [
    { value: '7d', label: '1 Week' },
    { value: '1mo', label: '1 Month' },
    { value: '1y', label: '1 Year' },
    { value: '3y', label: '3 Years' },
    { value: '5y', label: '5 Years' },
    { value: 'max', label: 'Max' }
  ]

  // Scroll to the selected period button when period changes
  useEffect(() => {
    if (scrollable && scrollContainerRef.current) {
      const selectedButton = scrollContainerRef.current.querySelector('.Mui-selected')
      if (selectedButton) {
        const containerWidth = scrollContainerRef.current.clientWidth
        const buttonLeft = selectedButton.offsetLeft
        const buttonWidth = selectedButton.clientWidth
        
        // Center the selected button in the scroll container
        scrollContainerRef.current.scrollLeft = buttonLeft - (containerWidth / 2) + (buttonWidth / 2)
      }
    }
  }, [selectedPeriod, scrollable])

  // Check if container needs to be scrollable
  useEffect(() => {
    setScrollable(isMobile || isTablet)
  }, [isMobile, isTablet])
  
  // Check if device is touch-enabled
  useEffect(() => {
    setIsTouchDevice('ontouchstart' in window || navigator.maxTouchPoints > 0)
  }, [])
  
  // Check scroll position to show/hide arrows
  useEffect(() => {
    const checkScroll = () => {
      if (scrollContainerRef.current) {
        const { scrollLeft, scrollWidth, clientWidth } = scrollContainerRef.current
        setShowLeftArrow(scrollLeft > 0)
        setShowRightArrow(scrollLeft < scrollWidth - clientWidth - 5) // 5px buffer
      }
    }
    
    checkScroll()
    
    const scrollContainer = scrollContainerRef.current
    if (scrollContainer) {
      scrollContainer.addEventListener('scroll', checkScroll)
      return () => scrollContainer.removeEventListener('scroll', checkScroll)
    }
  }, [scrollable])
  
  // Scroll functions
  const scrollLeft = () => {
    if (scrollContainerRef.current) {
      const scrollAmount = scrollContainerRef.current.clientWidth / 2
      scrollContainerRef.current.scrollBy({ left: -scrollAmount, behavior: 'smooth' })
    }
  }
  
  const scrollRight = () => {
    if (scrollContainerRef.current) {
      const scrollAmount = scrollContainerRef.current.clientWidth / 2
      scrollContainerRef.current.scrollBy({ left: scrollAmount, behavior: 'smooth' })
    }
  }

  return (
    <Box 
      sx={{ 
        mb: 3,
        display: 'flex',
        alignItems: 'center',
        ...(scrollable && {
          overflow: 'hidden',
          position: 'relative',
          '&::after': {
            content: '""',
            position: 'absolute',
            right: 0,
            top: 0,
            height: '100%',
            width: '20px',
            background: 'linear-gradient(to right, rgba(255,255,255,0), rgba(255,255,255,0.8))',
            pointerEvents: 'none',
            zIndex: 1
          },
          '&::before': {
            content: '""',
            position: 'absolute',
            left: 0,
            top: 0,
            height: '100%',
            width: '20px',
            background: 'linear-gradient(to left, rgba(255,255,255,0), rgba(255,255,255,0.8))',
            pointerEvents: 'none',
            zIndex: 1
          }
        })
      }}
    >
      {scrollable && !isTouchDevice && showLeftArrow && (
        <IconButton 
          onClick={scrollLeft}
          size="small"
          sx={{ 
            position: 'absolute', 
            left: 0, 
            zIndex: 2,
            backgroundColor: 'background.paper',
            boxShadow: 1,
            '&:hover': {
              backgroundColor: 'action.hover'
            }
          }}
          aria-label="scroll left"
        >
          <KeyboardArrowLeftIcon />
        </IconButton>
      )}
      <Box
        ref={scrollContainerRef}
        sx={{  
          width: '100%',
          overflowX: scrollable ? 'auto' : 'visible',
          overflowY: 'hidden',
          WebkitOverflowScrolling: 'touch',
          scrollbarWidth: 'none', // Firefox
          msOverflowStyle: 'none', // IE/Edge
          '&::-webkit-scrollbar': { // Chrome/Safari/Opera
            display: 'none'
          },
          pb: 1, // Add padding to avoid cut-off shadows
          // Add smooth scrolling
          scrollBehavior: 'smooth'
        }}
      >
        <ToggleButtonGroup
          value={selectedPeriod}
          exclusive
          onChange={(e, value) => value && onPeriodChange(value)}
          aria-label="time period"
          sx={{
            display: 'inline-flex',
            flexWrap: 'nowrap',
            width: scrollable ? 'max-content' : 'auto',
            '& .MuiToggleButton-root': {
              border: '1px solid',
              borderColor: 'divider',
              px: scrollable ? 1.5 : 2, // Slightly smaller padding on mobile
              py: 0.75,
              color: 'text.secondary',
              fontSize: scrollable ? '0.8125rem' : '0.875rem', // Slightly smaller font on mobile
              fontWeight: 500,
              transition: 'all 0.2s ease-in-out',
              whiteSpace: 'nowrap', // Prevent text wrapping
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
      
      {scrollable && !isTouchDevice && showRightArrow && (
        <IconButton 
          onClick={scrollRight}
          size="small"
          sx={{ 
            position: 'absolute', 
            right: 0, 
            zIndex: 2,
            backgroundColor: 'background.paper',
            boxShadow: 1,
            '&:hover': {
              backgroundColor: 'action.hover'
            }
          }}
          aria-label="scroll right"
        >
          <KeyboardArrowRightIcon />
        </IconButton>
      )}
    </Box>
  )
}

export default TimeRangeSelector