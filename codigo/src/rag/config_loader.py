import yaml
import os

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "../../config/rag_config.yaml")

def load_config():
    """Carrega configurações do arquivo YAML."""
    
    with open(CONFIG_PATH, "r", encoding="utf-8") as file:
        config = yaml.safe_load(file)
    return config["rag"]

CONFIG = load_config()
