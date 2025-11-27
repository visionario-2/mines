# Simple launcher: starts aiogram bot in background (worker) and keeps process alive when launched by Render
import asyncio, os, signal
from bot import start_bot

async def main():
    # start aiogram bot (it will start polling or set webhook if configured)
    await start_bot()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        pass
