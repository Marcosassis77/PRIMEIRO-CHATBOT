import os
import streamlit as st
from dotenv import load_dotenv
from google import genai

load_dotenv()
minha_chave = os.getenv("GEMINI_API_KEY")

st.set_page_config(page_title="Meu Chatbot Gemini", page_icon="🤖")
st.title("🤖 Chatbot Gemini")

@st.cache_resource
def get_client():
    return genai.Client(api_key=minha_chave)

cliente = get_client()

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
            resposta = cliente.models.generate_content(
                model="gemini-3.6-flash",
                contents=prompt
            )
            conteudo_resposta = resposta.text
            st.markdown(conteudo_resposta)
            st.session_state.messages.append({"role": "assistant", "content": conteudo_resposta})
        except Exception as e:
            st.error(f"Ocorreu um erro: {e}")