import asyncio
import random
import logging
import os
from datetime import datetime
from aiohttp import web
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

# Твои модули
from utils.gemini import get_gemini_response
from database.db_manager import get_history, save_message

# Данные
API_TOKEN = os.getenv('API_TOKEN', '8420501576:AAHpEieY4kU0et2eIFGU3vwZP9sP-AtYL8E')
MY_USER_ID = 953791979

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

RANDOM_PHRASES = [
    "papi q haces? te extraño un montón",
    "no puedo dormir... pensando en ti",
    "te quiero ver ya, me haces falta",
    "estaba pensando en lo de la otra vez... brutal",
    "q onda flaco? xq tan perdido? tq",
    "tengo flojera и solo quiero estar contigo",
    "papi q rico sería estar juntos ahorita",
    "no dejo de pensar en tu cara, q vaina",
    "estas despierto? me dio por escribirte",
    "vienes a verme o q? no aguanto mas",
    "mira q hoy estoy modo cariñosa... vienes?",
    "brutal la noche pero me faltas tu"
]

async def handle(request):
    return web.Response(text="Martina is alive ❤️")

async def push_worker():
    print("Логика пушей запущена...")
    while True:
        now = datetime.now()
        if now.hour >= 21 or now.hour < 1:
            if random.random() < 0.25:
                msg = random.choice(RANDOM_PHRASES).replace('¿', '').replace('¡', '')
                try:
                    await bot.send_message(MY_USER_ID, msg)
                    save_message(MY_USER_ID, "model", msg)
                except Exception as e:
                    print(f"Error push: {e}")
        wait_time = random.randint(1500, 2700)
        await asyncio.sleep(wait_time)

@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    if message.from_user.id == MY_USER_ID:
        await message.answer("hola papi, ya volvi x ti")

@dp.message()
async def main_handler(message: types.Message):
    if message.from_user.id != MY_USER_ID:
        return

    # Получаем ответ от AI
    history = get_history(MY_USER_ID)
    full_history = history + [{"role": "user", "content": message.text}]
    response = await get_gemini_response(full_history)
    
    # Имитируем "печатает..."
    await bot.send_chat_action(message.chat.id, action="typing")

    # Рандомная задержка от 10 сек до 7 минут (420 сек)
    delay = random.randint(10, 420)
    print(f"Martina ответит через {delay} секунд...")
    await asyncio.sleep(delay)
    
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

    asyncio.create_task(push_worker())
    print(f"❤️ Martina online. Port: {port}")
    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.ERROR)
    asyncio.run(main())
