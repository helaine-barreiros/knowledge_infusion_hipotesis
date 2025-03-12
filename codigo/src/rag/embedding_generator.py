import torch
from transformers import AutoTokenizer, AutoModel
from src.rag.config_loader import CONFIG
import os
import json
import logging

# Configuração do logger
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Carrega o modelo e tokenizer com base nas configurações
try:
    logging.info("Carregando modelo de embeddings...")

    tokenizer = AutoTokenizer.from_pretrained(CONFIG["embedding_model"])
    model = AutoModel.from_pretrained(CONFIG["embedding_model"], trust_remote_code=True)

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
    logging.info(f"Gerando embeddings para o texto: {text}")
    
    if not text or not isinstance(text, str):
        logging.warning("Texto inválido fornecido para embedding.")
        return None
    
    try:
        inputs = tokenizer(text, padding=True, truncation=True, return_tensors="pt", max_length=CONFIG["max_tokens"])

        with torch.no_grad():
            outputs = model(**inputs, output_hidden_states=True, return_dict=True)
            embedding = outputs.hidden_states[-1][:, 0, :]
        
        if CONFIG["normalize_embeddings"]:
            embedding = torch.nn.functional.normalize(embedding, p=2, dim=1)

        return embedding.tolist()
    except Exception as e:
        logging.error(f"Erro ao gerar embeddings: {e}")
        return None

def save_embeddings(embeddings, filename, chunk_index=None):
    """Salva embeddings em um arquivo JSON. Cada chunk recebe um nome único."""
    if embeddings is None:
        logging.warning(f"Embeddings inválidos para {filename}, não serão salvos.")
        return
    
    try:
        os.makedirs(CONFIG["embeddings_dir"], exist_ok=True)
        filename = f"{filename}_chunk{chunk_index}" if chunk_index is not None else filename
        filepath = os.path.join(CONFIG["embeddings_dir"], f"{filename}.json")

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(embeddings, f)
        
        logging.info(f"✅ Embeddings salvos com sucesso: {filepath}")
    except Exception as e:
        logging.error(f"Erro ao salvar embeddings para {filename}: {e}")

def process_and_store_embeddings(documents):
    """
    Gera e armazena embeddings para todos os documentos carregados,
    segmentando-os por quebras de linha dupla.
    """
    processed_embeddings = {}

    for filename, text in documents.items():
        logging.info(f"📄 Processando {filename}...")

        # Divide o texto em chunks usando \n\n como separador
        chunks = split_by_newline(text)

        for idx, chunk in enumerate(chunks):
            logging.info(f"Gerando embedding para {filename} - Chunk {idx}...")
            embedding = generate_embedding(chunk)
            
            if embedding is not None:
                save_embeddings(embedding, filename, chunk_index=idx)
                processed_embeddings[f"{filename}_chunk{idx}"] = embedding
            else:
                logging.warning(f"Falha ao gerar embedding para {filename} - Chunk {idx}.")

    return processed_embeddings  # Retorna os embeddings para uso posterior
