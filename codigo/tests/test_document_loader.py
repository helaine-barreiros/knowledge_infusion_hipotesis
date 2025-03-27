import unittest
import sys
import os

# Adiciona o diretório raiz do projeto ao path do Python
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.rag.document_loader import load_documents, read_txt, read_pdf_in_pages
import logging

# Configuração do logger
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Diretório onde você colocará os arquivos de teste
TEST_DSK_DIR = "tests/test_dsk"

class TestDocumentLoader(unittest.TestCase):
    
    def test_read_txt(self):
        """Testa a leitura de um arquivo TXT na pasta test_dsk."""
        file_path = os.path.join(TEST_DSK_DIR, "test_file.txt")
        self.assertTrue(os.path.exists(file_path), f"Arquivo {file_path} não encontrado.")
        
        content = read_txt(file_path)
        self.assertGreater(len(content.strip()), 0, "O arquivo TXT parece estar vazio.")

    def test_read_pdf(self):
        """Testa a leitura de um arquivo PDF na pasta test_dsk."""
        file_path = os.path.join(TEST_DSK_DIR, "test_file.pdf")
        self.assertTrue(os.path.exists(file_path), f"Arquivo {file_path} não encontrado.")
        
        content = read_pdf_in_pages(file_path)
        self.assertGreater(len(content.strip()), 0, "O arquivo PDF parece estar vazio.")

    def test_load_documents(self):
        """Testa o carregamento de documentos da pasta test_dsk."""
        documents = load_documents(TEST_DSK_DIR)
        self.assertGreater(len(documents), 0, "Nenhum documento foi carregado da pasta test_dsk.")
        
        # Verificar se pelo menos um arquivo TXT e um PDF foram carregados
        txt_files = [f for f in documents if f.endswith(".txt")]
        pdf_files = [f for f in documents if f.endswith(".pdf")]
        
        self.assertGreater(len(txt_files), 0, "Nenhum arquivo TXT foi carregado.")
        self.assertGreater(len(pdf_files), 0, "Nenhum arquivo PDF foi carregado.")

if __name__ == "__main__":
    unittest.main()
