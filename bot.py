import os
import asyncio
import random
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from telethon import TelegramClient
from telethon.tl.types import MessageMediaPhoto, MessageMediaDocument

# === Переменные окружения ===
BOT_TOKEN = os.getenv("BOT_TOKEN")
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

telethon_client = TelegramClient('session_name', API_ID, API_HASH)
CHANNEL_USERNAME = "pure_cognitions_adhd"
coworking_links = ["https://zoom.us/j/1234567890"]

keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
keyboard.add(KeyboardButton("Материалы СДВГ"))
keyboard.add(KeyboardButton("Коворкинг"))
keyboard.add(KeyboardButton("Интервал"))
keyboard.add(KeyboardButton("Поддержка"))

@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    await message.answer("Привет! Выбери опцию:", reply_markup=keyboard)

@dp.message_handler(lambda m: m.text == "Материалы СДВГ")
async def send_material(message: types.Message):
    await telethon_client.start()
    async for post in telethon_client.iter_messages(CHANNEL_USERNAME, limit=10):
        text = post.message or ""
        chunks = [text[i:i+1024] for i in range(0, len(text), 1024)]
        for chunk in chunks:
            await message.answer(chunk)
        if isinstance(post.media, MessageMediaPhoto):
            await message.answer_photo(post.photo)
        elif isinstance(post.media, MessageMediaDocument):
            await message.answer_document(post.document)

@dp.message_handler(lambda m: m.text == "Коворкинг")
async def coworking(message: types.Message):
    if coworking_links:
        link = random.choice(coworking_links)
        await message.answer(f"Присоединяйся к коворкингу: {link}")
    else:
        await message.answer("Ссылки коворкинга пока нет 😅")

@dp.message_handler(lambda m: m.text == "Интервал")
async def interval(message: types.Message):
    total_seconds = 20 * 60
    for remaining in range(total_seconds, 0, -1):
        mins, secs = divmod(remaining, 60)
        await message.answer(f"Осталось: {mins:02d}:{secs:02d}")
        await asyncio.sleep(60)
    await message.answer("⏰ Таймер завершён! С тобой всё в порядке 🔔")

@dp.message_handler(lambda m: m.text == "Поддержка")
async def support(message: types.Message):
    await message.answer("С тобой всё в порядке ❤️")

if __name__ == "__main__":
    import nest_asyncio
    nest_asyncio.apply()
    from aiogram.utils import executor
    executor.start_polling(dp, skip_updates=True)









