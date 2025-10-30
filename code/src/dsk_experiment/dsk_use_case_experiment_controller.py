from datetime import datetime
from tqdm import tqdm

from src.plantuml_utils.plantuml_use_case_controller import PlantUMLUseCaseController
from src.dsk_experiment.dsk_use_case_comparator import UMLDiagramComparator, ComparisonConfig
from src.utils.logger import Logger
from src.llm.llm_service import LLMService
from src.utils.system_parametrization import SYSTEM_CONFIG
from src.utils.file_util import FileUtil

import os
import re


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
            self.TREATMENT_MODEL_1_TOP_P = SYSTEM_CONFIG.get("artifacts.treatment_model_1_top_p")
            self.TREATMENT_MODEL_2_TOP_P = SYSTEM_CONFIG.get("artifacts.treatment_model_2_top_p")
            self.TREATMENT_MODEL_1_TOP_K = SYSTEM_CONFIG.get("artifacts.treatment_model_1_top_k")
            self.TREATMENT_MODEL_2_TOP_K = SYSTEM_CONFIG.get("artifacts.treatment_model_2_top_k")
            self.TREATMENT_MODEL_2_PRESENCE_PENALTY = SYSTEM_CONFIG.get("artifacts.treatment_model_2_presence_penalty")
            self.TREATMENT_MODEL_1_PRESENCE_PENALTY = SYSTEM_CONFIG.get("artifacts.treatment_model_1_presence_penalty")
            self.TREATMENT_MODEL_2_FREQUENCE_PENALTY = SYSTEM_CONFIG.get("artifacts.treatment_model_2_frequence_penalty")
            self.TREATMENT_MODEL_1_FREQUENCE_PENALTY = SYSTEM_CONFIG.get("artifacts.treatment_model_1_frequence_penalty")
            self.TREATMENT_MODEL_1_NUM_PREDICT = SYSTEM_CONFIG.get("artifacts.treatment_model_1_num_predict")
            self.TREATMENT_MODEL_2_NUM_PREDICT = SYSTEM_CONFIG.get("artifacts.treatment_model_2_num_predict")

            self.GENERAL_OUTPUT_DIRECTORY = SYSTEM_CONFIG.get("general.output_directory")
            self.ARTIFACTS_OUTPUT_DIRECTORY = SYSTEM_CONFIG.get("artifacts.output_directory")
            self.REPORT_OUTPUT_DIRECTORY = SYSTEM_CONFIG.get("general.report_directory")
            self.REPORT_ANALYSIS_OUTPUT_DIRECTORY = SYSTEM_CONFIG.get("artifacts.output_analysis_directory")

            os.makedirs(self.GENERAL_OUTPUT_DIRECTORY, exist_ok=True)
            os.makedirs(self.REPORT_OUTPUT_DIRECTORY, exist_ok=True)
            os.makedirs(os.path.join(self.REPORT_OUTPUT_DIRECTORY, self.REPORT_ANALYSIS_OUTPUT_DIRECTORY), exist_ok=True)

            self.PIPELINE_PROCESSOR = SYSTEM_CONFIG.get("artifacts.pipeline_processor")
            self.TREATMENT_PUML_REFERENCE_FULLNAME = SYSTEM_CONFIG.get("artifacts.reference_puml_evaluator")
            self.TREATMENT_IMG_REFERENCE_FULLNAME = SYSTEM_CONFIG.get("artifacts.reference_image_evaluator")
            self.ENCODING = SYSTEM_CONFIG.get("general.encoding")
            self.DIAGRAM_EXTENSION = SYSTEM_CONFIG.get("general.diagram_extension")
            self.initialized = True

    def collect_overall_diagrams_evaluation_report(self, source_data_prefix=None):

        report_output_directory = self._get_report_output_directory_fullpath()

        if not source_data_prefix:
            source_data_prefix = "ollama-"

        diagram_collected_summary_evaluations = self._collect_report_metrics_data(source_data_prefix=source_data_prefix, overall=True)

        date_time_generation = datetime.now().strftime("%Y-%m-%d-%H%M")
        report_filename = f"{source_data_prefix}-overall_diagrams_evaluation_report-{date_time_generation}"

        overall_report_markdown = self.controller.generate_overall_diagrams_evaluation_markdown_report(diagram_collected_summary_evaluations)
        overall_report_excel = self.controller.generate_overall_diagrams_evaluation_excel_report(diagram_collected_summary_evaluations)

        self.LOGGER.info(f"Generated overall report for {source_data_prefix}")
        self.LOGGER.info(f"Report files saved in: {report_output_directory}")

        self.fileUtil.save_to_file(f"{report_filename}.md", report_output_directory, overall_report_markdown)
        self.fileUtil.save_to_file(f"{report_filename}.xlsx", report_output_directory, overall_report_excel)

    def collect_individual_diagrams_evaluation_report(self, source_data_prefix=None):
        self.LOGGER.info(f"Generating individual collect reports for {source_data_prefix}")

        report_output_directory = self._get_report_output_directory_fullpath()

        if not source_data_prefix:
            source_data_prefix = "ollama-"

        diagram_collected_report_details = self._collect_report_metrics_data(source_data_prefix, overall=False)

        for report_id, report_detail in diagram_collected_report_details:
            report_filename = f"{report_id}-comparison-report.md"

            self.LOGGER.info(f"Generated report for {report_filename}")

            self.fileUtil.save_to_file(f"{report_filename}", report_output_directory, report_detail["markdown_report"][1])
            self.LOGGER.info(f"Generated Individual Collect Report {report_id} file saved in: {report_output_directory}/{report_filename}")

        self.LOGGER.info(f"Generated all Individual Collect reports for {source_data_prefix}")

    def collect_dsk_treatment_samples_to_use_case_artifacts(self, iterator_number, start_time):

        if not self.PIPELINE_PROCESSOR:
            self.LOGGER.error("Pipeline processor not defined in the system configuration.")
            return

        if self.PIPELINE_PROCESSOR in ["parallel", "treatment1"]:
            self._apply_dsk_treatment_to_use_case_artifact(treatment_number=1, provider=self.TREATMENT_PROVIDER_1,
                                                           model=self.TREATMENT_MODEL_1,
                                                           temperature=self.TREATMENT_MODEL_1_TEMPERATURE,
                                                           top_p=self.TREATMENT_MODEL_1_TOP_P, top_k=self.TREATMENT_MODEL_1_TOP_K,
                                                           presence_penalty=self.TREATMENT_MODEL_1_PRESENCE_PENALTY,
                                                           frequency_penalty=self.TREATMENT_MODEL_1_FREQUENCE_PENALTY,
                                                           num_predict=self.TREATMENT_MODEL_1_NUM_PREDICT,
                                                           iterator_number=iterator_number, start_time=start_time)

        if self.PIPELINE_PROCESSOR in ["parallel", "treatment2"]:
            self._apply_dsk_treatment_to_use_case_artifact(treatment_number=2, provider=self.TREATMENT_PROVIDER_2,
                                                           model=self.TREATMENT_MODEL_2,
                                                           temperature=self.TREATMENT_MODEL_2_TEMPERATURE,
                                                           top_p=self.TREATMENT_MODEL_2_TOP_P, top_k=self.TREATMENT_MODEL_2_TOP_K,
                                                           presence_penalty=self.TREATMENT_MODEL_2_PRESENCE_PENALTY,
                                                           frequency_penalty=self.TREATMENT_MODEL_2_FREQUENCE_PENALTY,
                                                           num_predict=self.TREATMENT_MODEL_2_NUM_PREDICT,
                                                           iterator_number=iterator_number, start_time=start_time)

    def _apply_dsk_treatment_to_use_case_artifact(self, treatment_number, provider, model, temperature, top_p, top_k, presence_penalty, frequency_penalty,
                                                  num_predict, iterator_number, start_time):

        self.LOGGER.info(f"🧠 Generating diagram for treatment {treatment_number}: provider={provider} model:{model} temperature:{temperature}.")

        treatment_response = self.LLM.executeLLM(prompt=self.USER_PROMPT, provider=provider, model=model,
                                                 temperature=temperature,
                                                 top_p=top_p,
                                                 top_k=top_k,
                                                 presence_penalty=presence_penalty,
                                                 frequency_penalty=frequency_penalty,
                                                 num_predict=num_predict,
                                                 system_prompt=self.SYSTEM_PROMPT)

        treatment_filename = f"{provider}-{model.replace(':', '-')}-{temperature}-collect-{iterator_number}.txt"
        treatment_output_directory = f"{self.ARTIFACTS_OUTPUT_DIRECTORY}/{provider}-{model.replace(':', '-')}-temp{temperature}-{start_time.strftime('%m-%d-%I%M%p')}"

        if not os.path.exists(treatment_output_directory):
            os.makedirs(treatment_output_directory)

        self.LOGGER.info(f"💾 Saving treatment {treatment_number} response")
        self.fileUtil.save_to_file(treatment_filename, treatment_output_directory, treatment_response)

        plantuml_code = self.controller.extract_plantuml_use_case_code(treatment_response)
        artifact_name = f"{provider}-{model.replace(':', '-')}-temp{temperature}-collect-{iterator_number}.puml"

        self.fileUtil.save_to_file(artifact_name, treatment_output_directory, plantuml_code)

        # artifact_image_name = f"{provider}-{model.replace(':', '-')}-temp{temperature}-collect-{iterator_number}.png"

        # if not plantuml_code:
        #    self.fileUtil.generate_png_empty_file(artifact_image_name, treatment_output_directory, artifact_image_name)
        # else:
        #    plantuml_image = self.controller.extract_plantuml_use_case_image(treatment_response)
        #    self.fileUtil.save_to_file_with_error_handling(artifact_image_name, treatment_output_directory,
        #                                                                plantuml_image)

    def extract_info_from_filename(self, filename):
        # Remove extensão
        base = os.path.splitext(os.path.basename(filename))[0]

        # Expressão regular para capturar os grupos
        match = re.match(r"^(?P<provider>[^-]+)-(?P<modelo>.+)-temp(?P<temp>[\d.]+)-collect-(?P<collect>\d+)$", base)

        if not match:
            return None  # ou lançar um erro

        return {
            "provider": match.group("provider"),
            "modelo": match.group("modelo"),
            "temperatura": float(match.group("temp")),
            "coleta": int(match.group("collect"))
        }

    def _get_report_output_directory_fullpath(self):
        return os.path.join(self.REPORT_OUTPUT_DIRECTORY, self.REPORT_ANALYSIS_OUTPUT_DIRECTORY)

    def _collect_report_metrics_data(self, source_data_prefix, overall=True):
        diagram_collected_metrics = []

        self.LOGGER.info(f"Scanning directory:{self.ARTIFACTS_OUTPUT_DIRECTORY}")

        collected_data_dirs = [
            os.path.join(self.ARTIFACTS_OUTPUT_DIRECTORY, d)
            for d in os.listdir(self.ARTIFACTS_OUTPUT_DIRECTORY)
            if d.startswith(source_data_prefix) and os.path.isdir(os.path.join(self.ARTIFACTS_OUTPUT_DIRECTORY, d))
        ]

        self.LOGGER.info(f"Selected directories:{collected_data_dirs}")

        all_puml_paths = []
        for model_dir in collected_data_dirs:
            for dirpath, _, filenames in os.walk(model_dir):
                puml_files = [f for f in filenames if f.endswith(self.DIAGRAM_EXTENSION)]
                for f in puml_files:
                    all_puml_paths.append(os.path.join(dirpath, f))

        total = len(all_puml_paths)
        if total == 0:
            self.LOGGER.warning(f"No .puml files to proccess in {source_data_prefix}.")
            return []

        for fullpath in tqdm(all_puml_paths, desc="Processando arquivos .puml"):
            puml_filename = os.path.basename(fullpath)
            model_info = self.extract_info_from_filename(puml_filename)

            config = ComparisonConfig(
                reference_plantuml_diagram_fullname=self.TREATMENT_PUML_REFERENCE_FULLNAME,
                generated_plantuml_diagram_fullname=fullpath,
                evaluated_llm_model_info=model_info,
                generate_image_metrics=not overall,
            )

            comparator = UMLDiagramComparator(config)
            if overall:
                result = comparator.get_element_metrics()
            else:
                result = comparator.generate_diagram_report()

            diagram_collected_metrics.append(result)

        return diagram_collected_metrics
