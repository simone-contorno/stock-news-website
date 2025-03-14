import logging
import json
import requests
from typing import Dict, Any, List
from ..core.config import settings

logger = logging.getLogger(__name__)

def generate_news_summary(symbol: str, news_articles: List[Dict[str, Any]], price_data: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Generate a summary of news articles and analyze correlation with price trends using Together AI.
    
    Args:
        symbol: The stock symbol
        news_articles: List of news articles with title, description, etc.
        price_data: List of price data points with timestamp, close, etc.
    
    Returns:
        Dictionary with summary and analysis
    """
    # Validate API key
    if not settings.TOGETHER_API_KEY:
        logger.error("TOGETHER_API_KEY not configured in settings")
        return {
            "status": "error",
            "message": "TOGETHER_API_KEY environment variable is not properly configured"
        }
    
    if not news_articles:
        logger.warning(f"No news articles provided for {symbol}")
        return {
            "status": "error",
            "message": "No news articles available for analysis"
        }
    
    if not price_data:
        logger.warning(f"No price data provided for {symbol}")
        return {
            "status": "error",
            "message": "No price data available for analysis"
        }
    
    # Prepare news data for the prompt
    news_text = "\n\n".join([f"Title: {article.get('title', '')}\nSource: {article.get('source', '')}\nDate: {article.get('published_at', '')}\nDescription: {article.get('description', '')}" 
                           for article in news_articles[:10]])  # Limit to 10 articles to avoid token limits
    
    # Extract price trend information
    start_price = price_data[0]['close'] if price_data else None
    end_price = price_data[-1]['close'] if price_data else None
    price_change = None
    price_change_percent = None
    
    if start_price is not None and end_price is not None:
        price_change = end_price - start_price
        price_change_percent = (price_change / start_price) * 100
    
    # Construct the prompt for the AI
    prompt = f"""
You are a financial analyst assistant. Based on the following news articles about {symbol} stock and its price data, please:

1. Provide a concise summary of key events (2-3 paragraphs)
2. Analyze how these news events correlate with the observed price trend
3. Highlight the most significant news that likely impacted the stock price

Stock: {symbol}
Price Change: {price_change_percent:.2f}% (${price_change:.2f})

News Articles:
{news_text}

Your analysis should be factual, balanced, and focus on the relationship between news and price movements.
"""
    
    # Prepare the API request
    headers = {
        "Authorization": f"Bearer {settings.TOGETHER_API_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": settings.TOGETHER_API_MODEL,
        "prompt": prompt,
        "max_tokens": 1000,
        "temperature": 0.7,
        "top_p": 0.9,
        "top_k": 40,
        "repetition_penalty": 1.0,
        "stop": ["<|im_end|>", "<|endoftext|>"]
    }
    
    try:
        response = requests.post(
            settings.TOGETHER_API_BASE_URL,
            headers=headers,
            json=data,
            timeout=settings.TOGETHER_API_TIMEOUT
        )
        
        response.raise_for_status()
        result = response.json()
        
        if 'choices' in result and len(result['choices']) > 0:
            summary_text = result['choices'][0]['text'].strip()
            
            # Split the summary into sections
            sections = summary_text.split('\n\n')
            
            # Extract summary and analysis (basic parsing)
            summary = sections[0] if sections else ""
            analysis = "\n\n".join(sections[1:]) if len(sections) > 1 else ""
            
            return {
                "status": "success",
                "data": {
                    "summary": summary,
                    "analysis": analysis,
                    "full_text": summary_text
                }
            }
        else:
            logger.error(f"Unexpected API response format: {result}")
            return {
                "status": "error",
                "message": "Failed to generate summary: Unexpected API response format"
            }
            
    except requests.exceptions.RequestException as e:
        logger.error(f"API request error: {str(e)}")
        return {
            "status": "error",
            "message": f"Failed to generate summary: {str(e)}"
        }
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return {
            "status": "error",
            "message": f"An unexpected error occurred: {str(e)}"
        }