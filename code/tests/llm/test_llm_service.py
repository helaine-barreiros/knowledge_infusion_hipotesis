import unittest
from unittest.mock import patch, MagicMock, ANY

# Mock the system parametrization before importing
import sys
sys.modules['utils.system_parametrization'] = MagicMock()
sys.modules['utils.system_parametrization'].SYSTEM_CONFIG = MagicMock()

# Now import the modules
from src.llm.llm_service import (
    LLMService, LLMStrategyFactory, 
    OpenAIStrategy, OllamaStrategy
)


class TestLLMService(unittest.TestCase):

    def setUp(self):
        # Reset the singleton instance before each test
        LLMService._instance = None
        
        # Configure system config mock with default values
        self.config_mock = sys.modules['utils.system_parametrization'].SYSTEM_CONFIG
        self.config_mock.get.side_effect = self._mock_config_get

    def _mock_config_get(self, key, default=None):
        # Default configuration for testing
        config = {
            "rag.default_provider": "openai",
            "rag.openai_api_key": "test_api_key",
            "rag.openai_base_url": "https://api.openai.com/v1",
            "rag.openai_model": "gpt-4o",
            "rag.ollama_url": "http://localhost:11434/api/chat",
            "rag.ollama_model": "phi4-mini"
        }
        return config.get(key, default)

    def test_llm_service_singleton(self):
        """Test that LLMService follows the singleton pattern"""
        service1 = LLMService()
        service2 = LLMService()
        
        self.assertIs(service1, service2)

    @patch('src.llm.llm_service.LLMStrategyFactory.create_strategy')
    def test_execute_llm_with_default_provider(self, mock_create_strategy):
        """Test executeLLM method with default provider"""
        # Setup mock strategy
        mock_strategy = MagicMock()
        mock_strategy.execute.return_value = "Test response"
        mock_create_strategy.return_value = mock_strategy
        
        # Execute
        service = LLMService()
        response = service.executeLLM("Test prompt")
        
        # Assert
        self.assertEqual(response, "Test response")
        mock_create_strategy.assert_called_once_with("openai")
        mock_strategy.execute.assert_called_once_with("Test prompt")

    @patch('src.llm.llm_service.LLMStrategyFactory.create_strategy')
    def test_execute_llm_with_specific_provider(self, mock_create_strategy):
        """Test executeLLM method with a specific provider"""
        # Setup mock strategy
        mock_strategy = MagicMock()
        mock_strategy.execute.return_value = "Test response"
        mock_create_strategy.return_value = mock_strategy
        
        # Execute
        service = LLMService()
        response = service.executeLLM("Test prompt", provider="ollama")
        
        # Assert
        self.assertEqual(response, "Test response")
        mock_create_strategy.assert_called_once_with("ollama")
        mock_strategy.execute.assert_called_once_with("Test prompt")

    @patch('src.llm.llm_service.LLMStrategyFactory.create_strategy')
    def test_execute_llm_with_parameters(self, mock_create_strategy):
        """Test executeLLM method with additional parameters"""
        # Setup mock strategy
        mock_strategy = MagicMock()
        mock_strategy.execute.return_value = "Test response"
        mock_create_strategy.return_value = mock_strategy
        
        # Execute
        service = LLMService()
        response = service.executeLLM(
            "Test prompt", 
            provider="openai", 
            model="gpt-4", 
            temperature=0.5, 
            system_prompt="You are a helpful assistant"
        )
        
        # Assert
        self.assertEqual(response, "Test response")
        mock_create_strategy.assert_called_once_with("openai")
        mock_strategy.execute.assert_called_once_with(
            "Test prompt", 
            model="gpt-4", 
            temperature=0.5, 
            system_prompt="You are a helpful assistant"
        )


class TestLLMStrategyFactory(unittest.TestCase):

    @patch('src.llm.llm_service.OpenAIStrategy')
    def test_create_strategy_openai(self, mock_openai_strategy):
        """Test creating an OpenAI strategy"""
        # Setup mock
        mock_instance = MagicMock()
        mock_openai_strategy.return_value = mock_instance
        
        # Execute
        strategy = LLMStrategyFactory.create_strategy("openai")
        
        # Assert
        self.assertEqual(strategy, mock_instance)
        mock_openai_strategy.assert_called_once()

    @patch('src.llm.llm_service.OllamaStrategy')
    def test_create_strategy_ollama(self, mock_ollama_strategy):
        """Test creating an Ollama strategy"""
        # Setup mock
        mock_instance = MagicMock()
        mock_ollama_strategy.return_value = mock_instance
        
        # Execute
        strategy = LLMStrategyFactory.create_strategy("ollama")
        
        # Assert
        self.assertEqual(strategy, mock_instance)
        mock_ollama_strategy.assert_called_once()

    def test_create_strategy_invalid(self):
        """Test creating an invalid strategy raises ValueError"""
        with self.assertRaises(ValueError):
            LLMStrategyFactory.create_strategy("invalid_provider")


