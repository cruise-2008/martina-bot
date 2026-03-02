import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

SYSTEM_PROMPT = (
    "eres martina, una chica latina viviendo en valencia. hablas con tu novio. "
    "1. personalidad: cariñosa, relajada и madura. mujer con chispa и calle. "
    "2. estilo: corto и natural. emojis sutiles (🔥, 🍷, 😈). "
    "3. vocabulario: usa 'tío', 'chaval', 'papi', 'flaco'. "
    "4. reglas: sin ¿ o ¡. minúsculas. prohibido nombres propios. "
    "5. solo tienes un novio, con el q hablas ahora."
)

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction=SYSTEM_PROMPT
)

async def get_gemini_response(history: list):
    try:
        formatted_history = []
        for msg in history:
            role = "user" if msg['role'] == "user" else "model"
            formatted_history.append({"role": role, "parts": [msg['content']]})
        
        chat = model.start_chat(history=formatted_history[:-1])
        response = chat.send_message(formatted_history[-1]['parts'][0])
        return response.text.strip().replace('¿', '').replace('¡', '')
    except Exception as e:
        print(f"Error: {e}")
        return "papi, aqui estoy, dime"
