import requests
import datetime
from config import open_weather_token
from messages import weather_start_message
from aiogram.dispatcher.filters.text import Text
from aiogram.dispatcher.fsm.state import StatesGroup, State
from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram import Router, types

from keyboards.simple_row import make_row_keyboard

cancle_weather_state_botton = ['Я больше не хочу смотреть погоду']

router = Router()

class GetingWeather(StatesGroup):
    getting_weather = State()

@router.message(Text(text="посмотреть погоду", text_ignore_case=True))
async def start_weather_script(message: Message, state: FSMContext):
    await message.answer(
        text= weather_start_message,
        reply_markup=make_row_keyboard(cancle_weather_state_botton)
    )
    # Устанавливаем пользователю состояние "выбирает название"
    await state.set_state(GetingWeather.getting_weather)

@router.message(GetingWeather.getting_weather)
async def get_weather(message: types.Message):

    code_to_smile = {
        'Clear': 'Ясно \N{black sun with rays}',
        'Clouds': 'Облачно \N{sun behind cloud}',
        'Rain': 'Дождь \N{umbrella with rain drops}',
        'Drizzle': 'Дождь \N{umbrella with rain drops}',
        'Thunderstorm': 'Гроза \N{high voltage sign}',
        'Snow': 'Снег \N{snowflake}',
        'Mist': 'Туман \N{foggy}',

}

    try:
        r = requests.get(
            f'https://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={open_weather_token}&units=metric')
    
        data = r.json()

        city = data['name']

        weather_discription = data['weather'][0]['main']

        if weather_discription in code_to_smile:
            wd = code_to_smile[weather_discription]
        else:
            wd = 'Лучше выгляни ка в окно...'

        cur_weather = data['main']['temp']
        humidity = data['main']['humidity']
        pressure = data['main']['pressure']
        wind = data['wind']['speed']
        sunrise_timestamp = datetime.datetime.fromtimestamp(data['sys']['sunrise'])
        sunset_timestamp = datetime.datetime.fromtimestamp(data['sys']['sunset'])
        length_of_the_day = sunset_timestamp - sunrise_timestamp

        await message.reply(#f'___{datetime.datetime.now().strftime('%d')}___\n'
            f'Погода в {city}:\n\n {wd}\n\n🌡  Температура: {cur_weather}C°\n\n'
            f'💧  Влажность: {humidity}%\n\n⚗️  Давление: {pressure} мм.рт.ст.\n\n🌬  Ветер: {wind} м/с\n\n'
            f'🌄  Восход солнца: {sunrise_timestamp}\n\n🌇  Заход солнца: {sunset_timestamp}\n\n'
            f'🌏  Продолжительность дня: {length_of_the_day}\n\n'
            f'Хорошего дня! ✨')


    except Exception as ex:
        await message.reply('\N{heavy exclamation mark symbol} Проверьте название города \N{heavy exclamation mark symbol}')