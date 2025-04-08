import unittest
import os
import tempfile
import shutil
from pathlib import Path
from unittest.mock import patch, MagicMock, mock_open

# Mock the logger before importing
import sys
sys.modules['utils.logger'] = MagicMock()
sys.modules['utils.logger'].Logger = MagicMock()

# Import the module after mocking dependencies
import src.utils.system_parametrization as system_parametrization
from src.utils.system_parametrization import SystemParametrization


class TestSystemParametrization(unittest.TestCase):

    def setUp(self):
        # Create a temporary directory for testing
        self.temp_dir = tempfile.mkdtemp()
        
        # Reset the singleton instance before each test
        SystemParametrization._instance = None
        SystemParametrization._initialized = False
        SystemParametrization._config = {}
        
        # Set up a test configuration
        self.test_config = {
            "rag": {
                "dsk_dir": "./dsk_test",
                "embeddings_dir": "./embeddings_test",
                "output_directory": "./output_test",
                "log_level": "INFO"
            },
            "test_key": "test_value"
        }

    def tearDown(self):
        # Clean up the temporary directory
        shutil.rmtree(self.temp_dir)

    @patch('src.utils.system_parametrization.yaml.safe_load')
    @patch('src.utils.system_parametrization.Path.exists')
    @patch('builtins.open', new_callable=mock_open)
    def test_init_and_load_config(self, mock_file, mock_exists, mock_safe_load):
        # Configure mocks
        mock_exists.return_value = True
        mock_safe_load.return_value = self.test_config
        
        # Create instance
        with patch.object(SystemParametrization, '_setup_directories'):
            config = SystemParametrization()
            
            # Verify file was opened
            mock_file.assert_called_once()
            
            # Verify yaml.safe_load was called
            mock_safe_load.assert_called_once()
            
            # Verify config was loaded
            self.assertEqual(config._config, self.test_config)

    def test_singleton_pattern(self):
        # Create first instance
        with patch.object(SystemParametrization, '_load_config'), \
             patch.object(SystemParametrization, '_setup_directories'):
            config1 = SystemParametrization()
            config1._config = {"test": "value"}
            
            # Create second instance
            config2 = SystemParametrization()
            
            # Verify both are the same object
            self.assertIs(config1, config2)
            self.assertEqual(config2._config, {"test": "value"})

    @patch.object(SystemParametrization, '_load_config')
    def test_setup_directories(self, _):
        # Create instance with mocked base_dir
        config = SystemParametrization()
        config._base_dir = Path(self.temp_dir)
        config._config = self.test_config
        
        # Call method
        config._setup_directories()
        
        # Verify directories were created
        directories = ["dsk_test", "embeddings_test", "output_test", "log"]
        for dir_name in directories:
            dir_path = Path(self.temp_dir) / dir_name
            self.assertTrue(dir_path.exists())
            
        # Verify absolute paths were stored in config
        self.assertTrue("_abs_dsk_dir" in config._config)
        self.assertTrue("_abs_embeddings_dir" in config._config)
        self.assertTrue("_abs_output_dir" in config._config)
        self.assertTrue("_abs_log_dir" in config._config)

    def test_get_method_simple_key(self):
        # Create instance
        with patch.object(SystemParametrization, '_load_config'), \
             patch.object(SystemParametrization, '_setup_directories'):
            config = SystemParametrization()
            config._config = {"simple_key": "simple_value"}
            
            # Test get with existing key
            value = config.get("simple_key")
            self.assertEqual(value, "simple_value")
            
            # Test get with non-existing key
            value = config.get("non_existing")
            self.assertIsNone(value)
            
            # Test get with default value
            value = config.get("non_existing", "default")
            self.assertEqual(value, "default")

    def test_get_method_nested_key(self):
        # Create instance
        with patch.object(SystemParametrization, '_load_config'), \
             patch.object(SystemParametrization, '_setup_directories'):
            config = SystemParametrization()
            config._config = {
                "parent": {
                    "child": {
                        "grandchild": "nested_value"
                    }
                }
            }
            
            # Test get with nested key
            value = config.get("parent.child.grandchild")
            self.assertEqual(value, "nested_value")
            
            # Test get with non-existing nested key
            value = config.get("parent.non_existing")
            self.assertIsNone(value)
            
            # Test get with invalid parent key
            value = config.get("non_existing.child")
            self.assertIsNone(value)

    def test_set_method(self):
        # Create instance
        with patch.object(SystemParametrization, '_load_config'), \
             patch.object(SystemParametrization, '_setup_directories'):
            config = SystemParametrization()
            config._config = {}
            
            # Test set with simple key
            config.set("simple_key", "simple_value")
            self.assertEqual(config._config["simple_key"], "simple_value")
            
            # Test set with nested key (existing parents)
            config._config = {"parent": {"child": {}}}
            config.set("parent.child.grandchild", "nested_value")
            self.assertEqual(config._config["parent"]["child"]["grandchild"], "nested_value")
            
            # Test set with nested key (non-existing parents)
            config._config = {}
            config.set("parent.child.grandchild", "nested_value")
            self.assertEqual(config._config["parent"]["child"]["grandchild"], "nested_value")

    def test_update_method(self):
        # Create instance
        with patch.object(SystemParametrization, '_load_config'), \
             patch.object(SystemParametrization, '_setup_directories'):
            config = SystemParametrization()
            config._config = {}
            
            # Test update with simple dict
            update_dict = {"key1": "value1", "key2": "value2"}
            config.update(update_dict)
            self.assertEqual(config._config["key1"], "value1")
            self.assertEqual(config._config["key2"], "value2")
            
            # Test update with nested dict
            update_dict = {
                "parent": {
                    "child1": "value1",
                    "child2": {
                        "grandchild": "value2"
                    }
                }
            }
            config._config = {}
            config.update(update_dict)
            self.assertEqual(config._config["parent"]["child1"], "value1")
            self.assertEqual(config._config["parent"]["child2"]["grandchild"], "value2")
            
            # Test update with prefix
            config._config = {}
            config.update({"child1": "value1"}, prefix="parent")
            self.assertEqual(config._config["parent"]["child1"], "value1")

    @patch('builtins.open', new_callable=mock_open)
    def test_save_config(self, mock_file):
        # Create instance
        with patch.object(SystemParametrization, '_load_config'), \
             patch.object(SystemParametrization, '_setup_directories'):
            config = SystemParametrization()
            config._config = self.test_config
            config._config_dir = Path(self.temp_dir)
            config._config_file = Path(self.temp_dir) / "config.yaml"
            
            # Call method
            config.save_config()
            
            # Verify file was opened for writing
            mock_file.assert_called_once_with(config._config_file, 'w', encoding='utf-8')
            # Verify yaml.dump was called via the file handle
            handle = mock_file()
            self.assertTrue(handle.write.called)

    def test_get_log_level(self):
        # Create instance
        with patch.object(SystemParametrization, '_load_config'), \
             patch.object(SystemParametrization, '_setup_directories'):
            config = SystemParametrization()
            
            # Test with different log levels
            log_levels = {
                "DEBUG": 10,  # logging.DEBUG
                "INFO": 20,   # logging.INFO
                "WARNING": 30,  # logging.WARNING
                "ERROR": 40,  # logging.ERROR
                "CRITICAL": 50  # logging.CRITICAL
            }
            
            for level_str, level_int in log_levels.items():
                config._config = {"rag": {"log_level": level_str}}
                self.assertEqual(config.get_log_level(), level_int)
            
            # Test with invalid log level
            config._config = {"rag": {"log_level": "INVALID"}}
            self.assertEqual(config.get_log_level(), 20)  # logging.INFO is default
            
            # Test with missing log level
            config._config = {}
            self.assertEqual(config.get_log_level(), 20)  # logging.INFO is default

    def test_get_abs_path(self):
        # Create instance
        with patch.object(SystemParametrization, '_load_config'), \
             patch.object(SystemParametrization, '_setup_directories'):
            config = SystemParametrization()
            config._base_dir = Path(self.temp_dir)
            
            # Test with absolute path
            abs_path = "/absolute/path"
            config._config = {"path_key": abs_path}
            self.assertEqual(config.get_abs_path("path_key"), Path(abs_path))
            
            # Test with relative path
            rel_path = "relative/path"
            config._config = {"path_key": rel_path}
            self.assertEqual(config.get_abs_path("path_key"), Path(self.temp_dir) / rel_path)
            
            # Test with None path
            config._config = {}
            self.assertIsNone(config.get_abs_path("path_key"))

    def test_properties(self):
        # Create instance
        with patch.object(SystemParametrization, '_load_config'), \
             patch.object(SystemParametrization, '_setup_directories'):
            config = SystemParametrization()
            config._base_dir = Path(self.temp_dir)
            config._config_file = Path(self.temp_dir) / "config.yaml"
            config._config = self.test_config
            
            # Test all_params property
            all_params = config.all_params
            self.assertEqual(all_params, self.test_config)
            # Verify it's a copy
            all_params["new_key"] = "new_value"
            self.assertNotIn("new_key", config._config)
            
            # Test base_dir property
            self.assertEqual(config.base_dir, Path(self.temp_dir))
            
            # Test config_file property
            self.assertEqual(config.config_file, Path(self.temp_dir) / "config.yaml")

    def test_get_system_config(self):
        # Test function returns singleton instance
        with patch.object(SystemParametrization, '_load_config'), \
             patch.object(SystemParametrization, '_setup_directories'):
            # Replace the singleton with our test instance
            system_parametrization.SYSTEM_CONFIG = SystemParametrization()
            
            config = system_parametrization.get_system_config()
            self.assertIs(config, system_parametrization.SYSTEM_CONFIG)


if __name__ == '__main__':
    unittest.main()