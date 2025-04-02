from utils.document_loader import load_documents, read_txt, read_pdf_in_pages
import logging

import unittest
import sys
import os


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

TEST_DSK_DIR = "tests/test_dsk"


class TestDocumentLoader(unittest.TestCase):

    def test_read_txt(self):
        """Tests reading a TXT file in the test_dsk folder."""
        file_path = os.path.join(TEST_DSK_DIR, "test_file.txt")
        self.assertTrue(os.path.exists(file_path), f"File {file_path} not found.")

        content = read_txt(file_path)
        self.assertGreater(len(content.strip()), 0, "The TXT file appears to be empty.")

    def test_read_pdf(self):
        """Tests the reading of a PDF file in the test_dsk folder."""
        file_path = os.path.join(TEST_DSK_DIR, "test_file.pdf")
        self.assertTrue(os.path.exists(file_path), f"File {file_path} not found.")

        content = read_pdf_in_pages(file_path)
        self.assertGreater(len(content.strip()), 0, "The PDF file appears to be empty.")

    def test_load_documents(self):
        """Test loading documents from the testdisk folder."""
        documents = load_documents(TEST_DSK_DIR)
        self.assertGreater(len(documents), 0, "No documents were loaded from the test_dsk folder.")

        txt_files = [f for f in documents if f.endswith(".txt")]
        pdf_files = [f for f in documents if f.endswith(".pdf")]

        self.assertGreater(len(txt_files), 0, "No TXT file was uploaded.")
        self.assertGreater(len(pdf_files), 0, "No PDF file was uploaded.")


if __name__ == "__main__":
    unittest.main()
