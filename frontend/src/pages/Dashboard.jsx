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

  useEffect(() => {
    if (status === 'idle') {
      dispatch(fetchStocks())
    }
    // Fetch initial prices only for dashboard stocks
    dashboardStocks.forEach(stock => {
      if (!prices[stock.symbol]) {
        dispatch(fetchStockPrices({ symbol: stock.symbol, period: '7d' }))
      }
    })
  }, [status, dispatch, dashboardStocks, prices])

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
    if (stockPrices.length >= 2) {
      const latest = parseFloat(stockPrices[stockPrices.length - 1].close)
      const previous = parseFloat(stockPrices[stockPrices.length - 2].close)
      const change = ((latest - previous) / previous) * 100
      return {
        value: change.toFixed(2),
        isPositive: change > 0,
        color: change > 0 ? 'success.main' : change < 0 ? 'error.main' : 'text.secondary'
      }
    }
    return null
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
        <Carousel
          animation="slide"
          interval={5000}
          sx={{ minHeight: '100px' }}
        >
          {dashboardStocks.map((stock) => {
            const change = getStockChange(stock.symbol)
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
                {change && (
                  <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 1 }}>
                    {change.isPositive ? 
                      <TrendingUpIcon sx={{ color: change.color }} /> : 
                      <TrendingDownIcon sx={{ color: change.color }} />
                    }
                    <Typography sx={{ color: change.color }}>
                      {change.value}%
                    </Typography>
                  </Box>
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