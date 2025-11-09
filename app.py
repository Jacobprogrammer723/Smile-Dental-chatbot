import streamlit as st
import requests

# === PAGE CONFIG ===
st.set_page_config(
    page_title="Smile Dental AI Assistant",
    page_icon="🦷",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# === CUSTOM CSS FOR MODERN LOOK ===
st.markdown("""
<style>
    .main {
        background: linear-gradient(135deg, #f0f7ff 0%, #e6f7f7 100%);
        padding: 2rem;
    }
    .stApp {
        background: transparent;
    }
    .title-box {
        background: white;
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
        text-align: center;
        margin-bottom: 2rem;
    }
    .chat-container {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
        margin-bottom: 1.5rem;
    }
    .buy-box {
        background: linear-gradient(135deg, #1e90ff, #00c2cb);
        color: white;
        padding: 2rem;
        border-radius: 20px;
        text-align: center;
        box-shadow: 0 8px 20px rgba(30,144,255,0.3);
        margin-top: 2rem;
    }
    .buy-box h2 {
        margin: 0 0 1rem 0;
        font-size: 1.8rem;
    }
    .price-tag {
        font-size: 2.2rem;
        font-weight: bold;
        margin: 0.5rem 0;
    }
    .discount {
        background: #ff4757;
        color: white;
        padding: 0.4rem 1rem;
        border-radius: 50px;
        font-size: 0.9rem;
        display: inline-block;
        margin-top: 0.5rem;
    }
    .form-box {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        margin-top: 1rem;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    .stButton>button {
        background: #00c2cb;
        color: white;
        border: none;
        border-radius: 50px;
        padding: 0.7rem 1.5rem;
        font-weight: bold;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        background: #1e90ff;
        transform: translateY(-2px);
        box-shadow: 0 6px 15px rgba(30,144,255,0.4);
    }
    .success-box {
        background: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 10px;
        border: 1px solid #c3e6cb;
        margin-top: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# === HEADER ===
with st.container():
    col1, col2, col3 = st.columns([1, 3, 1])
    with col2:
        st.markdown("""
        <div class="title-box">
            <h1 style="margin:0; color:#1e90ff;">🦷 Smile Dental AI Assistant</h1>
            <p style="color:#666; font-size:1.1rem;">Book appointments, get prices, collect leads – <strong>24/7</strong></p>
        </div>
        """, unsafe_allow_html=True)

# === API & PROMPT (USD PRICES) ===
API_KEY = st.secrets["GROK_KEY"]
SYSTEM_PROMPT = """You are Tandis, a friendly and professional AI assistant for Smile Dental Clinic in Stockholm.
Always respond in perfect English. Keep answers short and helpful.
Prices: Check-up $76, Whitening $285, Implants from $1,425.
Always ask for name and phone to book an appointment.
Offer 10% off first visit.
Never lie – say "I'll check with the team" if unsure.
Goal: Collect leads and book appointments."""

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]

# === CHAT INTERFACE ===
with st.container():
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    
    for msg in st.session_state.messages[1:]:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])
    
    if prompt := st.chat_input("Hello! How can I help with your smile today?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)
        
        with st.chat_message("assistant"):
            with st.spinner("Tandis is thinking..."):
                try:
                    response = requests.post(
                        "https://api.x.ai/v1/chat/completions",
                        headers={"Authorization": f"Bearer {API_KEY}"},
                        json={"model": "grok-4-fast", "messages": st.session_state.messages}
                    ).json()
                    answer = response["choices"][0]["message"]["content"]
                    st.write(answer)
                    st.session_state.messages.append({"role": "assistant", "content": answer})
                except Exception:
                    st.error("Something went wrong – please try again.")
    
    st.markdown('</div>', unsafe_allow_html=True)

# === BUY BOT SECTION (USD) ===
st.markdown(f"""
<div class="buy-box">
    <h2>Get Your Own AI Dental Assistant!</h2>
    <p class="price-tag">$1,900 + $475/month</p>
    <p><strong>Live in 24h • Invoice • No lock-in</strong></p>
    <div class="discount">First 10 buyers: Pay via Venmo/Zelle → $665 OFF!</div>
</div>
""", unsafe_allow_html=True)

with st.container():
    st.markdown('<div class="form-box">', unsafe_allow_html=True)
    with st.form("buy_bot_form", clear_on_submit=True):
        st.subheader("Fill in → Get invoice + bot in 24h")
        
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Your name *", placeholder="Anna Smith")
            clinic = st.text_input("Clinic name *", placeholder="Bright Smile Clinic")
        with col2:
            email = st.text_input("Email (invoice) *", placeholder="anna@brightsmile.com")
            phone = st.text_input("Phone *", placeholder="+1 (555) 123-4567")
        
        payment_note = st.text_input("Venmo/Zelle/PayPal (optional, for $665 discount)", placeholder="@YourHandle")
        
        submitted = st.form_submit_button("SUBMIT ORDER → PAY LATER")
        
        if submitted:
            if name and clinic and email and phone:
                st.markdown(f"""
                <div class="success-box">
                    <h3>THANK YOU {name.upper()}!</h3>
                    <p><strong>Order received for:</strong> {clinic}</p>
                    <p>Invoice ($1,900 + $475/month) will be sent to <strong>{email}</strong> within 2 hours.</p>
                    <p>Pay via Venmo/Zelle to <strong>@SmileDentalAI</strong> for <strong>$665 discount</strong> (first 10 only!)</p>
                    <p><strong>Your bot goes live tomorrow!</strong></p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.error("Please fill in all required fields (*)")
    
    st.markdown('</div>', unsafe_allow_html=True)

# === FOOTER ===
st.markdown("""
---
<div style="text-align:center; color:#888; font-size:0.9rem; margin-top:2rem;">
    Built with Streamlit & Grok 4 • Smile Dental AI • Global 2025
</div>
""", unsafe_allow_html=True)
