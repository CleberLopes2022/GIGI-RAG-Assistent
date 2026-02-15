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

    perguntas = [item["pergunta"] for item in base]
    embeddings = modelo.encode(perguntas, convert_to_tensor=True)

    return embeddings


# ==========================
# 🔹 Classe Retriever
# ==========================

class Retriever:

    def __init__(self):
        # 🔥 NÃO carrega nada pesado aqui
        self.modelo = None
        self.base = None
        self.embeddings = None

    def carregar(self):
        if self.modelo is None:
            self.modelo = carregar_modelo()

        if self.base is None:
            self.base = carregar_base()

        if self.embeddings is None:
            self.embeddings = gerar_embeddings()

    def buscar_contexto(self, pergunta):

        # 🔥 Só carrega quando necessário
        self.carregar()

        pergunta_norm = normalizar_texto(pergunta)
        pergunta_emb = self.modelo.encode(pergunta_norm, convert_to_tensor=True)

        similaridades = util.pytorch_cos_sim(
            pergunta_emb,
            self.embeddings
        )[0]

        top_resultados = similaridades.topk(TOP_K)

        logging.info(f"Pergunta: {pergunta}")
        logging.info(f"Similaridades: {[round(s.item(),3) for s in top_resultados.values]}")

        contextos = []

        for idx, sim in zip(top_resultados.indices, top_resultados.values):

            sim = sim.item()

            if sim > SIMILARITY_THRESHOLD or not contextos:

                resposta = self.base[idx]["resposta"]

                if isinstance(resposta, list):
                    resposta = random.choice(resposta)

                contextos.append(f"- {resposta}")

        return "\n".join(contextos) if contextos else None



