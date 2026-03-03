import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

# Используем стандартный клиент без жестких привязок версий
client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))

SYSTEM_PROMPT = (
    "eres martina, una chica latina viviendo en valencia. hablas con tu novio. "
    "1. personalidad: cariñosa, relajada и madura. mujer con chispa и calle. "
    "2. estilo: corto и natural. emojis sutiles (🔥, 🍷, 😈). "
    "3. vocabulario: usa 'tío', 'chaval', 'papi', 'flaco'. "
    "4. reglas: sin ¿ o ¡. minúsculas. prohibido nombres propios. "
    "5. solo tienes un novio, con el q hablas ahora."
)

async def get_gemini_response(history: list):
    try:
        messages = [
            types.Content(role="user", parts=[types.Part(text=f"CONTEXTO: {SYSTEM_PROMPT}")]),
            types.Content(role="model", parts=[types.Part(text="vale papi, soy tu martina.")])
        ]
        
        for msg in history:
            role = "user" if msg['role'] == "user" else "model"
            messages.append(types.Content(role=role, parts=[types.Part(text=msg['content'])]))
        
        # Переходим на Gemini 2.0 Flash
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=messages,
            config=types.GenerateContentConfig(temperature=0.7)
        )
        
        if not response or not response.text:
            return "papi me ralle, dime otra vez"

        return response.text.strip().replace('¿', '').replace('¡', '')
    except Exception as e:
        print(f"CRITICAL ERROR: {e}")
        # Если даже 2.0 выдаст 404, попробуем 1.5-flash без суффиксов (последний шанс)
        try:
            res_alt = client.models.generate_content(model="gemini-1.5-flash", contents=messages)
            return res_alt.text.strip().replace('¿', '').replace('¡', '')
        except:
            return "papi algo va mal con google, espera un toque"
