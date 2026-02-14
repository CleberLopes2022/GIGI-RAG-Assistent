import streamlit as st

def inicializar_memoria():
    if "historico" not in st.session_state:
        st.session_state.historico = []

def adicionar_mensagem(remetente, mensagem):
    st.session_state.historico.append((remetente, mensagem))

def obter_historico():
    return st.session_state.historico
