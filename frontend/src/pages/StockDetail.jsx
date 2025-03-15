import React, { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'
import { useDispatch, useSelector } from 'react-redux'
import { Box, Typography, Paper, CircularProgress, Alert, Container, Fade, Button, Tooltip } from '@mui/material'
import Highcharts from 'highcharts'
import HighchartsReact from 'highcharts-react-official'
import exporting from 'highcharts/modules/exporting'
import offlineExporting from 'highcharts/modules/offline-exporting'
import { ShowChart as ShowChartIcon, OpenInNew as OpenInNewIcon } from '@mui/icons-material'
import { fetchStockPrices } from '../store/stocksSlice'
import TimeRangeSelector from '../components/TimeRangeSelector'
import NewsSection from '../components/NewsSection'
import NewsSummary from '../components/NewsSummary'

// Initialize Highcharts modules
exporting(Highcharts)
offlineExporting(Highcharts)

const StockDetail = () => {
  const { symbol } = useParams()
  const dispatch = useDispatch()
  const [selectedPeriod, setSelectedPeriod] = useState('7d')
  const [selectedDate, setSelectedDate] = useState(() => {
    const today = new Date()
    today.setHours(0, 0, 0, 0)
    return today
  })
  const [news, setNews] = useState([])
  const [newsWarning, setNewsWarning] = useState('')
  const [newsError, setNewsError] = useState(false)
  const [newsLoading, setNewsLoading] = useState(false)
  const [newsSummary, setNewsSummary] = useState(null)
  const [summaryLoading, setSummaryLoading] = useState(false)
  const [summaryError, setSummaryError] = useState(null)
  const [chartLoaded, setChartLoaded] = useState(false)
  const [newsLoaded, setNewsLoaded] = useState(false)
  const [isDateSelected, setIsDateSelected] = useState(false)
  const stockPrices = useSelector((state) => state.stocks.prices[symbol]?.[selectedPeriod])
  const pricesStatus = useSelector((state) => state.stocks.pricesStatus[symbol]?.[selectedPeriod])
  const pricesError = useSelector((state) => state.stocks.pricesError[symbol]?.[selectedPeriod])

  useEffect(() => {
    setChartLoaded(false)
    dispatch(fetchStockPrices({ symbol, period: selectedPeriod }))
  }, [dispatch, symbol, selectedPeriod])
  
  // Monitor when chart data is loaded
  useEffect(() => {
    if (pricesStatus === 'succeeded' && stockPrices && stockPrices.length > 0) {
      setChartLoaded(true)
    }
  }, [pricesStatus, stockPrices])

  useEffect(() => {
    // Only fetch news after chart is loaded
    if (!chartLoaded) return;
    
    setNewsError(false)
    setNewsLoading(true)
    setNewsLoaded(false)
    
    fetch(`http://localhost:8000/api/stocks/${symbol}/news?period=${selectedPeriod}`)
      .then(response => {
        if (!response.ok) {
          if (response.status === 429) {
            setNews([])
            setNewsWarning('Daily news rate limit reached.')
            setNewsError(true)
            return Promise.reject('Rate limit reached')
          } else {
            return response.json().then(errorData => {
              setNews([])
              setNewsWarning(errorData.detail || 'An error occurred while fetching news')
              setNewsError(true)
              return Promise.reject(errorData.detail || 'Error fetching news')
            })
          }
        }
        return response.json()
      })
      .then(data => {
        if (data.data) {
          setNews(data.data)
          setNewsWarning(data.warning || '')
        } else {
          setNews(data)
          setNewsWarning('')
        }
        setNewsLoaded(true)
      })
      .catch(error => {
        console.error('Error fetching news:', error)
        // We don't set any state here that would prevent rendering the chart
      })
      .finally(() => {
        setNewsLoading(false)
      })
  }, [symbol, selectedPeriod, chartLoaded])
  
  // Fetch news summary and analysis after news is loaded
  useEffect(() => {
    // Only fetch AI summary after news is loaded and no specific date is selected
    if (!newsLoaded || isDateSelected) return;
    
    setSummaryLoading(true)
    setSummaryError(null)
    setNewsSummary(null)
    
    fetch(`http://localhost:8000/api/stocks/${symbol}/news-summary?period=${selectedPeriod}`)
      .then(response => {
        if (!response.ok) {
          if (response.status === 429) {
            setSummaryError('API rate limit reached. Please try again later.')
            return Promise.reject('Rate limit reached')
          } else {
            return response.json().then(errorData => {
              setSummaryError(errorData.detail || 'An error occurred while generating the news summary')
              return Promise.reject(errorData.detail || 'Error generating summary')
            })
          }
        }
        return response.json()
      })
      .then(data => {
        if (data.status === 'success' && data.data) {
          setNewsSummary(data.data)
        } else {
          setSummaryError('Failed to generate news summary')
        }
      })
      .catch(error => {
        console.error('Error fetching news summary:', error)
      })
      .finally(() => {
        setSummaryLoading(false)
      })
  }, [symbol, selectedPeriod, newsLoaded])

  const fetchNewsForDate = async (date) => {
    try {
      const formattedDate = date.toISOString().split('T')[0];
      
      // Set flag to indicate a specific date is selected
      setIsDateSelected(true);
      
      // First, fetch news for the selected date
      setNewsLoading(true);
      setNewsLoaded(false);
      setNewsError(false);
      
      const newsResponse = await fetch(`http://localhost:8000/api/stocks/${symbol}/news?date=${formattedDate}`);
      
      if (!newsResponse.ok) {
        if (newsResponse.status === 429) {
          setNews([]);
          setNewsWarning('Daily news rate limit reached.');
          setNewsError(true);
          setNewsLoading(false);
          return;
        }
        const errorData = await newsResponse.json();
        setNews([]);
        setNewsWarning(errorData.detail || 'An error occurred while fetching news');
        setNewsError(true);
        setNewsLoading(false);
        return;
      }

      const newsData = await newsResponse.json();
      setNews(newsData.data || []);
      setNewsWarning(newsData.warning || '');
      setNewsLoaded(true);
      setNewsLoading(false);
      
      // Only after news is loaded, fetch the AI summary
      setSummaryLoading(true);
      setSummaryError(null);
      setNewsSummary(null);
      
      // Add one day to the date for the AI service
      const nextDay = new Date(date);
      nextDay.setDate(nextDay.getDate() + 1);
      const offsetFormattedDate = nextDay.toISOString().split('T')[0];
      
      const summaryResponse = await fetch(`http://localhost:8000/api/stocks/${symbol}/news-summary?date=${offsetFormattedDate}`);
      
      if (!summaryResponse.ok) {
        if (summaryResponse.status === 429) {
          setSummaryError('API rate limit reached. Please try again later.');
        } else {
          const errorData = await summaryResponse.json();
          setSummaryError(errorData.detail || 'An error occurred while generating the news summary');
        }
      } else {
        const summaryData = await summaryResponse.json();
        if (summaryData.status === 'success' && summaryData.data) {
          setNewsSummary(summaryData.data);
        } else {
          setSummaryError('Failed to generate news summary');
        }
      }
      
      setSummaryLoading(false);
    } catch (error) {
      console.error('Error fetching data for date:', error);
      setNewsWarning('Failed to fetch news for selected date');
      setSummaryError('Failed to generate news summary');
      setNewsLoading(false);
      setSummaryLoading(false);
    }
  };

  const chartOptions = {
    chart: {
      type: 'line',
      height: 400,
      style: {
        fontFamily: 'Inter, Roboto, sans-serif',
        cursor: 'pointer'  // Set default cursor for chart area
      },
      animation: {
        duration: 500
      },
      events: {
        click: function(event) {
          if (event.xAxis && event.xAxis[0]) {
            // Get date from chart click without any adjustments
            const clickTime = event.xAxis[0].value;
            const date = new Date(clickTime);
            // Ensure we're using the exact date from the click without timezone adjustments
            const year = date.getFullYear();
            const month = date.getMonth();
            const day = date.getDate();
            // Create a new date object with the exact year, month, and day
            const exactDate = new Date(year, month, day, 0, 0, 0, 0);
            setSelectedDate(exactDate);
            // Also fetch news for this date when clicking on chart area
            fetchNewsForDate(exactDate);
          }
        }
      }
    },
    title: {
      text: `${symbol.replace('^', ' ')} Stock Price`,
      style: {
        fontSize: '20px',
        fontWeight: '500',
        color: '#1A1A1A'
      }
    },
    time: {
      useUTC: false
    },
    xAxis: {
      type: 'datetime',
      labels: {
        format: '{value:%Y-%m-%d}',
        style: {
          color: '#4A4A4A'
        }
      },
      lineColor: '#E0E0E0',
      tickColor: '#E0E0E0'
    },
    yAxis: {
      title: {
        text: 'Price',
        style: {
          color: '#4A4A4A'
        }
      },
      gridLineColor: '#E0E0E0',
      labels: {
        style: {
          color: '#4A4A4A'
        },
        formatter: function() {
          return '$' + this.value.toFixed(2)
        }
      }
    },
    tooltip: {
      backgroundColor: 'rgba(255, 255, 255, 0.9)',
      borderColor: '#E0E0E0',
      borderRadius: 8,
      padding: 12,
      shadow: false,
      style: {
        fontSize: '14px'
      },
      formatter: function() {
        // Create a new date object from the timestamp and ensure it's using local time
        // Don't use Highcharts.dateFormat which might apply timezone adjustments
        const date = new Date(this.x);
        const year = date.getFullYear();
        const month = String(date.getMonth() + 1).padStart(2, '0');
        const day = String(date.getDate()).padStart(2, '0');
        const formattedDate = `${year}-${month}-${day}`;
        
        return `<b>${symbol.replace('^', ' ')}</b><br/>
                Date: ${formattedDate}<br/>
                Price: $${this.y.toFixed(2)}`;
      }
    },
    plotOptions: {
      series: {
        animation: {
          duration: 1000
        },
        states: {
          hover: {
            lineWidth: 2,
            cursor: 'pointer'  // Set cursor for hover state
          }
        },
        cursor: 'pointer',  // Set cursor for series
        point: {
          events: {
            click: function() {
              // Get the date from the point's x value (timestamp)
              const pointTime = this.x;
              const date = new Date(pointTime);
              // Ensure we're using the exact date from the point without timezone adjustments
              const year = date.getFullYear();
              const month = date.getMonth();
              const day = date.getDate();
              // Create a new date object with the exact year, month, and day
              const exactDate = new Date(year, month, day, 0, 0, 0, 0);
              // Set as selected date and fetch news for this exact date
              setSelectedDate(exactDate);
              fetchNewsForDate(exactDate);
            }
          }
        }
      }
    },
    exporting: {
      enabled: true,
      menuItemDefinitions: {
        downloadPNG: {
          text: 'Download PNG'
        },
        downloadPDF: {
          text: 'Download PDF'
        },
        downloadSVG: {
          text: 'Download SVG'
        },
        downloadCSV: {
          text: 'Download CSV'
        },
        printChart: {
          text: 'Print Chart'
        }
      },
      buttons: {
        contextButton: {
          menuItems: ['downloadPNG', 'downloadPDF', 'downloadSVG', 'downloadCSV', 'printChart']
        }
      }
    },
    series: [{
      name: symbol.replace('^', ''),
      data: stockPrices ? stockPrices.map(price => {
        // Parse the timestamp string to create a date object
        const timestampParts = price.timestamp.split(' ')[0].split('-');
        const year = parseInt(timestampParts[0]);
        const month = parseInt(timestampParts[1]) - 1; // JavaScript months are 0-indexed
        const day = parseInt(timestampParts[2]);
        
        // Create a date object with the exact year, month, and day
        const date = new Date(year, month, day);
        
        return [
          date.getTime(),
          parseFloat(price.close)
        ];
      }).sort((a, b) => a[0] - b[0]) : [], // Keep data sorted by date
      color: '#0B3954',
      lineWidth: 2
    }],
    credits: {
      enabled: false
    }
  }

  // Reset isDateSelected when period changes
  useEffect(() => {
    setIsDateSelected(false);
  }, [selectedPeriod]);

  return (
    <Container maxWidth="lg" sx={{ py: 4 }}>
      <Fade in={true} timeout={500}>
        <Box>
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
            {pricesStatus === 'loading' ? (
              <Box display="flex" justifyContent="center" alignItems="center" minHeight="400px">
                <CircularProgress />
              </Box>
            ) : pricesStatus === 'failed' ? (
              <Alert severity="error" sx={{ mb: 2 }}>
                Error loading stock prices: {pricesError || 'Graph temporarily not available'}
              </Alert>
            ) : !stockPrices || stockPrices.length === 0 ? (
              <Alert severity="info" sx={{ mb: 2 }}>
                No price data available for the selected time period.
              </Alert>
            ) : (
              <>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
                  <Typography
                    variant="h5"
                    sx={{
                      fontWeight: 600,
                      color: 'text.primary',
                      display: 'flex',
                      alignItems: 'center',
                      gap: 1
                    }}
                  >
                    <ShowChartIcon sx={{ color: 'primary.main' }} />
                    Stock Price Chart
                  </Typography>
                  <Tooltip title="View on Yahoo Finance">
                    <Button
                      variant="outlined"
                      size="small"
                      endIcon={<OpenInNewIcon />}
                      href={`https://finance.yahoo.com/quote/${symbol}`}
                      target="_blank"
                      rel="noopener noreferrer"
                      sx={{ textTransform: 'none' }}
                    >
                      Yahoo Finance
                    </Button>
                  </Tooltip>
                </Box>
                <Box sx={{ mb: 3 }}>
                  <TimeRangeSelector
                    selectedPeriod={selectedPeriod}
                    onPeriodChange={setSelectedPeriod}
                  />
                </Box>
                <HighchartsReact
                  highcharts={Highcharts}
                  options={chartOptions}
                />
              </>
            )}
          </Paper>
          
          <NewsSummary 
            symbol={symbol}
            period={selectedPeriod}
            isLoading={summaryLoading}
            error={summaryError}
            data={newsSummary}
          />
          
          <NewsSection 
            news={news} 
            warning={newsWarning} 
            selectedDate={selectedDate} 
            isLoading={newsLoading}
          />
        </Box>
      </Fade>
    </Container>
  )
}

export default StockDetail