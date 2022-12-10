from messages import start_message, scraping_start_message
import asyncio
from selenium import webdriver
from bs4 import BeautifulSoup
import time
from aiogram import Router, F, types
from aiogram.dispatcher.fsm.state import StatesGroup, State
from aiogram.dispatcher.fsm.context import FSMContext
# from aiogram.dispatcher.filters.command import Command
from aiogram.types import Message
from aiogram.dispatcher.filters import Text
from aiogram.utils.keyboard import ReplyKeyboardBuilder

router = Router()

other_markers = ["ещё картинки", 'еще', 'ещё']
other_request = ["другой запрос"]

kb = [
        [
            types.KeyboardButton(text="Ещё картинки"),
            types.KeyboardButton(text="Другой запрос"),
            types.KeyboardButton(text="Я больше не хочу искать картинки")
        ],
    ]
keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Введи запрос или выбери, что хочешь сделать дальше?"
    )

list_of_images = []
current_sending_page = 1
COUNT_FOR_SENDING = 5

scroll_num = 20
sleep_timer = 1#+=sleep_timer
limit = 20#+=limit

def get_images(var, sleep_timer, limit):

    global list_of_images
    list_of_images = []

    url = f'https://ru.pinterest.com/search/pins/?q={var}'

    options = webdriver.ChromeOptions()  
    options.add_argument('--blink-settings=imagesEnabled=false') 
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(executable_path='chromedriver.exe', options=options)
    driver.maximize_window()
    driver.get(url)
    driver.execute_script(f"document.body.style.zoom='{1}%'")
    driver.execute_script("window.dispatchEvent(new Event('resize'));")

    time.sleep(sleep_timer)

    # for i in range(1, scroll_num):
    #    driver.execute_script('window.scrollTo(1, 100000)')
    #    print ('scroll-down')
    #    time.sleep(sleep_timer)
    
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    for object in soup.findAll('img', limit=limit):

        link = object.get('src').replace('236x', '736x')
        if link not in list_of_images:
            list_of_images.append(link)

def get_five_photos():

    global list_of_images
    global current_sending_page
    
    start_index = (current_sending_page-1) * COUNT_FOR_SENDING
    images = list_of_images[start_index:start_index + COUNT_FOR_SENDING]
    current_sending_page += 1

    return images

class GetingImages(StatesGroup):
    getting_images = State()
    sending_other_images = State()

@router.message(Text(text="искать картинки", text_ignore_case=True))
async def start_weather_script(message: Message, state: FSMContext):
    
    global keyboard
    await message.answer(
        text= scraping_start_message, reply_markup=keyboard)
    # Устанавливаем пользователю состояние "выбирает название"
    await state.set_state(GetingImages.getting_images)
    

@router.message(GetingImages.sending_other_images, F.text.lower().in_(other_markers))
async def send_other_photos(message: types.Message):
    global sleep_timer
    global limit
    global current_sending_page

    if list_of_images == []:
        await message.answer('Вы еще ничего не искали!')
    else:
        if get_five_photos() == []:
            sleep_timer += 1
            limit += 20
            get_images(pin_request_input, sleep_timer, limit)
        current_sending_page -= 1
        images_link = get_five_photos()
        map_images_link = list(map(lambda x: types.InputMediaPhoto(media = x), images_link))
        await message.answer('Еще '+pin_request_input) 
        await message.answer_media_group(map_images_link)

@router.message(GetingImages.sending_other_images, F.text.lower().in_(other_request))
async def with_puree(message: types.Message, state: FSMContext):
    await message.answer("Хорошо, введите другой запрос.", 
    reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(GetingImages.getting_images)


@router.message(GetingImages.getting_images)
async def send(message: types.Message, state: FSMContext):

    # result_message = message.text.lower()

    global sleep_timer
    global limit
    global current_sending_page
    global pin_request_input
    global keyboard

    pin_request_input = message.text
    current_sending_page = 1
    get_images(message.text, sleep_timer, limit)
    images_link = get_five_photos()
    map_images_link = list(map(lambda x: types.InputMediaPhoto(media = x), images_link))
    await message.answer(pin_request_input, reply_markup=keyboard)
    await message.answer_media_group(map_images_link)
    await state.set_state(GetingImages.sending_other_images)