from aiogram import F, Router, types

from common.manager import content_manager
from tgbot.keyboard import get_start_keyboard

router = Router()

@router.callback_query(F.text.strip() == "back_to_start")
async def back_to_start(callback: types.CallbackQuery):
    await callback.message.answer(
        content_manager.get("start"),
        reply_markup=get_start_keyboard()
    )
    await callback.answer()