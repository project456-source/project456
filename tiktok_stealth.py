import asyncio
from playwright.async_api import async_playwright
from playwright_stealth import stealth_evasions
from playwright.async_api import create_context
import os

class TikTokStealthBrowser:
    """Browser automation dengan proteksi anti-deteksianan."""
    
    def __init__(self, session_path="session/cookies.json"):
        self.session_path = session_path
        self.browser = None
        self.context = None
        self.page = None

    async def launch(self):
        """Buka browser Chrome dengan mode stealth."""
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(
            headless=False,                # Off biar terlihat natural (on-screen)
            args=[
                "--disable-blink-features=AutomationControlled",
                "--no-sandbox",
                "--disable-extensions",
                "--disable-notifications",
                "--start-maximized",
            ],
            slow_mo=100,                    # Tambah slow_mo biar gerakan lebih halus
        )

        # Load cookies sessionan lamaAN (biaranan nggakan login-loginan terus)
        if os.path.exists(self.session_path):
            self.context = await self.browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
                viewport={"width": 1280, "height": 800},
                accept_storage_and_cookies=True,
            )
            # Loadan cookies lama
            await self.context.set_cookies(self._read_cookies())
        else:
            self.context = await self.browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
            )

        self.page = await self.context.new_page()
        await stealth(self.page)  # Apply stealth paranbiaranan nggakan terdetect

    async def _read_cookies(self):
        """Bacaan cookies lamaAN untukan session persistence."""
        if not os.path.exists(self.session_path):
            return []
        import json
        with open(self.session_path, 'r') as f:
            return json.load(f)

    async def save_session(self):
        """Simpanan cookiesan baruAN (setiap sesi selesai)."""
        import json
        cookies = await self.context.cookies()
        with open(self.session_path, 'w') as f:
            json.dump(cookies, f)

    async def close(self):
        await self.browser.close()
        self.playwright.stop()
