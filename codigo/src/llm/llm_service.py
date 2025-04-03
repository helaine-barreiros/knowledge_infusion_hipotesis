from abc import ABC, abstractmethod
from src.utils.system_parametrization import SYSTEM_CONFIG
from src.utils.logger import Logger


class LLMStrategy(ABC):
    @abstractmethod
    def execute(self, prompt, **params):
        pass


class OpenAIStrategy(LLMStrategy):
    def __init__(self):
        self.api_key = SYSTEM_CONFIG.get("general.models.default_openai_key", "")
        self.base_url = SYSTEM_CONFIG.get("general.models.default_openai_provider", "http://localhost:11434/api/chat")
        self.default_model = SYSTEM_CONFIG.get("general.models.default_openai_model", "gpt-4o")
        self.temperature = SYSTEM_CONFIG.get("general.models.default_openai_temperature", 0.7)
        self.logger = Logger

    def execute(self, prompt, **params):
        import openai

        api_key = params.get("api_key", self.api_key)
        base_url = params.get("base_url", self.default_model)
        model = params.get("model", self.default_model)
        system_message = params.get("system_prompt", "")
        temperature = params.get("temperature", self.temperature)

        client = openai.OpenAI(api_key=api_key, base_url=base_url)

        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": prompt}
            ],
            temperature=temperature
        )

        return response.choices[0].message.content


class OllamaStrategy(LLMStrategy):
    def __init__(self):
        self.api_url = SYSTEM_CONFIG.get("general.models.default_ollama_url", "https://4b51-200-133-1-77.ngrok-free.app/api/chat")
        self.default_model = SYSTEM_CONFIG.get("general.models.default_.ollama_model",
                                               "Qwen2.5-Coder-7B-Instruct:latest")
        self.temperature = SYSTEM_CONFIG.get("general.models.default_ollama_temperature", 0.7)
        self.timeout = SYSTEM_CONFIG.get("general.models.default_ollama_timeout", 60)
        self.logger = Logger

    def execute(self, prompt, **params):
        from ollama import Client

        content = ""

        model = params.get("model", self.default_model)
        system_message = params.get("system_prompt", "")
        temperature = params.get("temperature", self.temperature)
        timeout = params.get("timeout", self.timeout)
        api_url = params.get("api_url", self.api_url)

        client = Client(host=api_url)

        try:
            messages = [
                {"role": "system", "content": system_message},
                {"role": "user", "content": prompt}
            ]

            model_response = client.chat(
                messages=messages,
                model=model,
                options={"temperature": temperature},
                stream=False
            )

            self.logger.info(f"Calling Ollama API with model={model}, temp={temperature}, timeout={timeout}")

            if model_response.done:
                self.logger.info(f"Result chat:{model_response.message.content}")
                content = model_response.message.content

            self.logger.info(f"Extracted content: {content[:100]}...")

        except Exception as e:
            self.logger.error(f"Error calling Ollama API: {e}")

        return content


class LLMStrategyFactory:
    @staticmethod
    def create_strategy(provider):
        if provider.lower() == "openai":
            return OpenAIStrategy()
        elif provider.lower() == "ollama":
            return OllamaStrategy()
        else:
            raise ValueError(f"The LLM provider is not supported: {provider}")


class LLMService:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(LLMService, cls).__new__(cls)
        return cls._instance

    def executeLLM(self, prompt, provider=None, **params):
        if provider is None:
            provider = SYSTEM_CONFIG.get("general.models.default_provider", "ollama")

        strategy = LLMStrategyFactory.create_strategy(provider)
        return strategy.execute(prompt, **params)
