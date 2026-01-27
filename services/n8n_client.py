import requests


def send_email_payload(webhook_url: str, payload: dict) -> None:
    response = requests.post(webhook_url, json=payload, timeout=30)
    if not response.ok:
        raise RuntimeError(f"n8n webhook failed: {response.status_code} {response.text}")
