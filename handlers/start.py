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
    isAllCorrect = State()

@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    if not db.user_exists(message.from_user.id):
        await message.answer("Вы новый пользователь! Выберите ваш класс в клавиатуре ниже.", reply_markup=grade_letter.grade_kb())
        await state.set_state(Grades.grade)
        return
    await message.answer("Добро пожаловать в бота! Это — бот с расписанием уроков в школе №9. Воспользуйтесь кнопками ниже для управления ботом.", reply_markup=ReplyKeyboardRemove())

@router.message(Grades.grade)
async def grade_handler(message: Message, state: FSMContext):
    grade = message.text
    await state.update_data(grade=grade)
    await message.answer("Вы выбрали класс {}. Выберите букву класса ниже.".format(grade), reply_markup=grade_letter.letter_kb(grade=message.text))
    await state.set_state(Grades.letter)

@router.message(Grades.letter)
async def letter_handler(message: Message, state: FSMContext):
    letter = message.text
    await state.update_data(letter=letter)
    gradeLetter = await state.get_data()
    await message.answer(f"Вы в {gradeLetter['grade']}{gradeLetter['letter']} классе. Всё верно?", reply_markup=grade_letter.isAllCorrect_kb())
    await state.set_state(Grades.isAllCorrect)

@router.message(Grades.isAllCorrect)
async def isAllCorrect_handler(message: Message, state: FSMContext):
    if message.text == "Всё верно":
        gradeLetter = await state.get_data()
        db.add_user(message.from_user.id, int(gradeLetter['grade']), str(gradeLetter['letter']))
        await message.answer("Отлично!", reply_markup=ReplyKeyboardRemove())
        await state.clear()
        await state.set_state(None)
        
    else:
        await message.answer("Начинаем заново. Выберите ваш класс в клавиатуре ниже.", reply_markup=grade_letter.grade_kb())
        await state.clear()
        await state.set_state(Grades.grade)