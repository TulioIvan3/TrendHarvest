import asyncio
import argparse
from datetime import datetime
from shared.config import Config
from shared.logger import setup_logger
from modules.detector.instagram_detector import InstagramDetector
from modules.detector.tiktok_detector import TikTokDetector
from modules.content.instagram_creator import InstagramContentCreator
from modules.content.tiktok_creator import TikTokContentCreator
from modules.tasks.instagram_poster import InstagramPoster
from modules.tasks.tiktok_uploader import TikTokUploader

class TrendHarvestBot:
    def __init__(self):
        self.config = Config.load()
        self.logger = setup_logger('orchestrator')
        self.detectors = {
            'instagram': InstagramDetector(),
            'tiktok': TikTokDetector()
        }
        self.creators = {
            'instagram': InstagramContentCreator(),
            'tiktok': TikTokContentCreator()
        }
        self.publishers = {
            'instagram': InstagramPoster(),
            'tiktok': TikTokUploader()
        }

    async def run_cycle(self):
        self.logger.info("Starting detection cycle")
        
        # Detecção em paralelo
        trends = {}
        for platform, detector in self.detectors.items():
            trends[platform] = await self._safe_detect(detector)
        
        # Criação e publicação
        for platform, platform_trends in trends.items():
            for trend in platform_trends[:self.config.get('limits.max_posts')]:
                content = await self._create_content(platform, trend)
                if content:
                    await self._publish_content(platform, content)

    async def _safe_detect(self, detector):
        try:
            if isinstance(detector, InstagramDetector):
                return detector.get_trending_hashtags()
            return detector.get_trending_videos()
        except Exception as e:
            self.logger.error(f"Detection failed: {str(e)}")
            return []

    async def _create_content(self, platform, trend):
        creator = self.creators[platform]
        try:
            if platform == 'instagram':
                return creator.generate_post(trend)
            return creator.generate_script(trend)
        except Exception as e:
            self.logger.error(f"Content creation failed: {str(e)}")
            return None

    async def _publish_content(self, platform, content):
        publisher = self.publishers[platform]
        try:
            if platform == 'instagram':
                await publisher.post(content)
            else:
                await publisher.upload(content)
        except Exception as e:
            self.logger.error(f"Publishing failed: {str(e)}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--daemon", action="store_true")
    parser.add_argument("--interval", type=int, default=3600)
    args = parser.parse_args()

    bot = TrendHarvestBot()

    async def main():
        if args.daemon:
            while True:
                await bot.run_cycle()
                await asyncio.sleep(args.interval)
        else:
            await bot.run_cycle()

    asyncio.run(main())