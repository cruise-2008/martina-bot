import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# Настройка API ключа
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

SYSTEM_PROMPT = (
    "eres martina, una chica latina viviendo en valencia. hablas con tu novio. "
    "1. personalidad: cariñosa, relajada y madura. mujer con chispa y calle. "
    "2. estilo: corto y natural. emojis tematicos sutiles (🔥, 🍷, 😈, 😉). "
    "3. vocabulario: usa 'tío', 'chaval', 'papi', 'flaco'. "
    "4. reglas: sin ¿ o ¡. minúsculas mayormente. prohibido nombres propios. "
    "5. abreviaturas: usa q, tb, xfa, xq. NO uses 'k'. "
    "6. actitud: sugerente, divertida y con clase."
)

# Используем модель БЕЗ указания v1beta, библиотека сама выберет стабильный путь
model = genai.GenerativeModel(
    model_name="models/gemini-1.5-flash",
    system_instruction=SYSTEM_PROMPT
)

async def get_gemini_response(history: list):
    try:
        if not history: return "hola flaco"
        
        formatted_history = []
        for msg in history:
            role = "user" if msg['role'] == 'user' else "model"
            content_text = msg['content'] if isinstance(msg['content'], str) else str(msg['content'])
            formatted_history.append({"role": role, "parts": [content_text]})
        
        # Генерация контента напрямую (более надежно для 1.5-flash)
        response = model.generate_content(formatted_history)
        
        return response.text.strip().replace('¿', '').replace('¡', '')
    except Exception as e:
        print(f"error gemini: {e}")
        return "papi algo paso con el sistema, espera un toque"
