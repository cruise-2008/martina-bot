import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

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

model = genai.GenerativeModel(
    model_name="gemini-2.0-flash",
    system_instruction=SYSTEM_PROMPT
)

async def get_gemini_response(history: list):
    try:
        formatted_history = []
        for msg in history:
            role = "user" if msg['role'] == 'user' else "model"
            # Передаем только строку контента, чтобы избежать ошибки Blob
            content_text = msg['content'] if isinstance(msg['content'], str) else str(msg['content'])
            formatted_history.append({"role": role, "parts": [content_text]})
        
        chat = model.start_chat(history=formatted_history[:-1])
        response = chat.send_message(formatted_history[-1]['parts'][0])
        
        text = response.text.strip().replace('¿', '').replace('¡', '')
        return text
    except Exception as e:
        print(f"error gemini: {e}")
        return "papi algo paso con el sistema, espera un toque"
