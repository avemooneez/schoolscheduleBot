from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.filters import Command
from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.redis import RedisStorage
from keyboards import grade_letter
from db import Database

storage = RedisStorage.from_url("redis://localhost:6379/0")
router = Router()
db = Database()

class Grades(StatesGroup):
    grade = State()
    letter = State()

@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    await message.answer("Добро пожаловать в бота!")
    if not db.user_exists(message.from_user.id):
        await message.answer("Вы новый пользователь! Выберите ваш класс в клавиатуре ниже.", reply_markup=grade_letter.grade_kb())
        await state.set_state(Grades.grade)

@router.message(Grades.grade)
async def grade_handler(message: Message, state: FSMContext):
    grade = message.text
    await state.update_data(grade=grade)
    print(state.data)
    await message.answer("Вы выбрали класс {}. Выберите букву класса ниже.".format(grade), reply_markup=grade_letter.letter_kb(grade=message.text))
    await state.set_state(Grades.letter)