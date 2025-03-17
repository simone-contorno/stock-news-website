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

// Backend server URL for production
const backendDomain = 'stock-news-website.onrender.com';

// Set the API URL based on the environment
let BACKEND_URL;

if (isProduction) {
  // In production, use the dedicated backend URL
  if (window.location.hostname.includes('vercel.app')) {
    BACKEND_URL = `https://${backendDomain}`; // Use HTTPS instead of HTTP
  } else if (window.location.hostname.includes('render.com')) {
    // If we're on Render, use relative URL to ensure same-origin requests
    BACKEND_URL = '';
  } else {
    // Fallback to the dedicated backend URL
    BACKEND_URL = `https://${backendDomain}`; // Use HTTPS instead of HTTP
  }
} else {
  // Development environment
  BACKEND_URL = 'http://localhost:8000/api';
}

// Add console logging to help debug API connection issues
console.log(`Environment: ${isProduction ? 'Production' : 'Development'}`); 
console.log(`API URL: ${BACKEND_URL}`);

export { BACKEND_URL, isProduction };