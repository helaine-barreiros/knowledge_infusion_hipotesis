from re import search, DOTALL
from src.utils.plantuml.plantuml import PlantUML
from src.utils.system_parametrization import SYSTEM_CONFIG
from src.utils.logger import Logger
from src.utils.plantuml.plantuml_parser import PlantUMLUseCaseParser

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
            self.LOGGER.critical(f"Failed to generate diagram image: {str(e)}")

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
        diagram = []

        try:
            extracted_code = self.extract_plantuml_use_case_code(plantuml_code)
            if not extracted_code:
                return diagram

            diagram = self.parser.parse(extracted_code)
            self.LOGGER.info(f"Extracted diagram:{diagram}")

        except Exception as e:
            self.LOGGER.error(f"Error extracting use case diagram: {str(e)}")

        return diagram

    def extract_excel_report(self, plantuml_code):
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
            diagram = self.extract_plantuml_use_case_components(plantuml_code)

            consolidated_data = []

            consolidated_data.extend(
                {
                    'Type': 'Actor',
                    'Name': actor['name'],
                    'Alias': actor['alias'],
                    'Details': f"Type: {actor['type']}",
                }
                for actor in diagram['actors']
            )
            consolidated_data.extend(
                {
                    'Type': 'Use Case',
                    'Name': use_case['name'],
                    'Alias': use_case['alias'],
                    'Details': f"Type: {use_case['type']}",
                }
                for use_case in diagram['use_cases']
            )

            consolidated_data.extend(
                {
                    'Type': 'Relationship',
                    'Name': f"{rel['source']} --> {rel['target']}",
                    'Alias': '',
                    'Details': f"Type: {rel['type']}, Kind: {rel.get('kind', '')}",
                }
                for rel in diagram['relationships']
            )

            consolidated_data.extend(
                {
                    'Type': 'Note',
                    'Name': note['target'],
                    'Alias': '',
                    'Details': note['content'],
                }
                for note in diagram['notes']
            )

            consolidated_data.extend(
                {
                    'Type': 'Rectangle',
                    'Name': rect['name'],
                    'Alias': '',
                    'Details': '',
                }
                for rect in diagram['rectangles']
            )

            df_consolidated = pd.DataFrame(consolidated_data)

            with io.BytesIO() as buffer:
                with pd.ExcelWriter(buffer, engine="xlsxwriter") as writer:
                    df_consolidated.to_excel(writer, sheet_name="Use Case Report", index=False)

                buffer.seek(0)
                excel_bytes = buffer.read()

            self.LOGGER.info("Excel report generated successfully")

        except Exception as e:
            self.LOGGER.error(f"Error generating Excel report: {str(e)}")

        return excel_bytes
