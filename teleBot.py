from telegram.ext import Application
import asyncio
from telegram.error import RetryAfter
import os

API_TOKEN = os.getenv('API_TOKEN')
CHAT_ID = os.getenv('CHAT_ID')

def send_tele_message(message: str, chat_id: str = CHAT_ID) -> None:
    loop = asyncio.get_event_loop()
    if loop.is_closed():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    loop.run_until_complete(send_tele_message_async(message, chat_id))


async def send_tele_message_async(message: str, chat_id: str) -> None:
    try:
        await application.bot.send_message(chat_id=chat_id, text=message)
    except RetryAfter as e:
        await asyncio.sleep(e.retry_after)

application = Application.builder().token(API_TOKEN).build()
