from re import search, DOTALL
from plantuml import PlantUML
from src.utils.system_parametrization import SYSTEM_CONFIG
from src.utils.logger import Logger
from src.plantuml_utils.plantuml_parser_use_case import PlantUMLUseCaseParser
from openpyxl import load_workbook
from collections.abc import Mapping
import pandas as pd
from io import BytesIO
from collections.abc import Mapping

import io
import os
import pandas as pd
import re
import json
from typing import List, Dict


class PlantUMLUseCaseController:

    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(PlantUMLUseCaseController, cls).__new__(cls)
        return cls._instance

    def __init__(self, *args, **kwargs):
        if not hasattr(self, "initialized"):
            self.LOGGER = Logger
            self.PLANT_UML_URL = SYSTEM_CONFIG.get("artifacts.plantuml_png_url", "http://www.plantuml.com/plantuml/png/")
            self.PLANTUML_SERVER = PlantUML(url=self.PLANT_UML_URL)
            self.initialized = True

    def extract_plantuml_use_case_code(self, text_with_code: str) -> str:
        """
        Extracts the PlantUML code block from a given text.

        Args:
            text_with_code (str): The text containing the PlantUML code. 
                                If no code is provided or the text is empty, 
                                the method will return an empty string.

        Returns:
            str: The extracted PlantUML code block if found, otherwise an empty string.

        Notes:
            - The method searches for a PlantUML code block delimited by 
            "@startuml" and "@enduml" within the provided text.
            - The method does not validate whether the extracted code represents 
            a valid use case diagram. It simply returns the content between 
            "@startuml" and "@enduml".
            - If the text does not contain a valid PlantUML code block, 
            the method will return an empty string.
            - The method does not raise exceptions and is safe to call with 
            invalid or empty input.
        """
        if not text_with_code:
            return ""

        return (
            match[0]
            if (
                match := search(r"@startuml[\s\S]*?@enduml", text_with_code, DOTALL)
            )
            else ""
        )

    def extract_plantuml_use_case_image(self, plantuml_code: str):
        """
        Generates a diagram image from a given PlantUML use case diagram code and returns it as a byte array.

        Args:
            plantuml_code (str): A string that may or may not contain a PlantUML code block. 
                                The method only works with use case diagrams and will not 
                                process other types of diagrams.

        Returns:
            bytes: The generated diagram image as a byte array if successful, otherwise `None`.

        Notes:
            - The method first attempts to extract the PlantUML code block from the provided string.
            - If the extracted code represents a valid use case diagram, it will generate the diagram image.
            - The method does not validate or process other types of diagrams (e.g., class diagrams, sequence diagrams).
            - If an error occurs during the process, the method logs a critical error message and returns `None`.
            - The method does not raise exceptions and is safe to call with invalid or empty input.
            - The image is generated using the PlantUML server and returned as a byte array.
        """

        diagram_image = None

        try:
            extracted_code = self.extract_plantuml_use_case_code(plantuml_code)
            diagram_image = self.PLANTUML_SERVER.processes(extracted_code)

        except Exception as e:
            self.LOGGER.info(f"Could not generate diagram image: {str(e)}")

        return diagram_image

    def generate_overall_diagrams_evaluation_markdown_report(self, data_objects):
        if not data_objects:
            return "# COLLECTED DATA DETAILED REPORT\n\nNo data available."

        # Ordena colunas de forma consistente
        keys = list(data_objects[0].keys())

        # Cabeçalho
        markdown = "# COLLECTED DATA DETAILED REPORT\n\n"
        markdown += "| " + " | ".join(keys) + " |\n"
        markdown += "| " + " | ".join(["---"] * len(keys)) + " |\n"

        # Linhas
        for obj in data_objects:
            row = []
            for key in keys:
                value = obj.get(key, "")
                if isinstance(value, (dict, list)):
                    try:
                        value = json.dumps(value, ensure_ascii=False, separators=(",", ":"))
                    except:
                        value = str(value)
                row.append(str(value).replace("\n", " ").replace("|", "\\|"))
            markdown += "| " + " | ".join(row) + " |\n"

        return markdown

    def generate_overall_diagrams_evaluation_excel_report(self, data_objects):
        if not data_objects:
            return b''

        # Prepara os dados para o DataFrame
        def flatten_value(value):
            if isinstance(value, (dict, list)):
                try:
                    return json.dumps(value, ensure_ascii=False, separators=(",", ":"))
                except:
                    return str(value)
            return value

        processed_data = []
        for obj in data_objects:
            row = {key: flatten_value(value) for key, value in obj.items()}
            processed_data.append(row)

        # Cria o DataFrame
        df = pd.DataFrame(processed_data)

        # Salva o DataFrame em memória (Excel)
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name='Detailed Diagrams Report')

        return output.getvalue()
