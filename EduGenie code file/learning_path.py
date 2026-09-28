"""
Learning Path Module
Generates a personalized, structured learning path (beginner -> advanced)
for a given topic using Gemini.
"""

import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=GEMINI_API_KEY) if GEMINI_API_KEY else None


def get_learning_recommendations(topic: str) -> str:
    if not GEMINI_API_KEY:
        return "Error occurred: GEMINI_API_KEY is not set. Add it to your .env file."

    prompt = f"""You are an AI tutor. The student wants to learn about: {topic}.
Suggest a structured and adaptive learning path including key topics, order of
learning, and useful resources (videos, articles, or books).
Include beginner, intermediate, and advanced levels if needed.
"""
    try:
        chat = client.chats.create(model="gemini-3.6-flash")
        response = chat.send_message(prompt)

        if hasattr(response, "text") and response.text:
            return response.text
        elif hasattr(response, "parts") and response.parts:
            return response.parts[0].text
        else:
            return "Could not extract content from Gemini response."
    except Exception as e:
        return f"Error occurred: {e}"
