from utils.logger import Logger
from utils.system_parametrization import SYSTEM_CONFIG

import os
import PyPDF2
import fitz
import logging
import base64


LOGGER = Logger


def read_txt(file_path):
    LOGGER.info(f"Reading TXT file: {file_path}")

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()
    except Exception as e:
        LOGGER.error(f"Failed to read TXT file {file_path}: {e}")
        return None


def read_pdf(file_path):
    LOGGER.info(f"Reading PDF file: {file_path}")

    text = ""

    try:
        with open(file_path, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                extracted_text = page.extract_text()
                if extracted_text:
                    text += extracted_text + "\n"
                else:
                    LOGGER.warning(f"No text extracted from page in {file_path}")
    except Exception as e:
        LOGGER.error(f"Failed to read PDF file {file_path}: {e}")

    return text


def load_documents(directory=None, load_pdf_in_base64=False):

    if directory is None:
        directory = SYSTEM_CONFIG.get("dsk_dir")

        if not directory:
            logging.critical("Configuration error: 'dsk_dir' is missing in CONFIG")
            raise Exception("Configuration error: 'dsk_dir' is missing in CONFIG")

    if not os.path.exists(directory):
        os.makedirs(directory)
        logging.debug(f"Directory created: {directory}")

    LOGGER.info(f"Using knowledge directory: {directory}")

    documents = {}

    LOGGER.info(f"Loading documents from directory: {directory}")

    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)

        content = None

        if filename.endswith(".txt"):
            content = read_txt(file_path)

        elif filename.endswith(".pdf"):
            if load_pdf_in_base64:
                content = get_pdf_base64(file_path)
            else:
                content = fitz.open(file_path)

        if content is None:
            LOGGER.error(f"Skipping file due to read error: {file_path}")
        else:
            documents[filename] = content

    LOGGER.info(f"Finished loading documents. Total loaded: {len(documents)}")

    return documents


def get_pdf_base64(file_path):
    content = None

    try:
        with open(file_path, "rb") as pdf_file:
            pdf_bytes = pdf_file.read() 
            content = base64.b64encode(pdf_bytes).decode("utf-8")

    except Exception as e:
        print(f"Error reading or encoding PDF: {e}")

    return content
