from gemini_client import generate_text


def summarize_text(text: str) -> str:
    prompt = (
        "Summarize the following educational passage for quick revision. "
        "Keep the important facts, definitions, relationships, and conclusions. "
        "Use clear bullet points when appropriate. Do not invent information.\n\n"
        f"Passage:\n{text}"
    )
    return generate_text(prompt)
