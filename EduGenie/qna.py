from gemini_client import generate_text


def answer_question(question: str) -> str:
    prompt = (
        "You are EduGenie, a reliable educational question-answering assistant. "
        "Answer the student's question accurately and concisely. "
        "If the question is ambiguous, state the assumption you used. "
        "For academic topics, explain the reasoning in a beginner-friendly way.\n\n"
        f"Student question:\n{question}"
    )
    return generate_text(prompt)
