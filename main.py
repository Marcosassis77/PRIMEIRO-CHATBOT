import os
import streamlit as st
from dotenv import load_dotenv
from google import genai
from google.genai import types

st.set_page_config(page_title="Nexus AI Pro", page_icon="⚡", layout="wide")

# CSS para ocultar marcas d'água, avisos e menus do Streamlit
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
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
    st.error("⚠️ Erro de inicialização do sistema. Contacte o suporte.")
    st.stop()

@st.cache_resource
def get_client(api_key):
    return genai.Client(api_key=api_key)

cliente = get_client(minha_chave)

with st.sidebar:
    st.title("⚙️ Painel de Controlo")
    persona = st.selectbox("Especialista:", [
        "Consultor de Negócios & Vendas",
        "Especialista em Marketing Digital",
        "Programador Senior (Python/JS)",
        "Assistente Executivo Geral"
    ])
    tom = st.select_slider("Tom:", options=["Muito Direto", "Equilibrado", "Detalhado & Explicativo"], value="Equilibrado")
    if st.button("🗑️ Limpar Histórico", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# Prompts com regras estritas para ocultar qualquer menção a IA/Google/Gemini
regra_whitelabel = (
    " REGRA ABSOLUTA E INVIOLÁVEL: Nunca mencione que é uma inteligência artificial, um modelo de linguagem, a Google, o Gemini ou que foi programado/gerado por qualquer empresa de IA. "
    "Apresente-se sempre estritamente como um especialista humano ou como o sistema corporativo Nexus Pro. "
    "Nunca diga 'Como uma IA...' ou 'Fui treinado por...'. Caso perguntem quem você é, responda que é o assistente virtual exclusivo da plataforma Nexus Pro."
)

prompts_sistema = {
    "Consultor de Negócios & Vendas": f"Atua como consultor estratégico focado em vendas e ROI. Responda em português.{regra_whitelabel}",
    "Especialista em Marketing Digital": f"Atua como copywriter especialista em conversão e redes sociais. Responda em português.{regra_whitelabel}",
    "Programador Senior (Python/JS)": f"Atua como engenheiro de software senior com código limpo. Responda em português.{regra_whitelabel}",
    "Assistente Executivo Geral": f"Atua como assistente executivo altamente produtivo. Responda em português.{regra_whitelabel}"
}

st.markdown('<div class="main-header">Nexus Pro</div>', unsafe_allow_html=True)
st.caption(f"Módulo Ativo: {persona} | Modo: {tom}")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Como posso ajudar a sua empresa hoje?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("A processar pedido..."):
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
                st.error("Ocorreu um erro ao processar a resposta. Tente novamente.")
