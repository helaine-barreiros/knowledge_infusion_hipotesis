from re import search, DOTALL
from plantuml import PlantUML
from src.utils.system_parametrization import SYSTEM_CONFIG
from src.utils.logger import Logger
from src.plantuml_utils.plantuml_parser_use_case import PlantUMLUseCaseParser

import io
import pandas as pd


class PlantUMLUseCaseController:

    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(PlantUMLUseCaseController, cls).__new__(cls)
        return cls._instance

    def __init__(self, *args, **kwargs):
        if not hasattr(self, "initialized"):
            """
            Initializes the PlantUMLUseCaseController class.
            """
            self.LOGGER = Logger
            self.PLANT_UML_URL = SYSTEM_CONFIG.get("artifacts.plantuml_png_url", "http://www.plantuml.com/plantuml/png/")
            self.PLANTUML_SERVER = PlantUML(url=self.PLANT_UML_URL)
            self.parser = PlantUMLUseCaseParser()
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
            self.LOGGER.critical(f"Failed to generate diagram image: {e}")

        return diagram_image

    def extract_plantuml_use_case_components(self, plantuml_code):
        """
        Extracts components and their counts from a given PlantUML use case diagram code.

        Args:
            plantuml_code (str): The PlantUML code to analyze. If no code is provided,
                                the method will return None.

        Returns:
            Dict[str, List[Dict[str, Any]]]: A dictionary containing the extracted components,
            or None if extraction fails.

        Notes:
            - If `plantuml_code` is not provided or is invalid, the method will return None.
            - The method does not raise exceptions. Instead, it logs error messages
            when issues occur during the parsing process.
        """
        components = None

        try:
            extracted_code = self.extract_plantuml_use_case_code(plantuml_code)
            if not extracted_code:
                return None

            components = self.parser.parse(extracted_code)

            # Verificar se o parser retornou um valor válido
            if not components or not isinstance(components, dict):
                return None

        except Exception as e:
            self.LOGGER.error(f"Error extracting use case components: {str(e)}")
            return None

        return components

    def extract_excel_report(self, plantuml_code, output_filename: str):
        """
        Extracts components from PlantUML code and generates an Excel report.

        Args:
            plantuml_code (str): The PlantUML code to analyze.
            output_filename (str): The name of the Excel file to create.

        Returns:
            bytes: The Excel file contents as bytes if successful, otherwise None.

        Notes:
            - The method extracts components using extract_plantuml_use_case_components.
            - If components cannot be extracted, the method returns None.
            - The Excel file contains two sheets: "Components" and "Relations".
            - If an error occurs during the process, the method logs an error message and returns None.
        """

        excel_bytes = None

        try:
            components = self.extract_plantuml_use_case_components(plantuml_code)
            
            # Verificar se components é None ou vazio antes de tentar acessar
            if not components:
                self.LOGGER.debug("Not declared components.")
                return None
                
            # Obter relações e garantir valor padrão como lista vazia
            relations = components.get("relations", [])

            # Verificar se componentes é um dicionário vazio ou inválido 
            if not isinstance(components, dict):
                self.LOGGER.debug("Components is not a valid dictionary.")
                return None

            # Criar DataFrames
            df_components = pd.DataFrame(components)
            df_relations = pd.DataFrame(relations)

            # Gerar Excel em memória
            with io.BytesIO() as buffer:
                with pd.ExcelWriter(buffer, engine="xlsxwriter") as writer:
                    df_components.to_excel(writer, sheet_name="Components", index=False)
                    df_relations.to_excel(writer, sheet_name="Relations", index=False)

                buffer.seek(0)
                excel_bytes = buffer.read()

            self.LOGGER.info("Excel report generated successfully")

        except Exception as e:
            self.LOGGER.error(f"Error generating Excel report: {str(e)}")

        return excel_bytes
