import os
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from explanation_module import explain_topic
from qna import answer_question
from quiz_module import generate_quiz
from summary_module import summarize_text
from learning_path import get_learning_recommendations

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent

app = FastAPI(
    title="EduGenie",
    description="Google Gemini powered learning assistant",
    version="1.0.0",
)

app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
templates = Jinja2Templates(directory=BASE_DIR / "templates")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
    request=request,
    name="index.html",
    context={"app_name": "EduGenie"},
)


@app.get("/health")
async def health():
    return {
        "status": "ok",
        "gemini_configured": bool(os.getenv("GEMINI_API_KEY")),
        "local_explainer_enabled": os.getenv("USE_LOCAL_EXPLAINER", "false").lower() == "true",
    }


@app.post("/qa")
async def qa(question: str = Form(...)):
    question = question.strip()
    if not question:
        raise HTTPException(status_code=400, detail="Please enter a question.")
    return JSONResponse({"result": answer_question(question)})


@app.post("/explain")
async def explain(topic: str = Form(...)):
    topic = topic.strip()
    if not topic:
        raise HTTPException(status_code=400, detail="Please enter a topic.")
    return JSONResponse({"result": explain_topic(topic)})


@app.post("/quiz")
async def quiz(text: str = Form(...)):
    text = text.strip()
    if not text:
        raise HTTPException(status_code=400, detail="Please enter a topic or passage.")
    return JSONResponse({"result": generate_quiz(text)})


@app.post("/summarize")
async def summarize(text: str = Form(...)):
    text = text.strip()
    if not text:
        raise HTTPException(status_code=400, detail="Please enter text to summarize.")
    return JSONResponse({"result": summarize_text(text)})


@app.post("/learn/recommendations")
async def learn(topic: str = Form(...)):
    topic = topic.strip()
    if not topic:
        raise HTTPException(status_code=400, detail="Please enter a topic.")
    return JSONResponse({"result": get_learning_recommendations(topic)})
