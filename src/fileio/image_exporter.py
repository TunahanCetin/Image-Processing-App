"""
@file image_exporter.py
@brief Handles safe image exporting to different formats.

This module provides functionality to safely export images to disk in various formats.
It automatically handles type conversion for different image types (float, boolean, integer)
and ensures proper scaling of values to ensure compatibility with standard image formats.
"""

from skimage import io, img_as_ubyte
import numpy as np
import os

class ImageExporter:
    """
    @class ImageExporter
    @brief Safely export images to disk ensuring correct data format.
    
    This class provides static methods for saving images with automatic
    data type conversion and range normalization to ensure compatibility
    with standard image formats like PNG and JPEG.
    """

    @staticmethod
    def save_image(image, file_path):
        """
        @brief Save the given image safely to the specified file path.
        
        Automatically converts images to uint8 if necessary (float, bool, etc.).
        The function handles various input types:
        - Boolean arrays are converted to 0/255 values
        - Float arrays are clipped to [0,1] range and converted to 0-255 scale
        - Integer arrays outside 0-255 range are rescaled
        
        @param image Numpy image array to be saved
        @param file_path Target file path where the image will be saved
        @throws ValueError If no image is provided or if conversion fails
        """
        if image is None:
            raise ValueError("No image to save.")

        # Handle boolean images
        if image.dtype == bool:
            image = (image.astype(np.uint8)) * 255

        # Handle float images (0.0 - 1.0) or potentially out-of-bounds values
        elif np.issubdtype(image.dtype, np.floating):
            image = np.clip(image, 0, 1)
            image = img_as_ubyte(image)

        # Handle integer images (ensure within 0-255 for uint8 compatibility)
        elif np.issubdtype(image.dtype, np.integer):
            if image.max() > 255:
                image = (image / image.max() * 255).astype(np.uint8)
            else:
                image = image.astype(np.uint8)

        # Finally, save
        io.imsave(file_path, image)

    @staticmethod
    def export_as(image, current_file_path, export_format):
        """
        @brief Export the current image to a different format (.jpg or .png).
        
        This method creates a new file with the specified format while keeping
        the same base filename. For example, 'image.jpg' exported as '.png'
        would become 'image.png'.
        
        @param image Numpy image array to be exported
        @param current_file_path Current file path to determine export path
        @param export_format New format to export (e.g., '.jpg' or '.png')
        @return The export path where the image was saved
        @throws ValueError If the export format is invalid
        """
        if not export_format.startswith('.'):
            raise ValueError("Invalid format extension.")

        base, _ = os.path.splitext(current_file_path)
        export_path = base + export_format
        ImageExporter.save_image(image, export_path)
        return export_path