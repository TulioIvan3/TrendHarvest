import os
from dotenv import load_dotenv
from typing import Dict, Any

class Config:
    _instance = None
    
    def __init__(self):
        load_dotenv()
        self.settings = {
            'instagram': {
                'username': os.getenv('INSTAGRAM_USER'),
                'password': os.getenv('INSTAGRAM_PASS')
            },
            'tiktok': {
                'session_id': os.getenv('TIKTOK_SESSION_ID')
            },
            'limits': {
                'max_posts': int(os.getenv('MAX_POSTS_PER_DAY', 5)),
                'delay': int(os.getenv('REQUEST_DELAY', 15))
            },
            'monetization': {
                'affiliate_link': os.getenv('AFFILIATE_LINK'),
                'cpa_link': os.getenv('CPA_LINK')
            },
            'database': {
                'mongo_uri': os.getenv('MONGO_URI')
            }
        }

    @classmethod
    def load(cls) -> 'Config':
        if not cls._instance:
            cls._instance = cls()
        return cls._instance

    def get(self, key: str, default: Any = None) -> Any:
        keys = key.split('.')
        value = self.settings
        for k in keys:
            value = value.get(k, {})
        return value if value != {} else default