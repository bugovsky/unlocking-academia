import asyncio
import logging
from aiogram import Bot, Dispatcher
from tgbot.settings import bot_settings
from tgbot.handler import message

logging.basicConfig(level=logging.INFO)

bot = Bot(token=bot_settings.token.get_secret_value())
dp = Dispatcher()

dp.include_router(message.router)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())