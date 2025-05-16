from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from common.manager import content_manager

async def get_start_keyboard():
    buttons = await content_manager.aget_buttons("start")
    callback_map = {
        "💸 Стипендии": "scholarships",
        "🚗 Программы международной мобильности": "mobility",
        "🔬 Лаборатории": "labs",
        "💼 Проекты и НУГи": "projects",
        "❓ Часто задаваемые вопросы": "faq",
        "📩 Отправить вопрос / Записаться на консультацию": "ask",
        "📚 Конференции / Публикации": "conferences",
    }
    keyboard = [
        [InlineKeyboardButton(text=button["text"], url=button["url"] if button["url"] else None, callback_data=callback_map.get(button["text"]))]
        for button in buttons
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

async def get_scholarships_keyboard():
    buttons = await content_manager.aget_buttons("scholarships")
    keyboard = [
        [InlineKeyboardButton(text=button["text"], url=button["url"] if button["url"] else None, callback_data="active_scholarships" if button["text"] == "Активные программы стипендий" else "archive_scholarships" if button["text"] == "Архив стипендиальных программ" else None)]
        for button in buttons
    ]
    keyboard.append([InlineKeyboardButton(text="Назад", callback_data="back")])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

async def get_mobility_keyboard():
    buttons = await content_manager.aget_buttons("mobility")
    keyboard = [
        [InlineKeyboardButton(text=button["text"], url=button["url"])]
        for button in buttons
    ]
    keyboard.append([InlineKeyboardButton(text="Назад", callback_data="back")])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

async def get_labs_keyboard():
    buttons = await content_manager.aget_buttons("labs")
    keyboard = [
        [InlineKeyboardButton(text=button["text"], url=button["url"])]
        for button in buttons
    ]
    keyboard.append([InlineKeyboardButton(text="Назад", callback_data="back")])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

async def get_projects_keyboard():
    buttons = await content_manager.aget_buttons("projects")
    keyboard = [
        [InlineKeyboardButton(text=button["text"], url=button["url"] if button["url"] else None, callback_data="projects_participation" if button["text"] == "Участие в проектах" else "nug" if button["text"] == "Про научно-учебные группы" else None)]
        for button in buttons
    ]
    keyboard.append([InlineKeyboardButton(text="Назад", callback_data="back")])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

async def get_faq_keyboard():
    buttons = await content_manager.aget_buttons("faq")
    keyboard = [
        [InlineKeyboardButton(text=button["text"], url=button["url"] if button["url"] else None, callback_data="what_is_nug" if button["text"] == "Что такое НУГ?" else "funding_info" if button["text"] == "Как получить финансирование?" else None)]
        for button in buttons
    ]
    keyboard.append([InlineKeyboardButton(text="Назад", callback_data="back")])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

async def get_active_scholarships_keyboard():
    buttons = await content_manager.aget_buttons("active_scholarships")
    keyboard = [
        [InlineKeyboardButton(text=button["text"], url=button["url"])]
        for button in buttons
    ]
    keyboard.append([InlineKeyboardButton(text="Назад", callback_data="back")])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

async def get_archive_scholarships_keyboard():
    buttons = await content_manager.aget_buttons("archive_scholarships")
    keyboard = [
        [InlineKeyboardButton(text=button["text"], url=button["url"])]
        for button in buttons
    ]
    keyboard.append([InlineKeyboardButton(text="Назад", callback_data="back")])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

async def get_projects_participation_keyboard():
    buttons = await content_manager.aget_buttons("projects_participation")
    keyboard = [
        [InlineKeyboardButton(text=button["text"], url=button["url"])]
        for button in buttons
    ]
    keyboard.append([InlineKeyboardButton(text="Назад", callback_data="back")])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

async def get_nug_keyboard():
    buttons = await content_manager.aget_buttons("nug")
    keyboard = [
        [InlineKeyboardButton(text=button["text"], url=button["url"])]
        for button in buttons
    ]
    keyboard.append([InlineKeyboardButton(text="Назад", callback_data="back")])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

async def get_conferences_keyboard():
    buttons = await content_manager.aget_buttons("conferences")
    keyboard = [
        [InlineKeyboardButton(text=button["text"], url=button["url"])]
        for button in buttons
    ]
    keyboard.append([InlineKeyboardButton(text="Назад", callback_data="back")])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

async def get_back_to_start_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Вернуться в стартовое меню", callback_data="back_to_start")]
    ])