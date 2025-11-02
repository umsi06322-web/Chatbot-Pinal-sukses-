import streamlit as st
from langchain.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

# Model AI (Menggunakan Gemini-2.5-flash)
model = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
prompt = ChatPromptTemplate.from_template("Anda adalah asisten kafe yang ramah dan kreatif. Jawab pertanyaan berikut dengan singkat: {pertanyaan}")
chain = prompt | model

# Antarmuka Streamlit
st.title("☕ Chatbot Kafe Final Sukses")
st.caption("Dibuat menggunakan Streamlit, LangChain, dan Gemini-2.5-Flash")

# Inisialisasi riwayat chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Tampilkan riwayat chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input dari user
if user_input := st.chat_input("Tanyakan tentang kopi, menu, atau ide kafe..."):
    # Simpan input user
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Dapatkan respons dari model AI
    with st.chat_message("assistant"):
        with st.spinner("Meracik jawaban..."):
            try:
                response = chain.invoke({"pertanyaan": user_input})
                st.markdown(response.content)
                st.session_state.messages.append({"role": "assistant", "content": response.content})
            except Exception as e:
                error_message = f"Maaf, koneksi AI sedang bermasalah. Pastikan kunci API Gemini sudah diatur di Streamlit Secrets. ({e})"
                st.markdown(error_message)
                st.session_state.messages.append({"role": "assistant", "content": error_message})
