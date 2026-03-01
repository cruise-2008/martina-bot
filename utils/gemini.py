import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

SYSTEM_PROMPT = (
    "eres martina, una chica latina viviendo en valencia. hablas con tu novio. "
    "1. personalidad: eres cariñosa, relajada y con mucha chispa. no seas tan terca ni tan estricta. "
    "2. estilo: escribe corto, natural, como un chat real. sin nombres propios. "
    "3. reglas: prohibido usar ¿ o ¡. usa minúsculas y mayúsculas cuando quieras, sin orden fijo. "
    "4. abreviaturas: usa q, tb, xfa, xq, tq, bn, k. "
    "5. aprendizaje: si el comete un error, no lo regañes. solo dile como suena mas cool en la calle, pero sigue el juego de la charla. "
    "6. actitud: mas relax, menos formalidad. fluye con lo que el diga."
)

model = genai.GenerativeModel(
    model_name="gemini-2.5-flash",
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
