import React, { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'
import { useDispatch, useSelector } from 'react-redux'
import { Box, Typography, Paper, CircularProgress, Alert, Container, Fade } from '@mui/material'
import Highcharts from 'highcharts'
import HighchartsReact from 'highcharts-react-official'
import { fetchStockPrices } from '../store/stocksSlice'
import TimeRangeSelector from '../components/TimeRangeSelector'
import NewsSection from '../components/NewsSection'

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
  const stockPrices = useSelector((state) => state.stocks.prices[symbol]?.[selectedPeriod])
  const pricesStatus = useSelector((state) => state.stocks.pricesStatus[symbol]?.[selectedPeriod])
  const pricesError = useSelector((state) => state.stocks.pricesError[symbol]?.[selectedPeriod])

  useEffect(() => {
    dispatch(fetchStockPrices({ symbol, period: selectedPeriod }))
  }, [dispatch, symbol, selectedPeriod])

  useEffect(() => {
    setNewsError(false)
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
      })
      .catch(error => {
        console.error('Error fetching news:', error)
        // We don't set any state here that would prevent rendering the chart
      })
  }, [symbol, selectedPeriod])

  const fetchNewsForDate = async (date) => {
    try {
      const formattedDate = date.toISOString().split('T')[0];
      const response = await fetch(`http://localhost:8000/api/stocks/${symbol}/news?date=${formattedDate}`);
      
      if (!response.ok) {
        if (response.status === 429) {
          setNewsWarning('Daily news rate limit reached.');
          setNewsError(true);
          return;
        }
        const errorData = await response.json();
        setNewsWarning(errorData.detail || 'An error occurred while fetching news');
        setNewsError(true);
        return;
      }

      const data = await response.json();
      setNews(data.data || []);
      setNewsWarning(data.warning || '');
    } catch (error) {
      console.error('Error fetching news for date:', error);
      setNewsWarning('Failed to fetch news for selected date');
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
            const date = new Date(event.xAxis[0].value)
            date.setHours(0, 0, 0, 0)
            setSelectedDate(date)
          }
        }
      }
    },
    title: {
      text: `${symbol} Stock Price`,
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
        const date = new Date(this.x);
        date.setDate(date.getDate() + 1); // Add one day to fix tooltip date display
        return `<b>${symbol}</b><br/>
                Date: ${Highcharts.dateFormat('%Y-%m-%d', date)}<br/>
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
              const date = new Date(this.x);
              date.setHours(0, 0, 0, 0);
              setSelectedDate(date);
              fetchNewsForDate(date);
            }
          }
        }
      }
    },
    series: [{
      name: symbol,
      data: stockPrices ? stockPrices.map(price => {
        const date = new Date(price.timestamp);
        // Add one day to fix the offset
        date.setDate(date.getDate() + 1);
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
          
          <NewsSection news={news} warning={newsWarning} selectedDate={selectedDate} />
        </Box>
      </Fade>
    </Container>
  )
}

export default StockDetail