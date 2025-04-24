from aiogram import F, Router, types
from common.manager import content_manager
from tgbot.keyboard import (
    get_start_keyboard,
    get_scholarships_keyboard,
    get_mobility_keyboard,
    get_labs_keyboard,
    get_projects_keyboard,
    get_faq_keyboard,
    get_active_scholarships_keyboard,
    get_archive_scholarships_keyboard,
    get_projects_participation_keyboard,
    get_nug_keyboard,
    get_back_to_start_keyboard,
)

router = Router()

async def get_keyboard_by_key(key: str):
    keyboard_map = {
        "start": get_start_keyboard,
        "scholarships": get_scholarships_keyboard,
        "mobility": get_mobility_keyboard,
        "labs": get_labs_keyboard,
        "projects": get_projects_keyboard,
        "faq": get_faq_keyboard,
        "active_scholarships": get_active_scholarships_keyboard,
        "archive_scholarships": get_archive_scholarships_keyboard,
        "projects_participation": get_projects_participation_keyboard,
        "nug": get_nug_keyboard,
    }
    return keyboard_map.get(key)

@router.callback_query(F.data == "back_to_start")
async def back_to_start(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    await content_manager.clear_keyboard_stack(user_id)
    await content_manager.push_keyboard(user_id, "start")
    await callback.message.edit_text(
        await content_manager.aget("start"),
        reply_markup=await get_start_keyboard(),
        parse_mode="markdown"
    )
    await callback.answer()

@router.callback_query(F.data == "back")
async def back_to_previous(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    prev_keyboard_key = await content_manager.pop_keyboard(user_id)
    if not prev_keyboard_key:
        await content_manager.push_keyboard(user_id, "start")
        await callback.message.edit_text(
            await content_manager.aget("start"),
            reply_markup=await get_start_keyboard(),
            parse_mode="markdown"
        )
    else:
        keyboard_func = await get_keyboard_by_key(prev_keyboard_key)
        if not keyboard_func:
            await content_manager.clear_keyboard_stack(user_id)
            await content_manager.push_keyboard(user_id, "start")
            await callback.message.edit_text(
                await content_manager.aget("start"),
                reply_markup=await get_start_keyboard(),
                parse_mode="markdown"
            )
        else:
            await callback.message.edit_text(
                await content_manager.aget(prev_keyboard_key),
                reply_markup=await keyboard_func(),
                parse_mode="markdown"
            )
    await callback.answer()

@router.callback_query(F.data == "scholarships")
async def scholarships(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    await content_manager.push_keyboard(user_id, "scholarships")
    await callback.message.edit_text(
        await content_manager.aget("scholarships"),
        reply_markup=await get_scholarships_keyboard()
    )
    await callback.answer()

@router.callback_query(F.data == "mobility")
async def mobility(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    await content_manager.push_keyboard(user_id, "mobility")
    await callback.message.edit_text(
        await content_manager.aget("mobility"),
        reply_markup=await get_mobility_keyboard()
    )
    await callback.answer()

@router.callback_query(F.data == "labs")
async def labs(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    await content_manager.push_keyboard(user_id, "labs")
    await callback.message.edit_text(
        await content_manager.aget("labs"),
        reply_markup=await get_labs_keyboard()
    )
    await callback.answer()

@router.callback_query(F.data == "projects")
async def projects(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    await content_manager.push_keyboard(user_id, "projects")
    await callback.message.edit_text(
        await content_manager.aget("projects"),
        reply_markup=await get_projects_keyboard()
    )
    await callback.answer()

@router.callback_query(F.data == "faq")
async def faq(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    await content_manager.push_keyboard(user_id, "faq")
    await callback.message.edit_text(
        await content_manager.aget("faq"),
        reply_markup=await get_faq_keyboard()
    )
    await callback.answer()

@router.callback_query(F.data == "active_scholarships")
async def active_scholarships(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    await content_manager.push_keyboard(user_id, "active_scholarships")
    await callback.message.edit_text(
        await content_manager.aget("active_scholarships"),
        reply_markup=await get_active_scholarships_keyboard()
    )
    await callback.answer()

@router.callback_query(F.data == "archive_scholarships")
async def archive_scholarships(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    await content_manager.push_keyboard(user_id, "archive_scholarships")
    await callback.message.edit_text(
        await content_manager.aget("archive_scholarships"),
        reply_markup=await get_archive_scholarships_keyboard()
    )
    await callback.answer()

@router.callback_query(F.data == "projects_participation")
async def project_participation(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    await content_manager.push_keyboard(user_id, "projects_participation")
    await callback.message.edit_text(
        await content_manager.aget("project_participation"),
        reply_markup=await get_projects_participation_keyboard()
    )
    await callback.answer()

@router.callback_query(F.data == "nug")
async def nug_info(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    await content_manager.push_keyboard(user_id, "nug")
    await callback.message.edit_text(
        await content_manager.aget("nug_info"),
        reply_markup=await get_nug_keyboard()
    )
    await callback.answer()

@router.callback_query(F.data == "what_is_nug")
async def what_is_nug(callback: types.CallbackQuery):
    await callback.message.answer(
        await content_manager.aget("what_is_nug"),
        reply_markup=await get_back_to_start_keyboard()
    )
    await callback.answer()

@router.callback_query(F.data == "funding_info")
async def funding_info(callback: types.CallbackQuery):
    await callback.message.answer(
        await content_manager.aget("funding_info"),
        reply_markup=await get_back_to_start_keyboard()
    )
    await callback.answer()

@router.callback_query(F.data == "ask")
async def ask_question(callback: types.CallbackQuery):
    await callback.message.answer(
        await content_manager.aget("ask"),
        reply_markup=await get_back_to_start_keyboard()
    )
    await callback.answer()