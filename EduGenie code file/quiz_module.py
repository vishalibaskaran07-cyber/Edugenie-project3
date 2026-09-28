"""
Quiz Module
Generates 3 multiple-choice questions (4 options each) from a passage
using Gemini, and safely parses the JSON it returns.
"""

import os
import re
import json
from google import genai
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=GEMINI_API_KEY) if GEMINI_API_KEY else None


def clean_json_block(text: str) -> str:
    """Strip Markdown ```json ... ``` fences (and plain ``` fences) if present."""
    match = re.search(r"```(?:json)?\s*(.*?)```", text, flags=re.DOTALL)
    if match:
        return match.group(1).strip()
    return text.strip()


def generate_quiz(text: str) -> list:
    if not GEMINI_API_KEY:
        return [{"error": "GEMINI_API_KEY is not set. Add it to your .env file."}]

    try:
        prompt = f"""You are a quiz generator.

From the following passage, create 3 multiple-choice questions. Each question should include:
- A "question"
- A list of 4 "options"
- A correct "answer" that must exactly match one of the options.

Respond with valid JSON ONLY (no Markdown, no extra text), in this exact shape:
[
  {{
    "question": "What is ...?",
    "options": ["A", "B", "C", "D"],
    "answer": "A"
  }}
]

Passage:
{text}
"""
        chat = client.chats.create(model="gemini-3.6-flash")
        response = chat.send_message(prompt)
        quiz_text = response.text.strip()

        cleaned_text = clean_json_block(quiz_text)
        quiz = json.loads(cleaned_text)

        # basic shape validation so a malformed response doesn't crash the frontend
        if not isinstance(quiz, list):
            raise ValueError("Expected a JSON list of questions.")

        return quiz
    except json.JSONDecodeError as e:
        return [{"error": f"Could not parse quiz JSON: {e}"}]
    except Exception as e:
        return [{"error": f"Error in Quiz generation: {e}"}]
