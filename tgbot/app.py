from aiogram import Bot, Dispatcher
from tgbot.settings import bot_settings
from tgbot.handler import message, callback

bot = Bot(token=bot_settings.token.get_secret_value())

def create_dispatcher():
    dp = Dispatcher()
    dp.include_router(message.router)
    dp.include_router(callback.router)

    return dp

dispatcher = create_dispatcher()
