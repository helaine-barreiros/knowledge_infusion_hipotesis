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

    def add_embeddings(self, embeddings, filenames):
        """Adiciona embeddings ao índice FAISS."""
        if len(embeddings) == 0:
            logging.warning("Nenhum embedding fornecido para indexação.")
            return

        vectors = np.array(embeddings).astype('float32')
        self.index.add(vectors)  # Adiciona os vetores ao índice

        # Mapeia os IDs no índice aos nomes dos arquivos
        for i, filename in enumerate(filenames):
            self.id_map[self.index.ntotal - len(filenames) + i] = filename

        logging.info(f"✅ {len(embeddings)} embeddings adicionados ao FAISS!")

    def search(self, query_embedding, top_k=5):
        """Busca os embeddings mais similares no índice FAISS."""
        query_vector = np.array([query_embedding]).astype('float32')
        distances, indices = self.index.search(query_vector, top_k)

        results = []
        for i, idx in enumerate(indices[0]):
            if idx < 0:
                continue
            filename = self.id_map.get(idx, "Desconhecido")
            results.append((filename, distances[0][i]))

        return results

    def save_index(self):
        """Salva o índice FAISS em disco."""
        faiss.write_index(self.index, FAISS_INDEX_PATH)
        with open(FAISS_INDEX_PATH + "_map.json", "w") as f:
            json.dump(self.id_map, f)
        logging.info(f"💾 Índice FAISS salvo em {FAISS_INDEX_PATH}!")

    def load_index(self):
        """Carrega o índice FAISS de disco, se existir."""
        if os.path.exists(FAISS_INDEX_PATH):
            self.index = faiss.read_index(FAISS_INDEX_PATH)
            with open(FAISS_INDEX_PATH + "_map.json", "r") as f:
                self.id_map = json.load(f)
            logging.info("✅ Índice FAISS carregado com sucesso!")
        else:
            logging.warning("⚠️ Nenhum índice FAISS encontrado. Criando novo índice.")
