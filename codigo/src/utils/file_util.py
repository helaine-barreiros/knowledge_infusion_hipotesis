from PIL import Image, ImageDraw, ImageFont
from src.utils.logger import Logger

import os

LOGGER = Logger


def save_to_file(filename, output_directory, content):
    success = True

    output_file = os.path.join(output_directory, filename)

    try:
        with open(output_file, 'w', encoding='utf-8') as file:
            file.write(content)

        LOGGER.info(f"File saved successfully at: {output_file}")

    except Exception as e:
        success = False
        LOGGER.critical(f"Failed to save file at {output_file}: {e}")
        raise IOError(f"Failed to save file at {output_file}: {e}") from e

    return success


def save_to_file_with_error_handling(filename, output_directory, content):

    output_file = os.path.join(output_directory, filename)

    try:
        with open(output_file, 'w', encoding='utf-8') as file:
            file.write(content)

        LOGGER.info(f"File saved successfully at: {output_file}")

    except Exception as e:
        _generate_file_error(filename, output_directory, output_file, e)


def _generate_file_error(filename, output_directory, output_file, e):
    try:
        LOGGER.critical(f"Failed to save file at {output_file}: {e}")

        error_output_file = os.path.join(
                output_directory,
                f"{filename if filename.endswith('.png') else f'{filename}_error.png'}"
            )
        error_image = Image.new("RGB", (400, 200), color=(255, 255, 255))
        draw = ImageDraw.Draw(error_image)
        font = ImageFont.load_default()
        draw.text((10, 90), "Error: Diagram generation failed", fill=(255, 0, 0), font=font)

        error_image.save(error_output_file)
        LOGGER.info(f"Error image saved:{error_output_file}")

    except Exception as e:
        LOGGER.critical(f"Failed to save error image at {output_file}: {e}")
