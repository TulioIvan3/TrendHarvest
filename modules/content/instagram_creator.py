# ADICIONE ESTA LINHA NO TOPO DO ARQUIVO
from typing import List, Dict  # Importação obrigatória

from openai import OpenAI
from shared.config import Config
from shared.logger import setup_logger

class InstagramContentCreator:
    def __init__(self):
        self.config = Config.load()
        self.logger = setup_logger('instagram_creator')
        self.client = OpenAI(api_key='sua_chave_openai')

    def generate_post(self, trend: Dict) -> Dict:
        """Gera post otimizado para Instagram"""
        prompt = f"Crie um post para Instagram sobre: {trend['desc']}\n"
        prompt += "- Texto curto (até 2200 caracteres)\n- Inclua 3-5 hashtags\n"
        prompt += "- Linguagem informal e engajadora"
        
        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        
        return {
            'text': response.choices[0].message.content,
            'hashtags': self._extract_hashtags(response.choices[0].message.content),
            'cta': f"Link na bio! 👆 {self.config.get('monetization.affiliate_link')}"
        }

    def _extract_hashtags(self, text: str) -> List[str]:  # Agora funcionará
        return [word[1:] for word in text.split() if word.startswith('#')]