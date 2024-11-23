from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.filters import Command
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.redis import RedisStorage
from keyboards import grade_letter
from db import Database

storage = RedisStorage.from_url("redis://localhost:6379/0")
router = Router()
db = Database()

class SettingsGrades(StatesGroup):
    grade = State()
    letter = State()
    isAllCorrect = State()

@router.message(Command("settings"))
async def cmd_start(message: Message, state: FSMContext):
    await message.answer("Выберите Ваш класс в клавиатуре ниже.", reply_markup=grade_letter.grade_kb())
    await state.set_state(SettingsGrades.grade)

@router.message(SettingsGrades.grade)
async def grade_handler(message: Message, state: FSMContext):
    grade = message.text
    await state.update_data(grade=grade)
    await message.answer("Вы выбрали класс {}. Выберите букву класса ниже.".format(grade), reply_markup=grade_letter.letter_kb(grade=message.text))
    await state.set_state(SettingsGrades.letter)

@router.message(SettingsGrades.letter)
async def letter_handler(message: Message, state: FSMContext):
    letter = message.text
    await state.update_data(letter=letter)
    gradeLetter = await state.get_data()
    await message.answer(f"Вы в {gradeLetter['grade']}{gradeLetter['letter']} классе. Всё верно?", reply_markup=grade_letter.isAllCorrect_kb())
    await state.set_state(SettingsGrades.isAllCorrect)

@router.message(SettingsGrades.isAllCorrect)
async def isAllCorrect_handler(message: Message, state: FSMContext):
    if message.text == "Всё верно":
        gradeLetter = await state.get_data()
        db.update_user(message.from_user.id, int(gradeLetter['grade']), str(gradeLetter['letter']))
        await message.answer("Отлично!", reply_markup=ReplyKeyboardRemove())
        await state.clear()
        await state.set_state(None)
        
    else:
        await message.answer("Начинаем заново. Выберите ваш класс в клавиатуре ниже.", reply_markup=grade_letter.grade_kb())
        await state.clear()
        await state.set_state(SettingsGrades.grade)