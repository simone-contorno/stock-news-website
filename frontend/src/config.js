/**
 * Configuration file for the Stock News Website
 * 
 * This file contains environment-specific configuration settings
 * that are used throughout the application.
 */

// Determine if we're in production based on the hostname
const isProduction = window.location.hostname !== 'localhost';

// Set the API URL based on the environment
const API_URL = isProduction
  ? 'https://stock-news-website.onrender.com/api' // Production API URL
  : 'http://localhost:8000/api'; // Development API URL

export { API_URL, isProduction };