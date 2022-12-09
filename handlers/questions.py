from aiogram import Router
from aiogram.dispatcher.filters.text import Text
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.dispatcher.fsm.context import FSMContext
from keyboards.first_question import main_question
from messages import start_message, darling_message

router = Router()  # [1]


@router.message(commands=["start"])  # [2]
async def cmd_start(message: Message):
    await message.answer(
        start_message,
        reply_markup=main_question()
    )

@router.message(Text(text= ["я больше не хочу смотреть погоду","я больше не хочу искать картинки"],
 text_ignore_case=True))
async def cmd_cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        text="Что хочешь делать дальше?",
        reply_markup=main_question()
    )

@router.message(Text(text="дарлинг", ignore_case=True))
async def darling(message: Message):
    await message.answer(darling_message)
