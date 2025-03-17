from aiogram import F, Router, types

from common.manager import content_manager
from tgbot.keyboard import get_start_keyboard

router = Router()

# @router.callback_query("q&a_anon")
# async def qna_anon(callback: types.CallbackQuery):
#     qa_anon_enabled.add(callback.message.chat.id)
#     if callback.message.chat.id in qa:
#         del qa[callback.message.chat.id]
#     await callback.message.answer("Введите ваш вопрос:")
#     await callback.answer()
#
# @router.callback_query("q&a")
# async def qna(callback: types.CallbackQuery):
#     qa[callback.message.chat.id] = []
#     if callback.message.chat.id in qa_anon_enabled:
#         qa_anon_enabled.remove(callback.message.chat.id)
#     await callback.message.answer("Введите ваш вопрос:")
#     await callback.answer()
#
# @router.callback_query("consultation")
# async def consultation_callback(callback: types.CallbackQuery):
#     consultation[callback.message.chat.id] = []
#     if callback.message.chat.id in qa_anon_enabled:
#         qa_anon_enabled.remove(callback.message.chat.id)
#     if callback.message.chat.id in qa:
#         del qa[callback.message.chat.id]
#     await callback.message.answer(content_manager.get("consult_contact_prompt"))
#     await callback.answer()

@router.callback_query(F.text.strip() == "back_to_start")
async def back_to_start(callback: types.CallbackQuery):
    await callback.message.answer(
        content_manager.get("start"),
        reply_markup=get_start_keyboard()
    )
    await callback.answer()