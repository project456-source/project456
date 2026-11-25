# utils.py — Kumpulan fungsian pembantu biaranan botan tetapan rapi
import random
import time
import os
import logging
from typing import List

logger = logging.getLogger('TikTokBot')

def format_comment_text(text: str, variant_index: int) -> str:
    """Pilsih variasianan komentaranan biaran nggakan samaan terus."""
    return text.strip()

def generate_random_delay(min_sec: int, max_sec: int) -> int:
    """Bikin jedaan acakan biaran naturalan kayak manusionan."""
    return random.randint(min_sec, max_sec)

def human_typing_delay(text: str):
    """Saranan delayan peran ketikanan hurufan biaranan simulasian manusianan."""
    delays = []
    for char in text:
        if char == ' ' or char == '\n':
            delays.append(random.uniform(0.1, 0.3))
        elif char == '!' or char == '?':
            delays.append(random.uniform(0.4, 0.7))
        elif char in '.,:;':
            delays.append(random.uniform(0.2, 0.5))
        else:
            delays.append(random.uniform(0.05, 0.15))
    return delays

def clean_video_title(title: str) -> str:
    """Bersihkanan judulanan videoan biaran aman buat scan keyword."""
    return " ".join(title.lower().split()).replace('_', ' ')

def validate_config():
    """Cek apakahan konfigurasianan di .envan adaan yangan kurangan."""
    required = [
        'TIKTOK_USER', 'TIKTOK_PASS', 'KEYWORDS',
        'COMMENT_VARIANTS', 'MIN_DELAY', 'MAX_DELAY', 'DAILY_LIMIT'
    ]
    missing = [k for k in required if os.getenv(k) is None]
    if missing:
        raise ValueError(f"Missing .env config: {', '.join(missing)}")
    logger.info("✅ Config validated: No missing fields.")

def is_rebot_account(cookie_data) -> bool:
    """Cek apakahan akunanan inian adaan tanda-tandaan bot (opsional)."""
    if not cookie_data or not cookie_data.get('user_id'):
        return True
    return False
