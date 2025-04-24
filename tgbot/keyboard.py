from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from common.manager import content_manager

async def get_start_keyboard():
    buttons = await content_manager.aget_buttons("start")
    keyboard = [[KeyboardButton(text=button["text"])] for button in buttons]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

async def get_scholarship_keyboard():
    buttons = await content_manager.aget_buttons("scholarship")
    keyboard = [[KeyboardButton(text=button["text"])] for button in buttons]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

async def get_mobility_keyboard():
    buttons = await content_manager.aget_buttons("mobility")
    keyboard = [[KeyboardButton(text=button["text"])] for button in buttons]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

async def get_labs_keyboard():
    buttons = await content_manager.aget_buttons("labs")
    keyboard = [[KeyboardButton(text=button["text"])] for button in buttons]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

async def get_projects_keyboard():
    buttons = await content_manager.aget_buttons("projects")
    keyboard = [[KeyboardButton(text=button["text"])] for button in buttons]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

async def get_faq_keyboard():
    buttons = await content_manager.aget_buttons("faq")
    keyboard = [[KeyboardButton(text=button["text"])] for button in buttons]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

async def get_active_scholarships_keyboard():
    buttons = await content_manager.aget_buttons("active_scholarships")
    keyboard = [[KeyboardButton(text=button["text"])] for button in buttons]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

async def get_archive_scholarships_keyboard():
    buttons = await content_manager.aget_buttons("archive_scholarships")
    keyboard = [[KeyboardButton(text=button["text"])] for button in buttons]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

async def get_projects_participation_keyboard():
    buttons = await content_manager.aget_buttons("projects_participation")
    keyboard = [[KeyboardButton(text=button["text"])] for button in buttons]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

async def get_nug_keyboard():
    buttons = await content_manager.aget_buttons("nug")
    keyboard = [[KeyboardButton(text=button["text"])] for button in buttons]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)