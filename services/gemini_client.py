# import time

# import requests


# def _extract_retry_delay(data: dict) -> float | None:
#     details = data.get("error", {}).get("details", [])
#     for item in details:
#         if item.get("@type") == "type.googleapis.com/google.rpc.RetryInfo":
#             delay = item.get("retryDelay", "").strip()
#             if delay.endswith("s"):
#                 try:
#                     return float(delay[:-1])
#                 except ValueError:
#                     return None
#     return None


# def _call_gemini(prompt: str, api_key: str, model: str) -> str:
#     endpoint = (
#         f"https://generativelanguage.googleapis.com/v1beta/models/"
#         f"{model}:generateContent?key={api_key}"
#     )
#     payload = {
#         "contents": [
#             {
#                 "parts": [
#                     {"text": prompt},
#                 ]
#             }
#         ]
#     }

#     for attempt in range(3):
#         response = requests.post(endpoint, json=payload, timeout=60)
#         if response.ok:
#             break

#         if response.status_code == 429:
#             try:
#                 data = response.json()
#             except ValueError:
#                 data = {}
#             delay = _extract_retry_delay(data) or 5.0
#             if attempt < 2:
#                 time.sleep(delay)
#                 continue
#         raise RuntimeError(f"Gemini request failed: {response.status_code} {response.text}")

#     data = response.json()
#     candidates = data.get("candidates", [])
#     if not candidates:
#         raise RuntimeError("Gemini returned no candidates.")

#     parts = candidates[0].get("content", {}).get("parts", [])
#     if not parts:
#         raise RuntimeError("Gemini returned an empty response.")

#     return parts[0].get("text", "").strip()


# def _format_messages(messages: list[dict]) -> str:
#     lines = []
#     for item in messages:
#         role = item.get("role", "user")
#         content = item.get("content", "")
#         lines.append(f"{role.upper()}: {content}")
#     return "\n".join(lines)


# def generate_chat_reply(messages: list[dict], api_key: str, model: str) -> str:
#     transcript = _format_messages(messages)
#     prompt = (
#         "You are a helpful assistant. Reply to the user based on the conversation.\n\n"
#         "Conversation:\n"
#         f"{transcript}\n\n"
#         "Assistant Reply:"
#     )
#     return _call_gemini(prompt, api_key, model)


# def summarize_chat(messages: list[dict], api_key: str, model: str) -> str:
#     transcript = _format_messages(messages)
#     prompt = (
#         "Summarize the following conversation as a short paragraph. "
#         "Keep it concise and clear.\n\n"
#         "Conversation:\n"
#         f"{transcript}\n\n"
#         "Summary:"
#     )
#     return _call_gemini(prompt, api_key, model)
