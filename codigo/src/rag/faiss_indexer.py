import faiss
import numpy as np
import os
import json
import logging

from src.rag.config_loader import CONFIG
from src.rag.embedding_generator import generate_embedding

# Configuração do logger
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

FAISS_INDEX_PATH = os.path.join(CONFIG["embeddings_dir"], "faiss_index")

class FaissIndexer:
    def __init__(self, embedding_dim=1024):  # Dimensão do modelo BGE Large
        """Inicializa o FAISS index."""
        self.index = faiss.IndexFlatL2(embedding_dim)  # Distância Euclidiana (L2)
        self.id_map = {}  # Mapeia IDs dos embeddings para nomes dos arquivos
        self.texts = []  # Lista para armazenar textos associados aos embeddings

    def add_embeddings(self, vector, paragraph):
        """Adiciona um embedding ao FAISS associando-o a um parágrafo específico."""
        vector = np.array(vector, dtype=np.float32)

        if vector.ndim == 1:
            vector = vector.reshape(1, -1)

        self.index.add(vector)  # Adiciona o vetor ao FAISS
        self.texts.append(paragraph)  # Associa o embedding ao parágrafo
        logging.info(f"✅ Embedding adicionado ao FAISS para o parágrafo: {paragraph[:50]}...")



    def search(self, query, top_k=3):
        """Busca no FAISS os parágrafos mais similares ao termo/frase consultado."""
        if not self.index or self.index.ntotal == 0:
            logging.warning("⚠️ O índice FAISS está vazio. Nenhuma busca pode ser realizada.")
            return []

        query_embedding = generate_embedding(query)[0]  # Geramos um embedding da consulta
        query_vector = np.array([query_embedding], dtype=np.float32)

        distances, indices = self.index.search(query_vector, top_k)

        results = []
        for i, idx in enumerate(indices[0]):
            if idx < 0 or idx >= len(self.texts):
                continue
            paragraph = self.texts[idx]  # Recupera o parágrafo associado ao embedding
            results.append((paragraph, distances[0][i]))

        return results

    def get_stored_embedding(self, term):
        """Recupera um embedding já armazenado no FAISS para um termo específico."""
        if term not in self.texts:
            logging.warning(f"⚠️ O termo '{term}' não foi indexado no FAISS.")
            return None

        idx = self.texts.index(term)  # Encontra a posição do termo no índice FAISS
        embedding = self.index.reconstruct(idx)  # Recupera o embedding
        
        if embedding is None:
            logging.error(f"❌ Falha ao recuperar embedding para '{term}'.")
            return None

        embedding = np.array(embedding, dtype=np.float32).reshape(1, -1)  # Garante formato correto
        return embedding


    def save_index(self):
        """Salva o índice FAISS em disco."""
        faiss.write_index(self.index, FAISS_INDEX_PATH)
        with open(FAISS_INDEX_PATH + "_map.json", "w") as f:
            json.dump(self.texts, f)  # Salva a lista de textos associados
        logging.info(f"💾 Índice FAISS salvo em {FAISS_INDEX_PATH}!")

    def load_index(self):
        """Carrega o índice FAISS de disco, se existir."""
        if os.path.exists(FAISS_INDEX_PATH):
            self.index = faiss.read_index(FAISS_INDEX_PATH)
            with open(FAISS_INDEX_PATH + "_map.json", "r") as f:
                self.texts = json.load(f)  # Carrega a lista de textos associados
            logging.info("✅ Índice FAISS carregado com sucesso!")
        else:
            logging.warning("⚠️ Nenhum índice FAISS encontrado. Criando novo índice.")
