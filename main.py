from bot import TikTokBot
import asyncio
import logging

async def main():
    bot = TikTokBot()
    await bot.run()

if __name__ == "__main__":
    import sys
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nBot stopped manually.")
        sys.exit(0)
