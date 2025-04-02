from src.plantuml_utils.plantuml_use_case_controller import PlantUMLUseCaseController

from utils.logger import Logger
from llm.llm_service import LLMService
from utils.system_parametrization import SYSTEM_CONFIG
from utils.file_util import FileUtil

import os


class DskExperimentController:

    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(DskExperimentController, cls).__new__(cls)
        return cls._instance

    def __init__(self, *args, **kwargs):

        if not hasattr(self, "initialized"):
            self.LOGGER = Logger
            self.LLM = LLMService()
            self.fileUtil = FileUtil()
            self.controller = PlantUMLUseCaseController()

            self.SYSTEM_PROMPT = SYSTEM_CONFIG.get("artifacts.system_prompt")
            self.USER_PROMPT = SYSTEM_CONFIG.get("artifacts.user_prompt")
            self.TREATMENT_MODEL_1 = SYSTEM_CONFIG.get("artifacts.treatment_model_1")
            self.TREATMENT_MODEL_2 = SYSTEM_CONFIG.get("artifacts.treatment_model_2")
            self.TREATMENT_PROVIDER_1 = SYSTEM_CONFIG.get("artifacts.treatment_provider_1")
            self.TREATMENT_PROVIDER_2 = SYSTEM_CONFIG.get("artifacts.treatment_provider_2")
            self.TREATMENT_MODEL_1_TEMPERATURE = SYSTEM_CONFIG.get("artifacts.treatment_model_1_temperature")
            self.TREATMENT_MODEL_2_TEMPERATURE = SYSTEM_CONFIG.get("artifacts.treatment_model_2_temperature")
            self.OUTPUT_DIRECTORY = SYSTEM_CONFIG.get("artifacts.output_directory")
            self.PIPELINE_PROCESSOR = SYSTEM_CONFIG.get("artifacts.pipeline_processor")
            self.initialized = True

    def collect_dsk_treatment_samples_to_use_case_artifacts(self, iterator_number, start_time):

        if not os.path.exists(self.OUTPUT_DIRECTORY):
            os.makedirs(self.OUTPUT_DIRECTORY)

        if not self.PIPELINE_PROCESSOR:
            self.LOGGER.error("Pipeline processor not defined in the system configuration.")
            return

        if self.PIPELINE_PROCESSOR in ["parallel", "treatment1"]:
            self._apply_dsk_treatment_to_use_case_artifact(treatment_number=1, provider=self.TREATMENT_PROVIDER_1,
                                                           model=self.TREATMENT_MODEL_1,
                                                           temperature=self.TREATMENT_MODEL_1_TEMPERATURE,
                                                           iterator_number=iterator_number, start_time=start_time)

        if self.PIPELINE_PROCESSOR in ["parallel", "treatment2"]:
            self._apply_dsk_treatment_to_use_case_artifact(treatment_number=2, provider=self.TREATMENT_PROVIDER_2,
                                                           model=self.TREATMENT_MODEL_2,
                                                           temperature=self.TREATMENT_MODEL_1_TEMPERATURE,
                                                           iterator_number=iterator_number, start_time=start_time)

    def _apply_dsk_treatment_to_use_case_artifact(self, treatment_number, provider, model, temperature, iterator_number, start_time):
        self.LOGGER.info(f"🧠 Generating diagram for treatment {treatment_number}: provider={provider} model:{model}.")

        treatment_response = self.LLM.executeLLM(prompt=self.USER_PROMPT, provider=provider, model=model,
                                                 temperature=temperature,
                                                 system_prompt=self.SYSTEM_PROMPT)

        treatment_filename = f"{provider}-{model}-{temperature}-collect-{iterator_number}.txt"
        treatment_output_directory = f"{self.OUTPUT_DIRECTORY}/{provider}-{model}-{temperature}-{start_time.strftime('%m-%d-%I%p')}"

        if not os.path.exists(treatment_output_directory):
            os.makedirs(treatment_output_directory)

        self.LOGGER.info(f"💾 Saving treatment {treatment_number} response")
        self.fileUtil.save_to_file(treatment_filename, treatment_output_directory, treatment_response)

        self.LOGGER.info(f"💾 Saving artifact treatment {treatment_number} artifact")
        plantuml_code = self.controller.extract_plantuml_use_case_code(treatment_response)
        artifact_name = f"{provider}-{model}-collect-{iterator_number}.puml"
        self.fileUtil.save_to_file(artifact_name, treatment_output_directory, plantuml_code)

        self.LOGGER.info(f"💾 Saving artifact treatment {treatment_number} image")
        plantuml_image = self.controller.extract_plantuml_use_case_image(treatment_response)
        artifact_image_name = f"{provider}-{model}-collect-{iterator_number}.png"
        self.fileUtil.save_to_file_with_error_handling(artifact_image_name, treatment_output_directory, plantuml_image)

        filename = f"{provider}-{model}-collect-{iterator_number}"
        artifact_excel_report = self.controller.extract_excel_report(plantuml_code, filename)
        artifact_excel_report = f"{provider}-{model}-collect-{iterator_number}.xlsx"
        self.fileUtil.save_to_file_with_error_handling(artifact_excel_report, treatment_output_directory,
                                                       artifact_excel_report)
