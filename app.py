# grok-chatbot-pro-template.py – FULLY CUSTOMIZABLE (no code required!)
import streamlit as st
import requests

# === SIDEBAR: BUYER CUSTOMIZES EVERYTHING HERE ===
with st.sidebar:
    st.header("Customize Your Bot")
    
    # Basic settings
    clinic_name = st.text_input("Business Name", "Your Awesome Business")
    logo_url = st.text_input("Logo URL (150x150 px)", "https://via.placeholder.com/150")
    calendar_link = st.text_input("Booking Link (Calendly, etc.)", "https://calendly.com/your-link")
    
    # Colors
    primary_color = st.color_picker("Primary Color", "#1e90ff")
    bg_color = st.color_picker("Background Color", "#f8f9fa")
    text_color = st.color_picker("Text Color", "#212529")
    
    # Font
    font_size = st.slider("Font Size (px)", 14, 24, 16)
    font_family = st.selectbox("Font Family", ["Arial", "Helvetica", "Georgia", "Courier New", "Verdana"])
    
    # AI model
    model = st.selectbox("AI Model", ["grok-4-fast (cheapest)", "gpt-4o-mini (ChatGPT)", "gemini-1.5-flash (Google)"])
    
    # Services (dynamic list)
    st.subheader("Services / Prices")
    services = []
    for i in range(10):
        with st.expander(f"Service {i+1}" if i > 0 else "Add Service"):
            name = st.text_input(f"Name##{i}", f"Service {i+1}", key=f"name{i}")
            price = st.text_input(f"Price##{i}", "$99", key=f"price{i}")
            desc = st.text_area(f"Description##{i}", "Short description", key=f"desc{i}")
            if name and price:
                services.append(f"- {name}: {price} – {desc}")
    
    services_text = "\n".join(services) if services else "- Custom Service: Contact us"
    
    # Welcome message
    welcome_msg = st.text_area("Welcome Message", "Hello! How can I help you today?")
    
    # API keys info
    st.subheader("API Keys (add in Streamlit secrets)")
    st.info("GROK_KEY = your-grok-key\nOPENAI_KEY = sk-...\nGEMINI_KEY = AIza...")

# === DYNAMIC SYSTEM PROMPT ===
SYSTEM_PROMPT = f"""You are a professional AI assistant for {clinic_name}.
Services:
{services_text}
Always ask for name + phone to book.
Booking link: {calendar_link}
Offer 10% off first visit.
Perfect English only."""

# === SELECT API BASED ON MODEL ===
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

# === DYNAMIC CSS ===
st.markdown(f"""
<style>
    .main {{background: {bg_color}; padding: 2rem 1rem; font-family: {font_family}; font-size: {font_size}px; color: {text_color};
