from aiogram import F, Router, types
from aiogram.filters.command import Command

from common.manager import content_manager, KEYBOARD_INFO
from tgbot.keyboard import (
    get_start_keyboard,
    get_scholarship_keyboard,
    get_mobility_keyboard,
    get_labs_keyboard,
    get_projects_keyboard,
    get_faq_keyboard,
    get_active_scholarships_keyboard,
    get_archive_scholarships_keyboard,
    get_projects_participation_keyboard,
    get_nug_keyboard,
)

router = Router()

async def get_keyboard_by_key(key: str):
    """Возвращает функцию клавиатуры по её ключу."""
    keyboard_map = {
        "start": get_start_keyboard,
        "scholarship": get_scholarship_keyboard,
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

@router.message(F.text.strip() == "💸 Стипендии")
async def scholarships(message: types.Message):
    user_id = message.from_user.id
    await content_manager.push_keyboard(user_id, "scholarship")
    await message.answer(
        await content_manager.aget("scholarships"),
        reply_markup=await get_scholarship_keyboard()
    )

@router.message(F.text.strip() == "🚗 Программы международной мобильности")
async def mobility(message: types.Message):
    user_id = message.from_user.id
    buttons = await content_manager.aget_buttons("mobility")
    for button in buttons:
        if button["text"] == message.text.strip() and button["url"]:
            await message.answer(f"Вы выбрали '{button['text']}'. Перейти: {button['url']}")
            return
    await content_manager.push_keyboard(user_id, "mobility")
    await message.answer(
        await content_manager.aget("mobility"),
        reply_markup=await get_mobility_keyboard()
    )

@router.message(F.text.strip() == "🔬 Лаборатории")
async def labs(message: types.Message):
    user_id = message.from_user.id
    buttons = await content_manager.aget_buttons("labs")
    for button in buttons:
        if button["text"] == message.text.strip() and button["url"]:
            await message.answer(f"Вы выбрали '{button['text']}'. Перейти: {button['url']}")
            return
    await content_manager.push_keyboard(user_id, "labs")
    await message.answer(
        await content_manager.aget("labs"),
        reply_markup=await get_labs_keyboard()
    )

@router.message(F.text.strip() == "💼 Проекты и НУГи")
async def projects(message: types.Message):
    user_id = message.from_user.id
    await content_manager.push_keyboard(user_id, "projects")
    await message.answer(
        await content_manager.aget("projects"),
        reply_markup=await get_projects_keyboard()
    )

@router.message(F.text.strip() == "❓ Часто задаваемые вопросы")
async def faq(message: types.Message):
    user_id = message.from_user.id
    await content_manager.push_keyboard(user_id, "faq")
    await message.answer(
        await content_manager.aget("faq"),
        reply_markup=await get_faq_keyboard()
    )

@router.message(F.text.strip() == "Активные программы стипендий")
async def active_scholarships(message: types.Message):
    user_id = message.from_user.id
    buttons = await content_manager.aget_buttons("active_scholarships")
    for button in buttons:
        if button["text"] == message.text.strip() and button["url"]:
            await message.answer(f"Вы выбрали '{button['text']}'. Перейти: {button['url']}")
            return
    await content_manager.push_keyboard(user_id, "active_scholarships")
    await message.answer(
        await content_manager.aget("active_scholarships"),
        reply_markup=await get_active_scholarships_keyboard()
    )

@router.message(F.text.strip() == "Архив стипендиальных программ")
async def archive_scholarships(message: types.Message):
    user_id = message.from_user.id
    buttons = await content_manager.aget_buttons("archive_scholarships")
    for button in buttons:
        if button["text"] == message.text.strip() and button["url"]:
            await message.answer(f"Вы выбрали '{button['text']}'. Перейти: {button['url']}")
            return
    await content_manager.push_keyboard(user_id, "archive_scholarships")
    await message.answer(
        await content_manager.aget("archive_scholarships"),
        reply_markup=await get_archive_scholarships_keyboard()
    )

@router.message(F.text.strip() == "Участие в проектах")
async def project_participation(message: types.Message):
    user_id = message.from_user.id
    buttons = await content_manager.aget_buttons("projects_participation")
    for button in buttons:
        if button["text"] == message.text.strip() and button["url"]:
            await message.answer(f"Вы выбрали '{button['text']}'. Перейти: {button['url']}")
            return
    await content_manager.push_keyboard(user_id, "projects_participation")
    await message.answer(
        await content_manager.aget("project_participation"),
        reply_markup=await get_projects_participation_keyboard()
    )

@router.message(F.text.strip() == "Про научно-учебные группы")
async def nug_info(message: types.Message):
    user_id = message.from_user.id
    buttons = await content_manager.aget_buttons("nug")
    for button in buttons:
        if button["text"] == message.text.strip() and button["url"]:
            await message.answer(f"Вы выбрали '{button['text']}'. Перейти: {button['url']}")
            return
    await content_manager.push_keyboard(user_id, "nug")
    await message.answer(
        await content_manager.aget("nug_info"),
        reply_markup=await get_nug_keyboard()
    )

@router.message(F.text.strip() == "Что такое НУГ?")
async def what_is_nug(message: types.Message):
    await message.answer(await content_manager.aget("what_is_nug"))

@router.message(F.text.strip() == "Как получить финансирование?")
async def funding_info(message: types.Message):
    await message.answer(await content_manager.aget("funding_info"))

@router.message(F.text.strip() == "Назад")
async def back_to_previous(message: types.Message):
    user_id = message.from_user.id
    await message.delete()  # Удаляем текущее сообщение
    prev_keyboard_key = await content_manager.pop_keyboard(user_id)
    if not prev_keyboard_key:
        await content_manager.push_keyboard(user_id, "start")
        await message.answer(
            await content_manager.aget("start"),
            reply_markup=await get_start_keyboard(),
            parse_mode="markdown"
        )
        return
    keyboard_func = await get_keyboard_by_key(prev_keyboard_key)
    if not keyboard_func:
        await content_manager.clear_keyboard_stack(user_id)
        await content_manager.push_keyboard(user_id, "start")
        await message.answer(
            await content_manager.aget("start"),
            reply_markup=await get_start_keyboard(),
            parse_mode="markdown"
        )
        return
    await message.answer(
        await content_manager.aget(prev_keyboard_key),
        reply_markup=await keyboard_func(),
        parse_mode="markdown"
    )

@router.message()
async def handle_message(message: types.Message):
    buttons = []
    for key in KEYBOARD_INFO.keys():
        buttons.extend(await content_manager.aget_buttons(key))
    for button in buttons:
        if button["text"] == message.text.strip() and button["url"]:
            await message.answer(f"Вы выбрали '{button['text']}'. Перейти: {button['url']}")
            return
    await message.answer(await content_manager.aget("unknown_command"))