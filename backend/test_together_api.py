import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get API key from environment
api_key = os.getenv('TOGETHER_API_KEY')
if not api_key:
    print("Error: TOGETHER_API_KEY not found in environment variables")
    exit(1)

# Test the chat completions endpoint
def test_chat_completions():
    url = "https://api.together.xyz/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "deepseek-ai/DeepSeek-R1-Distill-Llama-70B-free",
        "messages": [
            {"role": "user", "content": "Hello, how are you?"}
        ],
        "max_tokens": 100,
        "temperature": 0.7
    }
    
    try:
        print("Testing chat completions endpoint...")
        response = requests.post(url, headers=headers, json=data, timeout=30)
        print(f"Status code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("Success! Response:")
            print(json.dumps(result, indent=2))
            return True
        else:
            print(f"Error response: {response.text}")
            return False
    except Exception as e:
        print(f"Exception occurred: {str(e)}")
        return False

# Test the regular completions endpoint
def test_completions():
    url = "https://api.together.xyz/v1/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "deepseek-ai/DeepSeek-R1-Distill-Llama-70B-free",
        "prompt": "Hello, how are you?",
        "max_tokens": 100,
        "temperature": 0.7
    }
    
    try:
        print("\nTesting completions endpoint...")
        response = requests.post(url, headers=headers, json=data, timeout=30)
        print(f"Status code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("Success! Response:")
            print(json.dumps(result, indent=2))
            return True
        else:
            print(f"Error response: {response.text}")
            return False
    except Exception as e:
        print(f"Exception occurred: {str(e)}")
        return False

if __name__ == "__main__":
    print("Testing Together AI API with DeepSeek model...\n")
    chat_result = test_chat_completions()
    completions_result = test_completions()
    
    print("\nResults summary:")
    print(f"Chat completions endpoint: {'SUCCESS' if chat_result else 'FAILED'}")
    print(f"Completions endpoint: {'SUCCESS' if completions_result else 'FAILED'}")
    
    if chat_result and not completions_result:
        print("\nDiagnosis: The DeepSeek model requires the chat completions endpoint.")
        print("Solution: Update TOGETHER_API_BASE_URL in config.py to 'https://api.together.xyz/v1/chat/completions'")
    elif not chat_result and not completions_result:
        print("\nDiagnosis: Both endpoints failed. Check your API key and internet connection.")
    elif completions_result:
        print("\nDiagnosis: The completions endpoint works fine. The issue might be elsewhere.")