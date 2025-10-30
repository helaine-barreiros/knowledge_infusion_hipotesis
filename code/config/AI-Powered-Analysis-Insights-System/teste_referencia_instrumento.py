import os
import sys
from pathlib import Path
from Levenshtein import ratio as levenshtein_ratio
from src.dsk_experiment.dsk_use_case_comparator import UMLDiagramComparator
from src.utils.logger import Logger

# Initialize logger
LOGGER = Logger

def main():
    try:
        # Get the absolute path of the current file's directory
        BASE_DIR = Path(__file__).resolve().parent
        
        # Define file paths
        reference_puml = BASE_DIR / "reference-plantuml.puml"
        reference_png = BASE_DIR / "reference-plantuml.png"
        output_dir = BASE_DIR / "self_comparison_test"
        
        # Create output directory
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Verify files exist
        if not reference_puml.is_file():
            raise FileNotFoundError(f"PUML file not found: {reference_puml}")
        if not reference_png.is_file():
            raise FileNotFoundError(f"PNG file not found: {reference_png}")
            
        # Read PUML content
        with open(reference_puml, 'r', encoding='utf-8') as f:
            puml_content = f.read()
        
        # Initialize comparator
        comparator = UMLDiagramComparator(
            reference_plantuml=puml_content,
            reference_plantuml_image=str(reference_png),
            generated_plantuml=puml_content,
            generated_plantuml_image=str(reference_png),
            output_dir=str(output_dir),
            model_name="Self-Reference Test"
        )
        
        # Generate and save report
        report = comparator.generate_diagram_report()
        LOGGER.info(f"Comparison report generated in {output_dir}")
        
        test_string = "View Financial Insights Dashboard"
        similarity = levenshtein_ratio(test_string.lower(), test_string.lower())
        print(f"Similaridade entre strings idênticas: {similarity}")
        
        return report
        
    except Exception as e:
        LOGGER.error(f"Error during comparison: {str(e)}")
        raise

if __name__ == "__main__":
    main()