from src.rag_experiment.embedding_generator import generate_embedding, save_embeddings, process_and_store_embeddings
from utils.config_loader import CONFIG

import unittest
import sys
import os
import logging

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

TEST_EMBEDDINGS_DIR = "tests/test_embeddings"


class TestEmbeddingGenerator(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Configuração inicial para os testes"""
        os.makedirs(TEST_EMBEDDINGS_DIR, exist_ok=True)
        CONFIG["embeddings_dir"] = TEST_EMBEDDINGS_DIR  # Usa um diretório de teste para os embeddings
        logging.info("🛠️ Configuração inicial de testes concluída.")

    @classmethod
    def tearDownClass(cls):
        """Remove os arquivos de teste após execução"""
        if os.path.exists(TEST_EMBEDDINGS_DIR):
            logging.info(f"🧹 Removendo o diretório de embeddings de teste após execução")
            for file in os.listdir(TEST_EMBEDDINGS_DIR):
                os.remove(os.path.join(TEST_EMBEDDINGS_DIR, file))
            os.rmdir(TEST_EMBEDDINGS_DIR)
        else:
            logging.warning("⚠️ Diretório de embeddings de teste não encontrado para remoção.")

    def test_generate_embedding_valid_text(self):
        """Testa se a função de embedding gera um vetor válido"""
        logging.info("📝 Testando geração de embedding para um texto simples")

        text = "Teste de geração de embedding."
        embedding = generate_embedding(text)

        logging.info(f"Embedding gerado: {embedding}")

        self.assertIsInstance(embedding, list)
        self.assertGreater(len(embedding), 0, "⚠️ O embedding não contém valores.")

        # Verifica se cada embedding é um vetor de floats
        self.assertIsInstance(embedding[0], list)
        self.assertIsInstance(embedding[0][0], float)

    def test_process_and_store_embeddings(self):
        """Testa a geração e armazenamento de embeddings para múltiplos documentos"""
        logging.info("📂 Testando processamento de múltiplos documentos")

        documents = {
            "test_file.txt": "Texto de exemplo para teste.",
            "test_file.pdf": "Outro exemplo de texto."
        }

        embeddings = process_and_store_embeddings(documents)
        logging.info(f"Embeddings processados: {embeddings.keys()}")

        self.assertEqual(len(embeddings), len(documents), "⚠️ Nem todos os documentos foram processados corretamente.")

        # Verifica se os arquivos de embeddings foram realmente salvos
        for filename in documents.keys():
            filepath = os.path.join(TEST_EMBEDDINGS_DIR, f"{filename}_chunk0.json")
            self.assertTrue(os.path.exists(filepath), f"⚠️ Arquivo {filepath} não foi salvo.")

if __name__ == "__main__":
    unittest.main()
