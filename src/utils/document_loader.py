from utils.logger import Logger
from utils.system_parametrization import SYSTEM_CONFIG

import os
import PyPDF2
import fitz
import base64


class DocumentLoader:
    """
    Ensures that only one instance of the DocumentLoader class is created (Singleton pattern).

    Args:
        *args: Variable length argument list.
        **kwargs: Arbitrary keyword arguments.

    Returns:
        DocumentLoader: The single instance of the DocumentLoader class.
    """

    _instance = None

    def __new__(cls, *args, **kwargs):
        """
        Ensures that only one instance of the DocumentLoader class is created (Singleton pattern).

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            DocumentLoader: The single instance of the DocumentLoader class.
        """
        if cls._instance is None:
            cls._instance = super(DocumentLoader, cls).__new__(cls)

        return cls._instance

    def __init__(self, *args, **kwargs):
        """
        Initializes the DocumentLoader class.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Notes:
            - Ensures that the LOGGER attribute is initialized only once.
        """
        if not hasattr(self, "initialized"):
            self.LOGGER = Logger
            self.initialized = True

    def read_txt(self, file_path):
        """
        Reads the content of a TXT file.

        Args:
            file_path (str): The path to the TXT file.

        Returns:
            str: The content of the TXT file as a string, or None if an error occurs.

        Notes:
            - Logs an informational message when reading starts.
            - Logs an error message if the file cannot be read.
            - Uses UTF-8 encoding to read the file.
        """
        content = None

        if not file_path:
            return content

        self.LOGGER.info(f"Reading TXT file from : {file_path}")

        try:
            with open(file_path, "r", encoding="utf-8") as file:
                return file.read()
        except Exception as e:
            self.LOGGER.error(f"Failed to read TXT file {file_path}: {e}")

        return content

    def read_pdf_as_text(self, file_path):
        """
        Reads the content of a PDF file and extracts its text.

        Args:
            file_path (str): The path to the PDF file.

        Returns:
            str: The extracted text from the PDF file as a single string, or None if an error occurs.

        Notes:
            - Logs an informational message when reading starts.
            - Uses the `PyPDF2` library to read the PDF file.
            - Iterates through all pages of the PDF and extracts text from each page.
            - If no text is extracted from a page, logs a warning message.
            - If an error occurs while reading the file, logs an error message and returns None.
            - The extracted text from all pages is concatenated with a newline character (`\n`) between pages.
        """
        text = None

        if not file_path:
            return text

        self.LOGGER.info(f"Reading PDF file: {file_path}")

        try:
            with open(file_path, "rb") as file:
                reader = PyPDF2.PdfReader(file)

                text = ""

                for page in reader.pages:
                    if extracted_text := page.extract_text():
                        text += extracted_text + "\n"
                    else:
                        self.LOGGER.warning(f"No text extracted from page in {file_path}")

        except Exception as e:
            text = None
            self.LOGGER.info(f"Could not read PDF file {file_path}: {e}")

        return text

    def read_pdf_as_base64(self, file_path):
        """
        Loads documents from a specified directory, supporting TXT and PDF files.

        Args:
            directory (str, optional): The directory containing the documents. 
                                    If None, the directory is retrieved from the `SYSTEM_CONFIG` using the key `dsk_dir`.
            load_pdf_in_base64 (bool, optional): If True, PDF files are loaded as Base64-encoded strings. Defaults to False.

        Returns:
            dict: A dictionary where the keys are filenames and the values are the file contents.

        Raises:
            KeyError: If the `dsk_dir` key is missing in the configuration and no directory is provided.

        Notes:
            - If the directory does not exist, it is created automatically.
            - Logs the progress of loading documents, including the directory being used and the total number of documents loaded.
            - Supports the following file types:
                - `.txt`: Read as plain text using the `read_txt` method.
                - `.pdf`: Read as text using `fitz` (PyMuPDF) or encoded as Base64 using the `get_pdf_base64` method.
            - Skips files that cannot be read and logs an error message for each skipped file.
        """

        content = None

        if not file_path:
            return content

        try:
            with open(file_path, "rb") as pdf_file:
                pdf_bytes = pdf_file.read()
                content = base64.b64encode(pdf_bytes).decode("utf-8")

        except Exception as e:
            self.LOGGER.info(f"Error reading or encoding PDF: {e}")

        return content

    def load_documents(self, directory=None, load_pdf_in_base64=False):
        """
    Loads documents from a specified directory, supporting TXT and PDF files.

    Args:
        directory (str, optional): The directory containing the documents. 
                                   If None, the directory is retrieved from the `SYSTEM_CONFIG` using the key `dsk_dir`.
        load_pdf_in_base64 (bool, optional): If True, PDF files are loaded as Base64-encoded strings. Defaults to False.

    Returns:
        dict: A dictionary where the keys are filenames and the values are the file contents.

    Raises:
        KeyError: If the `dsk_dir` key is missing in the configuration and no directory is provided.

    Notes:
        - If the directory does not exist, it is created automatically.
        - Logs the progress of loading documents, including the directory being used and the total number of documents loaded.
        - Supports the following file types:
            - `.txt`: Read as plain text using the `read_txt` method.
            - `.pdf`: Read as text using `fitz` (PyMuPDF) or encoded as Base64 using the `get_pdf_base64` method.
        - Skips files that cannot be read and logs an error message for each skipped file.
    """

        documents = {}

        if directory is None:
            directory = SYSTEM_CONFIG.get("general.dsk_dir")

            if not directory:
                self.LOGGER.critical("'dsk_dir' is missing in CONFIG")
                raise KeyError("'dsk_dir' is missing in CONFIG file")

        if not os.path.exists(directory):
            os.makedirs(directory)
            self.LOGGER.debug(f"Directory created: {directory}")

        self.LOGGER.info(f"Using knowledge directory: {directory}")

        self.LOGGER.info(f"Loading documents from directory: {directory}")

        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)

            content = ""

            if filename.endswith(".txt"):
                content += self.read_txt(file_path)

            elif filename.endswith(".pdf"):
                if load_pdf_in_base64:
                    content = self.read_pdf_as_base64(file_path)
                else:
                    content = fitz.open(file_path)

            if content is None:
                self.LOGGER.error(f"Skipping file due to read error: {file_path}")
            else:
                documents[filename] = content

        self.LOGGER.info(f"Finished loading documents. Total loaded: {len(documents)}")

        return documents