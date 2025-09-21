import json
import random
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from telethon import TelegramClient

# ====== aiogram ======
API_TOKEN = '8269100824:AAHRKKLsu6ONuvVI7Znfo2gYaPSMvFIGE0E'
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# ====== Telethon ======
api_id = 20826736
api_hash = 'a6f86b57c3a12acf9fe2865cc6fce1e1'
channel = 'pure_cognitions_adhd'
telethon_client = TelegramClient('session_name', api_id, api_hash)

# ====== Главное меню ======
keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
keyboard.add(KeyboardButton('📚 Материалы по СДВГ'))
keyboard.add(KeyboardButton('💻 Коворкинг онлайн'))
keyboard.add(KeyboardButton('💛 Поддержка'))

# ====== Загрузка материалов и коворкинга ======
def load_materials():
    try:
        with open('materials.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return []

def load_coworking():
    try:
        with open('coworking.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return {}

materials = load_materials()
coworking_links = load_coworking()

# ====== Функция обновления материалов с канала ======
async def update_materials():
    global materials
    async with telethon_client:
        async for message in telethon_client.iter_messages(channel, limit=20):
            if message.message and '#adhd' in message.message.lower():
                item = {
                    "title": message.message.split('\n')[0],
                    "link": f"https://t.me/{channel}/{message.id}",
                    "description": message.message[:200] + "..."
                }
                if item not in materials:
                    materials.append(item)
        with open('materials.json', 'w', encoding='utf-8') as f:
            json.dump(materials, f, ensure_ascii=False, indent=2)

# ====== Хендлеры aiogram ======
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await update_materials()
    await message.answer("Привет! Выбирай опцию:", reply_markup=keyboard)

@dp.message_handler(lambda m: m.text == '📚 Материалы по СДВГ')
async def send_material(message: types.Message):
    await update_materials()
    material = random.choice(materials)
    await message.answer(f"{material['title']}\n{material['description']}\nСсылка: {material['link']}")

@dp.message_handler(lambda m: m.text == '💻 Коворкинг онлайн')
async def send_coworking_menu(message: types.Message):
    days_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    for day in coworking_links.keys():
        days_keyboard.add(KeyboardButton(day))
    days_keyboard.add(KeyboardButton('Главное меню'))
    await message.answer("Выбери день:", reply_markup=days_keyboard)

@dp.message_handler(lambda m: m.text in coworking_links.keys())
async def send_zoom_link(message: types.Message):
    link = coworking_links[message.text]
    await message.answer(f"Ссылка на Zoom для {message.text}: {link}")

@dp.message_handler(lambda m: m.text == 'Главное меню')
async def back_to_main(message: types.Message):
    await message.answer("Главное меню:", reply_markup=keyboard)

@dp.message_handler(lambda m: m.text == '💛 Поддержка')
async def send_support(message: types.Message):
    await message.answer("С тобой всё хорошо! 💛")

# ====== Запуск бота ======
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
