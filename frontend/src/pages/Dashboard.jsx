import React, { useEffect } from 'react'
import { useDispatch, useSelector } from 'react-redux'
import { Link } from 'react-router-dom'
import { Container, Grid, Card, CardContent, Typography, Box, Paper, CircularProgress } from '@mui/material'
import { fetchStocks, fetchStockPrices } from '../store/stocksSlice'
import Carousel from 'react-material-ui-carousel'
import TrendingUpIcon from '@mui/icons-material/TrendingUp'
import TrendingDownIcon from '@mui/icons-material/TrendingDown'
import ErrorMessage from '../components/ErrorMessage'

const Dashboard = () => {
  const dispatch = useDispatch()
  const { list: stocks, status, error } = useSelector((state) => state.stocks)
  const prices = useSelector((state) => state.stocks.prices)
   const pricesStatus = useSelector((state) => state.stocks.pricesStatus)

  // Filter stocks for the dashboard display
  const dashboardStocks = stocks.filter(stock => {
    // Main indices
    if (stock.symbol === '^GSPC' || stock.symbol === '^DJI' || stock.symbol === '^IXIC') {
      return true;
    }
    // Tech stocks
    if (stock.category === 'stock' && ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'NVDA', 'META', 'TSLA'].includes(stock.symbol)) {
      return true;
    }
    return false;
  });

  // Function to fetch stock prices sequentially
  const fetchStockPricesSequentially = async (stocksList) => {
    for (const stock of stocksList) {
      // Check if we already have data or if it's currently loading
      const hasData = prices[stock.symbol]?.['7d']?.length > 0;
      const isLoading = pricesStatus[stock.symbol]?.['7d'] === 'loading';
      const hasSucceeded = pricesStatus[stock.symbol]?.['7d'] === 'succeeded';
      
      // Only fetch if we don't have data, it's not loading, and hasn't already succeeded
      if (!hasData && !isLoading && !hasSucceeded) {
        await dispatch(fetchStockPrices({ symbol: stock.symbol, period: '7d' }))
      }
    }
  }

  useEffect(() => {
    if (status === 'idle') {
      dispatch(fetchStocks())
    }
  }, [status, dispatch])

  // Start fetching stock prices once we have the stock list
  useEffect(() => {
    if (dashboardStocks.length > 0) {
      fetchStockPricesSequentially(dashboardStocks)
    }
  }, [dashboardStocks, prices, pricesStatus]) // Add dependencies to prevent unnecessary fetches

  // Show loading indicator only when initially fetching the stock list
  if (status === 'loading') {
    return (
      <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', minHeight: '50vh' }}>
        <CircularProgress size={60} thickness={4} />
      </Box>
    )
  }

  if (status === 'failed') {
    return (
      <Container maxWidth="lg" sx={{ py: 4 }}>
        <ErrorMessage 
          title="Network Error" 
        />
      </Container>
    )
  }

  const getStockChange = (symbol) => {
    const stockPrices = prices[symbol]?.['7d'] || []
    
    // Find the last two valid data points with close values
    let validPrices = stockPrices.filter(price => {
      const closeValue = parseFloat(price.close);
      return !isNaN(closeValue) && closeValue !== 0;
    });
    
    if (validPrices.length >= 2) {
      const latest = parseFloat(validPrices[validPrices.length - 1].close);
      const previous = parseFloat(validPrices[validPrices.length - 2].close);
      
      // Both values should be valid at this point, but double-check anyway
      if (!isNaN(latest) && !isNaN(previous) && previous !== 0) {
        const change = ((latest - previous) / previous) * 100;
        return {
          value: change.toFixed(2),
          isPositive: change > 0,
          color: change > 0 ? 'success.main' : change < 0 ? 'error.main' : 'text.secondary'
        };
      }
    }
    return null;
  }

  return (
    <Container maxWidth="lg" sx={{ py: 4 }}>
      <Box sx={{ mb: 6 }}>
        <Typography variant="h3" gutterBottom sx={{ fontWeight: 600 }}>
          Welcome to Stock News
        </Typography>
        <Typography variant="h6" sx={{ color: 'text.secondary', mb: 4 }}>
          Your comprehensive platform for real-time stock market updates and financial news.
          Track your favorite stocks, analyze market trends, and stay informed with the latest news.
        </Typography>
      </Box>

      <Paper elevation={0} sx={{ p: 3, mb: 6, borderRadius: 2 }}>
        <Typography variant="h5" gutterBottom sx={{ fontWeight: 500 }}>
          Today's Market Movers
        </Typography>
        <Typography variant="caption" sx={{ display: 'block', mb: 2, color: 'text.secondary' }}>
          Note: Today's data is only available after market close. Percentages shown reflect changes between the last two available trading days.
        </Typography>
        <Carousel
          animation="slide"
          interval={5000}
          sx={{ minHeight: '100px' }}
        >
          {dashboardStocks.map((stock) => {
            const change = getStockChange(stock.symbol)
            const isLoading = !pricesStatus[stock.symbol] || pricesStatus[stock.symbol]['7d'] === 'loading'
            
            return (
              <Box
                key={stock.symbol}
                sx={{
                  textAlign: 'center',
                  p: 2
                }}
              >
                <Typography variant="h4" gutterBottom>
                  {stock.symbol.replace('^', '')}
                </Typography>
                <Typography variant="h6" sx={{ color: 'text.secondary' }}>
                  {stock.name}
                </Typography>
                {isLoading ? (
                  <Box sx={{ display: 'flex', justifyContent: 'center', mt: 1 }}>
                    <CircularProgress size={24} thickness={4} />
                  </Box>
                ) : change ? (
                  <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 1 }}>
                    {change.isPositive ? 
                      <TrendingUpIcon sx={{ color: change.color }} /> : 
                      <TrendingDownIcon sx={{ color: change.color }} />
                    }
                    <Typography sx={{ color: change.color }}>
                      {change.value}%
                    </Typography>
                  </Box>
                ) : (
                  <Typography sx={{ color: 'text.secondary' }}>
                    No data available
                  </Typography>
                )}
              </Box>
            )
          })}
        </Carousel>
      </Paper>

      <Typography variant="h5" gutterBottom sx={{ fontWeight: 500, mb: 3 }}>
        Top Stocks
      </Typography>
      <Grid container spacing={3}>
        {dashboardStocks.map((stock) => (
          <Grid item xs={12} sm={6} md={4} key={stock.symbol}>
            <Card
              component={Link}
              to={`/stock/${stock.symbol}`}
              sx={{
                textDecoration: 'none',
                height: '100%',
                display: 'flex',
                flexDirection: 'column',
                transition: 'transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out',
                '&:hover': {
                  transform: 'translateY(-4px)',
                  boxShadow: '0 4px 20px 0 rgba(0,0,0,0.1)'
                }
              }}
            >
              <CardContent sx={{ flexGrow: 1 }}>
                <Typography variant="h5" component="div" gutterBottom>
                  {stock.symbol.replace('^', '')}
                </Typography>
                <Typography color="text.secondary" gutterBottom>
                  {stock.name}
                </Typography>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>
    </Container>
  )
}

export default Dashboard