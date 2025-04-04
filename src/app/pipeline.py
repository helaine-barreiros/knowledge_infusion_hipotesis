from datetime import datetime
from src.dsk_experiment.dsk_use_case_experiment_controller import DskExperimentController
from src.utils.system_parametrization import SYSTEM_CONFIG
from src.utils.logger import Logger

LOGGER = Logger

qtd_iteractions = SYSTEM_CONFIG.get("general.iteractions")


def main():

    start_time = datetime.now()
    use_case_experiment_controller = DskExperimentController()

    LOGGER.info("┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓")
    LOGGER.info("┃               🚀 DSK KNOWLEDGE EXPERIMENT PIPELINE STARTED         ┃")
    LOGGER.info("┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛")

    iteractions = 1

    for i in range(1, qtd_iteractions + 1):
        LOGGER.info(f"STARTING EXPERIMENTAL COLLECTION {iteractions} OF {qtd_iteractions}")

        _print_iteration_log_data_start(qtd_iteractions, i)

        use_case_experiment_controller.collect_dsk_treatment_samples_to_use_case_artifacts(i, start_time)

        _print_iteration_log_end(i)

        iteractions += iteractions

    end_time = datetime.now()
    execution_time = end_time - start_time

    LOGGER.info("┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓")
    LOGGER.info("┃    🎉 DSK KNOWLEDGE EXPERIMENT PIPELINE COMPLETED SUCCESSFULLY   ┃")
    LOGGER.info(f"┃        ⏱️  Total execution time: {execution_time}                ┃")
    LOGGER.info("┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛")


def _print_iteration_log_end(i):
    LOGGER.info(f"✅ Iteration {i} completed")


def _print_iteration_log_data_start(qtd_iteractions, i):
    progress = int(qtd_iteractions * i / qtd_iteractions)
    progress_bar = "█" * progress + "░" * (qtd_iteractions - progress)
    percentage = int(100 * i / qtd_iteractions)

    LOGGER.info("┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓")
    LOGGER.info(f"┃ 🔄 ITERATION {i}{qtd_iteractions} [{progress_bar}] {percentage}%            ┃")
    LOGGER.info("┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛")


if __name__ == "__main__":

    main()
