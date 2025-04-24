from collections import namedtuple
import json
from typing import List, Dict, Optional

from redis import Redis
from redis.asyncio import Redis as AsyncRedis

from common.redis.client import redis, async_redis

ContentInfo = namedtuple("ContentInfo", ["name", "context", "default"])
KeyboardInfo = namedtuple("KeyboardInfo", ["name", "context", "default"])

CONTENT_INFO = {
    "start": ContentInfo(
        name="Старт",
        context="Сообщение при команде /start",
        default="Привет!\nЭто телеграм-бот проекта Unlocking Academia..."
    ),
    "scholarships": ContentInfo(
        name="Стипендии",
        context="Ответ на кнопку '💸 Стипендии'",
        default="🎓 Студентам предоставляются как государственные стипендии..."
    ),
    "mobility": ContentInfo(
        name="Программы международной мобильности",
        context="Ответ на кнопку '🚗 Программы международной мобильности'",
        default="Международные академические программы – это уникальный опыт..."
    ),
    "labs": ContentInfo(
        name="Лаборатории",
        context="Ответ на кнопку '🔬 Лаборатории'",
        default="Лаборатории – это точки роста академической среды..."
    ),
    "projects": ContentInfo(
        name="Проекты и НУГи",
        context="Ответ на кнопку '💼 Проекты и НУГи'",
        default="Здесь ты можешь узнать о проектах и возможностях\n(Раздел пополняется)"
    ),
    "ask": ContentInfo(
        name="Отправить нам вопрос / Записаться на консультацию",
        context="Ответ на кнопку '📩 Отправить нам вопрос'",
        default="Если ты не нашел интересующей тебя информации..."
    ),
    "faq": ContentInfo(
        name="Часто задаваемые вопросы",
        context="Ответ на кнопку '❓ Часто задаваемые вопросы'",
        default="Ответы на популярные вопросы можно найти здесь..."
    ),
    "active_scholarships": ContentInfo(
        name="Активные программы стипендий",
        context="Ответ на выбор 'Активные программы стипендий'",
        default="На данный момент можно подать заявки на следующие стипендии:"
    ),
    "archive_scholarships": ContentInfo(
        name="Архив стипендиальных программ",
        context="Ответ на выбор 'Архив стипендиальных программ'",
        default="Отбор на эти стипендии закончен..."
    ),
    "project_participation": ContentInfo(
        name="Участие в проектах",
        context="Ответ на выбор 'Участие в проектах'",
        default="Проект – это самостоятельная организованная деятельность..."
    ),
    "nug_info": ContentInfo(
        name="Про научно-учебные группы",
        context="Ответ на выбор 'Про научно-учебные группы'",
        default="Здесь ты можешь узнать о том, как происходит создание научно-учебных групп..."
    ),
    "what_is_nug": ContentInfo(
        name="Что такое НУГ?",
        context="Ответ на вопрос 'Что такое НУГ?'",
        default="Научно-учебная группа (НУГ) – коллектив исследователей..."
    ),
    "funding_info": ContentInfo(
        name="Как получить финансирование?",
        context="Ответ на вопрос 'Как получить финансирование?'",
        default="Вышка может оказать студенческим инициативам финансовую поддержку..."
    ),
    "unknown_command": ContentInfo(
        name="Неизвестная команда",
        context="Сообщение при вводе неизвестной команды",
        default="Я не знаю такой команды :("
    ),
}

KEYBOARD_INFO = {
    "mobility": KeyboardInfo(
        name="Программы мобильности",
        context="Кнопки меню программ мобильности",
        default=[
            {"text": "🌍 Направления мобильности", "url": "https://studyabroad.hse.ru/catalogue"},
            {"text": "🖋️ Подача заявок", "url": "https://studyabroad.hse.ru/howtoapply"},
            {"text": "💰 Гранты", "url": "https://studyabroad.hse.ru/grants/"},
            {"text": "Назад", "url": None}
        ]
    ),
    "labs": KeyboardInfo(
        name="Лаборатории",
        context="Кнопки меню лабораторий",
        default=[
            {"text": "Список лабораторий", "url": "https://www.hse.ru/science/nul/lab#pagetop"},
            {"text": "Вакансии", "url": "https://career.hse.ru/insidehse"},
            {"text": "Назад", "url": None}
        ]
    ),
    "active_scholarships": KeyboardInfo(
        name="Активные стипендии",
        context="Кнопки меню активных стипендий",
        default=[
            {"text": "Стипендия Россельхозбанка", "url": "https://svoevagro.ru/events/scholarship-program"},
            {"text": "Грант Президента Российской Федерации", "url": "https://грантыпрезидента.рф"},
            {"text": "Назад", "url": None}
        ]
    ),
    "archive_scholarships": KeyboardInfo(
        name="Архив стипендий",
        context="Кнопки меню архива стипендий",
        default=[
            {"text": "ПГАС", "url": "https://www.hse.ru/scholarships/academic_raised"},
            {"text": "Стипендия Правительства РФ", "url": "https://www.hse.ru/scholarships/government/"},
            {"text": "Стипендия Правительства Москвы", "url": "https://www.hse.ru/scholarships/mosgovt"},
            {"text": "Стипендия фонда Потанина", "url": "https://fondpotanin.ru/competitions/fellowships/"},
            {"text": "Стипендия Президента РФ для обучения за рубежом", "url": "https://стипендиатроссии.рф/forstudyingabroad"},
            {"text": "Стипендия Тинькофф", "url": "https://fintech.tinkoff.ru/scholarship/"},
            {"text": "Назад", "url": None}
        ]
    ),
    "projects_participation": KeyboardInfo(
        name="Участие в проектах",
        context="Кнопки меню участия в проектах",
        default=[
            {"text": "Ярмарка проектов", "url": "https://pf.hse.ru"},
            {"text": "Назад", "url": None}
        ]
    ),
    "nug": KeyboardInfo(
        name="Научно-учебные группы",
        context="Кнопки меню НУГов",
        default=[
            {"text": "Финансирование", "url": "https://www.hse.ru/science/scifund/nug/financing"},
            {"text": "Конкурс", "url": "https://www.hse.ru/science/scifund/nug/"},
            {"text": "Назад", "url": None}
        ]
    )
}

