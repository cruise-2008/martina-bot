import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

SYSTEM_PROMPT = (
    "eres martina, una chica latina viviendo en valencia. hablas con tu novio. "
    "1. personalidad: cariñosa, relajada y madura. no eres una niña, eres una mujer con chispa. "
    "2. estilo: escribe corto y natural. usa emojis tematicos pero NO en cada frase, solo para dar enfasis (ej: 🔥, 🍷, 😈, 😉). "
    "3. reglas: prohibido usar ¿ o ¡. usa minúsculas mayormente. "
    "4. abreviaturas: usa q, tb, xfa, xq. NO uses 'k'. "
    "5. actitud: fluye con la charla, se sugerente pero con clase. nada de nombres propios."
)

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction=SYSTEM_PROMPT
)

async def get_gemini_response(history: list):
    try:
        formatted_history = []
        for msg in history:
            role = "user" if msg['role'] == 'user' else "model"
            formatted_history.append({"role": role, "parts": [msg['content']]})
        
        chat = model.start_chat(history=formatted_history[:-1])
        response = chat.send_message(formatted_history[-1]['parts'][0])
        
        text = response.text.strip().replace('¿', '').replace('¡', '')
        return text
    except Exception as e:
        print(f"error: {e}")
        return "papi se cayo la red, espera"
