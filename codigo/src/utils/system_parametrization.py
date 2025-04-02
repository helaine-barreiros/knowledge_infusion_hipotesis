from pathlib import Path
from typing import Dict, Any
import os
import yaml
import logging

# Importar Logger sem configuração inicial
from src.utils.logger import Logger

LOGGER = Logger


class SystemParametrization:
    _instance = None
    _initialized = False
    _config: Dict[str, Any] = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SystemParametrization, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not self._initialized:
            self._base_dir = Path(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
            self._config_dir = self._base_dir / "config"
            self._config_file = self._config_dir / "experiment_dsk_config.yaml"
            
            # Configure logger with base directory
            LOGGER.configure(base_dir=self._base_dir)

            self._load_config()
            self._setup_directories()

            self._initialized = True

    def _load_config(self) -> None:
        try:
            if not self._config_file.exists():
                LOGGER.error(f"System configuration file not founded: {self._config_file}")
                return

            with open(self._config_file, 'r', encoding='utf-8') as f:
                self._config = yaml.safe_load(f)

            LOGGER.info(f"System configuration parameters loaded from {self._config_file}")
        except Exception as e:
            LOGGER.error(f"Error in load configuration file: {e}")

    def _setup_directories(self) -> None:
        directories = {
            "dsk_dir": self.get("rag.dsk_dir", "./dsk"),
            "embeddings_dir": self.get("rag.embeddings_dir", "./embeddings"),
            "output_dir": self.get("rag.output_directory", "./output"),
            "log_dir": "./log"
        }

        for name, path in directories.items():
            directory = path if isinstance(path, Path) else Path(path)
            if not directory.is_absolute():
                directory = self._base_dir / directory

            directory.mkdir(exist_ok=True, parents=True)

            self._config[f"_abs_{name}"] = str(directory)

    def get(self, key_path: str, default: Any = None) -> Any:
        if "." not in key_path:
            return self._config.get(key_path, default)

        keys = key_path.split(".")
        value = self._config

        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return default

        return value

    def set(self, key_path: str, value: Any) -> None:
        if "." not in key_path:
            self._config[key_path] = value
            return

        keys = key_path.split(".")
        config = self._config

        for key in keys[:-1]:
            if key not in config:
                config[key] = {}
            config = config[key]

        config[keys[-1]] = value

    def update(self, config_dict: Dict[str, Any], prefix: str = "") -> None:
        for key, value in config_dict.items():
            key_path = f"{prefix}.{key}" if prefix else key

            if isinstance(value, dict):
                self.update(value, key_path)
            else:
                self.set(key_path, value)

    def save_config(self) -> None:
        try:
            # Garantir que o diretório de configuração existe
            self._config_dir.mkdir(exist_ok=True, parents=True)

            with open(self._config_file, 'w', encoding='utf-8') as f:
                yaml.dump(self._config, f, default_flow_style=False, sort_keys=False)

            LOGGER.info(f"Configurations saved on {self._config_file}")
        except Exception as e:
            LOGGER.error(f"Error in saving configuration file: {e}")

    def get_log_level(self) -> int:
        log_level_str = self.get("rag.log_level", "INFO").upper()
        log_levels = {
            "DEBUG": logging.DEBUG,
            "INFO": logging.INFO,
            "WARNING": logging.WARNING,
            "ERROR": logging.ERROR,
            "CRITICAL": logging.CRITICAL
        }
        log_level = log_levels.get(log_level_str, logging.INFO)
        
        # Configure logger with the loaded log level
        LOGGER.configure(log_level=log_level)
        
        return log_level

    def get_abs_path(self, config_key: str) -> Path:
        path_str = self.get(config_key)
        if not path_str:
            return None

        path = Path(path_str)

        return path if path.is_absolute() else self._base_dir / path

    @property
    def all_params(self) -> Dict[str, Any]:
        return self._config.copy()

    @property
    def base_dir(self) -> Path:
        return self._base_dir

    @property
    def config_file(self) -> Path:
        return self._config_file


SYSTEM_CONFIG = SystemParametrization()


def get_system_config() -> SystemParametrization:
    return SYSTEM_CONFIG