class ContentManager:
    CONTENT_KEY = "unlocking_academia_content"
    BUTTONS_KEY_PREFIX = "unlocking_academia_buttons:"
    KEYBOARD_STACK_PREFIX = "unlocking_academia_user:"

    def __init__(self, r: Redis, ar: AsyncRedis):
        self._client = r
        self._async_client = ar
        self._fill_content()
        self._fill_buttons()

    def _fill_content(self):
        if not self._client.exists(self.CONTENT_KEY):
            default_content = {key: info.default for key, info in CONTENT_INFO.items()}
            self._client.hset(self.CONTENT_KEY, mapping=default_content)

    def _fill_buttons(self):
        for key, info in KEYBOARD_INFO.items():
            redis_key = f"{self.BUTTONS_KEY_PREFIX}{key}"
            if not self._client.exists(redis_key):
                self._client.set(redis_key, json.dumps(info.default))

    def get(self, key: str) -> str:
        return self._client.hget(self.CONTENT_KEY, key) or "Текст не найден"

    def set(self, key: str, value: str) -> None:
        self._client.hset(self.CONTENT_KEY, key, value)

    def get_all(self):
        return self._client.hgetall(self.CONTENT_KEY)

    async def aget(self, key: str, default: str = "Текст не найден") -> str:
        result = await self._async_client.hget(self.CONTENT_KEY, key) or default
        return result

    async def aset(self, key: str, value: str) -> None:
        await self._async_client.hset(self.CONTENT_KEY, key, value)

    def get_buttons(self, keyboard_key: str) -> List[Dict[str, str]]:
        redis_key = f"{self.BUTTONS_KEY_PREFIX}{keyboard_key}"
        buttons_json = self._client.get(redis_key)
        return json.loads(buttons_json) if buttons_json else []

    def set_buttons(self, keyboard_key: str, buttons: List[Dict[str, str]]) -> None:
        redis_key = f"{self.BUTTONS_KEY_PREFIX}{keyboard_key}"
        self._client.set(redis_key, json.dumps(buttons))

    async def aget_buttons(self, keyboard_key: str) -> List[Dict[str, str]]:
        redis_key = f"{self.BUTTONS_KEY_PREFIX}{keyboard_key}"
        buttons_json = await self._async_client.get(redis_key)
        result = json.loads(buttons_json) if buttons_json else []
        return result

    async def aset_buttons(self, keyboard_key: str, buttons: List[Dict[str, str]]) -> None:
        redis_key = f"{self.BUTTONS_KEY_PREFIX}{keyboard_key}"
        await self._async_client.set(redis_key, json.dumps(buttons))

    async def push_keyboard(self, user_id: int, keyboard_key: str) -> None:
        redis_key = f"{self.KEYBOARD_STACK_PREFIX}{user_id}:keyboard_stack"
        stack = await self._async_client.get(redis_key)
        stack = json.loads(stack) if stack else []
        stack.append(keyboard_key)
        await self._async_client.set(redis_key, json.dumps(stack))

    async def pop_keyboard(self, user_id: int) -> Optional[str]:
        redis_key = f"{self.KEYBOARD_STACK_PREFIX}{user_id}:keyboard_stack"
        stack = await self._async_client.get(redis_key)
        if not stack:
            return None
        stack = json.loads(stack)
        if len(stack) <= 1:
            await self._async_client.delete(redis_key)
            return None
        stack.pop()
        prev_keyboard = stack[-1] if stack else None
        await self._async_client.set(redis_key, json.dumps(stack))
        return prev_keyboard

    async def clear_keyboard_stack(self, user_id: int) -> None:
        redis_key = f"{self.KEYBOARD_STACK_PREFIX}{user_id}:keyboard_stack"
        await self._async_client.delete(redis_key)

content_manager = ContentManager(redis, async_redis)