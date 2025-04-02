from re import search, findall, DOTALL
from plantuml import PlantUML
from utils.system_parametrization import SYSTEM_CONFIG
from utils.logger import Logger


import os
import logging
import pandas as pd

LOGGER = Logger


PLANT_UML_URL = SYSTEM_CONFIG.get("plantuml_png_url", "http://www.plantuml.com/plantuml/png/")
PLANTUML_SERVER = PlantUML(url=PLANT_UML_URL)


def extract_plantuml_code(plantuml_code):
    return (
        match[0]
        if (
            match := search(r"@startuml[\s\S]*?@enduml", plantuml_code, DOTALL)
        )
        else ""
    )


def extract_plantuml_image(plantuml_code: str, output_filename: str, output_directory: str):
    diagram_image = None

    try:
        diagram_image = PLANTUML_SERVER.processes(plantuml_code)

    except Exception as e:
        LOGGER.critical(f"Failed to generate diagram image: {output_filename}=>: {e}")

    return diagram_image


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
        state_name = match[0] or match[2]
        alias = match[1] or state_name
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


def extract_excel_report(plantuml_code, output_filename: str):

    try:
        plantuml_code = extract_plantuml_code(plantuml_code)
        components, relations = extract_components_and_relations(plantuml_code)

        if not components:
            components = ["Not declared components"]
            logging.debug("Not declared components.")

        if not relations:
            logging.debug("Not declared relations.")
            relations = ["Not declared components"]

        df_components = pd.DataFrame(components)
        df_relations = pd.DataFrame(relations)

        with pd.ExcelWriter(f"{output_filename}.xlsx") as writer:
            df_components.to_excel(writer, sheet_name="Components", index=False)
            df_relations.to_excel(writer, sheet_name="Relations", index=False)

        logging.info(f"Excel report saved in: {output_filename}.xlsx")

    except Exception as e:
        _generate_error_excel(output_filename, e)


def _generate_error_excel(output_filename, e):
    try:
        LOGGER.error(f"Error generating Excel report: {str(e)}")

        empty_output_file = f"{output_filename}_error.xlsx"

        with pd.ExcelWriter(empty_output_file) as writer:
            pd.DataFrame().to_excel(writer, sheet_name="Error")

        LOGGER.info(f"Empty error report saved at: {empty_output_file}")

    except Exception as e:
        LOGGER.critical(f"Failed to save error Excel file: {str(e)}")
