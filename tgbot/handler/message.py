from aiogram import Router, types
from aiogram.filters.command import Command

from common.manager import content_manager
from tgbot.keyboard import get_start_keyboard

router = Router()

@router.message(Command("start"))
async def start_command(message: types.Message):
    user_id = message.from_user.id
    await content_manager.clear_keyboard_stack(user_id)
    await content_manager.push_keyboard(user_id, "start")
    await message.answer(
        await content_manager.aget("start"),
        reply_markup=await get_start_keyboard(),
        parse_mode="markdown"
    )

@router.message()
async def handle_message(message: types.Message):
    await message.answer(await content_manager.aget("unknown_command"))