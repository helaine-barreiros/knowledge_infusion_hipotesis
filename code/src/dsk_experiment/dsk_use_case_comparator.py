from skimage.metrics import structural_similarity as ssim
from matplotlib.patches import Wedge
from rapidfuzz import fuzz
from sentence_transformers import SentenceTransformer, util
from dataclasses import dataclass, field
from typing import Optional, Dict
from plantuml import PlantUML

from src.utils.system_parametrization import SYSTEM_CONFIG
from src.utils.file_util import FileUtil
from src.plantuml_utils.plantuml_parser_use_case import PlantUMLUseCaseParser
from src.utils.logger import Logger

import os
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import cv2
import pandas as pd
import datetime
import base64
import gc


@dataclass
class ComparisonConfig:
    reference_plantuml_diagram_fullname: str
    generated_plantuml_diagram_fullname: str
    requirements: Optional[str] = None
    render_images: bool = True
    output_dir: str = "comparison_output"
    evaluated_llm_model_info: Optional[Dict] = field(default_factory=dict)
    individual: bool = True
    generate_image_metrics: bool = False
    image_output_dir: str = ""


class UMLDiagramComparator:
    """
    A class for comparing UML diagrams and quantifying rework effort.

    This class compares a reference UML diagram with a generated UML diagram,
    calculating various metrics to quantify the differences and rework effort.
    """
    def __init__(self, config: ComparisonConfig):

        self.LOGGER = Logger

        self.GENERAL_OUTPUT_DIRECTORY = SYSTEM_CONFIG.get("general.output_directory")
        self.REPORT_OUTPUT_DIRECTORY = SYSTEM_CONFIG.get("general.report_directory")
        self.REPORT_ANALYSIS_OUTPUT_DIRECTORY = SYSTEM_CONFIG.get("artifacts.output_analysis_directory")

        os.makedirs(self.GENERAL_OUTPUT_DIRECTORY, exist_ok=True)
        os.makedirs(self.REPORT_OUTPUT_DIRECTORY, exist_ok=True)
        os.makedirs(os.path.join(self.REPORT_OUTPUT_DIRECTORY, self.REPORT_ANALYSIS_OUTPUT_DIRECTORY), exist_ok=True)

        self.FILE_UTIL = FileUtil()
        self.PLANT_UML_URL = SYSTEM_CONFIG.get("artifacts.plantuml_png_url", "http://www.plantuml.com/plantuml/png/")
        self.PLANTUML_SERVER = PlantUML(url=self.PLANT_UML_URL)

        self.sentece_transformer_model = self._load_or_save_sentence_model()

        self.config = config

        self.ENCODING = SYSTEM_CONFIG.get("general.encoding")

        self.model_info = config.evaluated_llm_model_info
        self.comparison_date = datetime.datetime.now()

        self.reference_plantuml_content = self._open_file(config.reference_plantuml_diagram_fullname)
        _reference_parser = PlantUMLUseCaseParser(config.reference_plantuml_diagram_fullname)
        self.reference_usecase_elements = _reference_parser.get_use_case_diagram()

        self.generated_plantuml_content = self._open_file(config.generated_plantuml_diagram_fullname)
        _generated_parser = PlantUMLUseCaseParser(config.generated_plantuml_diagram_fullname)
        self.generated_usecase_elements = _generated_parser.get_use_case_diagram()

        self.element_metrics = self._calculate_element_metrics()

        if (self.config.generate_image_metrics):

            arquivo = os.path.basename(config.reference_plantuml_diagram_fullname)  # "actor_test.puml"
            self.reference_image_name = os.path.splitext(arquivo)[0] + ".png"  # "actor_test.png"
            self.generated_image_name = f"{self.generated_usecase_elements['base_name']}.png"

            self.reference_image_fullname = os.path.join(self.REPORT_OUTPUT_DIRECTORY, self.REPORT_ANALYSIS_OUTPUT_DIRECTORY, self.reference_image_name)  # "actor_test.png"
            self.generated_image_fullname = os.path.join(self.REPORT_OUTPUT_DIRECTORY, self.REPORT_ANALYSIS_OUTPUT_DIRECTORY, self.generated_image_name)

            self.image_metrics = self._calculate_image_metrics()

    def get_collect_diagram_id(self):
        return self.config.generated_plantuml_diagram_fullname.split("/")[-1].removesuffix(".puml")[:-1]

    def get_element_metrics(self):
        return self.element_metrics

    def _calculate_element_metrics(self, similarity_threshold: float = 0.6):

        if not self.generated_usecase_elements or self.generated_usecase_elements['compile'] == "Error":
            return {
                "sample ID": self.model_info["coleta"],
                "model": self.model_info["modelo"],
                "temperature": self.model_info["temperatura"],
                "provider": self.model_info["provider"],
                "date_evaluation": self.comparison_date.strftime('%Y-%m-%d %H:%M:%S'),
                "compiled_diagram": False,

                "actors_expected_qtd": 0,
                "actors_detected_qtd": 0,
                "actors_balance_qtd": 0,
                "actors_coverage": 0,
                "actors_not_detected_qtd": 0,
                "actors_extra_detected_qtd": 0,
                "actors_expected_detail": {"common_names": []},
                "actors_missing_detail": [],
                "actors_extra_detail": [],

                "usecases_expected_qtd": 0,
                "usecases_detected_qtd": 0,
                "usecases_balance_qtd": 0,
                "usecases_coverage": 0,
                "usecases_not_detected_qtd": 0,
                "usecases_extra_detected_qtd": 0,
                "usecases_expected_detail": {"common_names": []},
                "usecases_missing_detail": [],
                "usecases_extra_detail": [],

                "relationships_expected_qtd": 0,
                "relationships_detected_qtd": 0,
                "relationships_balance_qtd": 0,
                "relationships_coverage": 0,
                "relationships_not_detected_qtd": 0,
                "relationships_extra_detected_qtd": 0,
                "relationships_expected_detail": {"common_names": []},
                "relationships_missing_detail": [],
                "relationships_extra_detail": [],

                "elements_expected": {"actors": 0, "use_cases": 0, "relationships": 0},
                "elements_to_add": {"actors": 0, "use_cases": 0, "relationships": 0},
                "elements_to_delete": {"actors": 0, "use_cases": 0, "relationships": 0},
                "total_add_operations": 0,
                "total_delete_operations": 0,
                "total_edit_operations": 0,

                "weighted_score": 0,
                "overall_weighted_score": 0,
                "code_similarity": 0
            }

        reference_model_actors_name = {actor.name.lower() for actor in self.reference_usecase_elements.get("actors", [])}
        generated_model_actors_name = {actor.name.lower() for actor in self.generated_usecase_elements.get("actors", [])}

        reference_model_usecases_name = {uc.name.lower() for uc in self.reference_usecase_elements.get("usecases", [])}
        generated_usecases_name = {uc.name.lower() for uc in self.generated_usecase_elements.get("usecases", [])}

        reference_model_relationships_name = {f"source:{uc.source.lower()}|target:{uc.target.lower()}|type:{uc.type.lower()}" for uc in self.reference_usecase_elements.get("relationships", [])}
        generated_model_relationships_name = {f"source:{uc.source.lower()}|target:{uc.target.lower()}|type:{uc.type.lower()}" for uc in self.generated_usecase_elements.get("relationships", [])}

        detected_missing_actors, extra_detected_actors, detected_actors = self._calculate_string_diff_with_similarity(reference_model_actors_name, generated_model_actors_name, 0.85)
        detected_missing_usecases, extra_detected_usecases, detected_usecases = self._calculate_string_diff_with_similarity(reference_model_usecases_name, generated_usecases_name, 0.85)
        detected_missing_relationships, extra_detected_relationships, detected_relationships = self._calculate_string_diff_with_similarity(reference_model_relationships_name, generated_model_relationships_name, 0.85)

        detected_actor_coverage = (
            len(detected_actors["common_names"]) / len(reference_model_actors_name)
            if detected_actors and reference_model_actors_name else 0
        )

        detected_usecase_coverage = (
            len(detected_usecases["common_names"]) / len(reference_model_usecases_name)
            if detected_usecases and reference_model_usecases_name else 0
        )

        detected_relationships_coverage = (
            len(detected_relationships["common_names"]) / len(reference_model_relationships_name)
            if detected_relationships and reference_model_relationships_name else 0
        )

        arithimetic_avg_for_detected_components = 0
        if detected_actor_coverage != 0 and detected_usecase_coverage != 0:
            arithimetic_avg_for_detected_components = (detected_actor_coverage + detected_usecase_coverage + detected_relationships_coverage) / 3

        expected_components_detected = {
            "actors": len(reference_model_actors_name),
            "use_cases": len(reference_model_usecases_name),
            "relationships": len(reference_model_relationships_name),
        }
        
        missing_components_detected = {
            "actors": len(detected_missing_actors),
            "use_cases": len(detected_missing_usecases),
            "relationships": len(detected_missing_relationships),
        }

        total_missing_components_detected = len(detected_missing_actors) + len(detected_missing_usecases) + len(detected_missing_relationships)

        extra_components_detected = {
            "actors": len(extra_detected_actors),
            "use_cases": len(extra_detected_usecases),
            "relationships": len(extra_detected_relationships),
        }

        total_extra_components_detected = len(extra_detected_actors) + len(extra_detected_usecases) + len(extra_detected_relationships)

        total_editions_suggested = (
            total_missing_components_detected +
            total_missing_components_detected
        )

        total_expected_elements = len(reference_model_actors_name) + len(reference_model_usecases_name) + len(reference_model_relationships_name)
        weighted_rework_score = self._calculate_weighted_rework(
            missing_components_detected,
            extra_components_detected,
            total_expected_elements
        )

        code_similarity = self._calculate_code_similarity_with_sentence_transformer(self.reference_plantuml_content, self.generated_plantuml_content)

        metrics = {
            "sample ID": self.model_info["coleta"],
            "model": self.model_info["modelo"],
            "temperature": self.model_info["temperatura"],
            "provider": self.model_info["provider"],
            "date_evaluation": self.comparison_date.strftime('%Y-%m-%d %H:%M:%S'),
            "compiled_diagram": self.generated_usecase_elements["compile"],
            "actors_expected_qtd": len(reference_model_actors_name),
            "actors_detected_qtd": len(detected_actors["common_names"]),
            "actors_balance_qtd": len(reference_model_actors_name) - len(detected_actors["common_names"]),
            "actors_coverage": detected_actor_coverage,

            "actors_not_detected_qtd": len(detected_missing_actors),
            "actors_extra_detected_qtd": len(extra_detected_actors),
            "actors_expected_detail": detected_actors,
            "actors_missing_detail": detected_missing_actors,
            "actors_extra_detail": extra_detected_actors,

            "usecases_expected_qtd": len(detected_usecases),
            "usecases_detected_qtd": len(detected_usecases["common_names"]),
            "usecases_balance_qtd": len(reference_model_usecases_name) - len(detected_usecases["common_names"]),
            "usecases_coverage": detected_usecase_coverage,

            "usecases_not_detected_qtd": len(detected_missing_usecases),
            "usecases_extra_detected_qtd": len(extra_detected_usecases),
            "usecases_expected_detail": detected_usecases,
            "usecases_missing_detail": detected_missing_usecases,
            "usecases_extra_detail": extra_detected_usecases,

            "relationships_expected_qtd": len(detected_relationships),
            "relationships_detected_qtd": len(detected_relationships["common_names"]),
            "relationships_balance_qtd": len(reference_model_relationships_name) - len(detected_relationships["common_names"]),
            "relationships_coverage": detected_relationships_coverage,

            "relationships_not_detected_qtd": len(detected_missing_relationships),
            "relationships_extra_detected_qtd": len(extra_detected_relationships),
            "relationships_expected_detail": detected_relationships,
            "relationships_missing_detail": detected_missing_relationships,
            "relationships_extra_detail": extra_detected_relationships,

            "elements_expected": expected_components_detected,
            "elements_to_add": missing_components_detected,
            "elements_to_delete": extra_components_detected,
            "total_add_operations": total_missing_components_detected,
            "total_delete_operations": total_extra_components_detected,
            "total_edit_operations": total_editions_suggested,

            "weighted_score": arithimetic_avg_for_detected_components,
            "overall_weighted_score": weighted_rework_score,
            "code_similarity": code_similarity
        }

        return metrics

    def _calculate_image_metrics(self):
        evaluation = {
            "ssim_score": 0,
            "mse": 0,
            "histogram_correlation": 0,
            "ssim_visualization_path": 0,
            "difference_image_path": 0
        }

        if (self.generated_usecase_elements["compile"] and self.reference_usecase_elements["compile"]):

            try:
                generated_diagram_image = self.PLANTUML_SERVER.processes(self.generated_plantuml_content)
                self.FILE_UTIL.save_to_file_with_error_handling(self.generated_image_name, self.REPORT_OUTPUT_DIRECTORY, self.REPORT_ANALYSIS_OUTPUT_DIRECTORY, generated_diagram_image)
                self.generated_usecase_image = cv2.imread(self.generated_image_fullname)

                reference_diagram_image = self.PLANTUML_SERVER.processes(self.reference_plantuml_content)
                self.FILE_UTIL.save_to_file_with_error_handling(self.reference_image_name, self.REPORT_OUTPUT_DIRECTORY, self.REPORT_ANALYSIS_OUTPUT_DIRECTORY, reference_diagram_image)
                self.reference_usecase_image = cv2.imread(self.reference_image_fullname)

            except Exception as e:
                self.LOGGER.error(f"Error extracting use case diagram image to calculate metrics: {str(e)}")
                return evaluation

            height = min(self.reference_usecase_image.shape[0], self.generated_usecase_image.shape[0])
            width = min(self.reference_usecase_image.shape[1], self.generated_usecase_image.shape[1])

            reference_image_resized = cv2.resize(self.reference_usecase_image, (width, height))
            generated_image_resized = cv2.resize(self.generated_usecase_image, (width, height))

            # Convert to grayscale for SSIM
            referenc_image_gray = cv2.cvtColor(reference_image_resized, cv2.COLOR_BGR2GRAY)
            generated_image_gray = cv2.cvtColor(generated_image_resized, cv2.COLOR_BGR2GRAY)

            # Calculate SSIM
            ssim_score, ssim_map = ssim(referenc_image_gray, generated_image_gray, full=True)

            # Calculate MSE
            mse = np.mean((referenc_image_gray - generated_image_gray) ** 2)

            # Generate SSIM heatmap visualization
            plt.figure(figsize=(12, 6))
            plt.subplot(1, 3, 1)
            plt.imshow(referenc_image_gray, cmap='gray')
            plt.title('Reference Diagram')
            plt.axis('off')

            plt.subplot(1, 3, 2)
            plt.imshow(generated_image_gray, cmap='gray')
            plt.title('Generated Diagram')
            plt.axis('off')

            plt.subplot(1, 3, 3)
            plt.imshow(ssim_map, cmap='jet')
            plt.colorbar()
            plt.title(f'SSIM Map (Score: {ssim_score:.3f})')
            plt.axis('off')

            # Save the visualization
            visualization_image_file_name = f"{self.generated_usecase_elements['base_name']}-ssim_visualization.png"
            ssim_vis_path = visualization_image_file_name
            plt.tight_layout()
            plt.savefig(ssim_vis_path)
            plt.close()

            # Generate difference image
            difference_img = cv2.absdiff(referenc_image_gray, generated_image_gray)

            # Apply color map to difference image
            difference_color = cv2.applyColorMap(difference_img, cv2.COLORMAP_JET)

            # Save difference image
            difference_image_file_name = f"{self.generated_usecase_elements['base_name']}-difference_image.png"
            diff_img_path = difference_image_file_name
            cv2.imwrite(diff_img_path, difference_color)

            # Calculate histogram similarity
            reference_diagram_histgram = cv2.calcHist([referenc_image_gray], [0], None, [256], [0, 256])
            generated_diagram_histogram = cv2.calcHist([generated_image_gray], [0], None, [256], [0, 256])

            # Normalize histograms
            cv2.normalize(reference_diagram_histgram, reference_diagram_histgram, 0, 1, cv2.NORM_MINMAX)
            cv2.normalize(generated_diagram_histogram, generated_diagram_histogram, 0, 1, cv2.NORM_MINMAX)

            # Calculate histogram correlation
            histogram_correlation_image = cv2.compareHist(reference_diagram_histgram, generated_diagram_histogram, cv2.HISTCMP_CORREL)

            evaluation =  {
                "ssim_score": ssim_score,
                "mse": mse,
                "histogram_correlation": histogram_correlation_image,
                "ssim_visualization_path": ssim_vis_path,
                "difference_image_path": diff_img_path
            }
    
        return evaluation

    def _calculate_weighted_rework(self, elements_to_add, elements_to_delete, total_elements_reference):
        """
        Compute a normalized weighted rework score between 0 and 1, representing the proportion of effort 
        needed to make the generated diagram production-ready.

        Score | Interpretação prática
        0.00 - 0.20 | Can be used directly
        0.21 - 0.40 | Requires some light adjustments
        0.41 - 0.60 | Requires moderate rework, still viable
        0.61 - 0.80 | Requires heavy rework, reevaluate reuse
        0.81 - 1.00 | Better to start from scratch

        Args:
            elements_to_add (dict): {'actors': int, 'use_cases': int, 'relationships': int}
            elements_to_delete (dict): {'actors': int, 'use_cases': int, 'relationships': int}
            total_elements_reference (int): Total number of elements in the reference diagram.
        """
        weights = {
            "add_actor": 0.67,
            "add_usecase": 1.0,
            "delete_actor": 0.53,
            "delete_usecase": 0.8,
            "add_relationship": 0.87,
            "delete_relationship": 0.67
        }

        weighted_raw_score = (
            weights["add_actor"] * elements_to_add["actors"] +
            weights["add_usecase"] * elements_to_add["use_cases"] +
            weights["add_relationship"] * elements_to_add["relationships"] +
            weights["delete_actor"] * elements_to_delete["actors"] +
            weights["delete_usecase"] * elements_to_delete["use_cases"] +
            weights["delete_relationship"] * elements_to_delete["relationships"]
        )

        normalized_score = weighted_raw_score / max(total_elements_reference, 1) 

        return min(normalized_score, 1.0)

    def _calculate_code_similarity_with_sentence_transformer(self, code1, code2, model_name: str = "microsoft/codebert-base"):
        """
        Compute textual similarity ratio between two PlantUML code snippets.
        """

        code1_embedding = self.sentece_transformer_model.encode(code1, convert_to_tensor=True)
        code2_embedding = self.sentece_transformer_model.encode(code2, convert_to_tensor=True)

        evaluated_similarity = float(util.pytorch_cos_sim(code1_embedding, code2_embedding).item())

        del code1_embedding, code2_embedding
        gc.collect()
        
        return round(evaluated_similarity, 4)

    def _generate_quality_metrics_radar_chart(self):
        """
        Generate a radar chart of key metrics.

        Returns:
            str: Path to the generated radar chart
        """
        plt.figure(figsize=(10, 10))

        # Categories for the radar chart
        categories = [
            'Actor Coverage',
            'Use Case Coverage',
            'Relationship Coverage',
            'AVG Weighted Score',
            'Overall Weighted Score',
            'Code Similarity'
        ]

        # TODO: Values for each category (normalized to 0-1)
        values = [
            self.element_metrics['actors_coverage'],
            self.element_metrics['usecases_coverage'],
            self.element_metrics['relationships_coverage'],
            self.element_metrics['weighted_score'],
            self.element_metrics['overall_weighted_score'],
            self.element_metrics['code_similarity']
        ]

        # Number of categories
        N = len(categories)

        # Compute angle for each category
        angles = [n / float(N) * 2 * np.pi for n in range(N)]
        angles += angles[:1]  # Close the loop

        # Add the values for the chart
        values += values[:1]  # Close the loop

        # Create the radar chart
        ax = plt.subplot(111, polar=True)

        # Draw the polygon connecting the values
        ax.fill(angles, values, alpha=0.25, color='blue')

        # Draw the value lines
        ax.plot(angles, values, 'o-', linewidth=2, color='blue')

        # Add category labels
        plt.xticks(angles[:-1], categories, fontsize=12)

        # Add radial labels (0%, 25%, etc.)
        ax.set_rlabel_position(0)

        plt.yticks([0.25, 0.5, 0.75, 1.0], ["25%", "50%", "75%", "100%"], color="grey", size=10)
        plt.ylim(0, 1)

        plt.title(f"{self.model_info["modelo"]}:{self.model_info["coleta"]} Quality Metrics", size=15, y=1.1)

        generated_radar_chart_file_name = f"{self.generated_usecase_elements['base_name']}-radar_chart.png"
        fullname_generated_radar_chart_file_name = os.path.join(self.REPORT_OUTPUT_DIRECTORY, self.REPORT_ANALYSIS_OUTPUT_DIRECTORY, generated_radar_chart_file_name)

        plt.tight_layout()
        plt.savefig(fullname_generated_radar_chart_file_name, dpi=300, bbox_inches='tight')
        plt.close()

        return generated_radar_chart_file_name

    def _generate_metrics_table_visualization(self):
        """
        Generate a detailed metrics table.

        Returns:
            str: Path to the generated metrics table
        """
        # Create a table of all metrics
        metrics_data = {
            "Category": [],
            "Metric": [],
            "Value": []
        }

        metrics_data["Category"].append("Diagram Information")
        metrics_data["Metric"].append("sample ID")
        metrics_data["Value"].append(self.element_metrics["sample ID"])

        metrics_data["Category"].append("Diagram Information")
        metrics_data["Metric"].append("Model")
        metrics_data["Value"].append(self.element_metrics["model"])

        metrics_data["Category"].append("Diagram Information")
        metrics_data["Metric"].append("Temperature")
        metrics_data["Value"].append(self.element_metrics["temperature"])

        metrics_data["Category"].append("Diagram Information")
        metrics_data["Metric"].append("Provider")
        metrics_data["Value"].append(self.element_metrics["provider"])

        metrics_data["Category"].append("Diagram Information")
        metrics_data["Metric"].append("Date Evaluation")
        metrics_data["Value"].append(self.element_metrics["date_evaluation"])

        metrics_data["Category"].append("Diagram Information")
        metrics_data["Metric"].append("Compiled Diagram")
        metrics_data["Value"].append(self.element_metrics["compiled_diagram"])

        metrics_data["Category"].append("Actors Information")
        metrics_data["Metric"].append("Actors Expected Qtd")
        metrics_data["Value"].append(self.element_metrics["actors_expected_qtd"])

        metrics_data["Category"].append("Actors Information")
        metrics_data["Metric"].append("Actors Detected Qtd")
        metrics_data["Value"].append(self.element_metrics["actors_detected_qtd"])

        metrics_data["Category"].append("Actors Information")
        metrics_data["Metric"].append("Actors Balance Qtd")
        metrics_data["Value"].append(self.element_metrics["actors_balance_qtd"])

        metrics_data["Category"].append("Actors Information")
        metrics_data["Metric"].append("Actors Coverage Metric")
        metrics_data["Value"].append(f"{self.element_metrics["actors_coverage"]:.2%}")

        metrics_data["Category"].append("Actors Information")
        metrics_data["Metric"].append("Actors Not Detected Qtd")
        metrics_data["Value"].append(self.element_metrics["actors_not_detected_qtd"])

        metrics_data["Category"].append("Actors Information")
        metrics_data["Metric"].append("Actors Extra Detected Qtd")
        metrics_data["Value"].append(self.element_metrics["actors_extra_detected_qtd"])

        metrics_data["Category"].append("Actors Information")
        metrics_data["Metric"].append("Actors Expected Detail")
        metrics_data["Value"].append(self.element_metrics["actors_expected_detail"])

        metrics_data["Category"].append("Actors Information")
        metrics_data["Metric"].append("Actors Missing Detail")
        metrics_data["Value"].append(self.element_metrics["actors_missing_detail"])

        metrics_data["Category"].append("Actors Information")
        metrics_data["Metric"].append("Actors Extra Detail")
        metrics_data["Value"].append(self.element_metrics["actors_extra_detail"])

        metrics_data["Category"].append("Use Cases Information")
        metrics_data["Metric"].append("Use Cases Expected Qtd")
        metrics_data["Value"].append(self.element_metrics["usecases_expected_qtd"])

        metrics_data["Category"].append("Use Cases Information")
        metrics_data["Metric"].append("Use Cases Detected Qtd")
        metrics_data["Value"].append(self.element_metrics["usecases_detected_qtd"])

        metrics_data["Category"].append("Use Cases Information")
        metrics_data["Metric"].append("Use Cases Balance Qtd")
        metrics_data["Value"].append(self.element_metrics["usecases_balance_qtd"])

        metrics_data["Category"].append("Use Cases Information")
        metrics_data["Metric"].append("Use Cases Coverage Metric")
        metrics_data["Value"].append(f"{self.element_metrics["usecases_coverage"]:.2%}")

        metrics_data["Category"].append("Use Cases Information")
        metrics_data["Metric"].append("Use Cases Not Detected Qtd")
        metrics_data["Value"].append(self.element_metrics["usecases_not_detected_qtd"])

        metrics_data["Category"].append("Use Cases Information")
        metrics_data["Metric"].append("Use Cases Extra Detected Qtd")
        metrics_data["Value"].append(self.element_metrics["usecases_extra_detected_qtd"])

        metrics_data["Category"].append("Use Cases Information")
        metrics_data["Metric"].append("Use Cases Expected Detail")
        metrics_data["Value"].append(self.element_metrics["usecases_expected_detail"])

        metrics_data["Category"].append("Use Cases Information")
        metrics_data["Metric"].append("Use Cases Missing Detail")
        metrics_data["Value"].append(self.element_metrics["usecases_missing_detail"])

        metrics_data["Category"].append("Use Cases Information")
        metrics_data["Metric"].append("Use Cases Extra Detail")
        metrics_data["Value"].append(self.element_metrics["usecases_extra_detail"])

        metrics_data["Category"].append("Relationships Information")
        metrics_data["Metric"].append("Relationships Expected Qtd")
        metrics_data["Value"].append(self.element_metrics["relationships_expected_qtd"])

        metrics_data["Category"].append("Relationships Information")
        metrics_data["Metric"].append("Relationships Detected Qtd")
        metrics_data["Value"].append(self.element_metrics["relationships_detected_qtd"])

        metrics_data["Category"].append("Relationships Information")
        metrics_data["Metric"].append("Relationships Balance Qtd")
        metrics_data["Value"].append(self.element_metrics["relationships_balance_qtd"])

        metrics_data["Category"].append("Relationships Information")
        metrics_data["Metric"].append("Relationships Coverage Metric")
        metrics_data["Value"].append(f"{self.element_metrics["relationships_coverage"]:.2%}")

        metrics_data["Category"].append("Relationships Information")
        metrics_data["Metric"].append("Relationships Not Detected Qtd")
        metrics_data["Value"].append(self.element_metrics["relationships_not_detected_qtd"])

        metrics_data["Category"].append("Relationships Information")
        metrics_data["Metric"].append("Relationships Extra Detected Qtd")
        metrics_data["Value"].append(self.element_metrics["relationships_extra_detected_qtd"])

        metrics_data["Category"].append("Relationships Information")
        metrics_data["Metric"].append("Relationships Expected Detail")
        metrics_data["Value"].append(self.element_metrics["relationships_expected_detail"])

        metrics_data["Category"].append("Relationships Information")
        metrics_data["Metric"].append("Relationships Missing Detail")
        metrics_data["Value"].append(self.element_metrics["relationships_missing_detail"])

        metrics_data["Category"].append("Relationships Information")
        metrics_data["Metric"].append("Relationships Extra Detail")
        metrics_data["Value"].append(self.element_metrics["relationships_extra_detail"])

        metrics_data["Category"].append("Components Evaluation")
        metrics_data["Metric"].append("Missing Actors")
        metrics_data["Value"].append(self.element_metrics["elements_to_add"]["actors"])

        metrics_data["Category"].append("Components Evaluation")
        metrics_data["Metric"].append("Missing Use Cases")
        metrics_data["Value"].append(self.element_metrics["elements_to_add"]["use_cases"])

        metrics_data["Category"].append("Components Evaluation")
        metrics_data["Metric"].append("Missing Use Relationships")
        metrics_data["Value"].append(self.element_metrics["elements_to_add"]["relationships"])

        metrics_data["Category"].append("Components Evaluation")
        metrics_data["Metric"].append("Extra Actors")
        metrics_data["Value"].append(self.element_metrics["elements_to_delete"]["actors"])

        metrics_data["Category"].append("Components Evaluation")
        metrics_data["Metric"].append("Extra Use Cases")
        metrics_data["Value"].append(self.element_metrics["elements_to_delete"]["use_cases"])

        metrics_data["Category"].append("Components Evaluation")
        metrics_data["Metric"].append("Extra Relationships")
        metrics_data["Value"].append(self.element_metrics["elements_to_delete"]["relationships"])

        metrics_data["Category"].append("Components Evaluation")
        metrics_data["Metric"].append("Total Component Edit Operations")
        metrics_data["Value"].append(self.element_metrics["total_edit_operations"])

        metrics_data["Category"].append("Components Evaluation")
        metrics_data["Metric"].append("AVG Component Edit Operations")
        metrics_data["Value"].append(f"{self.element_metrics["weighted_score"]:.2f}")

        metrics_data["Category"].append("Components Evaluation")
        metrics_data["Metric"].append("Overall Wheighted Score")
        metrics_data["Value"].append(f"{self.element_metrics["overall_weighted_score"]:.2f}")

        metrics_data["Category"].append("Components Evaluation")
        metrics_data["Metric"].append("Code Similarity Score")
        metrics_data["Value"].append(f"{self.element_metrics["code_similarity"]:.2f}")

        # Create DataFrame
        df = pd.DataFrame(metrics_data)

        # Style the table
        styled_df = df.style.set_table_styles([
            {'selector': 'th', 'props': [('background-color', '#4472C4'), 
                                      ('color', 'white'),
                                      ('font-weight', 'bold'),
                                      ('text-align', 'center'),
                                      ('border', '1px solid #4472C4')]},
            {'selector': 'td', 'props': [('border', '1px solid #DDDDDD'),
                                      ('padding', '8px'),
                                      ('text-align', 'center')]},
        ])

        # Add alternating row colors
        styled_df = styled_df.set_properties(**{
            'background-color': '#F3F3F3',
            'subset': pd.IndexSlice[df.index % 2 == 0, :]
        })

        # Save as HTML
        html_path = f"{self.generated_usecase_elements['base_name']}-metrics_table.html"
        fullname_html_path = os.path.join(self.REPORT_OUTPUT_DIRECTORY, self.REPORT_ANALYSIS_OUTPUT_DIRECTORY, html_path)

        with open(fullname_html_path, 'w') as f:
            f.write(styled_df.to_html())

        # Convert to image for inclusion in report
        img_path = f"{self.generated_usecase_elements['base_name']}-metrics_table.png"
        fullname_img_path = os.path.join(self.REPORT_OUTPUT_DIRECTORY, self.REPORT_ANALYSIS_OUTPUT_DIRECTORY, img_path)

        # Use matplotlib to render the table as an image
        fig, ax = plt.subplots(figsize=(12, len(df) * 0.5 + 1))
        ax.axis('tight')
        ax.axis('off')
        table = ax.table(
            cellText=df.values,
            colLabels=df.columns,
            loc='center',
            cellLoc='center'
        )
        table.auto_set_font_size(False)
        table.set_fontsize(10)
        table.scale(1.2, 1.2)

        # Style the table header
        for (row, col), cell in table.get_celld().items():
            if row == 0:
                cell.set_text_props(fontproperties=plt.matplotlib.font_manager.FontProperties(weight='bold'))
                cell.set_facecolor('#4472C4')
                cell.set_text_props(color='white')
            elif row % 2 == 1:
                cell.set_facecolor('#F3F3F3')

        plt.tight_layout()
        plt.savefig(fullname_img_path, dpi=300, bbox_inches='tight')
        plt.close()

        return img_path

    def generate_diagram_report(self):
        """
        Generate a comprehensive report of the comparison results.

        Returns:
            dict: Dictionary containing paths to generated visualizations and reports
        """
        element_cov_path = self._generate_element_coverage_visualization()
        report_files = {"element_coverage_chart": element_cov_path}

        rework_path = self._generate_rework_effort_visualization()
        report_files["rework_effort_chart"] = rework_path

        score_path = self._generate_overall_score_visualization()
        report_files["overall_score_chart"] = score_path

        radar_path = self._generate_quality_metrics_radar_chart()
        report_files["radar_chart"] = radar_path

        metrics_path = self._generate_metrics_table_visualization()
        report_files["metrics_table"] = metrics_path

        # Generate markdown report
        report_path = self._generate_individual_diagram_markdown_report(report_files)
        report_files["markdown_report"] = report_path

        return self.get_collect_diagram_id(), report_files

    def _generate_individual_diagram_markdown_report(self, report_files):
        """
        Generate a Markdown report with insights and visualizations.

        Args:
            report_files (dict): Dictionary of paths to generated visualizations

        Returns:
            str: Path to the generated Markdown report
        """
        # report_path = f"{self.generated_usecase_elements['base_name']}-diagram_comparison_report.md"

        # Generate rework interpretation text
        score = self.element_metrics["overall_weighted_score"]

        if score <= 0.20:
            rework_interpretation = "Diagram ready or requires minimal fixes."
        elif score <= 0.40:
            rework_interpretation = " Minor rework needed to align with the reference."
        elif score <= 0.60:
            rework_interpretation = "Moderate rework required. Review structure and connections."
        elif score <= 0.80:
            rework_interpretation = "Heavy rework required. Consider whether reuse is efficient."
        else:
            rework_interpretation = "Too costly to fix. It may be better to rebuild the diagram from scratch."

        # Convert images to base64 for embedding in Markdown
        def embed_image_base64(image_path):
            if not os.path.exists(image_path):
                return None

            with open(image_path, "rb") as img_file:
                img_data = base64.b64encode(img_file.read()).decode('utf-8')

            # Get file extension
            ext = os.path.splitext(image_path)[1].lstrip('.')
            return f"data:image/{ext};base64,{img_data}"

        # Create report content
        report_content = f"""
# UML Use Case Diagram Comparison Report
---
**Model Evaluated:** {self.model_info["modelo"]}  
**Model Temperature:** {self.model_info["temperatura"]}  
**Model Prover:** {self.model_info["provider"]}  
**Model Sample ID:** {self.model_info["coleta"]}  
**Comparison Date:** {self.comparison_date.strftime('%Y-%m-%d %H:%M:%S')}  
**Overall Quality Score:** {self.element_metrics["overall_weighted_score"]:.2%}

**EVALUATION RESUME**:{rework_interpretation}

---

## 1. Overall Comparison

The comparison between the reference and generated UML use case diagrams shows:

- **Element Expected:** {self.element_metrics['elements_expected']}
- **Element Comparison:** {(self.element_metrics['weighted_score']):.2%}
    - **Actors:** **{self.element_metrics['actors_detected_qtd']}** detected of **{self.element_metrics['actors_expected_qtd']}**
    - **Use Cases:** **{self.element_metrics['usecases_detected_qtd']}** detected of **{self.element_metrics['usecases_expected_qtd']}**
    - **Relationships:** **{self.element_metrics['relationships_detected_qtd']}** detected of **{self.element_metrics['relationships_expected_qtd']}**

- **Total Edits Required:** **{self.element_metrics["elements_to_add"]}** to add, **{self.element_metrics["elements_to_delete"]}** to delete 
    - **Actors:** **{self.element_metrics["elements_to_add"]["actors"]}** to add, **{self.element_metrics["elements_to_delete"]["actors"]}** to delete.
    - **Use Cases:** **{self.element_metrics["elements_to_add"]["use_cases"]}** to add, **{self.element_metrics["elements_to_delete"]["use_cases"]}** to delete.
    - **Relationships:** **{self.element_metrics["elements_to_add"]["relationships"]}** to add, **{self.element_metrics["elements_to_delete"]["relationships"]}** to delete.

![Overall AVG Comparation Score]({report_files["overall_score_chart"]})

---

## 2. Elements Analysis

### Elements Key Metrics:

    - **Actor Coverage %:** {self.element_metrics['actors_coverage']:.2%}
    - **Use Case Coverage %:** {self.element_metrics['usecases_coverage']:.2%}
    - **Relationships Coverage %:** {self.element_metrics['relationships_coverage']:.2%}
    - **Missing Actors Qtd:** {self.element_metrics['elements_to_add']['actors']}
    - **Missing Use Cases Qtd:** {self.element_metrics['elements_to_add']['use_cases']}
    - **Missing Relationships Qtd:** {self.element_metrics['elements_to_add']['relationships']}
    - **Not Specified Actors Qtd:** {self.element_metrics['elements_to_delete']['actors']}
    - **Not Specified Use Cases Qtd:** {self.element_metrics['elements_to_delete']['use_cases']}
    - **Not Specified Relationships Qtd:** {self.element_metrics['elements_to_delete']['relationships']}

    ![Element Coverage]({report_files["element_coverage_chart"]})

### Elements Generated:

The LLM specifies the following elements according to the reference specification

"""

        if self.element_metrics["actors_expected_detail"]:
            report_content += "**Generated Actors:**\n"
            for actor in sorted(self.element_metrics["actors_expected_detail"]["common_names"]):
                report_content += f"- {actor}\n"
            report_content += "\n"
        else:
            report_content += "**Generated Actors:** None\n\n"

        if self.element_metrics["usecases_expected_detail"]:
            report_content += "**Generated Use Cases:**\n"
            for usecase in sorted(self.element_metrics["usecases_expected_detail"]["common_names"]):
                report_content += f"- {usecase}\n"
            report_content += "\n"
        else:
            report_content += "**Generated Use Cases:** None\n\n"

        if self.element_metrics["relationships_expected_detail"]:
            report_content += "**Generated Relationships:**\n"
            for relationship in sorted(self.element_metrics["relationships_expected_detail"]["common_names"]):
                parts = dict(part.split(':') for part in relationship.split('|'))
                formatted_rs = f"**source** {parts['source']} --> **target** {parts['target']} (type: {parts['type']})"
                report_content += f"- {formatted_rs}\n"
            report_content += "\n"
        else:
            report_content += "**Generated Relationships:** None\n\n"

        report_content += """

### Elements Not Generated:

The LLM no longer specifies the following elements according to the reference specification

    """
        # Add missing actors list
        if self.element_metrics["actors_missing_detail"]:
            report_content += "**Missing Actors:**\n"
            for actor in sorted(self.element_metrics["actors_missing_detail"]):
                report_content += f"- {actor}\n"
            report_content += "\n"
        else:
            report_content += "**Missing Actors:** None\n\n"

        # Add missing use cases list
        if self.element_metrics["usecases_missing_detail"]:
            report_content += "**Missing Use Cases:**\n"
            for usecase in sorted(self.element_metrics["usecases_missing_detail"]):
                report_content += f"- {usecase}\n"
            report_content += "\n"
        else:
            report_content += "**Missing Use Cases:** None\n\n"

        # Add missing relationships list
        if self.element_metrics["relationships_missing_detail"]:
            report_content += "**Missing Relationships:**\n"
            for relationship in sorted(self.element_metrics["relationships_missing_detail"]):
                parts = dict(part.split(':') for part in relationship.split('|'))
                formatted_rs = f"**source** {parts['source']} --> **target** {parts['target']} (type: {parts['type']})"
                report_content += f"- {formatted_rs}\n"
            report_content += "\n"
        else:
            report_content += "**Missing Relationships:** None\n\n"

        report_content += """

### Elements Not Specified But Generated:

The LLM specified the following elements outside the reference specification

        """
        # Add extra elements
        if self.element_metrics["actors_extra_detail"]:
            report_content += "**Actors Not Specified In Reference:**\n"
            for actor in sorted(self.element_metrics["actors_extra_detail"]):
                report_content += f"- {actor}\n"
            report_content += "\n"
        else:
            report_content += "**Actors Not Specified In Reference:** None\n\n"

        if self.element_metrics["usecases_extra_detail"]:
            report_content += "**Use Cases Not Specified In Reference:**\n"
            for uc in sorted(self.element_metrics["usecases_extra_detail"]):
                report_content += f"- {uc}\n"
            report_content += "\n"
        else:
            report_content += "**Use Cases Not Specified in Reference:** None\n\n"

        if self.element_metrics["relationships_extra_detail"]:
            report_content += "**Relationships Not Specified In Reference:**\n"
            for relationship in sorted(self.element_metrics["relationships_extra_detail"]):
                parts = dict(part.split(':') for part in relationship.split('|'))
                formatted_rs = f"**source** {parts['source']} --> **target** {parts['target']} (type: {parts['type']})"
                report_content += f"- {formatted_rs}\n"
            report_content += "\n"
        else:
            report_content += "**Relationships Not Specified In Reference:** None\n\n"

        # Add rework analysis
        report_content += f"""
## 3. Rework Analysis

### Required Edit Operations:
    - **Actors to Add:** {self.element_metrics["elements_to_add"]["actors"]}
    - **Use Cases to Add:** {self.element_metrics["elements_to_add"]["use_cases"]}
    - **Relationships to Add:** {self.element_metrics["elements_to_add"]["relationships"]}
    - **Total Add Operations:** {self.element_metrics["total_add_operations"]}

    - **Actors to Delete:** {self.element_metrics["elements_to_delete"]["actors"]}
    - **Use Cases to Delete:** {self.element_metrics["elements_to_delete"]["use_cases"]}
    - **Relationships to Delete:** {self.element_metrics["elements_to_delete"]["relationships"]}
    - **Total Delete Operations:** {self.element_metrics["total_delete_operations"]}

    - **Total Edit Operations:** {self.element_metrics["total_edit_operations"]}

    - **AVG Rework Score:** {self.element_metrics["weighted_score"]:.2f}
        ( arithimetic_avg_for_detected_components = (detected_actor_coverage + detected_usecase_coverage + detected_relationships_coverage) / 3)

### Weighted Rework Score

    The **Weighted Rework Score** is a normalized metric (ranging from 0 to 1) that estimates the proportion of effort required to adjust the generated UML use case diagram to align with the reference specification.

    This score accounts for the number and type of modifications needed — including additions and deletions of actors, use cases, and relationships — weighted by their relative effort. The final value is normalized by the total number of elements in the reference diagram, enabling consistent interpretation across different diagram sizes.

    The higher the score, the more extensive the rework required. A score close to 1 suggests that the diagram may be easier to rebuild from scratch than to fix.

    | Weighted Rework Score | Interpretation                              |
    |-----------------------|---------------------------------------------|
    | 0.00 - 0.20           | Diagram ready or requires minimal fixes   |
    | 0.21 - 0.40           | Minor rework needed                      |
    | 0.41 - 0.60           | Moderate rework required                 |
    | 0.61 - 0.80           | Heavy rework, consider redoing           |
    | 0.81 - 1.00           | Too costly to fix, better rebuild         |


- **Overall Rework Score:** {self.element_metrics["overall_weighted_score"]:.2f}

![Rework Effort]({report_files["rework_effort_chart"]})

## 4. Visualization Comparison

### Reference and Generated Diagrams
<table>
<tr>
    <td><b>Reference Diagram</b></td>
    <td><b>Generated Diagram</b></td>
</tr>
<tr>
    <td><img src="{self.reference_image_name}" alt="Reference Diagram" width="400"/></td>
    <td><img src="{self.generated_image_name}" alt="Generated Diagram" width="400"/></td>
</tr>
</table>

### Image Similarity Analysis Between Reference and Generated Diagrams

To complement the structural and semantic evaluation of the UML use case diagrams, was also performed an image-level similarity analysis. 
This allows to assess how visually similar the generated diagram is to the reference diagram — particularly important for evaluating general recognizability.

The following metrics were used:

- **SSIM (Structural Similarity Index)**
    SSIM measures the perceptual similarity between two images by comparing structural information, luminance, and contrast.  
    The value ranges from **0 (no similarity)** to **1 (perfect similarity)**.  
    This metric is widely adopted in image quality assessment because it aligns well with human visual perception.

- **MSE (Mean Squared Error)**
    MSE measures the average squared difference between the pixel intensities of the reference and the generated diagram.  
    Lower values indicate **higher similarity**.
    MSE is sensitive to even minor shifts or layout adjustments, so it is typically interpreted in combination with SSIM.

- **Histogram Correlation**
    This metric compares the distribution of pixel intensities (histograms) in both images.
    A value close to **1** indicates that the overall pixel intensity patterns are similar, even if the exact layout or structure differs.  
    This is useful to detect global visual consistency even when fine-grained alignment is not perfect.

        """

        # Add image similarity metrics if available
        if self.image_metrics:
            report_content += f"""### Image Similarity Metrics:
        - **SSIM Score for** `{self.generated_image_name}`: {self.image_metrics["ssim_score"]:.4f}
        - **MSE:** {self.image_metrics["mse"]:.2f}
        - **Histogram Correlation:** {self.image_metrics["histogram_correlation"]:.4f}

        ![SSIM Visualization]({self.image_metrics["ssim_visualization_path"]})

        ![Difference Image]({self.image_metrics["difference_image_path"]})
        """

        # Add radar chart for all metrics
        report_content += f"""
## 5. Key Metrics Overview

![Radar Chart]({os.path.basename(report_files["radar_chart"])})

## 6. Detailed Metrics

![Metrics Table]({os.path.basename(report_files["metrics_table"])})

## 7. Conclusion

        """
        score = self.element_metrics["overall_weighted_score"]

        if score <= 0.20:
            report_content += "The generated diagram shows **excellent alignment** with the reference. It can be used with minimal or no adjustments. "
        elif score <= 0.40:
            report_content += "The generated diagram shows **good alignment** with the reference. Minor rework is needed to improve precision."
        elif score <= 0.60:
            report_content += "The generated diagram shows **moderate alignment**. Some structural and semantic corrections are required. "
        elif score <= 0.80:
            report_content += "The generated diagram shows **low alignment**. Reuse is possible, but rework will be considerable. "
        else:
            report_content += "The generated diagram shows **poor alignment**. Rebuilding from scratch may be more efficient than fixing the current version. "

        report_content += """

---

        """

        return self.get_collect_diagram_id(), report_content

    def _generate_element_coverage_visualization(self):
        """
        Visualize element coverage metrics.

        Returns:
            str: Path to the generated visualization
        """
        categories = ["Actors", "Use Cases", "Relationships"]
        coverage_values = [
            self.element_metrics["actors_coverage"] * 100,
            self.element_metrics["usecases_coverage"] * 100,
            self.element_metrics["relationships_coverage"] * 100
        ]

        missing_values = [
            self.element_metrics["actors_not_detected_qtd"],
            self.element_metrics["usecases_not_detected_qtd"],
            self.element_metrics["relationships_not_detected_qtd"]
        ]

        not_in_reference_values = [
            self.element_metrics["actors_extra_detected_qtd"],
            self.element_metrics["usecases_extra_detected_qtd"],
            self.element_metrics["relationships_extra_detected_qtd"]
        ]

        # Create figure with custom style
        plt.figure(figsize=(12, 8))
        sns.set_style("whitegrid")

        # Coverage bar chart
        ax1 = plt.subplot(2, 2, 1)
        bars = ax1.bar(categories, coverage_values, color=sns.color_palette("viridis", 3))
        ax1.set_ylim(0, 100)
        ax1.set_ylabel("Coverage (%)")
        ax1.set_title("Detected Elements Coverage", fontsize=14)

        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height + 2,
                    f'{height:.1f}%', ha='center', va='bottom')

        # Missing elements bar chart
        ax2 = plt.subplot(2, 2, 2)
        bars = ax2.bar(categories, missing_values, color=sns.color_palette("coolwarm", 3))
        ax2.set_ylabel("Count")
        ax2.set_title("Missing Elements", fontsize=14)

        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                    f'{height}', ha='center', va='bottom')

        # Superfluous elements bar chart
        ax3 = plt.subplot(2, 2, 3)
        bars = ax3.bar(categories, not_in_reference_values, color=sns.color_palette("mako", 3))
        ax3.set_ylabel("Count")
        ax3.set_title("Not Specified Elements", fontsize=14)

        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            ax3.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                    f'{height}', ha='center', va='bottom')

        # Add text summary
        ax4 = plt.subplot(2, 2, 4)
        ax4.axis('off')
        summary_text = (
            f"**Element Coverage Summary**:\n\n"
            f"Actor Coverage: {self.element_metrics['actors_coverage']*100:.1f}%\n"
            f"Use Case Coverage: {self.element_metrics['usecases_coverage']*100:.1f}%\n"
            f"Relationship Coverage: {self.element_metrics['relationships_coverage']*100:.1f}%\n\n"
            f"Total Missing Elements: {sum(missing_values)}\n"
            f"Total Not Specified Elements: {sum(not_in_reference_values)}\n\n"
            f"Overall Element Quality Score: {self.element_metrics['weighted_score']*100:.1f}%"
        )
        ax4.text(0, 0.5, summary_text, fontsize=12, va='center')

        plt.tight_layout()

        # Save the visualization
        file_name = f"{self.generated_usecase_elements['base_name']}-element_coverage.png"
        fullname_file_name = os.path.abspath(os.path.join(self.REPORT_OUTPUT_DIRECTORY, self.REPORT_ANALYSIS_OUTPUT_DIRECTORY, file_name))

        plt.savefig(fullname_file_name, dpi=300, bbox_inches='tight')
        plt.close()

        return file_name

    def _generate_rework_effort_visualization(self):
        """
        Visualize rework effort metrics.

        Returns:
            str: Path to the generated visualization
        """
        # Prepare data
        categories = ["Add Actors", "Add Use Cases", "Delete Actors", "Delete Use Cases", "Add Relationships", "Delete Relationships"]

        values = [
            self.element_metrics["elements_to_add"]["actors"],
            self.element_metrics["elements_to_add"]["use_cases"],
            self.element_metrics["elements_to_add"]["relationships"],
            self.element_metrics["elements_to_delete"]["actors"],
            self.element_metrics["elements_to_delete"]["use_cases"],
            self.element_metrics["elements_to_delete"]["relationships"],
        ]

        # Create color map for effort intensity
        colors = sns.color_palette("YlOrRd", len(categories))

        # Create figure
        plt.figure(figsize=(12, 8))

        # Main rework effort chart
        ax1 = plt.subplot(2, 1, 1)
        bars = ax1.bar(categories, values, color=colors)
        ax1.set_ylabel("Number of Operations")
        ax1.set_title("Rework Effort by Operation Type", fontsize=14)
        plt.xticks(rotation=45, ha='right')

        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                    f'{height}', ha='center', va='bottom')

        # Weighted rework effort chart
        ax2 = plt.subplot(2, 1, 2)

        # Create a pie chart for the proportion of rework effort
        labels = ['Element Additions', 'Element Deletions']
        element_add_effort = (self.element_metrics["total_add_operations"])
        element_del_effort = (self.element_metrics["total_delete_operations"])

        sizes = [element_add_effort, element_del_effort]
        explode = (0.1, 0)  # explode first slice

        # Only create pie chart if there's rework to do
        if sum(sizes) > 0:
            ax2.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%', shadow=True, startangle=90, colors=sns.color_palette("Set2", 2))
            ax2.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle
            ax2.set_title(f"Distribution of Rework Effort (Total: {sum(sizes)} operations)", fontsize=14)
        else:
            ax2.text(0.5, 0.5, "No rework needed!", fontsize=16, ha='center', va='center')
            ax2.axis('off')

        plt.tight_layout()

        # Save the visualization
        file_name = f"{self.generated_usecase_elements['base_name']}-rework_effort.png"
        fullname_file_name = self.reference_image_fullname = os.path.join(self.REPORT_OUTPUT_DIRECTORY, self.REPORT_ANALYSIS_OUTPUT_DIRECTORY, file_name)

        plt.savefig(fullname_file_name, dpi=300, bbox_inches='tight')
        plt.close()

        return file_name

    def _generate_overall_score_visualization(self):
        """
        Visualize the overall score using a semicircular gauge chart.

        Returns:
            str: Path to the generated visualization
        """
        score = self.element_metrics["overall_weighted_score"]

        # Criar figura e eixo
        fig, ax = plt.subplots(figsize=(12, 8))

        # === Base do gauge ===
        base = Wedge(center=(0, 0), r=1, theta1=0, theta2=180, facecolor='lightgray', edgecolor='black', lw=0.5)
        ax.add_patch(base)

        # === Gauge preenchido ===
        end_angle = 180 * score
        if score < 0.4:
            color = 'darkred'
            interp = "Significant rework needed"
        elif score < 0.7:
            color = 'orange'
            interp = "Moderate rework needed"
        else:
            color = 'green'
            interp = "Good match, minimal rework"

        value = Wedge(center=(0, 0), r=1, theta1=0, theta2=end_angle, facecolor=color, edgecolor=None)
        ax.add_patch(value)

        # === Marcas (0%, 25%, 50%, ...) ===
        for pct in [0, 0.25, 0.5, 0.75, 1.0]:
            angle = np.deg2rad(180 * pct)
            x = np.cos(angle)
            y = np.sin(angle)
            ax.text(1.1 * x, 1.1 * y, f"{int(pct * 100)}%", ha='center', va='center', fontsize=8)

        # === Texto principal ===
        ax.text(0, 1.05, "Overall Diagram Quality Score", fontsize=14, ha='center', va='center', fontweight='bold')
        ax.text(0, -0.05, f"{score:.2%}", fontsize=28, ha='center', va='center', color='black')
        ax.text(0, -0.25, interp, fontsize=12, ha='center', va='center', fontweight='bold', color=color)

        ax.text(
            0, -0.5,
            f"""Score Components:
            Actors Coverage: {self.element_metrics["actors_coverage"]:.2%}
            Use Cases Coverage: {self.element_metrics["usecases_coverage"]:.2%}
            Relationship Coverage: {self.element_metrics["relationships_coverage"]:.2%}
            Code Similarity: {self.element_metrics["code_similarity"]:.2%}
            """,
            fontsize=10,
            ha='center',
            va='center',
            bbox=dict(facecolor='white', alpha=0.8, boxstyle='round,pad=0.5')
        )

        # === Ajustes de layout ===
        ax.set_aspect('equal')
        ax.set_xlim(-1.2, 1.2)
        ax.set_ylim(-0.75, 1.2)
        ax.axis('off')
        plt.tight_layout()

        output_dir = "reports/images"
        os.makedirs(output_dir, exist_ok=True)

        file_name = f"{self.generated_usecase_elements['base_name']}--overall_score.png"
        fullname_file_name = self.reference_image_fullname = os.path.join(self.REPORT_OUTPUT_DIRECTORY, self.REPORT_ANALYSIS_OUTPUT_DIRECTORY, file_name)

        plt.savefig(fullname_file_name, dpi=80, bbox_inches='tight')
        plt.close()

        return file_name

    def _extract_relationship_set(self, relationships):
        return {(r["source"], r["target"], r["type"]) for r in relationships}

    def _extract_connection_set(self, relationships):
        return {(r["source"], r["target"]) for r in relationships}

    def __calculate_diff(self, ref_set, gen_set):
        return ref_set - gen_set, gen_set - ref_set

    def _calculate_string_diff_with_similarity(self, ref_list, gen_list, similarity_threshold=0.85):
        matched_ref = set()
        matched_gen = set()
        common_names = []
        common_details = []

        for ref in ref_list:
            best_sim = 0.0
            best_match = None
            for gen in gen_list:
                sim = fuzz.ratio(ref.lower(), gen.lower()) / 100.0
                if sim > best_sim:
                    best_sim = sim
                    best_match = gen
            if best_sim >= similarity_threshold:
                common_names.append(ref)
                common_details.append((ref, best_match, round(best_sim, 2)))
                matched_ref.add(ref)
                matched_gen.add(best_match)

        missing = set(ref_list) - matched_ref
        extras = set(gen_list) - matched_gen

        common = {"common_names": common_names, "common_details": common_details}
        return missing, extras, common

    def _calculate_type_correctness(self, ref_relationships, gen_relationships):
        count = 0
        
        for ref_rel in ref_relationships:
            ref_pair = (ref_rel["source"], ref_rel["target"])
            for gen_rel in gen_relationships:
                if (gen_rel["source"], gen_rel["target"]) == ref_pair:
                    if gen_rel["type"] == ref_rel["type"]:
                        count += 1
                    break
                
        return count

    def _calculate_element_coverage(self):
        return (
            self.element_metrics["actors_coverage"] * 0.5 +
            self.element_metrics["usecases_coverage"] * 0.5
        )

    def _calculate_relationship_coverage(self):
        return (
            self.element_metrics["relationships_coverage"] * 0.7 +
            self.element_metrics["type_correctness"] * 0.3
        )

    def _calculate_name_similarity(self):
        return (
            self.element_metrics["avg_actor_name_similarity"] * 0.5 +
            self.element_metrics["avg_usecase_name_similarity"] * 0.5
        )

    def _open_file(self, full_file_name):
        file_to_open = None

        try:
            with open(full_file_name, 'r', encoding=self.ENCODING) as file:
                file_to_open = file.read()
        except FileNotFoundError:
            self.LOGGER.error(f"Unable to start the use case diagram comparator because the file could not be opened: {file_to_open}")

        return file_to_open

    def _load_or_save_sentence_model(self, huggingface_model: str = "microsoft/codebert-base"):
        if os.path.exists(self.GENERAL_OUTPUT_DIRECTORY):
            print(f"Loading Sentence Transformer Model from: {self.GENERAL_OUTPUT_DIRECTORY}")
            model = SentenceTransformer(huggingface_model)
        else:
            print(f"Sentence Transformer Model not founded. Downloading and saving in: {self.GENERAL_OUTPUT_DIRECTORY}")
            model = SentenceTransformer(huggingface_model)
            model.save(self.GENERAL_OUTPUT_DIRECTORY)

        return model
