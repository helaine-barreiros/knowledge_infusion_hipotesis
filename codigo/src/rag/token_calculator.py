from spacy import load
from transformers import AutoTokenizer

import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

tokenizer = AutoTokenizer.from_pretrained("teknium/OpenHermes-2.5-Mistral-7B", use_fast=False, force_download=True)
nlp = load("en_core_web_sm")
logging.info("Modelo carregado com sucesso!")

def count_tokens_from_message(message):
    #logging.debug(tokenizer.encode(message))
    return len(tokenizer.encode(message))

def count_tokens_from_documents(documents={}):
    tokens = 0

    for filename, content in documents.items():
        logging.info(f"Processing token counter from file: {filename} content:{content}")
        tokens += count_tokens_from_message(content)
        logging.info(f"{tokens} computed tokens")

    return tokens
