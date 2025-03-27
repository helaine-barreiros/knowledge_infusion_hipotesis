import os
import logging
import pandas as pd

from re import search, findall, DOTALL
from PIL import Image, ImageDraw, ImageFont
from plantuml import PlantUML

# Configuração do logger
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

PLANT_UML_URL="http://www.plantuml.com/plantuml/png/"
OUTPUT_DIRECTORY="rag_extracted_data"

def extract_plantuml_code(plantuml_code):
    code = ""

    pattern = r"@startuml[\s\S]*?@enduml"
    match = search(pattern, plantuml_code, DOTALL)
    
    if match:
        code = match.group(0) 
    
    return code

def save_plantuml_file(plantuml_code: str, output_filename : str, output_directory: str):
    try:
        output_file = os.path.join(output_directory, f"{output_filename}.puml")
        
        with open(output_file, 'w', encoding='utf-8') as file:
            file.write(plantuml_code)

        logging.info(f"Successfull diagram exported to: {output_file}")
        return output_file

    except Exception as e:
        logging.error(f"Could not save the PlantUML code. Errors: {str(e)}")
        return None

def generate_plantuml_image(plantuml_code: str, output_filename : str, output_directory: str):
    try:        
        output_file = os.path.join(output_directory, f"{output_filename}.png")
        
        plantuml_server = PlantUML(url=PLANT_UML_URL)

        #if plantuml_code.strip().startswith("@startuml") or not plantuml_code.strip().endswith("@enduml"):
        diagram_image = plantuml_server.processes(plantuml_code)
        #else:
            #acrescentar imagem falha
        #    logging.info(f"The diagram image {output_file} is not generated because the PlantUML code is not valid'.")

        with open(output_file, 'wb') as file:
            file.write(diagram_image)

        logging.info(f"Diagram image saved to: {output_file}")
        
    except Exception as e:
        logging.error(f"Could not generate diagram image from PlantUML code. Errors: {str(e)}")

        # Generate a failure image
        error_output_file = os.path.join(output_directory, f"{output_filename}_error.png")
        error_image = Image.new("RGB", (400, 200), color=(255, 255, 255))
        draw = ImageDraw.Draw(error_image)
        font = ImageFont.load_default()
        draw.text((10, 90), "Error: Diagram generation failed", fill=(255, 0, 0), font=font)
        
        # Save the error image
        error_image.save(error_output_file)
        logging.info(f"Error image saved to: {error_output_file}")

def extract_components_and_relations(plantuml_code):
    # Improved regex to capture all states, including nested states inside state blocks
    state_pattern = r'state\s+"?([^\"]+?)"?\s+(?:as\s+([\w\d_]+))?|state\s+([\w\d_]+)'
    nested_state_pattern = r'state\s+([\w\d_]+)\s*\{'  # Captures nested states
    transition_pattern = r'([\w\d_]+)\s*[-]{1,3}>\s*([\w\d_\*]+)\s*:?\s*(.*)'

    components = []
    alias_map = {}
    nested_states = set()

    # Find nested states
    for match in findall(nested_state_pattern, plantuml_code):
        nested_states.add(match)

    # Find components
    for match in findall(state_pattern, plantuml_code):
        state_name = match[0] if match[0] else match[2]
        alias = match[1] if match[1] else state_name
        alias_map[alias] = state_name
        components.append({"State": alias, "Complete Name": state_name, "Type": "normal"})

    # Include nested states as components
    for nested in nested_states:
        components.append({"State": nested, "Complete Name": nested, "Type": "nested"})

    # Include initial states and finals if they are in the diagram
    if '[*]' in plantuml_code:
        components.append({"State": "[*]", "Complete Name": "Start/End", "Type": "especial"})

    relations = []

    # Find transitions and ensure states in transitions are captured
    found_states = set(alias_map.keys())
    
    for match in findall(transition_pattern, plantuml_code):
        source, target, description = match
        
        # Resolve alias
        source_full = alias_map.get(source, source)
        target_full = alias_map.get(target, target)

        relations.append({"Source": source_full, "Destiny": target_full, "Description": description.strip()})
        
        # Ensure any missing state in transitions is added to components
        if source_full not in found_states:
            components.append({"State": source_full, "Complete Name": source_full, "Type": "implicit"})
            found_states.add(source_full)
        if target_full not in found_states:
            components.append({"State": target_full, "Complete Name": target_full, "Type": "implicit"})
            found_states.add(target_full)

    return components, relations

def generate_excel_report(plantuml_code, output_filename : str, output_directory: str):

    try:
        # Extract components and relations
        plantuml_code = extract_plantuml_code(plantuml_code)
        components, relations = extract_components_and_relations(plantuml_code)

        if not components:
            components = ["Not declared components"]
            logging.debug("Not declared components.")
        
        if not relations:
            logging.debug("Not declared relations.")
            relations = ["Not declared components"]

        # Create Diagram DataFrames
        df_components = pd.DataFrame(components)
        df_relations = pd.DataFrame(relations)

        # Save data in excel
        with pd.ExcelWriter(f"{output_directory}/{output_filename}.xlsx") as writer:
            df_components.to_excel(writer, sheet_name="Components", index=False)
            df_relations.to_excel(writer, sheet_name="Relations", index=False)

        logging.info(f"Excel report saved in: {output_directory}/{output_filename}.xlsx")

    except Exception as e:
        logging.error(f"Error generating Excel report: {str(e)}")
        
        # Create an empty Excel file in case of failure
        empty_output_file = os.path.join(output_directory, f"{output_filename}_error.xlsx")

        try:
            with pd.ExcelWriter(empty_output_file) as writer:
                pd.DataFrame().to_excel(writer, sheet_name="Error")
            logging.info(f"Empty error report saved at: {empty_output_file}")
        except Exception as e:
            logging.critical(f"Failed to save error Excel file: {str(e)}")