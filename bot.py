import asyncio
import logging
from aiogram import Bot, Dispatcher, F
from utils import tokens
from handlers import start, settings, send_schedule
from db import Database
from utils.downloading_file import SendScheduleImage
import os

db = Database()
schedule = SendScheduleImage()

def schedule_start():
    schedule.download_file(output_file=schedule.file_name)
    print("Скачано расписание")
    

async def main():
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s: %(message)s")

    db.start()
    
    bot = Bot(token=tokens.bot_token)
    dp = Dispatcher()

    dp.include_routers(
        start.router,
        settings.router,
        send_schedule.router,  
    )

    dp.message.filter(F.chat.type.in_({"private"}))
    await bot.delete_webhook(drop_pending_updates=True)

    
    if not os.path.exists('temp/schedule.docx'):
        schedule_start()
    # Создаем две асинхронные задачи: для пулинга бота и для проверки расписания
    task_polling = asyncio.create_task(dp.start_polling(bot))
    print("Started task 1")
    task_check_schedule = asyncio.create_task(schedule.check_new_schedule(bot=bot, db=db))
    print("Starting task 2")
    # Ждем, пока обе задачи не завершатся
    await asyncio.gather(task_polling, task_check_schedule)

if __name__ == "__main__":
    asyncio.run(main())
