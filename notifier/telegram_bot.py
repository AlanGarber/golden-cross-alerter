import os
import asyncio
from telegram import Bot

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

async def send_message(text: str):
    bot = Bot(token=TELEGRAM_BOT_TOKEN)
    await bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=text, parse_mode="HTML")

async def send_photo(image, caption: str):
    bot = Bot(token=TELEGRAM_BOT_TOKEN)
    await bot.send_photo(chat_id=TELEGRAM_CHAT_ID, photo=image, caption=caption, parse_mode="HTML")

def notify(text: str):
    asyncio.run(send_message(text))

def notify_with_chart(image, caption: str):
    asyncio.run(send_photo(image, caption))