import os
import streamlit as st
from dotenv import load_dotenv
from google import genai
from google.genai import types

st.set_page_config(page_title="Nexus AI Pro", page_icon="⚡", layout="wide")

st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stApp { background-color: #0E1117; }
    .main-header {
        font-size: 2.2rem; font-weight: 800;
        background: linear-gradient(90deg, #FF4B4B 0%, #FF8C00 100%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    }
    </style>
""", unsafe_allow_html=True)

load_dotenv()

minha_chave = None
try:
    if "GEMINI_API_KEY" in st.secrets:
        minha_chave = st.secrets["GEMINI_API_KEY"]
except Exception:
    pass

if not minha_chave:
    minha_chave = os.getenv("GEMINI_API_KEY")

if not minha_chave:
    st.error("⚠️ Adicione a GEMINI_API_KEY nos Secrets ou no .env.")
    st.stop()

@st.cache_resource
def get_client(api_key):
    return genai.Client(api_key=api_key)

cliente = get_client(minha_chave)

with st.sidebar:
    st.title("⚙️ Painel do Agente")
    persona = st.selectbox("Especialista:", [
        "Consultor de Negócios & Vendas",
        "Especialista em Marketing Digital",
        "Programador Senior (Python/JS)",
        "Assistente Pessoal Geral"
    ])
    tom = st.select_slider("Tom:", options=["Muito Direto", "Equilibrado", "Detalhado & Explicativo"], value="Equilibrado")
    if st.button("🗑️ Limpar Conversa", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

prompts_sistema = {
    "Consultor de Negócios & Vendas": "Atua como consultor estratégico focado em vendas e ROI. Responda em português.",
    "Especialista em Marketing Digital": "Atua como copywriter especialista em conversão e redes sociais. Responda em português.",
    "Programador Senior (Python/JS)": "Atua como engenheiro de software senior com código limpo. Responda em português.",
    "Assistente Pessoal Geral": "Atua como assistente executivo altamente produtivo. Responda em português."
}

st.markdown('<div class="main-header">Nexus AI Pro</div>', unsafe_allow_html=True)
st.caption(f"Módulo: {persona} | Tom: {tom}")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Como posso ajudar o seu negócio hoje?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("A analisar..."):
            try:
                resposta = cliente.models.generate_content(
                    model="gemini-3.6-flash",
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        system_instruction=f"{prompts_sistema[persona]} Nível de detalhe: {tom}.",
                        temperature=0.7 if tom == "Detalhado & Explicativo" else 0.3
                    )
                )
                conteudo = resposta.text
                st.markdown(conteudo)
                st.session_state.messages.append({"role": "assistant", "content": conteudo})
            except Exception as e:
                st.error(f"Erro: {e}")
