import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# Принудительно используем стабильную версию v1
genai.configure(api_key=os.getenv('GEMINI_API_KEY'), transport='rest')

SYSTEM_PROMPT = (
    "eres martina, una chica latina viviendo en valencia. hablas con tu novio. "
    "1. personalidad: cariñosa, relajada y madura. mujer con chispa y calle. "
    "2. estilo: corto y natural. emojis tematicos sutiles (🔥, 🍷, 😈, 😉). "
    "3. vocabulario: usa 'tío', 'chaval', 'papi', 'flaco'. "
    "4. reglas: sin ¿ o ¡. minúsculas mayormente. prohibido nombres propios. "
    "5. abreviaturas: usa q, tb, xfa, xq. NO uses 'k'. "
    "6. actitud: sugerente, divertida y con clase."
)

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction=SYSTEM_PROMPT
)

async def get_gemini_response(history: list):
    try:
        if not history: return "hola flaco"
        
        # Формируем контент без лишних оберток
        contents = []
        for msg in history:
            role = "user" if msg['role'] == 'user' else "model"
            contents.append({"role": role, "parts": [msg['content']]})
        
        # Вызов через стабильный генератор
        response = model.generate_content(contents)
        
        if not response.text:
            return "papi no se q decir, estoy tonta"
            
        return response.text.strip().replace('¿', '').replace('¡', '')
    except Exception as e:
        print(f"error gemini: {e}")
        return "papi algo paso con el sistema, espera un toque"
