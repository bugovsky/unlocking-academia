from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

def get_start_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="💸 Стипендии")],
            [KeyboardButton(text="🚗 Программы международной мобильности")],
            [KeyboardButton(text="🔬 Лаборатории")],
            [KeyboardButton(text="💼 Проекты и НУГи")],
            [KeyboardButton(text="❓ Часто задаваемые вопросы")],
            [KeyboardButton(text="👥 Индивидуальная консультация")],
            [KeyboardButton(text="📩 Отправить нам вопрос")]
        ],
        resize_keyboard=True
    )

def get_scholarship_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Активные программы стипендий")],
            [KeyboardButton(text="Архив стипендиальных программ")],
            [KeyboardButton(text="Назад")]
        ],
        resize_keyboard=True
    )

def get_mobility_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🌍 Направления мобильности", url="https://studyabroad.hse.ru/catalogue")],
        [InlineKeyboardButton(text="🖋️ Подача заявок", url="https://studyabroad.hse.ru/howtoapply")],
        [InlineKeyboardButton(text="💰 Гранты", url="https://studyabroad.hse.ru/grants/")],
        [InlineKeyboardButton(text="Назад", callback_data="back_to_start")]
    ])

def get_labs_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Список лабораторий", url="https://www.hse.ru/science/nul/lab#pagetop")],
        [InlineKeyboardButton(text="Вакансии", url="https://career.hse.ru/insidehse")],
        [InlineKeyboardButton(text="Назад", callback_data="back_to_start")]
    ])

def get_projects_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Участие в проектах")],
            [KeyboardButton(text="Про научно-учебные группы")],
            [KeyboardButton(text="Назад")]
        ],
        resize_keyboard=True
    )

def get_faq_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Что такое НУГ?")],
            [KeyboardButton(text="Как получить финансирование?")],
            [KeyboardButton(text="Назад")]
        ],
        resize_keyboard=True
    )

def get_active_scholarships_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Стипендия Россельхозбанка", url="https://svoevagro.ru/events/scholarship-program")],
        [InlineKeyboardButton(text="Грант Президента Российской Федерации", url="https://грантыпрезидента.рф")],
        [InlineKeyboardButton(text="Назад", callback_data="back_to_start")]
    ])

def get_archive_scholarships_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="ПГАС", url="https://www.hse.ru/scholarships/academic_raised")],
        [InlineKeyboardButton(text="Стипендия Правительства РФ", url="https://www.hse.ru/scholarships/government/")],
        [InlineKeyboardButton(text="Стипендия Правительства Москвы", url="https://www.hse.ru/scholarships/mosgovt")],
        [InlineKeyboardButton(text="Стипендия фонда Потанина", url="https://fondpotanin.ru/competitions/fellowships/")],
        [InlineKeyboardButton(text="Стипендия Президента РФ для обучения за рубежом", url="https://стипендиатроссии.рф/forstudyingabroad")],
        [InlineKeyboardButton(text="Стипендия Тинькофф", url="https://fintech.tinkoff.ru/scholarship/")],
        [InlineKeyboardButton(text="Назад", callback_data="back_to_start")]
    ])

def get_projects_participation_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Ярмарка проектов", url="https://pf.hse.ru")],
        [InlineKeyboardButton(text="Назад", callback_data="back_to_start")]
    ])

def get_nug_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Финансирование", url="https://www.hse.ru/science/scifund/nug/financing")],
        [InlineKeyboardButton(text="Конкурс", url="https://www.hse.ru/science/scifund/nug/")],
        [InlineKeyboardButton(text="Назад", callback_data="back_to_start")]
    ])