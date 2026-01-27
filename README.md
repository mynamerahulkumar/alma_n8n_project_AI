
# AI-Powered Chat Orchestrator

Simple Streamlit app that chats with Groq and sends a short summary to n8n on demand.

## Features
- Groq chat via API key
- Summary-on-demand
- User-triggered email automation with n8n webhook
- Works locally

## Setup

https://docs.n8n.io/integrations/creating-nodes/test/run-node-locally/
n8n start

### 1) Install dependencies

```bash
pip install -r requirements.txt
```

### 2) Set environment variables

```bash
export GROQ_API_KEY="your_api_key"
export N8N_WEBHOOK_URL="http://localhost:5678/webhook/your-webhook-path"
export GROQ_MODEL="openai/gpt-oss-120b"
```

### 3) Run the app

```bash
streamlit run app.py
```

## n8n Workflow (Local)

### A) Create and test the workflow
1) Create a new workflow and add a **Webhook** trigger (POST).
2) Add an **Email** node and map the incoming JSON field:
   - `message`
3) Click **Execute workflow** on the canvas to enable the test webhook.
4) In your `.env`, set:

```bash
N8N_WEBHOOK_URL="http://localhost:5678/webhook-test/your-path"
```

5) In the Streamlit app, click **Summarize & Send**.

> In test mode, the webhook only works once after you click **Execute workflow**. Click it again for another test call.

### B) Activate for production use
1) Activate the workflow (toggle in n8n).
2) Copy the production webhook URL (starts with `/webhook/`).
3) Update `.env`:

```bash
N8N_WEBHOOK_URL="http://localhost:5678/webhook/your-path"
```

## Payload Sent to n8n

```json
{
	"message": "Short summary paragraph..."
}
```
