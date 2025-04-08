from src.utils.system_parametrization import CONFIG
from src.rag_experiment.faiss_indexer import FaissIndexer
from keybert import KeyBERT
from sentence_transformers import SentenceTransformer
from sklearn.feature_extraction.text import TfidfVectorizer


import spacy
import os
import json
import logging
import numpy as np


logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

faiss_indexer = FaissIndexer(embedding_dim=1024)

# Carrega o modelo de embeddings BGE Large
try:
    logging.info("Carregando modelo de embeddings BGE Large...")
    model = SentenceTransformer("BAAI/bge-large-en")
    
    logging.info("Carregando modelo all-MiniLM-L6-v2 para extracao de palavras-chave...")
    # modelo para extrair palavras chave
    embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
    # Carregar modelo de NLP (spaCy)
    nlp = spacy.load("en_core_web_sm")  # Pode trocar por "pt_core_news_sm" para português

    # Inicializar modelo KeyBERT para extração de palavras-chave
    kw_model = KeyBERT()
    
    logging.info("Modelos carregados com sucesso!")

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

def split_by_page(document):
    """
    Divide o texto em chunks baseados em quebras de página.
    Mantém a separação semântica em páginas. Remove páginas em branco
    """

    #pages = [page.get_text("text") for page in document]
    return [page.get_textpage("text") for page in document]
    #return [page.strip() for page in pages if page.strip()]

def generate_embedding(text):
    """Gera embeddings para um texto usando o modelo BGE Large."""
    logging.info(f"Gerando embeddings para o texto: {repr(text)}")

    if not text or not isinstance(text, str):
        logging.warning("Texto inválido fornecido para embedding.")
        return None

    try:
        # Gera embeddings usando a função encode() do SentenceTransformer
        embedding = model.encode([text], normalize_embeddings=CONFIG["rag.normalize_embeddings"])

        return embedding.tolist()
    except Exception as e:
        logging.error(f"Erro ao gerar embeddings: {e}")
        return None

def extract_keywords_for_page_index(text, top=5):
    """
    Extrai palavras-chave significativas usando uma combinação de TF-IDF e KeyBERT.
    """

    # Remover stopwords e lematizar
    doc = nlp(text.lower())

    filtered_tokens = [token.lemma_ for token in doc if token.is_alpha and not token.is_stop]

    # Se o texto for pequeno, usar diretamente KeyBERT
    if len(filtered_tokens) < 10:
        logging.info("Extraindo keywords com KeyBERT")
        return kw_model.extract_keywords(text, keyphrase_ngram_range=(1, 2), top_n=top)

    # Caso contrário aplicar TF-IDF
    logging.info("Extraindo keywords com TF-IDF")
    vectorizer = TfidfVectorizer(max_features=100, stop_words='english')
    tfidf_matrix = vectorizer.fit_transform([" ".join(filtered_tokens)])
    feature_names = vectorizer.get_feature_names_out()
    
    # Obter palavras-chave com maior peso no TF-IDF
    tfidf_scores = np.array(tfidf_matrix.sum(axis=0)).flatten()
    sorted_indices = np.argsort(tfidf_scores)[::-1]  # Ordenar por importância
    top_keywords = [feature_names[i] for i in sorted_indices[:top_n]]
    
    return top_keywords

def save_embeddings_in_json(content, filename, page_number=None):
    """Salva um embedding de página gerado em arquivo JSON."""

    if content is None:
        logging.warning(f"⚠️ Não foi gerado embedding para página {page_number} do arquivo {filename}.")
        return

    try:
        os.makedirs(CONFIG["rag.embeddings_dir"], exist_ok=True)

        filename = f"{filename}_page{page_number}" if page_number is not None else filename
        filepath = os.path.join(CONFIG["rag.embeddings_dir"], f"{filename}.json")

        # Verifica se o arquivo já existe para evitar sobrescrita
        #if os.path.exists(filepath):
            #with open(filepath, "r", encoding="utf-8") as f:
                #embeddings_data = json.load(f)
        #else:
        embeddings_data = {}

        # Estrutura objeto JSON com as informações de geração do embedding
        embeddings_data[f"Page_{page_number}"] = {
            "embedding_content": content[0],  # Embedding do conteudo
            "embedding_keywords": content[1],  # Embedding do indexador
            "keywords": content[2],  # Keywords
            "content": content[3]  # Conteúdo da página
        }
            
        # Grava no JSON
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(embeddings_data, f, indent=4)

        logging.info(f"✅ Embedding da página {page_number} do documento {filename} salvos com sucesso: {filepath}")
    except Exception as e:
        logging.error(f"Erro ao salvar embedding da página {page_number} para {filename}: {e}")


def process_and_store_embeddings(documents):
    """
    Gera, armazena e indexa embeddings para todos os documentos carregados.
    """
    processed_embeddings = {}
    all_embeddings = []
    all_pages = []  # Alteração: armazenamos os parágrafos diretamente
    all_filenames = []

    for filename, document in documents.items():
        logging.info(f"📄 Processando {filename}...")

        # aqui vamos alterar o tratamento para o split por paginas do documento ao inves de paragrafos
        #chunks = split_by_newline(text)
        # os chunks sao as paginas de documentos pdf
        pages = split_by_page(document)

        embeddings_data = {}  # Dicionário para armazenar embeddings com textos

        for idx, page in enumerate(pages):
            # as páginas vazias já foram removidas
            #if not chunk.strip():
            #    continue  # Pular parágrafos vazios

            logging.info(f"Gerando embedding para {filename} - Chunk {idx}...")
            embedding = generate_embedding(page.getText())
            keywords = extract_keywords_for_page_index(page.getText())
            embeddingIndex =  generate_embedding(keywords)

            if embedding is not None:
                embeddings_data[f"Page_{idx}"] = {
                    "embedding_content": embedding[0],  # Embedding do conteudo
                    "embedding_keywords": embeddingIndex[0],  # Embedding do indexador
                    "keywords": keywords,  # Keywords
                    "content": page.getText()  # Conteúdo da página
                }
                
                save_embeddings_in_json(embeddings_data[f"Page_{idx}"], filename, idx)

                # TODO: agora precisamos salvar no FAISS com a mesma estrutura
                # PRECISO ADAPTAR O CODIGO DAQUI EM DIANTE

                processed_embeddings[f"{filename}_page{idx}"] = embedding

                all_embeddings.append(embedding[0])  # Convertendo para matriz FAISS
                all_texts.append(page.getText())  # Guardamos o parágrafo real para o FAISS
                all_filenames.append(f"{filename}_chunk{idx}")

            else:
                logging.warning(f"⚠️ Falha ao gerar embedding para {filename} - Chunk {idx}.")

        # Salva o JSON no formato correto
        json_filepath = os.path.join(CONFIG["rag.embeddings_dir"], f"{filename}.json")
        with open(json_filepath, "w", encoding="utf-8") as f:
            json.dump(embeddings_data, f, indent=4)

        logging.info(f"✅ Embeddings salvos com sucesso: {json_filepath}")

    # Adiciona embeddings ao FAISS corretamente
    faiss_indexer.add_embeddings(all_embeddings, all_texts)  # Agora associamos ao texto
    faiss_indexer.save_index()  # Salva o índice FAISS atualizado

    return processed_embeddings