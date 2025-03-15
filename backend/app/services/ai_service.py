import logging
import json
import requests
from typing import Dict, Any, List
from ..core.config import settings

logger = logging.getLogger(__name__)

def generate_news_summary(symbol: str, news_articles: List[Dict[str, Any]], price_data: List[Dict[str, Any]], date: str = None) -> Dict[str, Any]:
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
    
    # Filter data if a specific date is provided
    if date:
        # Filter news articles for the specific date
        filtered_news = []
        for article in news_articles:
            published_date = article.get('published_at', '')
            # Extract date part from ISO format (YYYY-MM-DDThh:mm:ss)
            if published_date:
                # Handle different date formats
                if 'T' in published_date:  # ISO format
                    article_date = published_date.split('T')[0]
                else:  # Try to extract YYYY-MM-DD part
                    article_date = published_date[:10] if len(published_date) >= 10 else published_date
                
                # Exact date match - ensure proper comparison
                if article_date == date:  
                    filtered_news.append(article)
        
        # Use filtered news if available, otherwise use original news
        news_to_analyze = filtered_news if filtered_news else news_articles
        
        # Filter price data for the specific date
        filtered_price = []
        for price_point in price_data:
            timestamp = price_point.get('timestamp', '')
            # Extract date part from timestamp
            if timestamp:
                # Handle different timestamp formats
                if ' ' in timestamp:  # Format: YYYY-MM-DD HH:MM:SS
                    price_date = timestamp.split(' ')[0]
                else:  # Try to extract YYYY-MM-DD part
                    price_date = timestamp[:10] if len(timestamp) >= 10 else timestamp
                
                # Compare with the requested date
                if price_date == date:  # Exact date match
                    filtered_price.append(price_point)
        
        # Use filtered price if available, otherwise use original price data
        price_to_analyze = filtered_price if filtered_price else price_data
    else:
        news_to_analyze = news_articles
        price_to_analyze = price_data
    
    # Prepare news data for the prompt
    news_text = "\n\n".join([f"Title: {article.get('title', '')}\nSource: {article.get('source', '')}\nDate: {article.get('published_at', '')}\nDescription: {article.get('description', '')}" 
                           for article in news_to_analyze[:10]])  # Limit to 10 articles to avoid token limits
    
    # Extract price trend information
    start_price = price_to_analyze[0]['close'] if price_to_analyze else None
    end_price = price_to_analyze[-1]['close'] if price_to_analyze else None
    price_change = None
    price_change_percent = None
    
    # Extract date information for analysis period
    # If a specific date is provided, use it directly to avoid any inconsistencies
    if date:
        start_date = date
        end_date = date
    else:
        start_date = price_to_analyze[0].get('timestamp', 'N/A').split(' ')[0] if price_to_analyze and ' ' in price_to_analyze[0].get('timestamp', 'N/A') else price_to_analyze[0].get('timestamp', 'N/A')[:10] if price_to_analyze else 'N/A'
        end_date = price_to_analyze[-1].get('timestamp', 'N/A').split(' ')[0] if price_to_analyze and ' ' in price_to_analyze[-1].get('timestamp', 'N/A') else price_to_analyze[-1].get('timestamp', 'N/A')[:10] if price_to_analyze else 'N/A'
    
    if start_price is not None and end_price is not None:
        price_change = end_price - start_price
        price_change_percent = (price_change / start_price) * 100

    # Construct the prompt for the AI
    prompt = f"""
You are a financial analyst assistant. Based on the following news articles about {symbol.replace("^","")} stock and its price data, create a structured, professional analysis with proper HTML formatting for web display.

{"Analysis for specific date: " + date if date else "Analysis for period: " + start_date + " to " + end_date}

Format your response using the following HTML structure:

<div class="analysis-period-section">
  <h2>Analysis Period</h2>
  <p>{"Date: " + date if date else "From " + start_date + " to " + end_date}</p>
  <p>Stock: {symbol.replace("^","")}</p>
  <p>Price Change: {price_change_percent:.2f}% (${price_change:.2f})</p>
</div>

<div class="news-summary-section">
  <h2>News Summary</h2>
  <ul>
    <li><span class="sentiment-indicator positive">●</span> Key news point 1</li>
    <li><span class="sentiment-indicator negative">●</span> Key news point 2</li>
    <!-- Add more bullet points as needed -->
  </ul>
</div>

<div class="price-correlation-section">
  <h2>Price Correlation</h2>
  <ul>
    <li><span class="correlation-indicator positive">●</span> Correlation point 1</li>
    <li><span class="correlation-indicator negative">●</span> Correlation point 2</li>
    <li><span class="correlation-indicator neutral">●</span> Correlation point 3</li>
    <!-- Add more bullet points as needed -->
  </ul>
</div>

<div class="trend-prediction-section">
  <h2>Trend Prediction</h2>
  <ul>
    <li><span class="prediction-indicator positive">●</span> Future scenario or factor 1</li>
    <li><span class="prediction-indicator negative">●</span> Future scenario or factor 2</li>
    <!-- Add more bullet points as needed -->
  </ul>
</div>

News Articles:
{news_text}

Your analysis should be factual, balanced, and focus only on the relationship between news and price movements. Do not include any disclaimers, introductions, or conclusions - just the four HTML-formatted sections above. Ensure all HTML tags are properly closed and formatted. Make sure to reference the specific date in your analysis.
"""
    
    # Prepare the API request
    headers = {
        "Authorization": f"Bearer {settings.TOGETHER_API_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": settings.TOGETHER_API_MODEL,
        "messages": [
            {"role": "user", "content": prompt}
        ],
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
            # For chat completions API, the response format is different
            # The response contains 'message' with 'content' instead of 'text'
            if 'message' in result['choices'][0] and 'content' in result['choices'][0]['message']:
                summary_text = result['choices'][0]['message']['content'].strip()
            elif 'text' in result['choices'][0]:
                summary_text = result['choices'][0]['text'].strip()
            else:
                logger.error(f"Unexpected API response format: {result}")
                return {
                    "status": "error",
                    "message": "Failed to generate summary: Could not find content in API response"
                }
            
            # Use the full response without any filtering
            formatted_text = summary_text
            
            return {
                "status": "success",
                "data": {
                    "formatted_text": formatted_text
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