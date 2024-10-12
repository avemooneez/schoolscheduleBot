from aiogram.types import Message, FSInputFile
from aiogram import Router, F
from keyboards import main
from utils.today import ScheduleImage
from db import Database
from datetime import datetime
import os

router = Router()
db = Database()

@router.message(F.text == "Сегодня")
async def cmd_today(message: Message):
    grade_full = db.get_grade(message.from_user.id)
    grade = str(grade_full[0]) + grade_full[1]
    if not os.path.exists(f"./temp/{datetime.now().strftime('%d-%m-%Y')}-{grade}.png"):
        print("Not exists")
        schedule_data = {
        "9А": [
            {
                "lesson": "Разговоры о важном",
                "time": "8:00 - 08:30",
                "room": "22"
            },
            {
                "lesson": 'Физика',
                "time": "8:35 - 9:10",
                "room": "22"
            },
            {
                "lesson": 'История',
                "time": "9:20 - 9:55",
                "room": "27"
            },
            {
                "lesson": 'Алгебра',
                "time": "10:10 - 10:45",
                "room": "26"
            },
            {
                "lesson": 'Физическая культура',
                "time": "11:00 - 11:35",
                "room": ""
            },
            {
                "lesson": 'Литература',
                "time": "11:45 - 12:20",
                "room": "39"
            },
            {
                "lesson": 'Информатика',
                "time": "12:25 - 13:00",
                "room": "21"
            }
        ]
    }
        schedule_image = ScheduleImage(schedule_data)
        image_path = schedule_image.generate_image(grade, "14.10.2024", "Понедельник")
    else:
        print("Exists")
        image_path = f"./temp/{datetime.now().strftime('%d-%m-%Y')}-{grade}.png"
    photo = FSInputFile(image_path)
    await message.answer_photo(photo=photo, reply_markup=main.main_kb())

