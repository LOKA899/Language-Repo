
import os
import sys
import json
import httpx
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_token(token=None):
    """Test if the provided token is valid with the League of Kingdoms API."""
    if token is None:
        token = os.getenv("AUTH_TOKEN")
        if not token:
            logger.error("No AUTH_TOKEN found. Please provide a token as an argument or set it in the environment.")
            return False
    
    logger.info(f"Testing token validity...")
    
    try:
        client = httpx.Client(
            headers={
                'Accept': '*/*',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept-Language': 'en-US,en;q=0.9',
                'Origin': 'https://play.leagueofkingdoms.com',
                'Referer': 'https://play.leagueofkingdoms.com/',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/114.0',
                'X-Access-Token': token
            }
        )
        
        device_info = {
            "deviceInfo": {
                "build": "global",
                "OS": "Windows 10",
                "country": "USA",
                "language": "English",
                "bundle": "",
                "version": "1.1694.152.229",
                "platform": "web",
                "pushId": ""
            }
        }
        
        response = client.post(
            'https://lok-api-live.leagueofkingdoms.com/api/auth/connect', 
            data={'json': json.dumps(device_info)}
        )
        
        result = response.json()
        
        if result.get('result') == True and 'token' in result:
            logger.info("Token is valid! Successfully connected to LOK API.")
            logger.info(f"Response: {json.dumps(result, indent=2)}")
            return True
        else:
            logger.error(f"Token is invalid or expired. Response: {json.dumps(result, indent=2)}")
            return False
            
    except Exception as e:
        logger.error(f"Error testing token: {str(e)}")
        return False

if __name__ == "__main__":
    token = sys.argv[1] if len(sys.argv) > 1 else None
    test_token(token)
