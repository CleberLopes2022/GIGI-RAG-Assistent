import streamlit as st
from rag.retriever import Retriever
from rag.generator import Generator
from rag.memory import inicializar_memoria, adicionar_mensagem, obter_historico

st.set_page_config(page_title="GIGI - Assistente DGI", layout="centered")
st.title("GIGI - Assistente Virtual DGI")

# Inicialização
retriever = Retriever()
generator = Generator()
inicializar_memoria()

# Entrada do usuário
pergunta = st.chat_input("Digite sua pergunta...")

if pergunta:

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

