import streamlit as st
import requests

st.set_page_config(page_title="🤖 Hugging Face Chat", layout="centered")
st.title('🤖 Hugging Face LLM Chat')

# Masukkan token Hugging Face di secrets.toml
#API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"
API_URL = "https://api-inference.huggingface.co/models/gpt2"

headers = {"Authorization": f"Bearer {st.secrets['HF_API_KEY']}"}
st.write(st.secrets['HF_API_KEY'])

# Fungsi untuk query model Hugging Face
#def query(payload):
#    response = requests.post(API_URL, headers=headers, json=payload)
#    return response.json()

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    st.write("HTTP Status Code:", response.status_code)
    st.write("Response Text:", response.text)
    try:
        return response.json()
    except requests.exceptions.JSONDecodeError as e:
        return {"error": f"JSON decode error: {e}"}

# Inisialisasi sesi pesan
if "messages" not in st.session_state:
    st.session_state.messages = []

# Tampilkan riwayat chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input dari user
if prompt := st.chat_input("Tanyakan sesuatu..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Kirim request ke Hugging Face
    with st.chat_message("assistant"):
        with st.spinner("Sedang berpikir..."):
            output = query({
                "inputs": prompt,
                "parameters": {"max_new_tokens": 256, "temperature": 0.7}
            })

            # Tangkap respon
            if isinstance(output, list) and 'generated_text' in output[0]:
                reply = output[0]['generated_text']
            elif isinstance(output, dict) and 'error' in output:
                reply = f"⚠️ Error: {output['error']}"
            else:
                reply = "⚠️ Terjadi kesalahan tak terduga."

            st.markdown(reply)
            st.session_state.messages.append({"role": "assistant", "content": reply})


