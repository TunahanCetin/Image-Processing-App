"""!
@file otsu.py
@brief Multi-Otsu Thresholding implementation for segmentation.

This file contains the implementation of multi-level Otsu thresholding,
a technique that automatically determines optimal thresholds to segment
an image into multiple classes.
*/
"""

from skimage.filters import threshold_multiotsu
from skimage.color import rgb2gray
import numpy as np
from processing.base_processor import BaseProcessor

class OtsuSegmentationProcessor(BaseProcessor):
    """!
    @brief Class that applies Multi-Otsu Thresholding for image segmentation.
    
    This processor implements Otsu's method, which is a clustering-based image
    thresholding technique that automatically calculates optimal thresholds
    by maximizing the between-class variance. The multi-level version segments
    the image into multiple classes (typically 3).
    */
    """
    
    def process(self, image):
        """!
        @brief Applies Multi-Otsu Thresholding segmentation to an image.
        
        The method converts RGB images to grayscale, calculates optimal thresholds
        using Otsu's method, and creates a segmented image with distinct regions.
        For RGB images, a colored visualization is generated.
        
        @param image NumPy array in RGB or grayscale format
        @return Segmented image with colored regions (RGB) or grayscale regions
        @exception RuntimeError If segmentation process fails
        */
        """
        try:
            # Make a copy to avoid modifying original
            image_copy = image.copy()
            
            # Convert to grayscale if needed
            if image_copy.ndim == 3:
                gray_image = rgb2gray(image_copy)
            else:
                gray_image = image_copy
            
            # Ensure image is in right format and range
            gray_image = (gray_image * 255).astype(np.uint8) if gray_image.max() <= 1.0 else gray_image.astype(np.uint8)
                
            # Apply multi-otsu thresholding (for 3 classes)
            # Handle potential failure by trying with 2 classes if 3 fails
            try:
                thresholds = threshold_multiotsu(gray_image, classes=3)
            except:
                print("Falling back to 2 classes for Otsu")
                thresholds = threshold_multiotsu(gray_image, classes=2)
            
            # Create the segmentation based on thresholds
            regions = np.digitize(gray_image, bins=thresholds)
            
            # If original was RGB, create a colored output
            if image_copy.ndim == 3:
                # Create a colored visualization
                colored_regions = np.zeros_like(image_copy)
                
                # Use different colors for each region
                num_regions = len(thresholds) + 1
                colors = [
                    [0, 0, 128],  # Dark blue
                    [0, 128, 0],  # Green
                    [128, 0, 0]   # Red
                ]
                
                # If we have fewer regions than colors, adjust
                colors = colors[:num_regions]
                
                for i in range(num_regions):
                    mask = regions == i
                    if i < len(colors):
                        colored_regions[mask] = colors[i]
                
                return colored_regions
            else:
                # Normalize to 0-255 for visualization
                segmented_image = (regions * (255 // (len(thresholds) + 1))).astype(np.uint8)
                return segmented_image
                
        except Exception as e:
            import traceback
            traceback.print_exc()
            raise RuntimeError(f"Error applying Otsu segmentation: {str(e)}")