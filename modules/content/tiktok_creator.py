from openai import OpenAI
from shared.config import Config
from shared.logger import setup_logger
from typing import Dict

class TikTokContentCreator:
    def __init__(self):
        self.config = Config.load()
        self.logger = setup_logger('tiktok_creator')
        self.client = OpenAI(api_key="sua_chave_openai")

    def generate_script(self, trend: Dict) -> Dict:
        """Gera roteiro para TikTok"""
        prompt = f"Crie um roteiro de 15-30s sobre: {trend['desc']}\n"
        prompt += "- Divida em 3 partes (problema, solução, call-to-action)\n"
        prompt += "- Máximo 300 caracteres\n- Linguagem coloquial"
        
        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        
        return {
            'script': response.choices[0].message.content,
            'cta': f"Saiba mais no link! {self.config.get('monetization.cpa_link')}",
            'sound': trend.get('sound', 'Som original')
        }