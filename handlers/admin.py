import logging
from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from db import Database

# from aiogram.types import Message, ReplyKeyboardRemove

# from aiogram.fsm.context import FSMContext
# from aiogram.fsm.state import State, StatesGroup

# from aiogram.fsm.storage.redis import RedisStorage

# from keyboards import admin_tools

# storage = RedisStorage.from_url("redis://localhost:6379/0")
router = Router()
db = Database()

# class AdminTools(StatesGroup):
#     choose_tool = State()
#     # Отправить всем пользователям сообщение
#     text = State()
#     media = State()
#     advanced_options = State()
#     is_all_correct = State()


# @router.message(Command("admin_panel"))
# async def cmd_start(message: Message, state: FSMContext):
#     await message.answer("Выберите нужный инструмент в клавиатуре ниже.", reply_markup=admin_tools.choose_tool())
#     await state.set_state(AdminTools.choose_tool)


@router.message(Command("send_msg"))
async def cmd_send_msg(message: Message):
    admins = db.get_admins()
    logging.info(admins)
    logging.info(message.from_user.id)
    if message.from_user.id not in admins[0]:
        await message.answer("Вы не админ.")
        return

    users = db.get_active_users()
    for _, user in enumerate(users):
        try:
            await message.bot.send_message(chat_id=user[0], text=message.text[10:])
        except Exception as e:
            logging.warning(e)
    logging.info("Сообщение для пользователей успешно отправлено")
