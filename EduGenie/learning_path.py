from gemini_client import generate_text


def get_learning_recommendations(topic: str) -> str:
    prompt = (
        "Create a personalized educational learning path for the topic below. "
        "Assume the learner is a beginner unless otherwise stated. "
        "Organize it from beginner to intermediate to advanced. "
        "For each stage, include concepts to learn, a suggested timeline, "
        "practice ideas, and useful resource types such as videos, articles, "
        "documentation, or books. Keep the plan practical and easy to follow.\n\n"
        f"Topic: {topic}"
    )
    return generate_text(prompt)
