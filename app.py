import streamlit as st
import requests

st.set_page_config(page_title="Smile Dental AI Assistant", page_icon="🦷")
st.title("🦷 Test Your New AI Dental Assistant!")
st.write("Ask anything – books appointments, gives prices, collects leads 24/7!")

# REPLACE WITH YOUR API KEY IN SECRETS!!!
API_KEY = st.secrets["GROK_KEY"]

SYSTEM_PROMPT = """You are Tandis, a friendly and professional AI assistant for Smile Dental Clinic in Stockholm.
Always respond in perfect English. Keep answers short and helpful.
Prices: Check-up 800 SEK, Whitening 3000 SEK, Implants from 15,000 SEK.
Always ask for name and phone to book an appointment.
Offer 10% off first visit.
Never lie – say "I'll check with the team" if unsure.
Goal: Collect leads and book appointments."""

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]

for msg in st.session_state.messages[1:]:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

if prompt := st.chat_input("Hello! How can I help with your teeth today?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = requests.post(
                    "https://api.x.ai/v1/chat/completions",
                    headers={"Authorization": f"Bearer {API_KEY}"},
                    json={"model": "grok-4-fast", "messages": st.session_state.messages}
                ).json()
                answer = response["choices"][0]["message"]["content"]
                st.write(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})
            except:
                st.write("Oops, something went wrong – try again!")

# SELF-SERVICE BUY BUTTON
if st.button("🚀 YES! I want this bot for MY clinic (20,000 SEK + 5,000 SEK/month)"):
    with st.form("buy_bot"):
        st.write("Fill in → get invoice + custom bot in 24h!")
        name = st.text_input("Your name")
        clinic = st.text_input("Clinic name")
        email = st.text_input("Email (invoice sent here)")
        phone = st.text_input("Phone")
        swish = st.text_input("Swish number (optional)")
        submitted = st.form_submit_button("SUBMIT ORDER → PAY LATER")
        if submitted:
            st.success(f"""
            🎉 THANK YOU {name}!  
            Order received for {clinic}.  
            Invoice for 20,000 SEK + 5,000 SEK/month sent to {email} within 2 hours.  
            Swish 123 456 78 90 for 7,000 SEK discount (first 10 buyers).  
            Your bot goes live tomorrow!  
            """)
