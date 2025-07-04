import streamlit as st
from together import Together

st.set_page_config(page_title="💬 Together AI Chat", layout="centered")
st.title("💬 Together AI Chat")

# Inisialisasi Together Client
client = Together(api_key=st.secrets["TOGETHER_API_KEY"])

# Inisialisasi pesan chat dalam session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Tampilkan riwayat chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input pengguna
if prompt := st.chat_input("Tanyakan sesuatu..."):
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Menunggu jawaban..."):
            try:
                response = client.chat.completions.create(
                    messages=st.session_state.messages,
                    model="meta-llama/Llama-3-70b-chat-hf",
                    max_tokens=1024,
                    temperature=0.5,
                    stream=False,
                )
                reply = response.choices[0].message.content
            except Exception as e:
                reply = f"⚠️ Terjadi kesalahan: {e}"

            st.markdown(reply)
            st.session_state.messages.append({"role": "assistant", "content": reply})

# Tombol untuk membersihkan chat
if st.button("🗑️ Bersihkan Chat"):
    st.session_state.messages = []
