import unittest
import os
import json
import logging
import numpy as np
from src.rag.faiss_indexer import FaissIndexer
from src.rag.config_loader import CONFIG

# Configuração do logger
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

EMBEDDINGS_DIR = "./embeddings"  # Diretório onde os embeddings já estão salvos
TEST_FAISS_DIR = "tests/test_faiss"
GLOSSARY_EMBEDDING_FILE = "Glossary_of_Terms.pdf_chunk0.json"  # Apenas esse arquivo será carregado

class TestGlossaryEmbeddings(unittest.TestCase):
    """Testa a recuperação de termos do Glossário usando FAISS e os embeddings pré-gerados."""

    @classmethod
    def setUpClass(cls):
        """Configuração inicial: Carrega FAISS apenas com os embeddings do Glossário."""
        os.makedirs(TEST_FAISS_DIR, exist_ok=True)
        CONFIG["embeddings_dir"] = EMBEDDINGS_DIR  # Define a pasta correta dos embeddings

        cls.faiss_indexer = FaissIndexer(embedding_dim=1024)  # Dimensão do modelo BGE Large
        cls.load_glossary_embedding_into_faiss()  # Carrega apenas o arquivo do Glossário

        logging.info(f"📂 FAISS contém {cls.faiss_indexer.index.ntotal} embeddings armazenados.")

    @classmethod
    def tearDownClass(cls):
        """Remove os arquivos de teste após execução."""
        if os.path.exists(TEST_FAISS_DIR):
            logging.info(f"🧹 Removendo diretório FAISS de teste após execução")
            for file in os.listdir(TEST_FAISS_DIR):
                os.remove(os.path.join(TEST_FAISS_DIR, file))
            os.rmdir(TEST_FAISS_DIR)
        else:
            logging.warning("⚠️ Diretório FAISS de teste não encontrado para remoção.")

    @classmethod
    def load_glossary_embedding_into_faiss(cls):
        """Carrega apenas os embeddings do Glossário no FAISS."""
        logging.info(f"🔍 Carregando embeddings do arquivo: {GLOSSARY_EMBEDDING_FILE}")

        filepath = os.path.join(EMBEDDINGS_DIR, GLOSSARY_EMBEDDING_FILE)
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"❌ Arquivo de embeddings não encontrado: {filepath}")

        with open(filepath, "r", encoding="utf-8") as f:
            embeddings = json.load(f)

        # Adiciona os embeddings no FAISS
        for emb in embeddings:
            vector = np.array(emb, dtype=np.float32)
            cls.faiss_indexer.add_to_index(vector, GLOSSARY_EMBEDDING_FILE)

        cls.faiss_indexer.save_index()  # Garante que FAISS salva o índice atualizado

    def test_retrieve_correct_definitions(self):
        """Testa se FAISS recupera corretamente as definições de termos do glossário."""
        logging.info("🔍 Testando recuperação de definições do Glossário...")

        test_queries = {
            "O que significa reserva?": "Ação de garantir um quarto para um hóspede antes da estadia.",
            "Qual a definição de check-in?": "Processo pelo qual um hóspede se registra no hotel.",
            "O que é um hóspede?": "Pessoa que reserva e utiliza os serviços do hotel.",
        }

        success_count = 0
        total_queries = len(test_queries)

        for query, expected_answer in test_queries.items():
            query_embedding = self.faiss_indexer.search_by_text(query, top_k=3)  # Recupera da FAISS
            logging.info(f"🔎 Consulta: {query}")
            logging.info(f"📌 Definição Esperada: {expected_answer}")
            logging.info(f"📊 Resultados Recuperados: {query_embedding}")

            # Verifica se algum resultado contém a resposta esperada
            correct_found = any(expected_answer.lower() in result.lower() for result in query_embedding)

            if correct_found:
                success_count += 1

        accuracy = success_count / total_queries
        logging.info(f"✅ Precisão da recuperação: {accuracy:.2%}")

        self.assertGreater(accuracy, 0.5, "⚠️ Precisão abaixo de 50%, recuperação pode estar ruim.")

if __name__ == "__main__":
    unittest.main()
