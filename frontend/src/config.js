/**
 * Configuration file for the Stock News Website
 * 
 * This file contains environment-specific configuration settings
 * that are used throughout the application.
 */

// Determine if we're in production based on the hostname
const isProduction = window.location.hostname !== 'localhost';

// Get the current domain for production use
const currentDomain = window.location.origin;

// Set the API URL based on the environment
let API_URL;

if (isProduction) {
  // In production, try to use the same domain if possible (for Vercel deployments)
  if (window.location.hostname.includes('vercel.app')) {
    API_URL = 'https://stock-news-website.onrender.com/api'; // Production API URL on Render
  } else if (window.location.hostname.includes('render.com')) {
    // If we're on Render, use relative URL to ensure same-origin requests
    API_URL = '/api';
  } else {
    // Fallback to the known production backend URL
    API_URL = 'https://stock-news-website.onrender.com/api';
  }
} else {
  // Development environment
  API_URL = 'http://localhost:8000/api';
}

// Add console logging to help debug API connection issues
console.log(`Environment: ${isProduction ? 'Production' : 'Development'}`); 
console.log(`API URL: ${API_URL}`);

export { API_URL, isProduction };