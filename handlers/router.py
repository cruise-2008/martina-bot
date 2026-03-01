from aiogram import Router, types
from sqlalchemy import select
from database.models import async_session, User, Message
from utils.gemini import get_gemini_response
from utils.queue import msg_queue
import asyncio

router = Router()

@router.message()
async def handle_message(message: types.Message):
    async with async_session() as session:
        # Регистрация или получение пользователя
        user = await session.scalar(select(User).where(User.tg_id == message.from_user.id))
        if not user:
            user = User(tg_id=message.from_user.id, username=message.from_user.username)
            session.add(user)
        
        # Сохранение входящего сообщения
        session.add(Message(user_id=message.from_user.id, role='user', content=message.text))
        await session.commit()

        # Получение истории (последние 10 сообщений)
        history_query = await session.execute(
            select(Message.role, Message.content)
            .where(Message.user_id == message.from_user.id)
            .order_by(Message.timestamp.desc())
            .limit(10)
        )
        history = [{"role": r, "content": c} for r, c in reversed(history_query.all())]

        # Добавление задачи в очередь (с передачей функции получения ответа)
        async def wrap_gemini(hist, tg_id):
            resp = await get_gemini_response(hist)
            async with async_session() as s:
                s.add(Message(user_id=tg_id, role='model', content=resp))
                await s.commit()
            return resp

        await msg_queue.add_task(message.bot, message.chat.id, wrap_gemini, history, message.from_user.id)
