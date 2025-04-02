from unittest.mock import patch, MagicMock
from src.utils.file_util import save_to_file_with_error_handling, _generate_file_error

import unittest
import os
import shutil
import tempfile

import sys
sys.modules['src.utils.logger'] = MagicMock()
sys.modules['src.utils.logger'].Logger = MagicMock()


class TestSaveToFileWithErrorHandling(unittest.TestCase):

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()

        sys.modules['src.utils.logger'].Logger.info.reset_mock()
        sys.modules['src.utils.logger'].Logger.critical.reset_mock()

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_save_to_file_with_error_handling_success(self):
        """Test successful file saving with error handling."""
        filename = "test_file.txt"
        content = "This is test content"

        save_to_file_with_error_handling(filename, self.test_dir, content)

        file_path = os.path.join(self.test_dir, filename)
        self.assertTrue(os.path.exists(file_path))

        with open(file_path, 'r', encoding='utf-8') as file:
            saved_content = file.read()
        self.assertEqual(saved_content, content)

        sys.modules['src.utils.logger'].Logger.info.assert_called_once()

    @patch('builtins.open')
    @patch('src.utils.file_util._generate_file_error')
    def test_save_to_file_with_error_handling_failure(self, mock_generate_error, mock_open):
        """Test handling of file saving errors."""
        filename = "test_file.txt"
        content = "This is test content"

        error = IOError("Failed to save file")
        mock_open.side_effect = error

        save_to_file_with_error_handling(filename, self.test_dir, content)

        output_file = os.path.join(self.test_dir, filename)
        mock_generate_error.assert_called_once_with(filename, self.test_dir, output_file, error)

    @patch('src.utils.file_util.Image.new')
    @patch('src.utils.file_util.ImageDraw.Draw')
    @patch('src.utils.file_util.ImageFont.load_default')
    def test_generate_file_error(self, mock_font, mock_draw, mock_new):
        """Test error image generation."""
        filename = "test_file.txt"
        output_file = os.path.join(self.test_dir, filename)
        error = Exception("Test error")

        mock_image = MagicMock()
        mock_new.return_value = mock_image
        mock_draw_obj = MagicMock()
        mock_draw.return_value = mock_draw_obj
        mock_font_obj = MagicMock()
        mock_font.return_value = mock_font_obj

        _generate_file_error(filename, self.test_dir, output_file, error)

        sys.modules['src.utils.logger'].Logger.critical.assert_called_once()

        mock_new.assert_called_once_with("RGB", (400, 200), color=(255, 255, 255))
        mock_draw.assert_called_once_with(mock_image)
        mock_draw_obj.text.assert_called_once()
        mock_image.save.assert_called_once()
        sys.modules['src.utils.logger'].Logger.info.assert_called_once()

    @patch('src.utils.file_util.Image.new')
    def test_generate_file_error_with_error(self, mock_new):
        """Test error handling during error image generation."""
        filename = "test_file.txt"
        output_file = os.path.join(self.test_dir, filename)
        error = Exception("Test error")

        sys.modules['src.utils.logger'].Logger.critical.reset_mock()

        mock_new.side_effect = Exception("Error creating image")

        _generate_file_error(filename, self.test_dir, output_file, error)

        self.assertEqual(sys.modules['src.utils.logger'].Logger.critical.call_count, 2)


if __name__ == '__main__':
    unittest.main()