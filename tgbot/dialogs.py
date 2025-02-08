from aiogram import types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

class DialogOption:
    def __init__(self, button_text, command_text, action):
        self.button_text = button_text
        self.command_text = command_text
        self.action = action


async def scholarships_action(message: types.Message):
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton("Активные программы стипендий"))
    kb.add(KeyboardButton("Архив стипендиальных программ"))
    text = (
        "🎓 Студентам предоставляются как государственные стипендии, так и стипендии от партнеров и фондов. \n"
        "Здесь вы можете узнать подробнее про стипендии, на которые открыт отбор, а также про стипендии, для которых он уже завершен. \n"
        "Подробности можно посмотреть в меню чат-бота"
    )
    await message.answer(text, reply_markup=kb)

async def mobility_action(message: types.Message):
    kb = InlineKeyboardMarkup(row_width=1)
    kb.add(
        InlineKeyboardButton("🌍 Направления мобильности", url="https://studyabroad.hse.ru/catalogue"),
        InlineKeyboardButton("🖋️ Подача заявок", url="https://studyabroad.hse.ru/howtoapply"),
        InlineKeyboardButton("💰 Гранты", url="https://studyabroad.hse.ru/grants/")
    )
    text = (
        "Международные академические программы – это уникальный опыт, отличные инвестиции в будущее и яркие впечатления от жизни и учебы в другой стране. Участие в международной студенческой мобильности предоставляет много возможностей: \n"
        " – Приобрести опыт сотрудничества в международной академической среде \n"
        " – Развить навыки межкультурной коммуникации и работы в команде \n"
        " – Повысить уровень владения иностранным языком \n"
        " – Познакомиться с образовательными системами других стран\n"
        " – Открыть новые карьерные перспективы \n"
    )
    await message.answer(text, reply_markup=kb)

async def labs_action(message: types.Message):
    kb = InlineKeyboardMarkup(row_width=1)
    kb.add(
        InlineKeyboardButton("Список лабораторий", url="https://www.hse.ru/science/nul/lab#pagetop"),
        InlineKeyboardButton("Вакансии", url="https://career.hse.ru/insidehse")
    )
    text = (
        "Лаборатории – это точки роста академической среды, создаваемые в Вышке как команды преподавателей, исследователей, аспирантов и студентов для реализации научных проектов в самых разных дисциплинах. \n"
        "Лаборатории строятся на принципах горизонтальной академической кооперации: студенты и аспиранты участвуют в их работе наравне с более старшими и более опытными коллегами"
    )
    await message.answer(text, reply_markup=kb)

async def projects_action(message: types.Message):
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton("Участие в проектах"))
    kb.add(KeyboardButton("Про научно-учебные группы"))
    await message.answer("Здесь ты можешь узнать о проектах и возможностях \n(Раздел пополняется)", reply_markup=kb)

async def ask_action(message: types.Message):
    kb = InlineKeyboardMarkup(row_width=1)
    kb.add(
        InlineKeyboardButton("Задать анонимно", callback_data="q&a_anon"),
        InlineKeyboardButton("Задать вопрос и оставить контакт", callback_data="q&a")
    )
    text = (
        "Если ты не нашел интересующей тебя информации, можешь задать нам вопрос: оставить его анонимно "
        "(тогда мы постараемся ответить на него в одном из постов нашего тг-канала) или оставить контакт для связи "
        "(если вопрос специфичный, мы обязательно тебе ответим в личных сообщениях)"
    )
    await message.answer(text, reply_markup=kb)

async def faq_action(message: types.Message):
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton("Что такое НУГ?"))
    kb.add(KeyboardButton("Как получить финансирование?"))
    text = (
        "Ответы на популярные вопросы можно найти здесь. Можешь посмотреть здесь, или если не нашел ответ – записаться на консультацию.\n"
        "(Раздел пополняется)"
    )
    await message.answer(text, reply_markup=kb)

async def consult_action(message: types.Message):
    kb = InlineKeyboardMarkup(row_width=1)
    kb.add(InlineKeyboardButton("Записаться на консультацию", callback_data="consultation"))
    text = (
        "Наш проект предоставляет возможность индивидуальной консультации с экспертом, который может ответить на вопросы про организацию проектной деятельности, "
        "исследовательскую траекторию и прочее. \nКонсультация осуществляется по предварительной записи"
    )
    await message.answer(text, reply_markup=kb)


