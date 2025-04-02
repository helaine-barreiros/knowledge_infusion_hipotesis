import unittest
import os
import numpy as np
import logging
from src.rag_experiment.faiss_indexer import FaissIndexer
from src.rag_experiment.embedding_generator import generate_embedding
from utils.config_loader import CONFIG

# Configuração do logger
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

TEST_FAISS_DIR = "tests/test_faiss"

class TestFaissIndexer(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Configuração inicial dos testes"""
        os.makedirs(TEST_FAISS_DIR, exist_ok=True)
        CONFIG["embeddings_dir"] = TEST_FAISS_DIR  # Define diretório de testes para embeddings

        cls.faiss_indexer = FaissIndexer(embedding_dim=1024)  # Dimensão do modelo BGE Large
        logging.info("🛠️ Configuração inicial de FAISS concluída.")

    @classmethod
    def tearDownClass(cls):
        """Remove os arquivos de teste após execução"""
        if os.path.exists(TEST_FAISS_DIR):
            logging.info(f"🧹 Removendo o diretório FAISS de teste após execução")
            for file in os.listdir(TEST_FAISS_DIR):
                os.remove(os.path.join(TEST_FAISS_DIR, file))
            os.rmdir(TEST_FAISS_DIR)
        else:
            logging.warning("⚠️ Diretório FAISS de teste não encontrado para remoção.")

    def test_add_embeddings(self):
        """Testa a adição de embeddings ao índice FAISS"""
        logging.info("📝 Testando adição de embeddings ao FAISS")

        texts = ["Diagrama UML representa estados.", "Máquinas de estado modelam processos."]
        embeddings = [generate_embedding(text)[0] for text in texts]  # Pegamos apenas a lista de floats
        filenames = ["uml_chunk0", "uml_chunk1"]

        self.faiss_indexer.add_embeddings(embeddings, filenames)

        self.assertEqual(self.faiss_indexer.index.ntotal, len(texts), "⚠️ O número de embeddings no índice FAISS não corresponde ao esperado.")

    def test_search_embeddings(self):
        """Testa a recuperação de embeddings mais similares"""
        logging.info("🔎 Testando recuperação de embeddings no FAISS")

        query_text = "Estados e transições em UML."
        query_embedding = generate_embedding(query_text)[0]

        results = self.faiss_indexer.search(query_embedding, top_k=2)
        logging.info(f"🔎 Resultados da busca: {results}")

        self.assertGreater(len(results), 0, "⚠️ Nenhum resultado foi retornado pelo FAISS.")
        self.assertIsInstance(results[0], tuple, "⚠️ O formato do resultado não está correto.")

    def test_save_and_load_index(self):
        """Testa a persistência do índice FAISS"""
        logging.info("💾 Testando salvar e carregar índice FAISS")

        self.faiss_indexer.save_index()
        self.faiss_indexer.load_index()

        self.assertGreater(self.faiss_indexer.index.ntotal, 0, "⚠️ O índice FAISS não foi carregado corretamente.")

if __name__ == "__main__":
    unittest.main()
