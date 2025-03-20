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
    
    async def __call__(self, request: Request, call_next: Callable):
        # Log incoming request
        logger.info(f"Request received: {request.method} {request.url.path}")
        
        # Acquire the semaphore (wait if another request is being processed)
        async with request_semaphore:
            logger.info(f"Processing request: {request.method} {request.url.path}")
            # Process the request
            response = await call_next(request)
            logger.info(f"Request completed: {request.method} {request.url.path}")
        
        return response