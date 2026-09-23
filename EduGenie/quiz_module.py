import json
import re
from typing import List

from pydantic import BaseModel, Field

from gemini_client import get_client, DEFAULT_MODEL


class QuizQuestion(BaseModel):
    question: str
    options: List[str] = Field(min_length=4, max_length=4)
    correct_answer: str
    explanation: str


class Quiz(BaseModel):
    questions: List[QuizQuestion] = Field(min_length=3, max_length=3)


def clean_json_block(text: str) -> str:
    text = text.strip()
    text = re.sub(r"^```(?:json)?\s*", "", text, flags=re.IGNORECASE)
    text = re.sub(r"\s*```$", "", text)
    return text.strip()


def _fallback_parse(text: str) -> Quiz:
    cleaned = clean_json_block(text)
    data = json.loads(cleaned)
    return Quiz.model_validate(data)


def generate_quiz(source_text: str) -> dict:
    prompt = (
        "Create exactly 3 multiple-choice questions from the educational text below. "
        "Each question must have exactly 4 options. "
        "The correct_answer must exactly match one option. "
        "Include a short explanation for the answer. "
        "Return only JSON matching the requested schema.\n\n"
        f"Educational text/topic:\n{source_text}"
    )

    client = get_client()
    response = client.models.generate_content(
        model=DEFAULT_MODEL,
        contents=prompt,
        config={
            "response_mime_type": "application/json",
            "response_schema": Quiz.model_json_schema(),
        },
    )

    raw = getattr(response, "text", None)
    if not raw:
        raise RuntimeError("Gemini returned an empty quiz response.")

    try:
        quiz = _fallback_parse(raw)
        return quiz.model_dump()
    except Exception as exc:
        raise RuntimeError(f"Quiz JSON parsing failed: {exc}") from exc
