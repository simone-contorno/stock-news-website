from fastapi import Request
import asyncio
from typing import Callable
import logging

# Configure logging
logger = logging.getLogger(__name__)

# Global semaphore to ensure sequential processing
request_semaphore = asyncio.Semaphore(1)


class SequentialRequestMiddleware:
    """
    Middleware to ensure sequential processing of API requests.
    Only one request will be processed at a time, with others waiting in a queue.
    """
    
    def __init__(self, app):
        self.app = app
    
    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            # Pass through non-HTTP requests (like WebSocket)
            await self.app(scope, receive, send)
            return
            
        # Create a new send function that we'll use to intercept the response
        async def send_wrapper(message):
            await send(message)
            
        # Process the request with semaphore to ensure sequential processing
        async with request_semaphore:
            # Extract path for logging
            path = scope.get("path", "unknown")
            method = scope.get("method", "unknown")
            logger.info(f"Processing request: {method} {path}")
            
            # Process the request
            await self.app(scope, receive, send_wrapper)
            
            logger.info(f"Request completed: {method} {path}")