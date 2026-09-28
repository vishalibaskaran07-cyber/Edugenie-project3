# EduGenie: Google Gemini Powered Learning Assistant

A lightweight AI-powered educational assistant. Ask questions, get simplified
explanations, generate quizzes, summarize passages, and get personalized
learning paths.

## What was fixed from the original draft

- **quiz_module.py**: added the missing `google.generativeai`, `re`, and
  `json` imports; the Markdown-fence-stripping regex now works whether or
  not the closing fence is on its own line; added JSON shape validation and
  a friendly error instead of crashing on a bad model response.
- **qna.py / summary_module.py / learning_path.py**: added the missing
  `google.generativeai` import and API-key configuration (loaded from a
  `.env` file via `python-dotenv`), plus a clear error message if the key
  is missing instead of a raw exception.
- **explanation_module.py**: the tokenizer/model now load lazily and are
  cached (previously reloaded logic ran at import time with no caching
  guard); generation runs inside `torch.no_grad()` for correctness and
  speed.
- **main.py**: consistent endpoint paths matching the spec (`/qa`,
  `/explain`, `/quiz`, `/summarize`, `/learn/recommendations`), input
  validation on both GET and POST routes, and a proper `/` route that
  serves the frontend.
- **templates/index.html**: completed the previously cut-off HTML/JS —
  every form now calls its corresponding endpoint and renders the result,
  including interactive quiz answer-checking.

## Project structure

```
EduGenie/
├── main.py                # FastAPI app & routes
├── explanation_module.py  # Local LaMini-Flan-T5 model (concept explanations)
├── qna.py                 # Gemini-powered Q&A
├── quiz_module.py         # Gemini-powered quiz generation
├── summary_module.py      # Gemini-powered summarization
├── learning_path.py       # Gemini-powered learning path recommendations
├── templates/
│   └── index.html         # Frontend UI
├── static/
│   └── style.css          # Styling
├── requirements.txt
├── .env.example
└── README.md
```

## Prerequisites

- Python 3.10+
- A Google Gemini API key from [Google AI Studio](https://aistudio.google.com/)

## Setup

1. Create and activate a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate   # Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Add your Gemini API key:
   ```bash
   cp .env.example .env
   # then edit .env and paste your key:
   # GEMINI_API_KEY=your_actual_key
   ```

## Run locally

```bash
uvicorn main:app --reload
```

Then open **http://127.0.0.1:8000** in your browser.

## Notes

- The first request to the "Explain" feature will download the
  `MBZUAI/LaMini-Flan-T5-783M` model (a few hundred MB), so it may take a
  moment the first time.
- If `GEMINI_API_KEY` is missing, the Q&A, Summary, Quiz, and Learning
  Path features will return a clear error message instead of crashing.
