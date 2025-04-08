from src.utils.file_util import FileUtil
from unittest.mock import patch, MagicMock

import unittest
import os
import shutil
import sys


sys.modules['src.utils.logger'] = MagicMock()
sys.modules['src.utils.logger'].Logger = MagicMock()

TEST_DSK_DIR = "tests/utils/file_resources"


class TestSaveToFile(unittest.TestCase):

    def setUp(self):
        self.test_dir = "tests/utils/file_resources"
        self.file_util = FileUtil()

    def test_save_to_file_success(self):
        """Test saving content to a file successfully."""
        filename = "test_save_file.txt"
        content = "This is test content"
        file_path = os.path.join(self.test_dir, filename)

        try:
            result = self.file_util.save_to_file(filename, self.test_dir, content)
            self.assertTrue(result)

            self.assertTrue(os.path.exists(file_path))

            with open(file_path, 'r', encoding='utf-8') as file:
                saved_content = file.read()
            self.assertEqual(saved_content, content)
        finally:
            if os.path.exists(file_path):
                os.remove(file_path)

    def test_save_to_file_nonexistent_directory(self):
        """Test saving to a nonexistent directory raises an exception."""
        filename = "test_file_nexistent.txt"
        content = "This is test content"
        nonexistent_dir = os.path.join(self.test_dir, "nonexistent_dir")

        with self.assertRaises(IOError):
            self.file_util.save_to_file(filename, nonexistent_dir, content)

    @patch('builtins.open')
    def test_save_to_file_permission_denied(self, mock_open):
        """Test handling permission denied error when saving a file."""
        filename = "test_file.txt"
        content = "This is test content"

        mock_open.side_effect = PermissionError("Permission denied")

        with self.assertRaises(IOError):
            self.file_util.save_to_file(filename, self.test_dir, content)


if __name__ == '__main__':
    unittest.main()
