import json
import random
import streamlit as st
from sentence_transformers import SentenceTransformer, util
from config.settings import MODEL_NAME, SIMILARITY_THRESHOLD, TOP_K
from utils.text_utils import normalizar_texto
import logging

logging.basicConfig(
    filename="rag_logs.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# ==========================
# 🔹 Carrega modelo (cacheado)
# ==========================

@st.cache_resource
def carregar_modelo():
    return SentenceTransformer(MODEL_NAME)

# ==========================
# 🔹 Carrega base (cacheado)
# ==========================

@st.cache_data
def carregar_base():
    with open("base_conhecimento.json", "r", encoding="utf-8") as f:
        return json.load(f)

# ==========================
# 🔹 Gera embeddings (cacheado)
# ==========================

@st.cache_resource
def gerar_embeddings():
    modelo = carregar_modelo()
    base = carregar_base()

    embeddings = []

    for item in base:
        pergunta = item["pergunta"]
        emb = modelo.encode(pergunta, convert_to_tensor=True)

        embeddings.append({
            "pergunta": pergunta,
            "resposta": item["resposta"],
            "embedding": emb
        })

    return embeddings


# ==========================
# 🔹 Classe Retriever
# ==========================

class Retriever:

    def __init__(self):
        self.modelo = carregar_modelo()
        self.base = carregar_base()
        self.embeddings = gerar_embeddings()

    def buscar_contexto(self, pergunta):

        pergunta_norm = normalizar_texto(pergunta)
        pergunta_emb = self.modelo.encode(pergunta_norm, convert_to_tensor=True)

        similaridades = []

        for item in self.embeddings:
            sim = util.pytorch_cos_sim(pergunta_emb, item["embedding"]).item()
            similaridades.append((sim, item))

        similaridades.sort(key=lambda x: x[0], reverse=True)

        logging.info(f"Pergunta: {pergunta}")
        logging.info(f"Similaridades: {[round(s,3) for s,_ in similaridades[:5]]}")


        contextos = []

        for sim, item in similaridades[:TOP_K]:
            if sim > SIMILARITY_THRESHOLD or not contextos:
                resposta = item["resposta"]

                if isinstance(resposta, list):
                    resposta = random.choice(resposta)

                contextos.append(f"- {resposta}")

        return "\n".join(contextos) if contextos else None


