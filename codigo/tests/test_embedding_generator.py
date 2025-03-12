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
        self.assertGreater(len(embedding[0]), 0)  # Embedding deve ter valores

    def test_generate_embedding_invalid_input(self):
        """Testa comportamento com entrada inválida"""
        embedding = generate_embedding("")
        self.assertIsNone(embedding)

        embedding = generate_embedding(None)
        self.assertIsNone(embedding)

    def test_save_embeddings(self):
        """Testa se os embeddings são salvos corretamente em um arquivo JSON"""
        test_embedding = [[0.1, 0.2, 0.3, 0.4]]  # Simula um embedding
        filename = "test_embedding"
        save_embeddings(test_embedding, filename)

        filepath = os.path.join(TEST_EMBEDDINGS_DIR, f"{filename}.json")
        self.assertTrue(os.path.exists(filepath))

        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
            self.assertEqual(data, test_embedding)

    def test_process_and_store_embeddings(self):
        """Testa a geração e armazenamento de embeddings para múltiplos documentos"""
        documents = {
            "test_file.txt": "Texto de exemplo para teste.",
            "test_file.pdf": "Outro exemplo de texto."
        }

        embeddings = process_and_store_embeddings(documents)
        self.assertEqual(len(embeddings), 2)  # Deve processar os dois documentos

        for filename in documents.keys():
            filepath = os.path.join(TEST_EMBEDDINGS_DIR, f"{filename}.json")
            self.assertTrue(os.path.exists(filepath))  # Verifica se os arquivos foram criados

if __name__ == "__main__":
    unittest.main()
