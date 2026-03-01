import asyncio
import random
from aiogram import types
from aiogram.utils.chat_action import ChatActionSender

class MessageQueue:
    def __init__(self):
        self.queue = asyncio.Queue()

    async def add_task(self, bot, chat_id, text_func, *args):
        await self.queue.put((bot, chat_id, text_func, args))

    async def worker(self):
        while True:
            bot, chat_id, text_func, args = await self.queue.get()
            try:
                # Случайная пауза перед началом "печатания" (от 1 до 3 сек)
                await asyncio.sleep(random.uniform(1, 3))
                
                async with ChatActionSender.typing(bot=bot, chat_id=chat_id):
                    # Получаем текст от Gemini
                    response_text = await text_func(*args)
                    
                    # Имитация времени набора текста в зависимости от длины сообщения
                    typing_time = len(response_text) * 0.05
                    await asyncio.sleep(min(typing_time, 5)) 
                    
                    await bot.send_message(chat_id, response_text)
            except Exception as e:
                print(f"Ошибка в очереди: {e}")
            finally:
                self.queue.task_done()

msg_queue = MessageQueue()
