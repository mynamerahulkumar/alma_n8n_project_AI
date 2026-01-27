from openai import OpenAI


def _call_groq(prompt: str, api_key: str, model: str) -> str:
    client = OpenAI(api_key=api_key, base_url="https://api.groq.com/openai/v1")
    response = client.responses.create(
        model=model,
        input=prompt,
        temperature=0.2,
    )
    return response.output_text.strip()


def _format_messages(messages: list[dict]) -> str:
    lines = []
    for item in messages:
        role = item.get("role", "user")
        content = item.get("content", "")
        lines.append(f"{role.upper()}: {content}")
    return "\n".join(lines)


def generate_chat_reply(messages: list[dict], api_key: str, model: str) -> str:
    transcript = _format_messages(messages)
    prompt = (
        "You are a helpful assistant. Reply to the user based on the conversation.\n\n"
        "Conversation:\n"
        f"{transcript}\n\n"
        "Assistant Reply:"
    )
    return _call_groq(prompt, api_key, model)


def summarize_chat(messages: list[dict], api_key: str, model: str) -> str:
    transcript = _format_messages(messages)
    prompt = (
        "Summarize the following conversation as a short paragraph. "
        "Keep it concise and clear.\n\n"
        "Conversation:\n"
        f"{transcript}\n\n"
        "Summary:"
    )
    return _call_groq(prompt, api_key, model)
