import os
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

# Tenta obter a chave dos Secrets do Streamlit Cloud; se falhar (localmente), obtém do .env
minha_chave = None
try:
    if "GEMINI_API_KEY" in st.secrets:
        minha_chave = st.secrets["GEMINI_API_KEY"]
except Exception:
    pass

if not minha_chave:
    minha_chave = os.getenv("GEMINI_API_KEY")

st.set_page_config(page_title="Meu Chatbot Gemini", page_icon="🤖")
st.title("🤖 Chatbot Gemini")

# Configura a chave na SDK da Google
if minha_chave:
    genai.configure(api_key=minha_chave)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Digite a sua pergunta..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            model = genai.GenerativeModel("gemini-1.5-flash")
            resposta = model.generate_content(prompt)
            conteudo_resposta = resposta.text
            
            st.markdown(conteudo_resposta)
            st.session_state.messages.append({"role": "assistant", "content": conteudo_resposta})
        except Exception as e:
            st.error(f"Ocorreu um erro: {e}")
