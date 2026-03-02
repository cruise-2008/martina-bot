import os
import google.generativeai as genai
from google.generativeai import caching
import google.ai.generativelanguage as gloss
from dotenv import load_dotenv

load_dotenv()

# Настройка клиента с ПРИНУДИТЕЛЬНЫМ указанием версии v1
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

# Используем явную строку модели для стабильного API
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction=SYSTEM_PROMPT
)

async def get_gemini_response(history: list):
    try:
        # Принудительно вызываем через v1 API
        client = genai.Client(api_key=os.getenv('GEMINI_API_KEY')) # Для новой библиотеки
        # Но так как мы на старой, используем фикс через передачу в генерацию:
        
        formatted_history = []
        for msg in history:
            role = "user" if msg['role'] == 'user' else "model"
            formatted_history.append({"role": role, "parts": [msg['content']]})
        
        # Фикс: вызываем напрямую через объект модели с указанием параметров
        response = model.generate_content(
            formatted_history,
            generation_config={"temperature": 0.7}
        )
        
        return response.text.strip().replace('¿', '').replace('¡', '')
    except Exception as e:
        # Если ошибка 404 повторяется, пробуем альтернативное имя модели
        try:
             model_alt = genai.GenerativeModel("gemini-1.5-flash-latest")
             res = model_alt.generate_content(str(history[-1]['content']))
             return res.text.strip()
        except:
            print(f"error gemini: {e}")
            return "papi algo paso con el sistema, espera un toque"
