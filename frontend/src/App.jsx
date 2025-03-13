import React from 'react'
import { Routes, Route } from 'react-router-dom'
import { ThemeProvider } from '@mui/material/styles'
import CssBaseline from '@mui/material/CssBaseline'
import theme from './theme'
import Navbar from './components/Navbar'
import Dashboard from './pages/Dashboard'
import StockDetail from './pages/StockDetail'
import Indices from './pages/Indices'
import Contact from './pages/Contact'

function App() {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Navbar />
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/stock/:symbol" element={<StockDetail />} />
        <Route path="/indices" element={<Indices />} />
        <Route path="/contact" element={<Contact />} />
      </Routes>
    </ThemeProvider>
  )
}

export default App