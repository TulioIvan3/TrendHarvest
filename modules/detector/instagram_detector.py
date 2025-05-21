import requests
from typing import List, Dict
from shared.config import Config
from shared.logger import setup_logger

class InstagramDetector:
    def __init__(self):
        self.config = Config.load()
        self.logger = setup_logger('instagram_detector')
        self.base_url = "https://www.instagram.com/api/v1"

    def get_trending_hashtags(self) -> List[Dict]:
        """Captura hashtags em alta"""
        headers = {
            'User-Agent': 'Instagram 219.0.0.12.117 Android',
            'Cookie': f'sessionid={self.config.get("tiktok.session_id")}'
        }
        
        try:
            response = requests.get(
                f"{self.base_url}/tags/trending",
                headers=headers
            )
            return [{
                'name': tag['name'],
                'post_count': tag['media_count']
            } for tag in response.json()['tags'][:10]]
            
        except Exception as e:
            self.logger.error(f"Failed to fetch trends: {str(e)}", extra={'platform': 'instagram'})
            return []

    def get_popular_posts(self, hashtag: str) -> List[Dict]:
        """Busca posts populares por hashtag"""
        params = {
            'query': hashtag,
            'count': 5
        }
        
        response = requests.get(
            f"{self.base_url}/tags/search",
            params=params
        )
        
        return [{
            'id': post['id'],
            'caption': post['caption']['text'],
            'likes': post['like_count']
        } for post in response.json()['items']]