import logging
from typing import Dict, Any
from datetime import datetime, timedelta
import requests
from fastapi import HTTPException
from ..core.config import settings

logger = logging.getLogger(__name__)

def get_stock_news(symbol: str, period: str = '7d') -> Dict[str, Any]:
    # Validate API key
    if not settings.NEWS_API_KEY:
        logger.error("NEWS_API_KEY not configured in settings")
        return {
            "status": "error",
            "message": "NEWS_API_KEY environment variable is not properly configured"
        }

    logger.info(f"Fetching news for symbol {symbol} with period {period}")

    # Convert period to days
    days = {
        '1d': 1,
        '7d': 7,
        '1m': 30,
        '3m': 90,
        '6m': 180,
        '1y': 365
    }.get(period, 7)

    # News API has a limit of 100 articles per request and only allows fetching news
    # from the last month for free tier
    days = min(days, 30)
    warning_message = None
    if days > 20:
        warning_message = 'Only showing news from the last 20 days due to API limitations.'

    # Format dates for the API in UTC
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=days)

    # Prepare API request parameters
    params = {
        'q': f'"{symbol}" OR "{symbol} stock"',
        'from': start_date.strftime('%Y-%m-%d'),
        'to': end_date.strftime('%Y-%m-%d'),
        'language': 'en',
        'sortBy': 'publishedAt',
        'pageSize': 100,
        'apiKey': settings.NEWS_API_KEY
    }

    page = 1
    page_size = params['pageSize']
    all_articles = []

    while True:
        try:
            logger.info(f"Making API request for page {page}")
            response = requests.get(settings.NEWS_API_BASE_URL, params=params, timeout=settings.NEWS_API_TIMEOUT)
                
            # Handle rate limiting and older data limitation
            if response.status_code == 429:
                logger.warning("Rate limit hit")
                return {
                    'status': 'rate_limit',
                    'message': 'Daily news rate limit reached.'
                }
            elif response.status_code == 426:
                logger.warning("Older data not available from News API")
                if all_articles:
                    return {
                        'status': 'partial_success',
                        'data': all_articles,
                        'warning': 'Older data not available, feature will arrive in future!'
                    }
                return {
                    'status': 'error',
                    'message': 'No articles available for the requested time period.'
                }
            
            response.raise_for_status()
            news_data = response.json()
            logger.info(f"API Response status: {news_data.get('status')}, Total results: {news_data.get('totalResults')}")

            if news_data.get('status') == 'ok' and 'articles' in news_data:
                articles = news_data['articles']
                if not articles:
                    logger.info("No more articles found")
                    break

                all_articles.extend([
                    {
                        'title': article.get('title', ''),
                        'description': article.get('description', ''),
                        'url': article.get('url', ''),
                        'source': article.get('source', {}).get('name', ''),
                        'published_at': article.get('publishedAt', '')
                    } for article in articles
                ])

                # Check if we've reached the end of available articles
                if len(articles) < page_size or page * page_size >= news_data.get('totalResults', 0):
                    logger.info(f"Completed fetching all articles. Total articles: {len(all_articles)}")
                    break

                # Increment page for next iteration
                page += 1
                
            else:
                error_message = news_data.get('message', 'Unknown error occurred while fetching news data')
                logger.error(f"API Error: {error_message}")
                return {
                    'status': 'error',
                    'message': f'API Error: {error_message}'
                }

        except requests.exceptions.RequestException as e:
            logger.error(f"Request error: {str(e)}")
            return {
                'status': 'error',
                'message': f'Failed to fetch news data: {str(e)}'
            }
    
    return {
        'status': 'success',
        'data': all_articles,
        'warning': warning_message
    }