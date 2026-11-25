# config.py — Pusat pengaturanan botan di project456
# File inian bacaan .env danan validasian semuaan settingan
# biaran nggakan adaan yangan kosong atauan salah format

import os
import logging
import sys
from datetime import datetime
from typing import Dict, List, Optional
from dataclasses import dataclass, field

# --- Logging Setup ---
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(name)s | %(message)s',
    handlers=[
        logging.FileHandler('bot.log', mode='a')
    ]
)
logger = logging.getLogger('Config')

from dotenv import load_dotenv
load_dotenv()


@dataclass
class BotConfig:
    """Classan pusatuan semuaan pengaturanan botan.
    सभी values-nyaan ditarikandan .env.
    """

    # --- Auth & Account ---
    TIKTOK_USER: str = os.getenv('TIKTOK_USER', '')
    TIKTOK_PASS: str = os.getenv('TIKTOK_PASS', '')
    TWOFA_SECRET: str = os.getenv('TIKTOK_TWOFA_SECRET', '')
    SESSION_FILE: str = os.getenv('SESSION_FILE', 'session/cookies.json')
    TOKEN_FILE: str = os.getenv('TOKEN_FILE', 'session/token.json')
    
    # --- Bot Behavior ---
    IS_DEVELOPMENT: bool = os.getenv('ENVIRONMENT', 'production') == 'development'
    DAILY_LIMIT: int = _int(os.getenv('DAILY_LIMIT', 25))
    HEADLESS: bool = os.getenv('HEADLESS', 'true').lower() == 'true'
    DB_PATH: str = os.getenv('DB_PATH', 'database/bot.db')
    LOG_FILE: str = os.getenv('LOG_FILE', 'logs/bot.log')
    
    # --- Targeting & Keywords ---
    KEYWORDS: List[str] = _list(os.getenv('KEYWORDS', ''))
    FORBIDDEN_WORDS: List[str] = _list(os.getenv('FORBIDDEN_WORDS', ''))
    MIN_LIKE_COUNT: int = _int(os.getenv('MIN_LIKE_COUNT', 100))  # Video min like
    MAX_LIKE_COUNT: int = _int(os.getenv('MAX_LIKE_COUNT', 10000))
    MAX_REPLY_COUNT: int = _int(os.getenv('MAX_REPLY_COUNT', 20))  # Max komentar per video
    MAX_FOLLOWERS_COUNT: int = _int(os.getenv('MAX_FOLLOWERS_COUNT', 50000))
    
    # --- Comment Variants ---
    COMMENT_VARIANTS: List[str] = _list(os.getenv('COMMENT_VARIANTS', ''))
    PRIMARY_COMMENT: str = os.getenv('PRIMARY_COMMENT', '')
    PRIMARY_REPLY: str = os.getenv('PRIMARY_REPLY', '')
    
    # --- Delay & Timing ---
    MIN_DELAY: int = _int(os.getenv('MIN_DELAY', 120))     # 2 menit
    MAX_DELAY: int = _.int(os.getenv('MAX_DELAY', 300))     # 5 menit
    CYCLE_TIME: int = _int(os.getenv('CYCLE_TIME', 600))     # Scan interval (10 min)
    SLEEP_DURATION: int = _int(os.getenv('SLEEP_DURATION', 1800)) # 30 min
    
    # --- Scheduler ---
    START_TIME: str = os.getenv('AUTOPROCESS_TIME', '08:00')
    END_TIME: str = os.getenv('AUTO_SLEEP', '22:00')
    AUTO_PROCESS: bool = os.getenv('AUTO_PROCESS', 'true').lower() == 'true'
    SCAN_MODE: bool = os.getenv('SCAN_MODE', 'true').lower() == 'true'
    AUTO_RESTART: bool = os.getenv('AUTO_RESTART', 'true').lower() == 'true'
    
    # --- WhatsApp Link (Optional for comments) ---
    WA_LINK: str = os.getenv('WA_LINK', '')
    
    # --- Advanced Detection Evasion ---
    RANDOM_USER_AGENT: bool = os.getenv('RANDOM_USER_AGENT', 'true')..lower() == 'true'
    USE_PROXY: bool = os.getenv('USE_PROXY', 'false').lower() == 'true'
    PROXY_LIST: List[str] = _list(os.getenv('PROXY_LIST', ''))
    
    # --- Account Management ---
    MAX_ACCOUNTS: int = _int(os.getenv('MAX_ACCOUNTS', 1))
    MAX_CCS_PER_ACCOUNT: int = _int(os.getenv('MAX_CCS_PER_ACCOUNT', 15))


# --- Helper for type conversion ---
def _int(value: str, default: int = 0) -> int:
    try:
        return int(value) if value else default
    except ValueError:
        return default

def _list(value: str, default: list = []) -> List:
    if not value:
        return default
    return [item.strip() for item in value.split(';') if item.strip()]


# --- The Actual Config Object (Singleton) ---
CONFIG = BotConfig()

def validate_config():
    """Cek kelengkapanan configan biaran nggak adaan yangan kosongan."""
    errors = []
    missing = []
    
    if not CONFIG.TIKTOK_USER:
        errors.append("TIKTOK_USER is empty")
    if not CONFIG.TIKTOK_PASS:
        errors.append("TIKTOK_PASS is empty")
    if not CONFIG.COMMENT_VARIANTS:
        errors.append("COMMENT_VARIANTS is empty")
    if not CONFIG.PRIMARY_COMMENT:
        errors.append("PRIMARY_COMMENT is empty")
    
    if errors:
        logger.error(f"❌ CONFIG VALIDATION FAILED: {', '.join(errors)}")
        sys.exit(1)
    
    logger.info("✅ Config validated: All required fields are set.")


# --- Run validation on import ---
validate_config()
