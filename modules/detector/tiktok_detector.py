import requests
from typing import List, Dict
from shared.config import Config
from shared.logger import setup_logger

class TikTokDetector:
    def __init__(self):
        self.config = Config.load()
        self.logger = setup_logger('tiktok_detector')
        self.trending_url = "https://www.tiktok.com/api/recommend/item_list/"

    def get_trending_videos(self) -> List[Dict]:
        """Captura vídeos em alta no TikTok"""
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Cookie': f'sessionid={self.config.get("tiktok.session_id")}'
        }
        
        try:
            response = requests.get(
                self.trending_url,
                headers=headers
            )
            return [{
                'id': item['id'],
                'desc': item['desc'],
                'views': item['stats']['playCount'],
                'sound': item['music']['title']
            } for item in response.json()['itemList'][:10]]
            
        except Exception as e:
            self.logger.error(f"Failed to fetch trends: {str(e)}", extra={'platform': 'tiktok'})
            return []