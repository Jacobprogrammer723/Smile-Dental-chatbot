# grok-chatbot-template.py – FIXED: No more AttributeError
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

# === API KEY ===
API_KEY = st.secrets.get("GROK_KEY")
if not API_KEY:
    st.error("Add your Grok API key in Streamlit secrets (GROK_KEY)")
    st.stop()

# === INIT MESSAGES IF NOT EXISTS ===
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]

# === HEADER ===
with st.container():
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if LOGO_URL:
            st.image(LOGO_URL, width=100)
        st.markdown(f"<h1 style='color:#1e90ff; margin:0;'>🤖 {CLINIC_NAME}</h1>", unsafe_allow_html=True)
        st.markdown("<p style='color:#666;'>24/7 AI Assistant – Book, Ask, Smile</p>", unsafe_allow_html=True)

# === CHAT ===
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
            payload = {
                "model": "grok-4-fast",
                "messages": st.session_state.messages  # NU FUNKAR DET!
            }
            response = requests.post(
                "https://api.x.ai/v1/chat/completions",
                headers={"Authorization": f"Bearer {API_KEY}"},
                json=payload
            ).json()
            answer = response["choices"][0]["message"]["content"]
            st.markdown(f"<div class='chat-message assistant-message'>{answer}</div>", unsafe_allow_html=True)
            st.session_state.messages.append({"role": "assistant", "content": answer})
        except Exception as e:
            st.error(f"Error: {str(e)} – Check API key")

st.markdown("<p style='text-align:center; color:#888; margin-top:3rem;'>Grok AI Chatbot Template • Instant Download</p>", unsafe_allow_html=True)
