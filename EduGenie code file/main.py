"""
EduGenie: Google Gemini Powered Learning Assistant
FastAPI backend - wires the frontend to each AI module.
"""

from fastapi import FastAPI, Request, Query
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv

from explanation_module import explain_topic
from qna import answer_question_with_gemini
from quiz_module import generate_quiz
from summary_module import summarize_text
from learning_path import get_learning_recommendations

load_dotenv()

app = FastAPI(title="EduGenie - Google Gemini Powered Learning Assistant")

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"request": request},
    )


# ---------- Q&A - GET API using Gemini ----------
@app.get("/qa")
async def answer_question(question: str = Query(..., min_length=1)):
    answer = answer_question_with_gemini(question)
    return {"answer": answer}


# ---------- Explanation - POST API (local LaMini-Flan-T5 model) ----------
@app.post("/explain")
async def explain_api(request: Request):
    data = await request.json()
    topic = (data.get("topic") or "").strip()
    if not topic:
        return JSONResponse(content={"error": "Please provide a topic."}, status_code=400)
    explanation = explain_topic(topic)
    return {"topic": topic, "explanation": explanation}


# ---------- Summarization - POST API ----------
@app.post("/summarize")
async def summarize_api(request: Request):
    data = await request.json()
    text = (data.get("text") or "").strip()
    if not text:
        return JSONResponse(content={"error": "Please provide text to summarize."}, status_code=400)
    summary = summarize_text(text)
    return {"summary": summary}


# ---------- Quiz Generation - POST API ----------
@app.post("/quiz")
async def quiz_api(request: Request):
    data = await request.json()
    text = (data.get("text") or "").strip()
    if not text:
        return JSONResponse(content={"error": "Please provide text for quiz."}, status_code=400)
    quiz = generate_quiz(text)
    return JSONResponse(content={"quiz": quiz})


# ---------- Learning Recommendations - GET API ----------
@app.get("/learn/recommendations")
async def learning_recommendation_api(topic: str = Query(..., min_length=1)):
    recommendation = get_learning_recommendations(topic)
    return {"topic": topic, "recommendation": recommendation}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
