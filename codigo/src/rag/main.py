from document_loader import load_documents
from embedding_generator import process_and_store_embeddings

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
