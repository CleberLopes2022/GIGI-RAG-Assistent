import os
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

def get_api_key():

    # 1️⃣ Primeiro tenta variável de ambiente (.env)
    api_key = os.getenv("GROQ_API_KEY")
    if api_key:
        return api_key

    # 2️⃣ Depois tenta Streamlit Cloud secrets
    try:
        return st.secrets["GROQ_API_KEY"]
    except Exception:
        pass

    raise ValueError("GROQ_API_KEY não encontrada. Configure no .env ou no Streamlit secrets.")
    

MODEL_NAME = "all-mpnet-base-v2"
SIMILARITY_THRESHOLD = 0.45
TOP_K = 5
LLM_MODEL = "llama-3.3-70b-versatile"



