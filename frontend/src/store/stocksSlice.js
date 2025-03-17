import { createSlice, createAsyncThunk } from '@reduxjs/toolkit'
import axios from 'axios'
import { API_URL } from '../config'

export const fetchStocks = createAsyncThunk('stocks/fetchStocks', async () => {
  const response = await axios.get(`${API_URL}/stocks/`)
  return response.data
})

export const fetchStockPrices = createAsyncThunk(
  'stocks/fetchStockPrices',
  async ({ symbol, period }) => {
    const response = await axios.get(`${API_URL}/stocks/${symbol}/prices?period=${period}`)
    return response.data
  }
)

const stocksSlice = createSlice({
  name: 'stocks',
  initialState: {
    list: [],
    prices: {},
    pricesStatus: {},
    pricesError: {},
    status: 'idle',
    error: null,
  },
  reducers: {},
  extraReducers: (builder) => {
    builder
      .addCase(fetchStocks.pending, (state) => {
        state.status = 'loading'
      })
      .addCase(fetchStocks.fulfilled, (state, action) => {
        state.status = 'succeeded'
        state.list = action.payload
      })
      .addCase(fetchStocks.rejected, (state, action) => {
        state.status = 'failed'
        state.error = action.error.message
      })
      .addCase(fetchStockPrices.pending, (state, action) => {
        const { symbol, period } = action.meta.arg
        if (!state.pricesStatus[symbol]) {
          state.pricesStatus[symbol] = {}
        }
        state.pricesStatus[symbol][period] = 'loading'
      })
      .addCase(fetchStockPrices.fulfilled, (state, action) => {
        const { symbol, period } = action.meta.arg
        if (!state.prices[symbol]) {
          state.prices[symbol] = {}
        }
        if (!state.pricesStatus[symbol]) {
          state.pricesStatus[symbol] = {}
        }
        // Ensure the data is an array before storing it
        const priceData = Array.isArray(action.payload) ? action.payload : [];
        state.prices[symbol][period] = priceData;
        state.pricesStatus[symbol][period] = 'succeeded'
      })
      .addCase(fetchStockPrices.rejected, (state, action) => {
        const { symbol, period } = action.meta.arg
        if (!state.pricesError[symbol]) {
          state.pricesError[symbol] = {}
        }
        if (!state.pricesStatus[symbol]) {
          state.pricesStatus[symbol] = {}
        }
        state.pricesError[symbol][period] = action.error.message
        state.pricesStatus[symbol][period] = 'failed'
      })
  },
})

export default stocksSlice.reducer