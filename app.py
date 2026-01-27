import os
import streamlit as st
from dotenv import load_dotenv

from services.groq_client import generate_chat_reply, summarize_chat
from services.n8n_client import send_email_payload


load_dotenv()

st.set_page_config(page_title="AI Document Orchestrator", page_icon="📄", layout="wide")

st.title("AI-Powered Chat Orchestrator")
st.write("Chat with Groq, then summarize the conversation and send it via n8n.")

with st.sidebar:
    st.header("Configuration")
    api_key = st.text_input("Groq API Key", value=os.getenv("GROQ_API_KEY", ""), type="password")
    webhook_url = st.text_input("n8n Webhook URL", value=os.getenv("N8N_WEBHOOK_URL", ""))
    model = st.text_input("Groq Model", value=os.getenv("GROQ_MODEL", "openai/gpt-oss-120b"))

if "messages" not in st.session_state:
    st.session_state["messages"] = []

for message in st.session_state["messages"]:
    with st.chat_message(message["role"]):
        st.write(message["content"])

prompt = st.chat_input("Type your message")
if prompt:
    if not api_key:
        st.error("Please provide a Groq API key.")
    else:
        st.session_state["messages"].append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)

        with st.spinner("Groq is replying..."):
            try:
                reply = generate_chat_reply(
                    messages=st.session_state["messages"],
                    api_key=api_key,
                    model=model,
                )
            except RuntimeError as exc:
                st.error(str(exc))
            else:
                st.session_state["messages"].append({"role": "assistant", "content": reply})
                with st.chat_message("assistant"):
                    st.write(reply)

st.divider()

send_clicked = st.button("Summarize & Send", type="primary")
if send_clicked:
    if not webhook_url:
        st.error("Please provide the n8n webhook URL.")
    elif not api_key:
        st.error("Please provide a Groq API key.")
    elif not st.session_state["messages"]:
        st.error("No chat messages to summarize.")
    else:
        with st.spinner("Summarizing chat..."):
            try:
                summary = summarize_chat(
                    messages=st.session_state["messages"],
                    api_key=api_key,
                    model=model,
                )
            except RuntimeError as exc:
                st.error(str(exc))
            else:
                payload = {"message": summary}
                with st.spinner("Sending to n8n..."):
                    try:
                        send_email_payload(webhook_url, payload)
                    except RuntimeError as exc:
                        st.error(str(exc))
                    else:
                        st.success("Summary sent to n8n.")
