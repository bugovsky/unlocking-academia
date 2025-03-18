from collections import namedtuple

from redis import Redis
from redis.asyncio import Redis as AsyncRedis

from common.redis.client import redis, async_redis

ContentInfo = namedtuple("ContentInfo", ["name", "context", "default"])

CONTENT_INFO = {
    "start": ContentInfo(
        name="Старт",
        context="Сообщение при команде /start",
        default="Привет!\nЭто телеграм-бот проекта Unlocking Academia..."
    ),
    "scholarships": ContentInfo(
        name="Стипендии", context="Ответ на кнопку '💸 Стипендии'",
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
        name="Отправить нам вопрос",
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
    )
}

class ContentManager:
    CONTENT_KEY = "unlocking_academia_content"

    def __init__(self, r: Redis, ar: AsyncRedis):
        self._client = r
        self._async_client = ar
        self._fill_content()

    def _fill_content(self):
        if not self._client.exists(self.CONTENT_KEY):
            default_content = {key: info.default for key, info in CONTENT_INFO.items()}
            self._client.hset(self.CONTENT_KEY, mapping=default_content)

    def get(self, key: str) -> str:
        return self._client.hget(self.CONTENT_KEY, key) or "Текст не найден"

    def set(self, key: str, value: str) -> None:
        self._client.hset(self.CONTENT_KEY, key, value)

    def get_all(self):
        return self._client.hgetall(self.CONTENT_KEY)

    async def aget(self, key: str) -> str:
        return await self._async_client.hget(self.CONTENT_KEY, key) or "Текст не найден"

    async def aset(self, key: str, value: str) -> None:
        await self._async_client.hset(self.CONTENT_KEY, key, value)


content_manager = ContentManager(redis, async_redis)