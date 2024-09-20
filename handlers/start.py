from aiogram.types import Message
from aiogram.filters import Command
from aiogram import Router
from db import Database


router = Router()
db = Database("./database.db")

@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer("Добро пожаловать в бота!")