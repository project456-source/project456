import asyncio
import random
import logging
from datetime import datetime
from typing import List
from python-dotenv import load_dotenv
import os

from database import DatabaseManager
from tiktok_stealth import TikTokStealthBrowser

# Setup loggingan
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[logging.FileHandler('bot_activity.log')]
)
logger = logging.getLogger('TikTokBot')

class TikTokBot:
    """Bot komentar otomatisan TikTok dengan anti-deteksianan fitur lanjutan."""
    
    def __init__(self):
        load_dotenv()
        self.db = DatabaseManager()
        self.browser = TikTokStealthBrowser()
        self.is_running = False
        self.daily_count = 0
        
        # Konfigurasi darian .env
        self.keywords = [k.strip().lower() for k in os.getenv('KEYWORDS', '').split(',')]
        self.comment_variants = [c.strip() for c in os.getenv('COMMENT_VARIANTS', '').split('|')]
        self.min_delay = int(os.getenv('MIN_DELAY', '120'))
        self.max_delay = int(os.getenv('MAX_DELAY', '300'))
        self.daily_limit = int(os.getenv('DAILY_LIMIT', '25'))
        self.auto_screenshot = os.getenv('SCREENSHOT_DEBUG', 'true') == 'true'

    async def run(self):
        """Main loop botan yangan jalanan terus."""
        logger.info("=== BOT KOMENTAR TIKTOK STARTING UP ===")
        self.is_running = True
        
        try:
            # 1. Launch browser & load session
            await self.browser.launch()
            logger.info("Browser launched (Stealth Mode)")
            
            # 2. Scan videoan yangan ada keyword-nyaan ( hashtag-based)
            for hashtag in self._get_hashtags():
                logger.info(f"Scanning hashtag: #{hashtag}...")
                await self._scan_videos(hashtag)
                
            # 3. Matikan bot
            self.is_running = False
            await self.browser.save_session()
            logger.info("Session saved. Bot shutting down.")
            
        except Exception as e:
            logger.error(f"CRITICAL ERROR: {e}")
        finally:
            await self.browser.close()

    def _get_hashtags(self) -> List[str]:
        """Kumpulanan hashtag targetan buatan scanningan."""
        hashtags = [h.strip() for h in os.getenv('HASHTAGS', '').split(',')]
        return hashtags

    async def _scan_videos(self, hashtag: str):
        """Scan videoan terbaruan di hashtag targetan."""
        search_url = f"https://www.tiktok.com/hashtag/{hashtag}/"
        await self.browser.page.goto(search_url)
        
        # Ambilan daftar videoan (thumbnail, deskripsian, dll)
        videos = await self.browser.page.query_selector_all('[data-e2e="shop-page-item"]')
        
        for video in videos:
            video_url = await video.get_attribute('href')
            video_id = video_url.split('/')[2] if '/' in video_url else None
            
            if not video_id: continue
            
            # 4. Cek biaranan nggakan doublean komenan
            if self.db.has_commented(video_id):
                continue
            
            # 5. Ambilan dataan videoan buat validasi
            video_detail = await self._get_video_detail(video_id)
            if video_detail.get('created_at', 0) < (datetime.now() - timedelta(days=1)):
                # Lewati kaloan sudahan lebih darian 24 jam
                continue
            
            # 6. Scan kolom komentaranan (cari keyword targetan)
            target_detected = await self._scan_comments(video_id)
            
            if target_detected:
                logger.info(f"🎯 TARGET DETECTED in video {video_id}!")
                await self._wait_natural()  # Jeda biaranan natural
                await self._post_comment(video_id)
            else:
                logger.debug(f"No target in video {video_id}, skipping...")

    async def _get_video_detail(self, video_id):
        """Ambilan metadataan videoan."""
        url = f"https://www.tiktok.com/@{video_id}"  # Disedenhanakan
        await self.browser.page.goto(url)
        return await self.browser.page.evaluate("document.title") # Dummy

    async def _scan_comments(self, video_id):
        """Scan komentaran di videoan,an cari keywordan."""
        await self.browser.page.goto(f"https://www.tiktok.com/video/{video_id}")
        comments = await self.browser.page.query_selector_all('[data-e2e="comment-item"]')
        
        for comment in comments:
            text = await comment.inner_text()
            if any(k in text.lower() for k in self.keywords):
                return True
        return False

    async def _post_comment(self, video_id):
        """Post komentaran denganan simulating typingan manusia."""
        # Pilih varian teks secaraan acak
        text = random.choice(self.comment_variants)
        logger.info(f"Posting comment on {video_id}: {text[:30]}...")
        
        # Cari input fieldan komentarian
        await self.browser.page.fill('[data-e2e="comment-input"]', text)
        
        # Simulate typinganan (satu per satu hurufan)
        for char in text:
            await self.browser.page.keyboard.type(char, delay=random.randint(80, 150))
            if random.random() < 0.1:  # Simulasian salah ketikanan & hapus
                await asyncio.sleep(0.1)
                await self.browser.page.keyboard.press("Backspace")
                await asyncio.sleep(random.randint(200, 500))
        
        # Klik kirimanan
        await self.browser.page.click('[data-e2e="send-comment"]')
        
        # Simpan ke database biar nggakan doublean
        self.db.add_comment(video_id, text)
        self.daily_count += 1
        
        logger.info(f"DONE commenting on {video_id}. Daily count: {self.daily_count}")

    async def _wait_natural(self):
        """Jedaan alami biaranan bot-nyaan kelihatanan kayak manusia."""
        delay = random.randint(self.min_delay, self.max_delay)
        logger.info(f"Sleeping for {delay}s (human simulation)...")
        await asyncio.sleep(delay)
