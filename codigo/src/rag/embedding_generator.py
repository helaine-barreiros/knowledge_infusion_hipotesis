import torch
from transformers import AutoTokenizer, AutoModel
from src.rag.config_loader import CONFIG
import os
import json
import logging

# Configuração do logger
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

try:
    # Carrega o modelo e tokenizer com base nas configurações

    logging.info("Carregando modelo de embeddings...")

    tokenizer = AutoTokenizer.from_pretrained(CONFIG["embedding_model"])
    model = AutoModel.from_pretrained(CONFIG["embedding_model"], trust_remote_code=True)

    logging.info("Modelo carregado com sucesso!")

except Exception as e:
    logging.error(f"Erro ao carregar modelo de embeddings: {e}")
    raise

def generate_embedding(text):
    """Gera embeddings para um texto usando o modelo NV-Embed."""

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

def save_embeddings(embeddings, filename):
    """Salva embeddings em um arquivo JSON."""

    if embeddings is None:
        logging.warning(f"Embeddings inválidos para {filename}, não serão salvos.")
        return
    
    try:
        os.makedirs(CONFIG["embeddings_dir"], exist_ok=True)
        filepath = os.path.join(CONFIG["embeddings_dir"], f"{filename}.json")

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(embeddings, f)
        
        logging.info(f"✅ Embeddings salvos com sucesso: {filepath}")
    except Exception as e:
        logging.error(f"Erro ao salvar embeddings para {filename}: {e}")

def process_and_store_embeddings(documents):
    """Gera e armazena embeddings para todos os documentos carregados."""

    processed_embeddings = {}
    
    for filename, text in documents.items():
        logging.info(f"Gerando embeddings para {filename}...")
        embeddings = generate_embedding(text)
        
        if embeddings is not None:
            save_embeddings(embeddings, filename)
            processed_embeddings[filename] = embeddings
        else:
            logging.warning(f"Falha ao gerar embeddings para {filename}.")

    return processed_embeddings  # Retorna os embeddings para uso posterior
