# AI-Powered Chat Orchestrator

Streamlit app that chats with Groq, optionally summarizes the conversation, and sends that summary to n8n via webhook.

## Architecture Diagram

```mermaid
flowchart TD
		A[User] -->|Chat input| B[Streamlit UI\napp.py]
		B -->|Chat request| C[Groq API\nservices/groq_client.py]
		C -->|Model response| B
		B -->|Summarize & Send| D[Summary builder\napp.py]
		D -->|POST JSON {message}| E[n8n Webhook\nservices/n8n_client.py]
		E -->|Automation (Email, etc.)| F[Downstream actions]

		B -->|Optional doc context| G[Document Loader\nutils/doc_loader.py]
		G --> B
```

## Code Explanation

### Entry Points
- `app.py`: Streamlit UI, chat flow orchestration, summary creation, and webhook submission.
- `main.py`: Alternate entry or helper wrapper (if used) for running the app or shared orchestration.

### Services
- `services/groq_client.py`: Thin client for Groq chat completions. Responsible for API calls and model selection via env vars.
- `services/n8n_client.py`: HTTP client to post summary payloads to the configured n8n webhook.
- `services/gemini_client.py`: Optional/alternative LLM client (if configured).

### Utilities
- `utils/doc_loader.py`: Loads local documents to provide extra context for responses.

### Data Flow
1. User enters a prompt in Streamlit.
2. UI sends the request to Groq via `groq_client`.
3. Response is rendered in the chat UI.
4. When user clicks **Summarize & Send**, the app builds a short summary.
5. The summary is sent to n8n via `n8n_client` as JSON: `{ "message": "..." }`.

## Environment Variables
- `GROQ_API_KEY`: Groq API key.
- `GROQ_MODEL`: Groq model name (default in code if not set).
- `N8N_WEBHOOK_URL`: n8n webhook URL.

## Run Locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## n8n Workflow (Local)

1. Create a workflow with **Webhook** (POST) trigger.
2. Add an **Email** node (or any automation) and map `message` from incoming JSON.
3. Click **Execute workflow** to enable the test webhook.
4. Set `N8N_WEBHOOK_URL` to the test URL (uses `/webhook-test/`).
5. In the app, click **Summarize & Send**.

For production, activate the workflow and switch to the `/webhook/` URL.

## Payload Sent to n8n

```json
{
	"message": "Short summary paragraph..."
}
```
