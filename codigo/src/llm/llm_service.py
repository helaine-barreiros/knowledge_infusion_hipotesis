from abc import ABC, abstractmethod
from src.utils.system_parametrization import SYSTEM_CONFIG


class LLMStrategy(ABC):
    @abstractmethod
    def execute(self, prompt, **params):
        pass


class OpenAIStrategy(LLMStrategy):
    def __init__(self):
        self.api_key = SYSTEM_CONFIG.get("rag.openai_api_key")
        self.base_url = SYSTEM_CONFIG.get("rag.openai_base_url", "https://api.openai.com/v1")
        self.default_model = SYSTEM_CONFIG.get("rag.openai_model", "gpt-4o")

    def execute(self, prompt, **params):
        import openai

        client = openai.OpenAI(api_key=self.api_key)

        model = params.get("model", self.default_model)
        system_message = params.get("system_prompt", "")
        temperature = params.get("temperature", 0.7)

        # Chamar a API OpenAI
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
        self.api_url = SYSTEM_CONFIG.get("rag.ollama_url", "http://localhost:11434/api/chat")
        self.default_model = SYSTEM_CONFIG.get("rag.ollama_model", "phi4-mini")

    def execute(self, prompt, **params):
        import requests
        import json
        import logging
        import re

        logger = logging.getLogger(__name__)
        
        model = params.get("model", self.default_model)
        system_message = params.get("system_prompt", "")
        temperature = params.get("temperature", 0.7)
        timeout = params.get("timeout", 60)  # Timeout padrão de 60 segundos

        payload = {
            "model": model,
            "messages": [
                {"role": "system", "content": system_message},
                {"role": "user", "content": prompt}
            ],
            "options": {
                "temperature": temperature
            },
            "stream": False  # Garantir que não estamos usando streaming
        }

        try:
            logger.info(f"Calling Ollama API with model={model}, temp={temperature}")
            response = requests.post(self.api_url, json=payload, timeout=timeout)
            response.raise_for_status()
            
            # Log da resposta para debug
            logger.debug(f"API response status: {response.status_code}")
            logger.debug(f"API response headers: {response.headers}")
            logger.debug(f"API response raw text: {response.text[:500]}...")
            
            # Tratamento para múltiplos JSONs na resposta (resposta de streaming)
            if "}{" in response.text:
                logger.info("Detected multiple JSON objects in response (streaming format)")
                
                # Extrair conteúdo de todos os objetos JSON
                content_parts = []
                
                # Encontre cada objeto JSON separadamente
                json_objects = re.findall(r'{[^{]*?}', response.text)
                logger.debug(f"Found {len(json_objects)} JSON objects")
                
                for json_str in json_objects:
                    try:
                        obj = json.loads(json_str)
                        if "message" in obj and "content" in obj["message"]:
                            content = obj["message"]["content"]
                            if content.strip():  # Se não estiver vazio
                                content_parts.append(content)
                    except json.JSONDecodeError:
                        logger.debug(f"Failed to parse JSON object: {json_str[:100]}...")
                
                if content_parts:
                    logger.info(f"Successfully extracted {len(content_parts)} content parts")
                    return "".join(content_parts)
                else:
                    logger.warning("No content found in JSON objects")
            
            # Tratamento normal para uma única resposta JSON
            try:
                # Tenta fazer o parse do JSON
                result = json.loads(response.text)
                logger.debug(f"JSON parsed successfully: {str(result)[:100]}...")
                
                if "message" in result and "content" in result["message"]:
                    content = result["message"]["content"]
                    logger.info(f"Extracted content: {content[:100]}...")
                    return content
                else:
                    logger.warning(f"Unexpected JSON structure: {result}")
                    # Tenta extrair conteúdo de outras formas possíveis
                    if isinstance(result, dict):
                        # Procura por 'content' em qualquer lugar da estrutura
                        for key, value in result.items():
                            if key == "content" and isinstance(value, str):
                                return value
                            elif isinstance(value, dict) and "content" in value:
                                return value["content"]
                    
                    # Extração final: qualquer texto que pareça uma resposta
                    text_response = str(result)
                    if len(text_response) > 20:
                        logger.info("Returning JSON as string")
                        return text_response
            except json.JSONDecodeError as e:
                logger.warning(f"JSON parsing error: {e}")
                
                # Poderíamos estar recebendo texto puro em vez de JSON
                if len(response.text) > 20:
                    logger.info("Returning raw text response")
                    return response.text.strip()
            
            # Solução de último recurso: retorne qualquer texto da resposta
            logger.warning("No structured content found, returning raw response")
            return f"Raw response: {response.text[:500]}..."
                
        except Exception as e:
            logger.error(f"Error calling Ollama API: {e}")
            logger.error(f"Payload was: {payload}")
            
            # Solução de emergência: retorne uma mensagem predefinida
            return f"Error occurred: {str(e)}. Unable to get response from model {model}."


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
            provider = SYSTEM_CONFIG.get("rag.default_provider", "openai")

        strategy = LLMStrategyFactory.create_strategy(provider)
        return strategy.execute(prompt, **params)
