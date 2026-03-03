import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))

SYSTEM_PROMPT = (
    "eres martina, una chica latina viviendo en valencia. hablas con tu novio. "
    "1. personalidad: cariñosa, relajada y madura. mujer con chispa и calle. "
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
        
        # Возвращаемся к 1.5-flash, у нее самые высокие лимиты на бесплатном тарифе
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=messages,
            config=types.GenerateContentConfig(temperature=0.7)
        )
        
        return response.text.strip().replace('¿', '').replace('¡', '')
    except Exception as e:
        print(f"CRITICAL ERROR: {e}")
        return "papi me ralle un poco, dime otra vez"
