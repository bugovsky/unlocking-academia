import os
import logging
import asyncio

from aiogram.filters import Command
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types

from tgbot.dialogs import dialog_options

load_dotenv()
TOKEN = os.getenv("TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher()

qaAnonEnabledForChatId = set()
qa = {}          # Словарь: chat_id -> list[str]
consultation = {}  # Словарь: chat_id -> list[str]


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    kb = [
        [types.KeyboardButton(text="💸 Стипендии")],
        [types.KeyboardButton(text="🚗 Программы международной мобильности")],
        [types.KeyboardButton(text="🔬 Лаборатории")],
        [types.KeyboardButton(text="💼 Проекты и НУГи")],
        [types.KeyboardButton(text="❓ Часто задаваемые вопросы")],
        [types.KeyboardButton(text="👥 Индивидуальная консультация")],
        [types.KeyboardButton(text="📩 Отправить нам вопрос")],
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

    text = (
        "Привет! \n"
        "Это телеграм-бот проекта Unlocking Academia, нацеленный на помощь студентам желающих развиваться в научной сфере.\n"
        "Здесь ты можешь узнать о возможностях, которые предоставляются студентам: стипендиях, программах мобильности и т. д. \n"
        "Чтобы начать, выбери один их пунктов меню"
    )
    await message.answer(text, reply_markup=keyboard)

@dp.message()
async def handle_message(message: types.Message):
    chat_id = message.chat.id
    text = message.text.strip()

    for option in dialog_options:
        if text == option.button_text or text == option.command_text:
            await option.action(message)
            qaAnonEnabledForChatId.discard(chat_id)
            qa.pop(chat_id, None)
            consultation.pop(chat_id, None)
            return

    if chat_id in qaAnonEnabledForChatId:
        data = [text]
        qaAnonEnabledForChatId.discard(chat_id)
        qa.pop(chat_id, None)
        await message.answer("Спасибо! Ваш вопрос записан.")
        return

    if chat_id in qa:
        if len(qa[chat_id]) == 0:
            qa[chat_id].append(text)
            await message.answer("А теперь, оставьте свой контакт, пожалуйста:")
            return
        else:
            qa[chat_id].append(text)
            data = qa[chat_id]
            await message.answer("Спасибо! Ваш вопрос записан. Скоро с вами свяжутся:)")
            qa.pop(chat_id, None)
            qaAnonEnabledForChatId.discard(chat_id)
            return

    if chat_id in consultation:
        if len(consultation[chat_id]) == 0:
            consultation[chat_id].append(text)
            await message.answer("С кем из экспертов вы хотели бы проконсультироваться? Можете также добавить подробностей о чем конкретно хотелось бы поговорить")
            return
        else:
            consultation[chat_id].append(text)
            data = consultation[chat_id]
            await message.answer("Ваша запись зафиксирована. Спасибо! Дополнительная информация о встрече придет от эксперта в ближайшее время:)")
            consultation.pop(chat_id, None)
            qaAnonEnabledForChatId.discard(chat_id)
            qa.pop(chat_id, None)
            return

    await message.answer("Я не знаю такой команды :(")

@dp.callback_query(lambda c: c.data)
async def process_callback(callback_query: types.CallbackQuery):
    chat_id = callback_query.message.chat.id
    data = callback_query.data

    if data == "q&a_anon":
        qaAnonEnabledForChatId.add(chat_id)
        qa.pop(chat_id, None)
        await bot.send_message(chat_id, "Введите ваш вопрос:")
    elif data == "q&a":
        qa[chat_id] = []
        qaAnonEnabledForChatId.discard(chat_id)
        await bot.send_message(chat_id, "Введите ваш вопрос:")
    elif data == "consultation":
        consultation[chat_id] = []
        qaAnonEnabledForChatId.discard(chat_id)
        qa.pop(chat_id, None)
        await bot.send_message(chat_id, "Для начала, отправьте сюда, пожалуйста, свой контакт (электронную почту, телеграм и т.п.)")
    await bot.answer_callback_query(callback_query.id)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
