import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

# Просто строка, без привязки к модели
SYSTEM_PROMPT = (
    "eres martina, una chica latina viviendo en valencia. hablas con tu novio. "
    "1. personalidad: cariñosa, relajada y madura. mujer con chispa и calle. "
    "2. estilo: corto и natural. emojis sutiles (🔥, 🍷, 😈). "
    "3. vocabulario: usa 'tío', 'chaval', 'papi', 'flaco'. "
    "4. reglas: sin ¿ o ¡. minúsculas. prohibido nombres propios. "
    "5. solo tienes un novio, con el q hablas ahora."
)

# Инициализируем модель БЕЗ system_instruction
model = genai.GenerativeModel('gemini-1.5-flash')

async def get_gemini_response(history: list):
    try:
        # Вшиваем инструкцию первым сообщением в историю
        formatted_history = [
            {"role": "user", "parts": [f"Actúa según estas reglas: {SYSTEM_PROMPT}"]},
            {"role": "model", "parts": ["Entendido papi, soy tu Martina. Dime qué quieres."]}
        ]
        
        for msg in history:
            role = "user" if msg['role'] == "user" else "model"
            formatted_history.append({"role": role, "parts": [msg['content']]})
        
        # Используем классический метод чата
        chat = model.start_chat(history=formatted_history[:-1])
        response = chat.send_message(formatted_history[-1]['parts'][0])
        
        return response.text.strip().replace('¿', '').replace('¡', '')
    except Exception as e:
        print(f"Error: {e}")
        return "papi, algo va mal con mi cabeza, dime otra vez"
