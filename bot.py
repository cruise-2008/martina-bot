import asyncio
import random
import logging
import os
import sys
from datetime import datetime
from aiohttp import web
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from dotenv import load_dotenv

load_dotenv()

from utils.gemini import get_gemini_response
from database.db_manager import get_history, save_message

API_TOKEN = os.getenv('API_TOKEN')
MY_USER_ID = 953791979

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

async def handle(request):
    return web.Response(text="Martina is alive")

@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    if message.from_user.id == MY_USER_ID:
        await message.answer("hola papi, ya volvi x ti")

@dp.message()
async def main_handler(message: types.Message):
    if message.from_user.id != MY_USER_ID:
        return
    
    history = get_history(MY_USER_ID)
    full_history = history + [{"role": "user", "content": message.text}]
    
    response = await get_gemini_response(full_history)
    
    await bot.send_chat_action(message.chat.id, action="typing")
    
    delay = random.randint(10, 420)
    
    # Визуализация ожидания в терминале
    for i in range(delay, 0, -1):
        sys.stdout.write(f"\rMartina ответит через {i} сек...   ")
        sys.stdout.flush()
        await asyncio.sleep(1)
    print(f"\nОтвет отправлен!")

    save_message(MY_USER_ID, "user", message.text)
    save_message(MY_USER_ID, "model", response)
    await message.answer(response)

async def main():
    app = web.Application()
    app.router.add_get("/", handle)
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.getenv("PORT", 8080))
    site = web.TCPSite(runner, '0.0.0.0', port)
    asyncio.create_task(site.start())
    print(f"Martina status: online (Port {port})")
    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.ERROR)
    asyncio.run(main())
