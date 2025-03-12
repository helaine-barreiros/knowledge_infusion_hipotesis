import unittest
import os
import logging
import numpy as np
from src.rag.faiss_indexer import FaissIndexer
from src.rag.embedding_generator import generate_embedding
from src.rag.config_loader import CONFIG

# Configuração do logger
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

TEST_FAISS_DIR = "tests/test_faiss"
GLOSSARY_TEST_FILE = "Glossary_of_Terms.pdf"

class TestGlossaryEmbeddings(unittest.TestCase):
    """Testa a recuperação de termos do Glossário usando embeddings e FAISS."""

    @classmethod
    def setUpClass(cls):
        """Configuração inicial: Define diretório de testes e carrega FAISS."""
        os.makedirs(TEST_FAISS_DIR, exist_ok=True)
        CONFIG["embeddings_dir"] = TEST_FAISS_DIR  # Define diretório de testes para embeddings

        cls.faiss_indexer = FaissIndexer(embedding_dim=1024)  # Dimensão do modelo BGE Large
        cls.faiss_indexer.load_index()  # Carrega o índice FAISS se existir
        logging.info("🛠️ Configuração inicial concluída para o teste do glossário.")

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
        distance_scores = []

        for query, expected_answer in test_queries.items():
            query_embedding = generate_embedding(query)[0]  # Pegamos apenas a lista de floats
            results = self.faiss_indexer.search(query_embedding, top_k=3)

            logging.info(f"🔎 Consulta: {query}")
            logging.info(f"📌 Definição Esperada: {expected_answer}")
            logging.info(f"📊 Resultados Recuperados: {results}")

            # Verifica se algum resultado contém a resposta esperada
            correct_found = any(expected_answer.lower() in result[0].lower() for result in results)

            if correct_found:
                success_count += 1
                distance_scores.append(results[0][1])  # Pega a distância do primeiro resultado

        accuracy = success_count / total_queries
        avg_distance = np.mean(distance_scores) if distance_scores else float("inf")

        logging.info(f"✅ Precisão da recuperação: {accuracy:.2%}")
        logging.info(f"📏 Distância média dos embeddings retornados: {avg_distance:.4f}")

        self.assertGreater(accuracy, 0.5, "⚠️ Precisão abaixo de 50%, recuperação pode estar ruim.")
        self.assertLess(avg_distance, 1.5, "⚠️ Média de distância alta, embeddings podem estar desalinhados.")

    def test_relevance_ranking(self):
        """Testa se as respostas esperadas aparecem no topo do ranking de FAISS."""
        logging.info("📊 Testando ranking de relevância das respostas...")

        test_queries = {
            "O que significa reserva?": "Ação de garantir um quarto para um hóspede antes da estadia.",
            "Qual a definição de check-in?": "Processo pelo qual um hóspede se registra no hotel.",
            "O que é um hóspede?": "Pessoa que reserva e utiliza os serviços do hotel.",
        }

        top1_count = 0
        total_queries = len(test_queries)

        for query, expected_answer in test_queries.items():
            query_embedding = generate_embedding(query)[0]  # Pegamos apenas a lista de floats
            results = self.faiss_indexer.search(query_embedding, top_k=3)

            logging.info(f"🔎 Consulta: {query}")
            logging.info(f"📌 Definição
