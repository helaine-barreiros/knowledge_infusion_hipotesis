import logging
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "src")))

#from src.rag.document_loader import load_documents
#from src.rag.embedding_generator import process_and_store_embeddings
from src.rag.llm_prompt import generate_diagram
from src.rag.extract_diagram_metadata import generate_plantuml_image
#from src.rag.token_calculator import count_tokens_from_documents

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def main():
    logging.info(f"DSK KNOWLEDGE EXPERIMENT PIPELINE STARTED")

    #print("🔹 Carregando documentos...")
    #documents = load_documents()

    
    #process_and_store_embeddings(documents)
    #count_tokens_from_documents(documents)

    plantuml_code = generate_diagram()

    generate_plantuml_image(plantuml_code, "teste")

    logging.info("🚀 DSK KNOWLEDGE EXPERIMENT PIPELINE CONCLUDED")

if __name__ == "__main__":
    main()
