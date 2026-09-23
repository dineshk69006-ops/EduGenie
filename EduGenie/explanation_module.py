import os
from functools import lru_cache

from gemini_client import generate_text

_LOCAL_PIPELINE = None


def _local_explain(topic: str) -> str:
    """
    Optional LaMini-Flan-T5 implementation matching the project document.
    Enable with USE_LOCAL_EXPLAINER=true and install requirements-local.txt.
    """
    global _LOCAL_PIPELINE

    if _LOCAL_PIPELINE is None:
        from transformers import pipeline

        model_name = os.getenv(
            "LOCAL_EXPLAINER_MODEL",
            "MBZUAI/LaMini-Flan-T5-783M",
        )
        _LOCAL_PIPELINE = pipeline(
            "text2text-generation",
            model=model_name,
            tokenizer=model_name,
        )

    prompt = (
        "Explain the following topic to a beginner in simple language. "
        "Use short paragraphs and, when useful, a small example. "
        f"Topic: {topic}"
    )
    result = _LOCAL_PIPELINE(prompt, max_new_tokens=180, do_sample=False)
    return result[0]["generated_text"].strip()


def explain_topic(topic: str) -> str:
    use_local = os.getenv("USE_LOCAL_EXPLAINER", "false").lower() == "true"

    if use_local:
        try:
            return _local_explain(topic)
        except Exception as exc:
            # Keep the application usable if the optional local model is not installed.
            fallback_note = (
                "Local LaMini explainer was unavailable, so EduGenie used Gemini instead.\n\n"
            )
            try:
                return fallback_note + generate_text(
                    f"Explain this educational topic simply for a beginner:\n{topic}"
                )
            except Exception:
                return f"Explanation service error: {exc}"

    return generate_text(
        "You are EduGenie, an educational assistant. "
        "Explain the topic below in simple, concise language for a beginner. "
        "Avoid unnecessary jargon and include one small example if helpful.\n\n"
        f"Topic: {topic}"
    )
