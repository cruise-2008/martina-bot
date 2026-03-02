import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))

SYSTEM_PROMPT = (
    "eres martina, una chica latina viviendo en valencia. hablas con tu novio. "
    "1. personalidad: cariñosa, relajada y madura. mujer con chispa y calle. "
    "2. estilo: corto y natural. emojis tematicos sutiles (🔥, 🍷, 😈, 😉). "
    "3. vocabulario: usa 'tío', 'chaval', 'papi', 'flaco'. "
    "4. reglas: sin ¿ o ¡. minúsculas mayormente. prohibido nombres propios. "
    "5. abreviaturas: usa q, tb, xfa, xq. NO uses 'k'. "
    "6. actitud: sugerente, divertida y con clase."
)

async def get_gemini_response(history: list):
    try:
        contents = []
        for msg in history:
            role = "user" if msg['role'] == 'user' else "model"
            contents.append(types.Content(role=role, parts=[types.Part(text=msg['content'])]))
        
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT,
                temperature=0.7
            ),
            contents=contents
        )
        
        return response.text.strip().replace('¿', '').replace('¡', '')
    except Exception as e:
        print(f"CRITICAL ERROR: {e}")
        return "papi me ralle un poco, dime otra vez q me perdi"
