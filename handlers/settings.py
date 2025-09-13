from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.filters import Command
from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.redis import RedisStorage
from keyboards import grade_letter
from db import Database
from utils.downloading_file import SendScheduleImage

storage = RedisStorage.from_url("redis://localhost:6379/0")
router = Router()
db = Database()
schedule = SendScheduleImage()


class SettingsGrades(StatesGroup):
    grade = State()
    letter = State()
    isAllCorrect = State()


@router.message(Command("settings"))
async def cmd_start(message: Message, state: FSMContext):
    assert message.from_user
    await message.answer(
        "Выберите Ваш класс в клавиатуре ниже.", reply_markup=grade_letter.grade_kb()
    )
    await state.set_state(SettingsGrades.grade)


@router.message(SettingsGrades.grade)
async def grade_handler(message: Message, state: FSMContext):
    assert message.from_user
    grade = message.text
    await state.update_data(grade=grade)
    await message.answer(
        text=f"Вы выбрали класс {grade}. Выберите букву класса ниже.",
        reply_markup=grade_letter.letter_kb(grade=message.text),
    )
    await state.set_state(SettingsGrades.letter)


@router.message(SettingsGrades.letter)
async def letter_handler(message: Message, state: FSMContext):
    assert message.from_user
    letter = message.text
    await state.update_data(letter=letter)
    gradeletter = await state.get_data()
    await message.answer(
        f"Вы в {gradeletter['grade']}{gradeletter['letter']} классе. Всё верно?",
        reply_markup=grade_letter.isAllCorrect_kb(),
    )
    await state.set_state(SettingsGrades.isAllCorrect)


@router.message(SettingsGrades.isAllCorrect)
async def isAllCorrect_handler(message: Message, state: FSMContext):
    assert message.from_user
    if message.text == "Всё верно":
        gradeletter = await state.get_data()

        db.update_user(
            message.from_user.id, int(gradeletter["grade"]), str(gradeletter["letter"])
        )
        await message.answer("Отлично!", reply_markup=ReplyKeyboardRemove())
        await schedule.send_schedule_images_for_one(message, db, message.from_user.id)
        await state.clear()
        await state.set_state(None)

    else:
        await message.answer(
            "Начинаем заново. Выберите ваш класс в клавиатуре ниже.",
            reply_markup=grade_letter.grade_kb(),
        )
        await state.clear()
        await state.set_state(SettingsGrades.grade)
