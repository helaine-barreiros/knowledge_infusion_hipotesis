import unittest
from unittest.mock import patch, MagicMock, call
import logging
import os
import sys
import tempfile
import shutil
from pathlib import Path

# Mock system_parametrization before import
sys.modules['src.utils.system_parametrization'] = MagicMock()
sys.modules['src.utils.system_parametrization'].SYSTEM_CONFIG = MagicMock()
sys.modules['src.utils.system_parametrization'].SYSTEM_CONFIG.get_log_level.return_value = logging.INFO
sys.modules['src.utils.system_parametrization'].SYSTEM_CONFIG.base_dir = '/tmp'

# Now we can import the modules
from src.utils.logger import Logger, LoggerSingleton


class TestLogger(unittest.TestCase):

    def setUp(self):
        # Reset the singleton instance before each test
        LoggerSingleton._instance = None
        
        # Create a temporary directory for logs
        self.temp_dir = tempfile.mkdtemp()
        sys.modules['src.utils.system_parametrization'].SYSTEM_CONFIG.base_dir = self.temp_dir
        
        # Set up a temporary stream for capturing log output
        self.log_output = MagicMock()
        
        # Mock colorlog
        self.mock_colorlog_handler = MagicMock()
        self.mock_file_handler = MagicMock()

    def tearDown(self):
        # Clean up the temporary directory
        shutil.rmtree(self.temp_dir)

    @patch('src.utils.logger.colorlog.getLogger')
    @patch('src.utils.logger.colorlog.StreamHandler')
    @patch('src.utils.logger.RotatingFileHandler')
    def test_logger_singleton_creation(self, mock_rotating_handler, mock_stream_handler, mock_get_logger):
        # Set up mocks
        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger
        mock_stream_handler.return_value = self.mock_colorlog_handler
        mock_rotating_handler.return_value = self.mock_file_handler
        
        # Get logger instance
        logger = LoggerSingleton.get_instance()
        
        # Verify logger was created with correct level
        self.assertEqual(logger, mock_logger)
        mock_logger.setLevel.assert_called_once_with(logging.INFO)
        
        # Verify handlers were added
        mock_logger.addHandler.assert_any_call(self.mock_colorlog_handler)
        mock_logger.addHandler.assert_any_call(self.mock_file_handler)
        
        # Verify log directory was created
        log_dir = Path(self.temp_dir) / "log"
        self.assertTrue(log_dir.exists())

    @patch('src.utils.logger.LoggerSingleton.get_instance')
    def test_logger_static_methods(self, mock_get_instance):
        # Set up mock
        mock_logger = MagicMock()
        mock_get_instance.return_value = mock_logger
        
        # Test debug method
        Logger.debug("Debug message")
        mock_logger.debug.assert_called_once_with("Debug message")
        
        # Test info method
        Logger.info("Info message")
        mock_logger.info.assert_called_once_with("Info message")
        
        # Test warning method
        Logger.warning("Warning message")
        mock_logger.warning.assert_called_once_with("Warning message")
        
        # Test error method
        Logger.error("Error message")
        mock_logger.error.assert_called_once_with("Error message")
        
        # Test critical method
        Logger.critical("Critical message")
        mock_logger.critical.assert_called_once_with("Critical message")
        
        # Test set_level method
        Logger.set_level(logging.DEBUG)
        mock_logger.setLevel.assert_called_once_with(logging.DEBUG)
        
        # Test get_logger method
        returned_logger = Logger.get_logger()
        self.assertEqual(returned_logger, mock_logger)

    def test_logger_singleton_reuse(self):
        # Reset singleton instance
        LoggerSingleton._instance = None
        
        # First call creates the instance
        logger1 = LoggerSingleton.get_instance()
        
        # Create a spy to track calls to _create_logger
        original_create_logger = LoggerSingleton._create_logger
        create_logger_called = [0]
        
        def spy_create_logger(*args, **kwargs):
            create_logger_called[0] += 1
            return original_create_logger(*args, **kwargs)
        
        LoggerSingleton._create_logger = classmethod(spy_create_logger)
        
        # Second call should reuse the instance
        logger2 = LoggerSingleton.get_instance()
        
        # Verify the same instance is returned
        self.assertIs(logger1, logger2)
        
        # _create_logger should not be called again
        self.assertEqual(create_logger_called[0], 0)


if __name__ == '__main__':
    unittest.main()