async def active_scholarships_action(message: types.Message):
    kb = InlineKeyboardMarkup(row_width=1)
    kb.add(
        InlineKeyboardButton("Стипендия Россельхозбанка", url="https://svoevagro.ru/events/scholarship-program"),
        InlineKeyboardButton("Грант Президента Российской Федерации", url="https://грантыпрезидента.рф")
    )
    await message.answer("На данный момент можно подать заявки на следующие стипендии:", reply_markup=kb)

async def archive_scholarships_action(message: types.Message):
    kb = InlineKeyboardMarkup(row_width=1)
    kb.add(
        InlineKeyboardButton("ПГАС", url="https://www.hse.ru/scholarships/academic_raised"),
        InlineKeyboardButton("Стипендия Правительства РФ", url="https://www.hse.ru/scholarships/government/"),
        InlineKeyboardButton("Стипендия Правительства Москвы", url="https://www.hse.ru/scholarships/mosgovt"),
        InlineKeyboardButton("Стипендия фонда Потанина", url="https://fondpotanin.ru/competitions/fellowships/"),
        InlineKeyboardButton("Стипендия Президента Российской Федерации для обучения за рубежом", url="https://стипендиатроссии.рф/forstudyingabroad"),
        InlineKeyboardButton("Стипендия Тинькофф", url="https://fintech.tinkoff.ru/scholarship/")
    )
    await message.answer("Отбор на эти стипендии закончен, но ты можешь попробовать свои силы в следующем сезоне:", reply_markup=kb)

async def participation_in_projects_action(message: types.Message):
    kb = InlineKeyboardMarkup(row_width=1)
    kb.add(InlineKeyboardButton("Ярмарка проектов", url="https://pf.hse.ru"))
    await message.answer(
        "Проект – это самостоятельная организованная деятельность студентов под кураторством руководителя, направленная на поиск решения практической или теоретически значимой проблемы. \n"
        "Узнать подробнее ты можешь на Ярмарке проектов", reply_markup=kb
    )

async def nug_action(message: types.Message):
    kb = InlineKeyboardMarkup(row_width=1)
    kb.add(
        InlineKeyboardButton("Финансирование", url="https://www.hse.ru/science/scifund/nug/financing"),
        InlineKeyboardButton("Конкурс", url="https://www.hse.ru/science/scifund/nug/")
    )
    await message.answer(
        "Здесь ты можешь узнать о том, как происходит создание научно-учебных групп, как пройти конкурс и зафиксировать результаты", reply_markup=kb
    )

async def what_is_nug_action(message: types.Message):
    await message.answer(
        "Научно-учебная группа (НУГ) – коллектив исследователей, включающий студентов бакалавриата, магистрантов, аспирантов, молодых преподавателей и/или научных сотрудников под руководством опытного наставника. "
        "НУГ создается на конкурсной основе, проекты поддерживаются на один год с возможностью пролонгации по результатам первого года работы еще на один год."
    )

async def what_is_initiative_group_action(message: types.Message):
    await message.answer("Здесь ответ")

async def financing_action(message: types.Message):
    await message.answer(
        "Вышка может оказать студенческим инициативам финансовую поддержку для реализации проектов и обеспечения текущей деятельности. На данный момент доступны следующие форматы поддержки: \n"
        " – КПСИ \n – Гранты \n – Внеакадемичекская мобильность"
    )

dialog_options = [
    DialogOption("💸 Стипендии", "/scholarships", scholarships_action),
    DialogOption("🚗 Программы международной мобильности", "/mobility", mobility_action),
    DialogOption("🔬 Лаборатории", "/labs", labs_action),
    DialogOption("💼 Проекты и НУГи", "/projects", projects_action),
    DialogOption("📩 Отправить нам вопрос", "/ask", ask_action),
    DialogOption("❓ Часто задаваемые вопросы", "/faq", faq_action),
    DialogOption("👥 Индивидуальная консультация", "/consult", consult_action),
    DialogOption("Активные программы стипендий", None, active_scholarships_action),
    DialogOption("Архив стипендиальных программ", None, archive_scholarships_action),
    DialogOption("Участие в проектах", None, participation_in_projects_action),
    DialogOption("Про научно-учебные группы", None, nug_action),
    DialogOption("Что такое НУГ?", None, what_is_nug_action),
    DialogOption("Что такое инициативная группа?", None, what_is_initiative_group_action),
    DialogOption("Как получить финансирование?", None, financing_action)
]
