# EduGenie — Google Gemini Powered Learning Assistant

EduGenie is a FastAPI + HTML/CSS educational assistant based on the supplied project document.

## Features

- Q&A
- Simple concept explanation
- 3-question MCQ quiz generation
- Passage summarization
- Beginner-to-advanced learning path recommendations
- Responsive web interface
- `/health` endpoint for configuration checking

## Architecture

```text
EduGenie/
├── main.py
├── gemini_client.py
├── explanation_module.py
├── qna.py
├── quiz_module.py
├── summary_module.py
├── learning_path.py
├── requirements.txt
├── requirements-local.txt
├── .env.example
├── README.md
├── templates/
│   └── index.html
└── static/
    ├── style.css
    └── app.js
```

## Windows + VS Code setup

1. Install Python 3.10 or newer.
2. Open this folder in VS Code.
3. Open **Terminal → New Terminal**.
4. Create a virtual environment:

```powershell
python -m venv .venv
```

5. Activate it:

```powershell
.venv\Scripts\activate
```

6. Install dependencies:

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

7. Copy `.env.example` to `.env`.
8. Put your Gemini API key in `.env`.
9. Start the server:

```powershell
python -m uvicorn main:app --reload
```

10. Open:

http://127.0.0.1:8000

## Test

Open:

http://127.0.0.1:8000/health

You should see JSON containing `"status": "ok"`.

Then test each task from the web UI.

## Optional local LaMini explanation

The project document specifies LaMini-Flan-T5-783M for concept explanation. The implementation supports it, but it is optional because the model download is much larger than the basic Gemini setup.

Install:

```powershell
pip install -r requirements-local.txt
```

Then set in `.env`:

```text
USE_LOCAL_EXPLAINER=true
```

On the first explanation request, Hugging Face Transformers downloads the model.

If the local model fails, EduGenie automatically falls back to Gemini.

## API endpoints

- `GET /`
- `GET /health`
- `POST /qa`
- `POST /explain`
- `POST /quiz`
- `POST /summarize`
- `POST /learn/recommendations`

## Notes

The original document names Gemini 1.5 Pro. This implementation uses the current Google GenAI Python SDK and a currently available Gemini model instead of hard-coding the older model name. The functional behavior remains aligned with the document.
