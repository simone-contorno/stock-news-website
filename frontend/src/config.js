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

// Backend server IPs for load balancing in production
const backendIPs = [
  '3.75.158.163',
  '3.125.183.140',
  '35.157.117.28'
];

// Function to select a backend IP using a simple round-robin approach
const getBackendIP = () => {
  // Use a timestamp-based approach to distribute requests
  const index = Math.floor(Date.now() / 1000) % backendIPs.length;
  return backendIPs[index];
};

// Set the API URL based on the environment
let API_URL;

if (isProduction) {
  // In production, use the load-balanced backend IPs
  if (window.location.hostname.includes('vercel.app')) {
    const backendIP = getBackendIP();
    API_URL = `http://${backendIP}/api`; // Use the selected backend IP
  } else if (window.location.hostname.includes('render.com')) {
    // If we're on Render, use relative URL to ensure same-origin requests
    API_URL = '/api';
  } else {
    // Fallback to the load-balanced backend
    const backendIP = getBackendIP();
    API_URL = `http://${backendIP}/api`;
  }
} else {
  // Development environment
  API_URL = 'http://localhost:8000/api';
}

// Add console logging to help debug API connection issues
console.log(`Environment: ${isProduction ? 'Production' : 'Development'}`); 
console.log(`API URL: ${API_URL}`);

export { API_URL, isProduction };