# chatbot-pro-template.py – Chatbot all models
import streamlit as st
import requests

st.set_page_config(page_title="Your AI Assistant", page_icon="🤖", layout="centered")


st.markdown("""
<style>
    /* Debug-ballong (0, 20, etc.) */
    section[data-testid="stDecoration"] {display: none !important;}
    /* Fullscreen-knapp */
    button[title="View fullscreen"] {display: none !important;}
    /* Fil-ikoner */
    .stTextInput > div > div > div > div > svg,
    .stTextArea > div > div > div > div > svg,
    [data-baseweb="input"] svg,
    svg[data-icon="paperclip"], svg[data-icon="upload"] {display: none !important;}
</style>
""", unsafe_allow_html=True)


# === SIDEBAR ===
with st.sidebar:
    st.header("Customize Your Bot")
    
    business_name = st.text_input("Business Name", "Your Awesome Business")
    logo_url = st.text_input("Logo URL (150x150 px)", "https://via.placeholder.com/150")
    booking_link = st.text_input("Booking Link", "https://calendly.com/your-link")
    
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

    # One-click demo
    if st.button("Load Dental Demo"):
        st.session_state.business_name = "Smile Clinic Stockholm"
        st.session_state.logo_url = "https://i.imgur.com/EXAMPLE.png"
        st.session_state.booking_link = "https://calendly.com/smileclinic"
        st.session_state.services_text = "- Check-up: $76\n- Whitening: $285\n- Implants: $1425"
        st.success("Dental demo loaded!")

# === SYSTEM PROMPT ===
SYSTEM_PROMPT = f"""You are a professional AI assistant for {business_name}.
Services:
{services_text}
Always ask for name + phone to book.
Booking link: {booking_link}
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

# === DYNAMIC CSS ===
css = f"""
<style>
    .main {{background: {bg_color}; padding: 2rem 1rem; font-family: {font_family}; font-size: {font_size}px; color: {text_color};}}
    .header {{text-align: center; padding: 2.5rem 1rem; background: white; border-radius: 25px; box-shadow: 0 8px 32px rgba(0,0,0,0.08); margin: 1rem auto; max-width: 800px;}}
    .chat-message {{padding: 1.2rem; border-radius: 15px; margin: 0.5rem 0; max-width: 80%;}}
    .user-message {{background: {primary_color}; color: white; margin-left: auto;}}
    .assistant-message {{background: #e9ecef; color: {text_color};}}
    .stChatInput > div > div > input {{border-radius: 25px !important; padding: 0.8rem 1.5rem !important; border: 2px solid {primary_color} !important;}}
    h1 {{color: {primary_color} !important; margin: 0.5rem 0 !important;}}
</style>
"""
st.markdown(css, unsafe_allow_html=True)

# Auto-scroll
st.markdown("<script>parent.document.querySelector('.stChatMessage')?.scrollIntoView({behavior: 'smooth', block: 'end'});</script>", unsafe_allow_html=True)

# === PERFECT HEADER ===
st.markdown("<div class='header'>", unsafe_allow_html=True)
if logo_url:
    st.image(logo_url, width=120)
st.markdown(f"<h1>🤖 {business_name}</h1>", unsafe_allow_html=True)
st.markdown("<p style='color:#666; font-size:1.1rem; margin:0;'>24/7 AI Assistant – Book, Ask, Smile</p>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# === CHAT ===
for msg in st.session_state.messages[1:]:
    if msg["role"] == "user":
        st.markdown(f"<div class='chat-message user-message'>{msg['content']}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='chat-message assistant-message'>{msg['content']}</div>", unsafe_allow_html=True)

if prompt := st.chat_input(welcome_msg):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.markdown(f"<div class='chat-message user-message'>{prompt}</div>", unsafe_allow_html=True)
    
    with st.spinner("Thinking..."):
        try:
            if "gemini" in model.lower():
                payload = {"contents": [{"role": "user" if m["role"] == "user" else "model", "parts": [{"text": m["content"]}]} for m in st.session_state.messages]}
                response = requests.post(f"{url}?key={API_KEY}", json=payload).json()
                answer = response["candidates"][0]["content"]["parts"][0]["text"]
            else:
                payload = {"model": payload_model, "messages": st.session_state.messages}
                response = requests.post(url, headers={"Authorization": f"Bearer {API_KEY}"}, json=payload).json()
                answer = response["choices"][0]["message"]["content"]
            
            st.markdown(f"<div class='chat-message assistant-message'>{answer}</div>", unsafe_allow_html=True)
            st.session_state.messages.append({"role": "assistant", "content": answer})
        except Exception as e:
            st.error(f"Error: {str(e)}")

# === LEAD EXPORT ===
if st.button("Export Leads (copy to email)"):
    leads = "\n".join([f"{m['role']}: {m['content']}" for m in st.session_state.messages if m['role'] == 'user'])
    st.code(leads)
    st.info("Copy → paste into email. Pro version auto-sends leads!")

# === FOOTER ===
st.markdown(f"<p style='text-align:center; color:#888; margin-top:3rem;'>Powered by {model.split()[0]} • Custom AI Assistant</p>", unsafe_allow_html=True)
