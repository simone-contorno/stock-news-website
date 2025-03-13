import React, { useEffect } from 'react'
import { useDispatch, useSelector } from 'react-redux'
import { Link } from 'react-router-dom'
import { Container, Grid, Card, CardContent, Typography, Box, Paper } from '@mui/material'
import { fetchStocks } from '../store/stocksSlice'
import Carousel from 'react-material-ui-carousel'

const Dashboard = () => {
  const dispatch = useDispatch()
  const { list: stocks, status, error } = useSelector((state) => state.stocks)

  useEffect(() => {
    if (status === 'idle') {
      dispatch(fetchStocks())
    }
  }, [status, dispatch])

  if (status === 'loading') {
    return <Typography>Loading...</Typography>
  }

  if (status === 'failed') {
    return <Typography color="error">{error}</Typography>
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
          {stocks.map((stock) => (
            <Box
              key={stock.symbol}
              sx={{
                textAlign: 'center',
                p: 2
              }}
            >
              <Typography variant="h4" gutterBottom>
                {stock.symbol}
              </Typography>
              <Typography variant="h6" sx={{ color: 'text.secondary' }}>
                {stock.name}
              </Typography>
            </Box>
          ))}
        </Carousel>
      </Paper>

      <Typography variant="h5" gutterBottom sx={{ fontWeight: 500, mb: 3 }}>
        Available Stocks
      </Typography>
      <Grid container spacing={3}>
        {stocks.map((stock) => (
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
                  {stock.symbol}
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