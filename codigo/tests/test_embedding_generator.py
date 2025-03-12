import unittest
import sys
import os
import json
# Adiciona o diretório raiz ao sys.path para permitir importações corretas
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.rag.embedding_generator import generate_embedding, save_embeddings, process_and_store_embeddings
from src.rag.config_loader import CONFIG
import logging

# Configuração do logger
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

TEST_EMBEDDINGS_DIR = "tests/test_embeddings"

class TestEmbeddingGenerator(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Configuração inicial para os testes"""
        os.makedirs(TEST_EMBEDDINGS_DIR, exist_ok=True)
        CONFIG["embeddings_dir"] = TEST_EMBEDDINGS_DIR  # Usa um diretório de teste para os embeddings

    @classmethod
    def tearDownClass(cls):
        logging.info(f"Removendo o diretório de embeddings de teste após execução")

        for file in os.listdir(TEST_EMBEDDINGS_DIR):
            os.remove(os.path.join(TEST_EMBEDDINGS_DIR, file))

        os.rmdir(TEST_EMBEDDINGS_DIR)

    def test_generate_embedding_valid_text(self):
        logging.info("Teste da função de embedding para um texto simples")
        
        text = "Teste de geração de embedding."
        embedding = generate_embedding(text)
        
        self.assertIsInstance(embedding, list)
        self.assertGreater(len(embedding), 0)  # Embedding deve conter valores

    def test_process_and_store_embeddings(self):
        """Testa a geração e armazenamento de embeddings para múltiplos documentos"""
        documents = {
            "test_file.txt": "Texto de exemplo para teste.",
            "test_file.pdf": "Outro exemplo de texto."
        }

        embeddings = process_and_store_embeddings(documents)
        self.assertEqual(len(embeddings), 2)  # Deve processar os dois documentos

if __name__ == "__main__":
    unittest.main()
