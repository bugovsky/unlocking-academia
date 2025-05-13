import logging

import typer

tgbot = typer.Typer(short_help="Запуск ТГ-бота")
logging.basicConfig(level=logging.INFO)


@tgbot.command(name="bot", short_help="Запустить тг-бота")
def launch_tgbot():
    import asyncio
    from tgbot.app import bot, dispatcher

    async def launch():
        await dispatcher.start_polling(bot)

    asyncio.run(launch())
