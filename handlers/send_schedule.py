from aiogram import Command, Router
from aiogram.types import Message

from db import Database
from utils.downloading_file import SendScheduleImage

router = Router()
db = Database()
schedule = SendScheduleImage()


@router.message(Command("schedule"))
async def cmd_schedule(message: Message):
    """Отправляет расписание по команде /schedule"""
    await schedule.send_schedule_images_for_one(message, db, message.from_user.id)
