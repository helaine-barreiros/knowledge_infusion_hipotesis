import logging
import sys
import os
import colorlog

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "src")))

from datetime import datetime
from src.rag.llm_prompt import generate_diagram
from src.rag.extract_diagram_metadata import generate_plantuml_image, generate_excel_report, save_plantuml_file
from src.rag.config_loader import CONFIG

def setup_colored_logging():
    handler = colorlog.StreamHandler()

    handler.setFormatter(
        colorlog.ColoredFormatter(
            "%(log_color)s[%(asctime)s] %(bold)s%(levelname)-8s%(reset)s %(blue)s%(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
            log_colors={
                'DEBUG': 'white',
                'INFO': 'green',
                'WARNING': 'yellow',
                'ERROR': 'red',
                'CRITICAL': 'red,bg_white',
            }
        )
    )
    
    logger = colorlog.getLogger()
    logger.handlers = []
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    
    return logger

def main():
    logger = setup_colored_logging()

    start_time = datetime.now()

    logger.info("┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓")
    logger.info("┃                     🚀 DSK KNOWLEDGE EXPERIMENT PIPELINE STARTED             ┃")
    logger.info("┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛")

    config_output_directory = CONFIG["output_directory"]
    qtd_iteractions = CONFIG["iteractions"]


    iteractions = 1    

    for i in range(1, qtd_iteractions + 1):
        logging.info(f"STARTING EXPERIMENTAL COLLECTION {iteractions} OF {qtd_iteractions}")

        progress = int(30 * i / qtd_iteractions)
        progress_bar = "█" * progress + "░" * (30 - progress)
        percentage = int(100 * i / qtd_iteractions)

        logger.info(f"┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓")
        logger.info(f"┃ 🔄 ITERATION {i}/{qtd_iteractions} [{progress_bar}] {percentage}%            ┃")
        logger.info(f"┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛")
        
        collect_openai(i, logger, start_time, config_output_directory, use_specific_knowledge=False)
        collect_openai(i, logger, start_time, config_output_directory, use_specific_knowledge=True)

        logger.info(f"✅ Iteration {i} completed")

    end_time = datetime.now()
    execution_time = end_time - start_time
    
    logger.info("┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓")
    logger.info("┃                🎉 DSK KNOWLEDGE EXPERIMENT PIPELINE COMPLETED SUCCESSFULLY   ┃")
    logger.info(f"┃                ⏱️  Total execution time: {execution_time}                      ┃")
    logger.info("┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛")

def collect_openai(iterator_number, logger, start_time, config_output_directory, use_specific_knowledge):
    model = "o3-mini"
    knowledge_description = "with-treatment" if use_specific_knowledge else "without-treatment"
    filename = f"{model}-{knowledge_description}-collect-{iterator_number}"
    output_directory= f"{config_output_directory}/OpenAI-{model}-{start_time.strftime("%m-%d-%I%p")}"
   
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    logger.info(f"🧠 Generating diagram with {model} model...")

    plantuml_code = generate_diagram(output_directory, filename, llm=model, use_specific_knowledge=use_specific_knowledge)
    
    logger.info(f"💾 Saving PlantUML code: {filename}.puml")
    save_plantuml_file(plantuml_code=plantuml_code, output_filename=filename, output_directory=output_directory)
    
    logger.info(f"🖼️ Generating diagram image: {filename}.png")
    generate_plantuml_image(plantuml_code, output_filename=filename, output_directory=output_directory)
    
    logger.info(f"📊 Generating Excel report: {filename}.xlsx")
    generate_excel_report(plantuml_code, output_filename=filename, output_directory=output_directory)


if __name__ == "__main__":
    main()
