from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

def main_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.add(KeyboardButton(text="Сегодня"))
    kb.add(KeyboardButton(text="Завтра"))
    kb.add(KeyboardButton(text="Настройки"))
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True)