from sentence_transformers import SentenceTransformer

import torch
import os
import json
import logging

from src.rag.config_loader import CONFIG
from src.rag.faiss_indexer import FaissIndexer


# Configuração do logger
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
faiss_indexer = FaissIndexer(embedding_dim=1024)

# Carrega o modelo de embeddings BGE Large
try:
    logging.info("Carregando modelo de embeddings BGE Large...")

    model = SentenceTransformer("BAAI/bge-large-en")

    logging.info("Modelo carregado com sucesso!")
except Exception as e:
    logging.error(f"Erro ao carregar modelo de embeddings: {e}")
    raise

def split_by_newline(text):
    """
    Divide o texto em chunks baseados em quebras de linha dupla (\n\n).
    Mantém a separação semântica dos parágrafos.
    """
    chunks = text.split("\n\n")
    return [chunk.strip() for chunk in chunks if len(chunk.strip()) > 0]

def generate_embedding(text):
    """Gera embeddings para um texto usando o modelo BGE Large."""
    logging.info(f"Gerando embeddings para o texto: {repr(text)}")

    if not text or not isinstance(text, str):
        logging.warning("Texto inválido fornecido para embedding.")
        return None

    try:
        # Gera embeddings usando a função encode() do SentenceTransformer
        embedding = model.encode([text], normalize_embeddings=CONFIG["normalize_embeddings"])

        return embedding.tolist()
    except Exception as e:
        logging.error(f"Erro ao gerar embeddings: {e}")
        return None

def save_embeddings(embeddings, text, filename, chunk_index=None):
    """Salva embeddings em um arquivo JSON junto com o texto associado."""
    if embeddings is None:
        logging.warning(f"⚠️ Embeddings inválidos para {filename}, não serão salvos.")
        return

    try:
        os.makedirs(CONFIG["embeddings_dir"], exist_ok=True)
        filename = f"{filename}_chunk{chunk_index}" if chunk_index is not None else filename
        filepath = os.path.join(CONFIG["embeddings_dir"], f"{filename}.json")

        # Verifica se o arquivo já existe para evitar sobrescrita
        if os.path.exists(filepath):
            with open(filepath, "r", encoding="utf-8") as f:
                embeddings_data = json.load(f)
        else:
            embeddings_data = {}

        # Salva o embedding e o parágrafo associado
        embeddings_data[f"Paragraph_{chunk_index}"] = {
            "embedding": embeddings[0],  # Vetor de embedding
            "text": text  # Texto associado
        }

        # Grava no JSON
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(embeddings_data, f, indent=4)

        logging.info(f"✅ Embeddings salvos com sucesso: {filepath}")
    except Exception as e:
        logging.error(f"Erro ao salvar embeddings para {filename}: {e}")


def process_and_store_embeddings(documents):
    """
    Gera, armazena e indexa embeddings para todos os documentos carregados.
    """
    processed_embeddings = {}
    all_embeddings = []
    all_texts = []  # Alteração: armazenamos os parágrafos diretamente
    all_filenames = []

    for filename, text in documents.items():
        logging.info(f"📄 Processando {filename}...")

        chunks = split_by_newline(text)
        embeddings_data = {}  # Dicionário para armazenar embeddings com textos

        for idx, chunk in enumerate(chunks):
            if not chunk.strip():
                continue  # Pular parágrafos vazios

            logging.info(f"Gerando embedding para {filename} - Chunk {idx}...")
            embedding = generate_embedding(chunk)

            if embedding is not None:
                embeddings_data[f"Paragraph_{idx}"] = {
                    "embedding": embedding[0],  # Garante que o vetor seja armazenado corretamente
                    "text": chunk  # Associamos o parágrafo correspondente
                }

                save_embeddings(embeddings_data, filename, chunk_index=idx)
                processed_embeddings[f"{filename}_chunk{idx}"] = embedding

                all_embeddings.append(embedding[0])  # Convertendo para matriz FAISS
                all_texts.append(chunk)  # Guardamos o parágrafo real para o FAISS
                all_filenames.append(f"{filename}_chunk{idx}")

            else:
                logging.warning(f"⚠️ Falha ao gerar embedding para {filename} - Chunk {idx}.")

        # Salva o JSON no formato correto
        json_filepath = os.path.join(CONFIG["embeddings_dir"], f"{filename}.json")
        with open(json_filepath, "w", encoding="utf-8") as f:
            json.dump(embeddings_data, f, indent=4)

        logging.info(f"✅ Embeddings salvos com sucesso: {json_filepath}")

    # Adiciona embeddings ao FAISS corretamente
    faiss_indexer.add_embeddings(all_embeddings, all_texts)  # Agora associamos ao texto
    faiss_indexer.save_index()  # Salva o índice FAISS atualizado

    return processed_embeddings