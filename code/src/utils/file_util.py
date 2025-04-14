from PIL import Image, ImageDraw, ImageFont
from src.utils.logger import Logger
from openpyxl import load_workbook
from openpyxl.utils.dataframe import dataframe_to_rows

import os
import pandas as pd


class FileUtil:
    """
    A utility class for file operations, including saving files and generating error images.
    """

    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(FileUtil, cls).__new__(cls)
        return cls._instance

    def __init__(self, *args, **kwargs):
        """
        Initializes the FileUtil class.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        if not hasattr(self, "initialized"):
            self.LOGGER = Logger
            self.initialized = True

    def save_to_file(self, filename, output_directory, content):
        """
        Saves the given content to a file in the specified output directory.

        Args:
            filename (str): The name of the file to save.
            output_directory (str): The directory where the file will be saved.
            content (str): The content to write to the file.

        Returns:
            bool: True if the file was saved successfully, False otherwise.

        Raises:
            IOError: If the file cannot be saved, an exception is raised with details.

        Notes:
            - The file is saved with UTF-8 encoding.
            - Logs a success message if the file is saved successfully.
            - Logs a critical error and raises an exception if the file cannot be saved.
        """
        success = True

        output_file = os.path.join(output_directory, filename)

        try:
            with open(output_file, 'w', encoding='utf-8') as file:
                file.write(content)

            self.LOGGER.info(f"File saved successfully at: {output_file}")

        except Exception as e:
            success = False
            self.LOGGER.critical(f"Failed to save file at {output_file}: {e}")
            raise IOError(f"Failed to save file at {output_file}: {e}") from e

        return success

    def save_to_file_with_error_handling(self, filename, output_directory, content):
        """
        Saves the given content to a file in the specified output directory with error handling.

        Args:
            filename (str): The name of the file to save.
            output_directory (str): The directory where the file will be saved.
            content (str): The content to write to the file.

        Notes:
            - If the file cannot be saved, the function handles errors based on the file extension:
                - For `.png` files, it generates an error image using `_generate_png_file_error`.
                - For `.xlsx` files, it generates an error Excel file using `_generate_excel_file_error`.
                - For other file types, it logs a critical error.
            - Logs a success message if the file is saved successfully.
            - Logs a critical error if the file cannot be saved.
        """
        success = True
        output_file = os.path.join(output_directory, filename)

        try:
            if filename.endswith('.txt') and isinstance(content, str):
                mode = 'w'
                encoding = 'utf-8'
            elif filename.endswith(('.png', '.xlsx')) and isinstance(content, bytes):
                mode = 'wb'
                encoding = None
            else:
                raise ValueError("Unsupported file type or content type mismatch.")

            with open(output_file, mode, encoding=encoding) as file:
                file.write(content)

            self.LOGGER.info(f"File saved successfully at: {output_file}")

        except Exception as e:
            success = False
            file_extension = os.path.splitext(filename)[1]

            self.LOGGER.critical(f"Failed to save file at {output_file}: {e}")

            if file_extension == ".png":
                self._generate_png_file_error(filename, output_directory, output_file, e)
            elif file_extension == ".xlsx":
                self._generate_excel_file_error(output_directory, filename, e)
            else:
                self.LOGGER.critical(f"Failed to save error file at {output_file}: {e}")

        return success

    def _generate_png_file_error(self, filename, output_directory, output_file, e):
        """
        Generates an error image for `.png` files when saving fails.

        Args:
            filename (str): The name of the original file that failed to save.
            output_directory (str): The directory where the error image will be saved.
            output_file (str): The full path of the original file that failed to save.
            e (Exception): The exception that occurred.

        Notes:
            - The error image is a 400x200 white image with the text "Error: Diagram generation failed" in red.
            - The error image is saved with the same name as the original file, or with `_error.png` appended if the original file does not end with `.png`.
            - Logs a critical error if the error image cannot be saved.
            - Logs a success message if the error image is saved successfully.
        """
        try:
            self.LOGGER.critical(f"Failed to save file at {output_file}: {e}")

            error_output_file = os.path.join(
                    output_directory,
                    f"{filename if filename.endswith('.png') else f'{filename}_error.png'}"
                )
            error_image = Image.new("RGB", (400, 200), color=(255, 255, 255))
            draw = ImageDraw.Draw(error_image)
            font = ImageFont.load_default()
            draw.text((10, 90), "Error: Diagram generation failed", fill=(255, 0, 0), font=font)

            error_image.save(error_output_file)
            self.LOGGER.info(f"Error image saved:{error_output_file}")

        except Exception as e:
            self.LOGGER.critical(f"Failed to save error image at {output_file}: {e}")

    def generate_png_empty_file(self, filename, output_directory, output_file):
        try:

            empty_output_file = os.path.join(
                    output_directory,
                    f"{filename if filename.endswith('.png') else f'{filename}_empty.png'}"
                )
            empty_image = Image.new("RGB", (400, 200), color=(255, 255, 255))
            draw = ImageDraw.Draw(empty_image)
            font = ImageFont.load_default()
            draw.text((10, 90), "No diagram detected", fill=(255, 0, 0), font=font)

            empty_image.save(empty_output_file)
            self.LOGGER.info(f"No detected image saved:{empty_output_file}")

        except Exception as e:
            self.LOGGER.critical(f"Failed to save empty image at {output_file}: {e}")

    def _generate_excel_file_error(self, output_directory, filename, e):
        """
        Generates an Excel file with two sheets ("Components" and "Relations") containing an error message.

        Args:
            output_directory (str): The directory where the error Excel file will be saved.
            filename (str): The name of the Excel file to save.
            e (Exception): The exception that occurred.

        Notes:
            - The Excel file will contain two sheets:
                - "Components": With the text "A processing error occurred".
                - "Relations": With the text "A processing error occurred".
            - Logs a critical error if the file cannot be saved.
        """
        try:
            # LOGGER.critical(f"Failed to process Excel file {filename}: {e}")

            error_message = "A processing error occurred"

            # Create DataFrames for the error message
            df_components = pd.DataFrame([{"Error": error_message}])
            df_relations = pd.DataFrame([{"Error": error_message}])

            error_output_file = os.path.join(output_directory, filename)

            # Write the Excel file with two sheets
            with pd.ExcelWriter(error_output_file, engine="xlsxwriter") as writer:
                df_components.to_excel(writer, sheet_name="Components", index=False)
                df_relations.to_excel(writer, sheet_name="Relations", index=False)

            self.LOGGER.info(f"Error Excel file saved: {error_output_file}")

        except Exception as inner_e:
            self.LOGGER.critical(f"Failed to save error Excel file at {filename}: {inner_e}")

    def generate_excel_empty_file(self, output_directory, filename):
        try:

            empty_message = "Not identified elements"

            # Create DataFrames for the error message
            df_components = pd.DataFrame([{"Error": empty_message}])

            empty_output_file = os.path.join(output_directory, filename)

            with pd.ExcelWriter(empty_output_file, engine="xlsxwriter") as writer:
                df_components.to_excel(writer, sheet_name="Components", index=False)

            self.LOGGER.info(f"Empty Excel file saved: {empty_output_file}")

        except Exception as inner_e:
            self.LOGGER.critical(f"Failed to save empty Excel file at {filename}: {inner_e}")

    def generate_data_collection_instrument(self, filename, output_directory, content):
        success = True
        output_file = os.path.join(output_directory, filename)

        try:

            with open(output_file, 'wb', encoding=None) as file:
                file.write(content)

            self.LOGGER.info(f"File saved successfully at: {output_file}")

        except Exception as e:
            success = False
            self.LOGGER.critical(f"Failed to save data collection instrument at {output_file}: {e}")

        return success

