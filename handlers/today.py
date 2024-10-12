from aiogram.types import Message
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.redis import RedisStorage
from keyboards import grade_letter, main
from db import Database

router = Router()
db = Database()

@router.message(F.text == "Сегодня")
async def cmd_today(message: Message, state: FSMContext):
    print(db.get_grade(message.from_user.id))
    await message.answer("#FREERUSSIA", reply_markup=main.main_kb())

