from aiogram.types import Message
from aiogram.filters import Command
from aiogram import Router, F
from db import Database
from utils.downloading_file import SendScheduleImage

router = Router()
db = Database()
schedule = SendScheduleImage()

@router.message(Command("schedule"))
async def cmd_schedule(message: Message):
    await schedule.send_schedule_images_for_one(message, db, message.from_user.id)
