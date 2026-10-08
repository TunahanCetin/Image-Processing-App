"""
@file image_loader.py
@brief Handles loading of image files from disk.

This module provides functionality for safely loading images from disk
with validation of file existence and format compatibility.
"""

from skimage import io
import os

class ImageLoader:
    """
    @class ImageLoader
    @brief Loads images from disk with validation.
    
    This class provides static methods for safely loading image files
    with proper validation of file existence and format support.
    Currently supports loading JPG and PNG image formats.
    """
    
    @staticmethod
    def load_image(file_path):
        """
        @brief Load an image from the specified file path.
        
        Validates that the file exists and has a supported format
        before attempting to load it.
        
        @param file_path Path to the image file to be loaded
        @return The loaded image as a numpy array
        @throws FileNotFoundError If the specified file does not exist
        @throws ValueError If the file has an unsupported format
        """
        if not os.path.isfile(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        if not file_path.lower().endswith(('.jpg', '.png')):
            raise ValueError("Only .jpg and .png files are supported.")

        image = io.imread(file_path)
        return image