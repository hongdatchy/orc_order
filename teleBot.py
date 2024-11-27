from telegram.ext import Application
import asyncio
from telegram.error import RetryAfter


# Đặt API Token của bot (lấy từ BotFather)
API_TOKEN = '8102292132:AAGikwNjpUCOwMYK8RipiUzJtYa_SIocgrE'
CHAT_ID = "-1002439069635"

# Hàm gửi message
def send_tele_message(message: str, chat_id: str = CHAT_ID) -> None:
    loop = asyncio.get_event_loop()
    if loop.is_closed():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    # Sử dụng vòng lặp mới
    loop.run_until_complete(send_tele_message_async(message, chat_id))


async def send_tele_message_async(message: str, chat_id: str) -> None:
    try:
        await application.bot.send_message(chat_id=chat_id, text=message)
    except RetryAfter as e:
        await asyncio.sleep(e.retry_after)  # Delay theo thời gian quy định bởi Telegram

# Khởi tạo Application
application = Application.builder().token(API_TOKEN).build()
