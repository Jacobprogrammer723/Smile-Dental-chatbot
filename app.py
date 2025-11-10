# chatbot-template-multi.py – Works with all AI models
import streamlit as st
import requests

st.set_page_config(page_title="Your AI Assistant", page_icon="🤖", layout="centered")

st.markdown("""
<style>
    .main {background: #f8f9fa; padding: 2rem 1rem;}
    .header {text-align: center; padding: 2rem 0; background: white; border-radius: 20px; box-shadow: 0 4px 20px rgba(0,0,0,0.05); margin-bottom: 2rem;}
    .chat-message {padding: 1.2rem; border-radius: 15px; margin: 0.5rem 0; max-width: 80%;}
    .user-message {background: #1e90ff; color: white; margin-left: auto;}
    .assistant-message {background: #e9ecef; color: #212529;}
    .stChatInput > div > div > input {border-radius: 25px !important; padding: 0.8rem 1.5rem !important;}
</style>
""", unsafe_allow_html=True)

# === CUSTOMIZE HERE ===
CLINIC_NAME = "Your Clinic Name"
LOGO_URL = "https://via.placeholder.com/150"
CALENDAR_LINK = "https://calendly.com/your-link"
SERVICES = """
- Service 1: $99 – Description
- Service 2: $199 – Description
"""
SYSTEM_PROMPT = f"""You are AI Assistant for {CLINIC_NAME}.
Use ONLY these services:
{SERVICES}
Always ask for name + phone to book.
Book via: {CALENDAR_LINK}
Offer 10% off first visit. Perfect English."""

# === CHOOSE MODEL ===
model_choice = st.selectbox("Choose AI model", ["Grok (cheapest)", "ChatGPT (gpt-4o-mini)", "Gemini (gemini-1.5-flash)"])

if model_choice == "Grok (cheapest)":
    API_KEY = st.secrets.get("GROK_KEY")
    url = "https://api.x.ai/v1/chat/completions"
    payload = {"model": "grok-4-fast", "messages": st.session_state.messages}
elif model_choice == "ChatGPT (gpt-4o-mini)":
    API_KEY = st.secrets.get("OPENAI_KEY")
    url = "https://api.openai.com/v1/chat/completions"
    payload = {"model": "gpt-4o-mini", "messages": st.session_state.messages}
else:
    API_KEY = st.secrets.get("GEMINI_KEY")
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"
    payload = {"contents": [{"role": "user" if m["role"] == "user" else "model", "parts": [{"text": m["content"]}]} for m in st.session_state.messages]}

if not API_KEY:
    st.error(f"Add your {model_choice.split()[0]} API key in Streamlit secrets!")
    st.stop()

# === CHAT LOGIC ===
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]

# Header
with st.container():
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if LOGO_URL:
            st.image(LOGO_URL, width=100)
        st.markdown(f"<h1 style='color:#1e90ff; margin:0;'>🤖 {CLINIC_NAME}</h1>", unsafe_allow_html=True)

for msg in st.session_state.messages[1:]:
    if msg["role"] == "user":
        st.markdown(f"<div class='chat-message user-message'>{msg['content']}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='chat-message assistant-message'>{msg['content']}</div>", unsafe_allow_html=True)

if prompt := st.chat_input("Hello! How can I help today?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.markdown(f"<div class='chat-message user-message'>{prompt}</div>", unsafe_allow_html=True)
    
    with st.spinner("Thinking..."):
        try:
            if "gemini" in model_choice.lower():
                payload["contents"].append({"role": "user", "parts": [{"text": prompt}]})
                response = requests.post(f"{url}?key={API_KEY}", json=payload).json()
                answer = response["candidates"][0]["content"]["parts"][0]["text"]
            else:
                payload["messages"].append({"role": "user", "content": prompt})
                response = requests.post(url, headers={"Authorization": f"Bearer {API_KEY}"}, json=payload).json()
                answer = response["choices"][0]["message"]["content"]
            
            st.markdown(f"<div class='chat-message assistant-message'>{answer}</div>", unsafe_allow_html=True)
            st.session_state.messages.append({"role": "assistant", "content": answer})
        except Exception as e:
            st.error(f"Error: {str(e)}")

st.markdown("<p style='text-align:center; color:#888; margin-top:3rem;'>Multi-Model AI Chatbot Template • Grok + ChatGPT + Gemini • $147</p>", unsafe_allow_html=True)
