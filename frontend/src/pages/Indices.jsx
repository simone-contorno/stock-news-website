import React, { useState, useEffect } from 'react'
import { useSelector, useDispatch } from 'react-redux'
import { Link } from 'react-router-dom'
import { 
  Container, Grid, Card, CardContent, Typography, Box,
  Tabs, Tab, Paper, Divider, CircularProgress
} from '@mui/material'
import SearchBar from '../components/SearchBar'
import { fetchStocks } from '../store/stocksSlice'
import ErrorMessage from '../components/ErrorMessage'

const Indices = () => {
  const dispatch = useDispatch()
  const { list: stocks, status, error } = useSelector((state) => state.stocks)
  const [searchTerm, setSearchTerm] = useState('')
  const [selectedCategory, setSelectedCategory] = useState('all')

  // Fetch stocks when component mounts if they're not already loaded
  useEffect(() => {
    if (status === 'idle') {
      dispatch(fetchStocks())
    }
  }, [status, dispatch])

  // Group stocks by category
  const categories = {
    major: { title: 'Major Indices', items: stocks.filter(s => s.category === 'major') },
    minor: { title: 'Regional & Sector Indices', items: stocks.filter(s => s.category === 'minor') },
    stock: { title: 'Major Stocks', items: stocks.filter(s => s.category === 'stock') }
  }

  const filteredStocks = stocks.filter(stock => {
    const matchesSearch = stock.symbol.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         stock.name.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesCategory = selectedCategory === 'all' || stock.category === selectedCategory;
    return matchesSearch && matchesCategory;
  });

  // Show loading indicator when initially fetching the stock list
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

  return (
    <Container maxWidth="lg" sx={{ py: 4 }}>
      <Box sx={{ mb: 4 }}>
        <Typography variant="h4" gutterBottom sx={{ fontWeight: 600 }}>
          Market Overview
        </Typography>
        <SearchBar onSearch={setSearchTerm} />
      </Box>

      <Paper sx={{ mb: 4 }}>
        <Tabs
          value={selectedCategory}
          onChange={(_, value) => setSelectedCategory(value)}
          sx={{ borderBottom: 1, borderColor: 'divider' }}
        >
          <Tab value="all" label="All" />
          <Tab value="major" label="Major Indices" />
          <Tab value="minor" label="Regional & Sector" />
          <Tab value="stock" label="Major Stocks" />
        </Tabs>
      </Paper>

      {selectedCategory === 'all' ? (
        // Show categorized sections when "All" is selected
        Object.entries(categories).map(([key, category]) => (
          <Box key={key} sx={{ mb: 6 }}>
            <Typography variant="h5" sx={{ mb: 3, fontWeight: 500 }}>
              {category.title}
            </Typography>
            <Grid container spacing={3}>
              {category.items
                .filter(stock => 
                  stock.symbol.toLowerCase().includes(searchTerm.toLowerCase()) ||
                  stock.name.toLowerCase().includes(searchTerm.toLowerCase())
                )
                .map(stock => (
                  <Grid item xs={12} sm={6} md={4} key={stock.symbol}>
                    <StockCard stock={stock} />
                  </Grid>
                ))}
            </Grid>
            <Divider sx={{ mt: 4 }} />
          </Box>
        ))
      ) : (
        // Show filtered items for selected category
        <Grid container spacing={3}>
          {filteredStocks.map(stock => (
            <Grid item xs={12} sm={6} md={4} key={stock.symbol}>
              <StockCard stock={stock} />
            </Grid>
          ))}
        </Grid>
      )}
    </Container>
  )
}

// Extracted StockCard component for cleaner code
const StockCard = ({ stock }) => (
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
      <Typography color="text.secondary">
        {stock.name}
      </Typography>
      <Typography variant="caption" color="text.secondary" sx={{ mt: 1, display: 'block' }}>
        Region: {stock.region}
      </Typography>
    </CardContent>
  </Card>
);

export default Indices