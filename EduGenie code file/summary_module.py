import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=GEMINI_API_KEY) if GEMINI_API_KEY else None


def summarize_text(text: str) -> str:
    try:
        if not GEMINI_API_KEY:
            return "Error in Summary: GEMINI_API_KEY is not set. Add it to your .env file."
        prompt = f"Summarize the following text in simple language:\n\n{text}"
        chat = client.chats.create(model="gemini-3.6-flash")
        response = chat.send_message(prompt)
        return response.text.strip()
    except Exception as e:
        return f"Error in Summary: {e}"
