from src.artifacts.plantuml.extract_diagram_content import (extract_plantuml_code, extract_excel_report,
                                                            extract_plantuml_image)

from utils.logger import Logger
from llm.llm_service import LLMService
from utils.system_parametrization import SYSTEM_CONFIG
from utils.file_util import save_to_file

import os
from src.utils.file_util import save_to_file_with_error_handling


LOGGER = Logger
LLM = LLMService()

SYSTEM_PROMPT = SYSTEM_CONFIG.get("system_prompt")
USER_PROMPT = SYSTEM_CONFIG.get("user_prompt")
TREATMENT_MODEL_1 = SYSTEM_CONFIG.get("treatment_model_1")
TREATMENT_MODEL_2 = SYSTEM_CONFIG.get("treatment_model_2")
TREATMENT_PROVIDER_1 = SYSTEM_CONFIG.get("treatment_provider_1")
TREATMENT_PROVIDER_2 = SYSTEM_CONFIG.get("treatment_provider_2")
OUTPUT_DIRECTORY = SYSTEM_CONFIG.get("output_directory")
PIPELINE_PROCESSOR = SYSTEM_CONFIG.get("pipeline_processor")


def collect_dsk_treatment_samples_to_use_case_artifacts(
    iterator_number, start_time
):

    if not os.path.exists(OUTPUT_DIRECTORY):
        os.makedirs(OUTPUT_DIRECTORY)

    if not PIPELINE_PROCESSOR:
        LOGGER.error("Pipeline processor not defined in the system configuration.")
        return

    if PIPELINE_PROCESSOR in ["parallel", "treatment1"]:
        _apply_dsk_treatment_to_use_case_artifact(1, TREATMENT_PROVIDER_1, TREATMENT_MODEL_1, iterator_number,
                                                  start_time)

    if PIPELINE_PROCESSOR in ["parallel", "treatment2"]:
        _apply_dsk_treatment_to_use_case_artifact(2, TREATMENT_PROVIDER_2, TREATMENT_MODEL_2, iterator_number,
                                                  start_time)


def _apply_dsk_treatment_to_use_case_artifact(treatment_number, provider, model, iterator_number, start_time):
    LOGGER.info(f"🧠 Generating diagram for treatment {treatment_number}: provider={provider} model:{model}.")

    treatment_response = LLM.executeLLM(USER_PROMPT, provider=provider, model=model,
                                        system_prompt=SYSTEM_PROMPT)

    treatment_filename = f"{provider}-{model}-collect-{iterator_number}.txt"
    treatment_output_directory = f"{OUTPUT_DIRECTORY}/{provider}-{model}-{start_time.strftime('%m-%d-%I%p')}"

    LOGGER.info(f"💾 Saving treatment {treatment_number} response")
    save_to_file(treatment_filename, treatment_output_directory, treatment_response)

    LOGGER.info(f"💾 Saving artifact treatment {treatment_number} artifact")
    plantuml_code = extract_plantuml_code(treatment_response)
    artifact_name = f"{provider}-{model}-collect-{iterator_number}.puml"
    save_to_file(artifact_name, treatment_output_directory, plantuml_code)

    LOGGER.info(f"💾 Saving artifact treatment {treatment_number} image")
    plantuml_image = extract_plantuml_image(treatment_response)
    artifact_image_name = f"{provider}-{model}-collect-{iterator_number}.png"
    save_to_file_with_error_handling(artifact_image_name, treatment_output_directory, plantuml_image)

    filename = f"{provider}-{model}-collect-{iterator_number}"
    extract_excel_report(plantuml_code, filename)
