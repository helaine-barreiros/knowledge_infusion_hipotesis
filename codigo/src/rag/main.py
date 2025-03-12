import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "src")))

from src.rag.document_loader import load_documents
from src.rag.embedding_generator import process_and_store_embeddings

def main():
    """Pipeline principal, carrega documentos e gera embeddings."""

    print("🔹 Carregando documentos...")
    documents = load_documents()

    if not documents:
        print("⚠️ Nenhum documento encontrado na pasta especificada. Verifique o diretório.")
        return

    print("✅ Documentos carregados. Gerando embeddings...")
    process_and_store_embeddings(documents)

    print("🚀 Processo concluído! Os embeddings foram armazenados.")

if __name__ == "__main__":
    main()
