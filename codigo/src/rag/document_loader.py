import os
import PyPDF2
#import fitz
import logging

from src.rag.config_loader import CONFIG

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def read_txt(file_path):
    """Retorna o conteúdo de um arquivo TXT."""
    
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()

def read_pdf(file_path):
    """Retorna o conteúdo de um arquivo PDF."""
    
    text = ""
    with open(file_path, "rb") as file:

        reader = PyPDF2.PdfReader(file)

        for page in reader.pages:
            text += page.extract_text() + "\n"

    return text

def load_documents(directory=None):
    """Carrega documentos do diretório definido nas configurações."""

    if directory is None:
        directory = CONFIG["dsk_dir"]
        
    documents = {}

    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)

        if filename.endswith(".txt"):
            #todo: remover este tipo de tratamento por enquanto
            documents[filename] = read_txt(file_path)
            #raise "Arquivos txt não são suportados"
        elif filename.endswith(".pdf"):
            #todo: alterei a leitura do pdf para abrir o pdf com a biblioteca fitz
            #documents[filename] = read_pdf(file_path)
           # documents[filename] = fitz.open(file_path)
           logging.warning("Deactivated functionality")

    return documents

