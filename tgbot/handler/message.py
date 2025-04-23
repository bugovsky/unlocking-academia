from aiogram import F, Router, types
from aiogram.filters.command import Command

from common.manager import content_manager
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

@router.message(Command("start"))
async def start_command(message: types.Message):
    await message.answer(
        await content_manager.aget("start"),
        reply_markup=get_start_keyboard(),
        parse_mode="markdown"
    )

@router.message(F.text.strip() == "💸 Стипендии")
async def scholarships(message: types.Message):
    await message.answer(
        await content_manager.aget("scholarships"),
        reply_markup=get_scholarship_keyboard()
    )

@router.message(F.text.strip() == "🚗 Программы международной мобильности")
async def mobility(message: types.Message):
    await message.answer(
        await content_manager.aget("mobility"),
        reply_markup=get_mobility_keyboard()
    )

@router.message(F.text.strip() == "🔬 Лаборатории")
async def labs(message: types.Message):
    await message.answer(
        await content_manager.aget("labs"),
        reply_markup=get_labs_keyboard()
    )

@router.message(F.text.strip() == "💼 Проекты и НУГи")
async def projects(message: types.Message):
    await message.answer(
        await content_manager.aget("projects"),
        reply_markup=get_projects_keyboard()
    )

@router.message(F.text.strip() == "❓ Часто задаваемые вопросы")
async def faq(message: types.Message):
    await message.answer(
        await content_manager.aget("faq"),
        reply_markup=get_faq_keyboard()
    )

@router.message(F.text.strip() == "Активные программы стипендий")
async def active_scholarships(message: types.Message):
    await message.answer(
        await content_manager.aget("active_scholarships"),
        reply_markup=get_active_scholarships_keyboard()
    )

@router.message(F.text.strip() == "Архив стипендиальных программ")
async def archive_scholarships(message: types.Message):
    await message.answer(
        await content_manager.aget("archive_scholarships"),
        reply_markup=get_archive_scholarships_keyboard()
    )

@router.message(F.text.strip() == "Участие в проектах")
async def project_participation(message: types.Message):
    await message.answer(
        await content_manager.aget("project_participation"),
        reply_markup=get_projects_participation_keyboard()
    )

@router.message(F.text.strip() == "Про научно-учебные группы")
async def nug_info(message: types.Message):
    await message.answer(
        await content_manager.aget("nug_info"),
        reply_markup=get_nug_keyboard()
    )

@router.message(F.text.strip() == "Что такое НУГ?")
async def what_is_nug(message: types.Message):
    await message.answer(await content_manager.aget("what_is_nug"))

@router.message(F.text.strip() == "Как получить финансирование?")
async def funding_info(message: types.Message):
    await message.answer(await content_manager.aget("funding_info"))

@router.message(F.text.strip() == "Назад")
async def back_to_start(message: types.Message):
    await message.answer(
        await content_manager.aget("start"),
        reply_markup=get_start_keyboard()
    )

@router.message
async def handle_message(message: types.Message):
    await message.answer(await content_manager.aget("unknown_command"))