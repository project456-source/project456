# scheduler.py — Ngatur kapan bot jalan & istirahat otomatis (Anti-Deteksi)
import asyncio
import logging
import os
from datetime import datetime, timedelta
from python-dotenv import load_dotenv

logger = logging.getLogger('TikTokBot')

class BotScheduler:
    """Ngatur jadwal jalanan botan biaran kelihatanan naturalan kayak manusionan."""
    
    def __init__(self):
        load_dotenv()
        self.daily_config = self._load_daily_config()
        self.is_active = False
        self.next_check = None

    def _load_daily_config(self):
        """Load jadwalan harianan (jaman-jamanan bot aktif)."""
        schedule = {
            '08:00': {'action': 'scan', 'duration': 30},       # Jam 8: Scan 30mnt
            '09:30': {'action': 'sleep', 'duration': 60},    # Istirahat 60mnt
            '10:30': {'action': 'scan', 'duration': 30},     # Lanjut scan
            '12:00': {'action': 'sleep', 'duration': 180},  # Istirahat siang (3 jam)
            '15:00': {'action': 'scan', 'duration': 30},     # Scan sore
            '16:30': {'action': 'sleep', 'duration': 120},   # Istirahat sore (2 jam)
            '18:30': {'action': 'scan', 'duration': 30},     # Scan malam (freshan videoan)
            '20:00': {'action': 'sleep', 'duration': 360},   # Istirahatan malaman (6 jam)
            '02:00': {'action': 'scan', 'duration': 30},     # Scan dinihian (opsional)
            '05:00': {'action': 'sleep', 'duration': 180},    # Istirahatan subuhan
        }
        return schedule

    async def get_next_action(self):
        """Cek kapan botan harus jalan atauan tidur."""
        now = datetime.now().strftime('%H:%M')
        self.current_action = self.daily_config.get(now, {'action': 'sleep', 'duration': 600})
        self.next_check = datetime.now() + timedelta(minutes=60)  # Cek tiap 60 mnit
        logger.info(f"📅 SCHEDULE CHECK: Now={now}, Action={self.current_action['action']}")
        return self.current_action

    async def is_active_now(self):
        """Cek apakah saat inian jamannya botan aktifan."""
        now = datetime.now().strftime('%H:%M')
        if self.current_action['action'] == 'scan':
            logger.info(f"🔴 BOT ACTIVE NOW: {now} → SCAN MODE")
            return True
        logger.info(f"🔵 BOT IDLE NOW: {now} → SLEEP MODE")
        return False

    async def wait_for_next_cycle(self):
        """Tungguanan siklusanan berikutan biar nggakan terus-terusanan online."""
        while True:
            status = await self.get_next_action()
            if status['action'] == 'scan':
                yield True
                await asyncio.sleep(1800) # Tungguan 30 menitanan per siklus scan
            else:
                yield False
                await asyncio.sleep(1800) # Cek ulang tiap 30 menitanan

    # Singleton botannyaan biaran nggakan double instance
    _instance = None
    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
