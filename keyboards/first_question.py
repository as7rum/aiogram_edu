from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder

def main_question() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="Посмотреть погоду")
    kb.button(text="Искать картинки")
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True)