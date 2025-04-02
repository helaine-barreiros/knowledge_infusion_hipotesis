from src.utils.document_loader import DocumentLoader
import logging
import unittest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

TEST_DSK_DIR = "tests/utils/file_resources"


class TestDocumentLoader(unittest.TestCase):

    def setUp(self):
        """Set up an instance of DocumentLoader for testing."""
        self.loader = DocumentLoader()

    def test_read_txt_valid_file(self):
        """Tests reading a TXT file in the test_dsk folder."""
        file_path = os.path.join(TEST_DSK_DIR, "test_file.txt")
        self.assertTrue(os.path.exists(file_path), f"File {file_path} not found.")

        content = self.loader.read_txt(file_path)
        self.assertGreater(len(content.strip()), 0, "The TXT file appears to be empty.")

    def test_read_txt_non_existent_file(self):
        """Tests reading a non-existent TXT file."""
        file_path = os.path.join(TEST_DSK_DIR, "non_existent_file.txt")

        content = self.loader.read_txt(file_path)
        self.assertIsNone(content, "Expected None for a non-existent file, but got a value.")

    def test_read_txt_empty_file_content(self):
        """Tests reading an empty TXT file."""
        file_path = os.path.join(TEST_DSK_DIR, "empty_file.txt")

        self.assertTrue(os.path.exists(file_path), f"File {file_path} not found.")

        content = self.loader.read_txt(file_path)

        self.assertEqual(content, "", "Expected an empty string for an empty file, but got a different value.")

    def test_read_pdf_valid_file(self):
        """Tests the reading of a PDF file in the test_dsk folder."""
        file_path = os.path.join(TEST_DSK_DIR, "test_file.pdf")
        self.assertTrue(os.path.exists(file_path), f"File {file_path} not found.")

        content = self.loader.read_pdf_as_text(file_path)
        self.assertGreater(len(content.strip()), 0, "The PDF file appears to be empty.")

    def test_load_documents_from_valid_directory(self):
        """Test loading documents from the test_dsk folder."""
        documents = self.loader.load_documents(TEST_DSK_DIR)
        self.assertGreater(len(documents), 0, "No documents were loaded from the test_dsk folder.")

        txt_files = [f for f in documents if f.endswith(".txt")]
        pdf_files = [f for f in documents if f.endswith(".pdf")]

        self.assertGreater(len(txt_files), 0, "No TXT file was uploaded.")
        self.assertGreater(len(pdf_files), 0, "No PDF file was uploaded.")


if __name__ == "__main__":
    unittest.main()
