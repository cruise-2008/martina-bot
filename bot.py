import asyncio
import random
import logging
from datetime import datetime
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

# Твои модули
from utils.gemini import get_gemini_response
from database.db_manager import get_history, save_message

# --- ДАННЫЕ ---
API_TOKEN = '8420501576:AAHpEieY4kU0et2eIFGU3vwZP9sP-AtYL8E'
MY_USER_ID = 953791979

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Список личных и ночных фраз Мартины
RANDOM_PHRASES = [
    "papi q haces? te extraño un montón",
    "no puedo dormir... pensando en ti",
    "te quiero ver ya, me haces falta",
    "estaba pensando en lo de la otra vez... brutal",
    "q onda flaco? xq tan perdido? tq",
    "tengo flojera y solo quiero estar contigo",
    "papi q rico sería estar juntos ahorita",
    "no dejo de pensar en tu cara, q vaina",
    "estas despierto? me dio por escribirte",
    "vienes a verme o q? no aguanto mas",
    "mira q hoy estoy modo cariñosa... vienes?",
    "brutal la noche pero me faltas tu"
]

async def push_worker():
    """Фоновая задача: пишет сама с 21:00 до 01:00"""
    print("Логика пушей (хочу/скучаю) запущена...")
    while True:
        now = datetime.now()
        # Интервал с 21:00 до 01:00
        if now.hour >= 21 or now.hour < 1:
            # Шанс 25% каждые 30-40 минут
            if random.random() < 0.25:
                msg = random.choice(RANDOM_PHRASES).replace('¿', '').replace('¡', '')
                try:
                    await bot.send_message(MY_USER_ID, msg)
                    save_message(MY_USER_ID, "model", msg)
                    print(f"Push enviado (cariño): {msg}")
                except Exception as e:
                    print(f"Error push: {e}")
        
        # Ждем случайное время от 25 до 45 минут, чтобы не было ровных интервалов
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

    history = get_history(MY_USER_ID)
    full_history = history + [{"role": "user", "content": message.text}]
    
    response = await get_gemini_response(full_history)
    
    save_message(MY_USER_ID, "user", message.text)
    save_message(MY_USER_ID, "model", response)
    
    await message.answer(response)

async def main():
    # Запускаем фоновую задачу для пушей
    asyncio.create_task(push_worker())
    
    print("❤️ Martina online. Пуши с 21:00 настроены.")
    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.ERROR)
    asyncio.run(main())
