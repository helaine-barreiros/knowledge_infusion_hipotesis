import faiss
import numpy as np
import os
import json
import logging
from src.rag.config_loader import CONFIG

# Configuração do logger
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

FAISS_INDEX_PATH = os.path.join(CONFIG["embeddings_dir"], "faiss_index")

class FaissIndexer:
    def __init__(self, embedding_dim=1024):  # Dimensão do modelo BGE Large
        """Inicializa o FAISS index."""
        self.index = faiss.IndexFlatL2(embedding_dim)  # Distância Euclidiana (L2)
        self.id_map = {}  # Mapeia IDs dos embeddings para nomes dos arquivos
        self.texts = []  # Lista para armazenar textos associados aos embeddings

    def add_embeddings(self, vector, text_id):
        """Adiciona um vetor ao índice FAISS e armazena a referência ao texto."""
        vector = np.array(vector, dtype=np.float32)  # Converte para float32 (necessário para FAISS)

        if vector.ndim == 1:  # Se for um vetor unidimensional, transforma em matriz 1xD
            vector = vector.reshape(1, -1)

        self.index.add(vector)  # Adiciona o vetor ao FAISS
        self.texts.append(text_id)  # Armazena a referência do texto associado
        logging.info(f"✅ Embedding adicionado ao FAISS com ID: {text_id}")

    def search(self, query_embedding, top_k=5):
        """Busca os embeddings mais similares no índice FAISS."""
        query_vector = np.array([query_embedding]).astype('float32')
        distances, indices = self.index.search(query_vector, top_k)

        results = []
        for i, idx in enumerate(indices[0]):
            if idx < 0 or idx >= len(self.texts):
                continue
            filename = self.texts[idx]  # Recupera o nome do arquivo associado ao embedding
            results.append((filename, distances[0][i]))

        return results

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
