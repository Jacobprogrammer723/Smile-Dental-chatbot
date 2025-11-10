# chatbot-pro-template.py – FULLY CUSTOMIZABLE
import streamlit as st
import requests

# === SIDEBAR CUSTOMIZER ===
with st.sidebar:
    st.header("Customize Your Bot")
    clinic_name = st.text_input("Business Name", "Your Awesome Business")
    logo_url = st.text_input("Logo URL (150x150 px)", "https://via.placeholder.com/150")
    calendar_link = st.text_input("Booking Link", "https://calendly.com/your-link")
    primary_color = st.color_picker("Primary Color", "#1e90ff")
    bg_color = st.color_picker("Background Color", "#f8f9fa")
    text_color = st.color_picker("Text Color", "#212529")
    font_size = st.slider("Font Size (px)", 14, 24, 16)
    font_family = st.selectbox("Font Family", ["Arial", "Helvetica", "Georgia", "Courier New", "Verdana"])
    model = st.selectbox("AI Model", ["grok-4-fast (cheapest)", "gpt-4o-mini (ChatGPT)", "gemini-1.5-flash (Google)"])
    
    st.subheader("Services")
    services = []
    for i in range(10):
        with st.expander(f"Service {i+1}" if i > 0 else "Add Service"):
            name = st.text_input(f"Name##{i}", f"Service {i+1}", key=f"name{i}")
            price = st.text_input(f"Price##{i}", "$99", key=f"price{i}")
            desc = st.text_area(f"Description##{i}", "Short description", key=f"desc{i}")
            if name and price:
                services.append(f"- {name}: {price} – {desc}")
    services_text = "\n".join(services) if services else "- Contact us for pricing"
    welcome_msg = st.text_area("Welcome Message", "Hello! How can I help you today?")

# === SYSTEM PROMPT ===
SYSTEM_PROMPT = f"""You are a professional AI assistant for {clinic_name}.
Services:
{services_text}
Always ask for name + phone to book.
Booking link: {calendar_link}
Offer 10% off first visit.
Perfect English only."""

# === API SETUP ===
if "grok" in model.lower():
    API_KEY = st.secrets.get("GROK_KEY")
    url = "https://api.x.ai/v1/chat/completions"
    payload_model = "grok-4-fast"
elif "chatgpt" in model.lower():
    API_KEY = st.secrets.get("OPENAI_KEY")
    url = "https://api.openai.com/v1/chat/completions"
    payload_model = "gpt-4o-mini"
else:
    API_KEY = st.secrets.get("GEMINI_KEY")
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"
    payload_model = None

if not API_KEY:
    st.error(f"Add your {model.split()[0]} API key in Streamlit secrets!")
    st.stop()

# === INIT CHAT ===
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]

# === CSS ===
css = f"""
<style>
    .main {{background: {bg_color}; padding: 2rem 1rem; font-family: {font_family}; font-size: {font_size}px; color: {text_color};}}
    .header {{text-align: center; padding: 2rem 0; background: white; border-radius: 20px; box-shadow: 0 4px 20px rgba(0,0,0,0.05); margin-bottom: 2rem;}}
    .chat-message {{padding: 1.2rem; border-radius: 15px; margin: 0.5rem 0; max-width: 80%;}}
    .user-message {{background: {primary_color}; color: white; margin-left: auto;}}
    .assistant-message {{background: #e9ecef; color: {text_color};}}
    .stChatInput > div > div > input {{border-radius: 25px !important; padding: 0.8rem 1.5rem !important; border: 2px solid {primary_color} !important;}}
    h1 {{color: {primary_color} !important;}}
    /* TA BORT FIL-IKONEN I ALLA TEXTFÄLT */
    .stTextInput > div > div > div > div > svg,
    .stTextArea > div > div > div > div > svg,
    [data-baseweb="input"] svg,
    svg[data-icon="paperclip"], 
    svg[data-icon="upload"] {{
        display: none !important;
    }}
</style>
"""
st.markdown(css, unsafe_allow_html=True)

st.markdown(f"<p style='text-align:center; color:#888; margin-top:3rem;'>Powered by {model.split()[0]} • Custom AI Assistant • $197</p>", unsafe_allow_html=True)
