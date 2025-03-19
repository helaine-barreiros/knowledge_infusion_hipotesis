import os
import logging
from re import search

from plantuml import PlantUML

# Configuração do logger
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

PLANT_UML_URL="http://www.plantuml.com/plantuml/png/"
OUTPUT_DIRECTORY="rag_extracted_data"

def clean_plantuml_code(plantuml_code):
    pattern = r"@startuml[\s\S]*?@enduml"
    match = search(pattern, plantuml_code, re.DOTALL)
    
    if match:
        return match.group(0) 
    else:
        return ""

def generate_plantuml_image(plantuml_code: str, filename : str, output_directory: str=OUTPUT_DIRECTORY):
    try:
        
        plantuml_code = clean_plantuml_code(plantuml_code)

        if not os.path.exists(output_directory):
            os.makedirs(output_directory)
        
        output_file = os.path.join(output_directory, f"{filename}.png")
        
        plantuml_server = PlantUML(url=PLANT_UML_URL)

        if not plantuml_code.strip().startswith("@startuml") or not plantuml_code.strip().endswith("@enduml"):
            logging.error("The PlantUML code is invalid'.")
            return None
        
        plantuml_server.processes(plantuml_code, output_file=output_file)

        logging.info(f"Diagrama gerado com sucesso: {output_file}")
        return output_file

    except Exception as e:
        logging.error(f"The PlantUML code has errors: {str(e)}")
        return None

