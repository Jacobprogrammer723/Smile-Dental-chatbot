import streamlit as st
import requests

# ============================================================
#       🟩 1. KUNDINSTÄLLNINGAR (ÄNDRA HÄR INFÖR VARJE KUND)
# ============================================================

# 👉 Här editerar du alla kundspecifika värden.
# 👉 Dessa behöver inte hämtas via sidomenyn (enklare att sälja).

CUSTOMER = {
    "business_name": "Smile Clinic Stockholm",       # ÄNDRA HÄR FÖR KUNDEN
    "logo_url": "https://via.placeholder.com/150",   # ÄNDRA HÄR FÖR KUNDEN
    "booking_link": "https://calendly.com/example",  # ÄNDRA HÄR FÖR KUNDEN

    # Lista över tjänster – enkel att redigera (namn, pris, beskrivning)
    "services": [
        "- Check-up: $76 – Full dental check-up",
        "- Whitening: $285 – Professional whitening treatment",
        "- Implants: $1425 – Titanium dental implant"
    ],

    # UI-design – ändra för kundens färger / brand
    "primary_color": "#1e90ff",
    "background_color": "#f8f9fa",
    "text_color": "#212529",
    "font_family": "Arial",
    "font_size": 16,

    # Modell som används – OpenAI/Grok/Gemini
    "ai_model": "gpt-4o-mini",  # "grok-4-fast" eller "gemini-1.5-flash"
}

# ============================================================
#             🟦 2. SYSTEMPROMPT (AUTO GENERERAD)
# ============================================================

def build_system_prompt(customer):
    services_text = "\n".join(customer["services"])

    return f"""
You are a professional AI assistant for {customer['business_name']}.

Services:
{services_text}

Always ask for name + phone number to book.
Booking link: {customer['booking_link']}
Offer 10% off first visit.
Answer in perfect English.
End EVERY answer with:
"Get your own AI chatbot for $299 → https://payhip.com/b/BF2hV"
"""

SYSTEM_PROMPT = build_system_prompt(CUSTOMER)

# ============================================================
#          🟨 3. INITIERA SESSION (CHATTMINNE)
# ============================================================

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]

# Begränsa historik (billigare API-kostnad)
def trim_history(history, limit=12):
    return [history[0]] + history[-limit:]


# ============================================================
#            🟧 4. VÄLJ MODEL + API NYCKEL
# ============================================================

model = CUSTOMER["ai_model"]
API_KEY = None
url = None
payload_model = None

if model == "grok-4-fast":
    API_KEY = st.secrets.get("GROK_KEY")
    url = "https://api.x.ai/v1/chat/completions"
    payload_model = "grok-4-fast"

elif model == "gpt-4o-mini":
    API_KEY = st.secrets.get("OPENAI_KEY")
    url = "https://api.openai.com/v1/chat/completions"
    payload_model = "gpt-4o-mini"

elif model == "gemini-1.5-flash":
    API_KEY = st.secrets.get("GEMINI_KEY")
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"

DEMO_MODE = not API_KEY


# ============================================================
#                 🟫 5. CSS DESIGN (FÖR KUND)
# ============================================================

st.markdown(f"""
<style>
    .main {{
        background: {CUSTOMER['background_color']};
        font-family: {CUSTOMER['font_family']};
        font-size: {CUSTOMER['font_size']}px;
        color: {CUSTOMER['text_color']};
    }}
    .chat-message {{
        padding: 1rem;
        border-radius: 12px;
        margin: 0.5rem 0;
        max-width: 80%;
    }}
    .user-message {{
        background: {CUSTOMER['primary_color']};
        color: white;
        margin-left: auto;
    }}
    .assistant-message {{
        background: #eeeeee;
        color: {CUSTOMER['text_color']};
    }}
</style>
""", unsafe_allow_html=True)


# ============================================================
#                         🟪 6. HEADER
# ============================================================

st.write("")
if CUSTOMER["logo_url"]:
    st.image(CUSTOMER["logo_url"], width=110)

st.markdown(
    f"<h1 style='text-align:center;'>🤖 {CUSTOMER['business_name']}</h1>",
    unsafe_allow_html=True
)
st.markdown("<p style='text-align:center;color:#666;'>24/7 AI Assistant</p>", unsafe_allow_html=True)


# ============================================================
#                     🟥 7. VISA CHATT
# ============================================================

for msg in st.session_state.messages[1:]:
    css = "user-message" if msg["role"] == "user" else "assistant-message"
    st.markdown(f"<div class='chat-message {css}'>{msg['content']}</div>", unsafe_allow_html=True)


# ============================================================
#                    🟩 8. CHATTINPUT
# ============================================================

prompt = st.chat_input(f"Hello! How can I help you?")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.spinner("Thinking..."):
        try:
            history = trim_history(st.session_state.messages)

            if DEMO_MODE:
                answer = "Demo mode — add API keys. Get your own bot for $299 → https://payhip.com/b/BF2hV"

            elif "gemini" in model:
                payload = {
                    "contents": [
                        {
                            "role": "user" if m["role"] == "user" else "model",
                            "parts": [{"text": m["content"]}]
                        }
                        for m in history if m["role"] != "system"
                    ],
                    "systemInstruction": {"parts": [{"text": SYSTEM_PROMPT}]}
                }
                response = requests.post(f"{url}?key={API_KEY}", json=payload).json()
                answer = response["candidates"][0]["content"]["parts"][0]["text"]

            else:
                payload = {"model": payload_model, "messages": history}
                response = requests.post(url, headers={"Authorization": f"Bearer {API_KEY}"}, json=payload).json()
                answer = response["choices"][0]["message"]["content"]

        except Exception as e:
            answer = f"Error: {str(e)}"

    st.session_state.messages.append({"role": "assistant", "content": answer})
    st.rerun()


# ============================================================
#                       🟦 9. FOOTER
# ============================================================

st.markdown(
    "<p style='text-align:center;color:#888;margin-top:2rem;'>Get your own bot → https://payhip.com/b/BF2hV</p>",
    unsafe_allow_html=True
)