class TestOpenAIStrategy(unittest.TestCase):

    def setUp(self):
        # Configure system config mock
        self.config_mock = sys.modules['utils.system_parametrization'].SYSTEM_CONFIG
        self.config_mock.get.side_effect = self._mock_config_get

    def _mock_config_get(self, key, default=None):
        # Default configuration for testing
        config = {
            "rag.openai_api_key": "test_api_key",
            "rag.openai_base_url": "https://api.openai.com/v1",
            "rag.openai_model": "gpt-4o"
        }
        return config.get(key, default)

    @patch('openai.OpenAI')
    def test_execute(self, mock_openai):
        """Test OpenAI strategy execution"""
        # Setup mock client and response
        mock_client = MagicMock()
        mock_openai.return_value = mock_client
        
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "OpenAI response"
        mock_client.chat.completions.create.return_value = mock_response
        
        # Execute
        strategy = OpenAIStrategy()
        response = strategy.execute(
            "Test prompt", 
            model="gpt-4", 
            system_prompt="You are a helpful assistant", 
            temperature=0.5
        )
        
        # Assert
        self.assertEqual(response, "OpenAI response")
        mock_openai.assert_called_once_with(api_key="test_api_key")
        mock_client.chat.completions.create.assert_called_once_with(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant"},
                {"role": "user", "content": "Test prompt"}
            ],
            temperature=0.5
        )

    @patch('openai.OpenAI')
    def test_execute_with_defaults(self, mock_openai):
        """Test OpenAI strategy execution with default parameters"""
        # Setup mock client and response
        mock_client = MagicMock()
        mock_openai.return_value = mock_client
        
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "OpenAI response"
        mock_client.chat.completions.create.return_value = mock_response
        
        # Execute
        strategy = OpenAIStrategy()
        response = strategy.execute("Test prompt")
        
        # Assert
        self.assertEqual(response, "OpenAI response")
        mock_openai.assert_called_once_with(api_key="test_api_key")
        mock_client.chat.completions.create.assert_called_once_with(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": ""},
                {"role": "user", "content": "Test prompt"}
            ],
            temperature=0.7
        )


class TestOllamaStrategy(unittest.TestCase):

    def setUp(self):
        # Configure system config mock
        self.config_mock = sys.modules['utils.system_parametrization'].SYSTEM_CONFIG
        self.config_mock.get.side_effect = self._mock_config_get

    def _mock_config_get(self, key, default=None):
        # Default configuration for testing
        config = {
            "rag.ollama_url": "http://localhost:11434/api/chat",
            "rag.ollama_model": "phi4-mini"
        }
        return config.get(key, default)

    @patch('requests.post')
    def test_execute(self, mock_post):
        """Test Ollama strategy execution"""
        # Setup mock response
        mock_response = MagicMock()
        mock_response.text = '{"message": {"content": "Ollama response"}}'
        mock_post.return_value = mock_response
        
        # Execute
        strategy = OllamaStrategy()
        response = strategy.execute(
            "Test prompt", 
            model="llama3", 
            system_prompt="You are a helpful assistant", 
            temperature=0.5
        )
        
        # Assert
        self.assertEqual(response, "Ollama response")
        mock_post.assert_called_once_with(
            "http://localhost:11434/api/chat", 
            json={
                "model": "llama3",
                "messages": [
                    {"role": "system", "content": "You are a helpful assistant"},
                    {"role": "user", "content": "Test prompt"}
                ],
                "options": {
                    "temperature": 0.5
                }
            }
        )
        mock_response.raise_for_status.assert_called_once()

    @patch('requests.post')
    def test_execute_with_defaults(self, mock_post):
        """Test Ollama strategy execution with default parameters"""
        # Setup mock response
        mock_response = MagicMock()
        mock_response.text = '{"message": {"content": "Ollama response"}}'
        mock_post.return_value = mock_response
        
        # Execute
        strategy = OllamaStrategy()
        response = strategy.execute("Test prompt")
        
        # Assert
        self.assertEqual(response, "Ollama response")
        mock_post.assert_called_once_with(
            "http://localhost:11434/api/chat", 
            json={
                "model": "phi4-mini",
                "messages": [
                    {"role": "system", "content": ""},
                    {"role": "user", "content": "Test prompt"}
                ],
                "options": {
                    "temperature": 0.7
                }
            }
        )
        mock_response.raise_for_status.assert_called_once()


if __name__ == '__main__':
    unittest.main()