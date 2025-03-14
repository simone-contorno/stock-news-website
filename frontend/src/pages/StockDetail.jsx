import React, { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'
import { useDispatch, useSelector } from 'react-redux'
import { Box, Typography, Paper, CircularProgress, Alert, Container, Fade } from '@mui/material'
import Highcharts from 'highcharts'
import HighchartsReact from 'highcharts-react-official'
import exporting from 'highcharts/modules/exporting'
import offlineExporting from 'highcharts/modules/offline-exporting'
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
    // Only fetch AI summary after news is loaded
    if (!newsLoaded) return;
    
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
      
      const summaryResponse = await fetch(`http://localhost:8000/api/stocks/${symbol}/news-summary?date=${formattedDate}`);
      
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
            const date = new Date(event.xAxis[0].value)
            date.setHours(0, 0, 0, 0)
            setSelectedDate(date)
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
        const date = new Date(this.x);
        date.setDate(date.getDate()+1); // Keep this adjustment for tooltip only
        return `<b>${symbol.replace('^', ' ')}</b><br/>
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
        const date = new Date(price.timestamp);
        date.setDate(date.getDate());
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