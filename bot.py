import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, F
from aiogram.types import BotCommand
from utils import tokens
from handlers import start, settings, send_schedule, admin
from db import Database
from utils.downloading_file import SendScheduleImage

db = Database()
schedule = SendScheduleImage()


def schedule_start():
    schedule.download_file(
        output_file=schedule.file_name
    )  # Функция скачивания расписания


async def main():
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s %(levelname)s: %(message)s"
    )

    db.start()

    bot = Bot(token=tokens.bot_token)
    dp = Dispatcher()

    await bot.set_my_commands(
        [
            BotCommand(command="start", description="Перезапуск бота"),
            BotCommand(command="settings", description="Настройки бота"),
            BotCommand(command="schedule", description="Отправить расписание"),
            BotCommand(command="info", description="Информация о боте"),
            BotCommand(command="help", description="Помощь"),
        ]
    )

    dp.include_routers(
        start.router,
        settings.router,
        send_schedule.router,
        admin.router,
    )

    dp.message.filter(F.chat.type.in_({"private"}))
    await bot.delete_webhook(drop_pending_updates=True)

    if not os.path.exists("temp/schedule.docx"):  # Проверка наличия файла с расписанием
        schedule_start()

    task_polling = asyncio.create_task(dp.start_polling(bot))
    task_check_schedule = asyncio.create_task(
        schedule.check_new_schedule(bot=bot, db=db)
    )
    # Две асинхронных задачи, task_polling - long polling телеграм бота,
    # task_check_schedule - бесконечная проверка на новое расписание

    await asyncio.gather(task_polling, task_check_schedule)  # Запуск двух async задач


if __name__ == "__main__":
    asyncio.run(main())
