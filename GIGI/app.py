import streamlit as st
from rag.retriever import Retriever
from rag.generator import Generator
from rag.memory import inicializar_memoria, adicionar_mensagem, obter_historico

st.set_page_config(page_title="GIGI - Assistente DGI", layout="centered")
st.title("GIGI - Assistente Virtual DGI")

# Inicializa memória leve (isso é tranquilo)
inicializar_memoria()

# 🔥 Carregamento sob demanda
@st.cache_resource
def carregar_componentes():
    retriever = Retriever()
    generator = Generator()
    return retriever, generator

# Entrada do usuário
pergunta = st.chat_input("Digite sua pergunta...")

if pergunta:

    retriever, generator = carregar_componentes()

    adicionar_mensagem("Usuário", pergunta)

    contexto = retriever.buscar_contexto(pergunta)

    if contexto:
        resposta = generator.gerar(pergunta, contexto, obter_historico())
    else:
        resposta = "Não encontrei informação suficiente na base."

    adicionar_mensagem("GIGI", resposta)

# Render histórico
for remetente, mensagem in obter_historico():
    if remetente == "Usuário":
        with st.chat_message("user"):
            st.write(mensagem)
    else:
        with st.chat_message("assistant"):
            st.write(mensagem)


