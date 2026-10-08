"""!
@file morphological_snakes.py
@brief Morphological Snakes segmentation implementation.

This file contains the implementation of segmentation using morphological snakes,
a technique that combines morphological operations with active contour models.
*/
"""

from skimage.segmentation import morphological_chan_vese, morphological_geodesic_active_contour
from skimage.filters import gaussian
from skimage.color import rgb2gray
import numpy as np
from processing.base_processor import BaseProcessor

class MorphologicalSnakesProcessor(BaseProcessor):
    """!
    @brief Class that applies Morphological Snakes segmentation to images.
    
    This processor implements segmentation using morphological snakes, which is 
    a technique that combines the Chan-Vese active contour model with morphological
    operations. It's efficient for segmenting objects with complex boundaries and
    is less sensitive to initialization than traditional active contours.
    */
    """
    
    def process(self, image):
        """!
        @brief Applies Morphological Snakes segmentation to an image.
        
        The method converts RGB images to grayscale, initializes a circular contour
        in the center of the image, and evolves it using morphological operations.
        The result is either a binary mask or a visualization with highlighted contours.
        
        @param image NumPy array in RGB or grayscale format
        @return Segmented image with highlighted contours (RGB) or binary mask (grayscale)
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
                gray_image = image_copy.astype(float)
                if gray_image.max() > 1.0:
                    gray_image = gray_image / 255.0
            
            # Ensure gray_image is normalized to [0,1]
            if gray_image.max() > 1.0:
                gray_image = gray_image / 255.0
                
            # Prepare initial contour - smaller and centered
            height, width = gray_image.shape
            
            # Create a circle in the middle
            init_ls = np.zeros(gray_image.shape, dtype=np.int8)
            center_y, center_x = height // 2, width // 2
            radius = min(height, width) // 6  # Smaller radius
            Y, X = np.ogrid[:height, :width]
            dist_from_center = np.sqrt((Y - center_y)**2 + (X - center_x)**2)
            init_ls[dist_from_center <= radius] = 1
            
            # Smooth the image to reduce noise
            gimage = gaussian(gray_image, sigma=2)
            
            # Apply morphological snake algorithm
            segmentation = morphological_chan_vese(
                gimage, 
                num_iter=100,
                init_level_set=init_ls,
                smoothing=1
            )
            
            # Create the output image
            if image_copy.ndim == 3:
                # Create a colored visualization
                result = np.zeros_like(image_copy)
                
                # Original image with reduced opacity in background
                result = image_copy.copy() * 0.7
                
                # Create a better visualization by overlaying the segmentation
                # Contour in a bright color
                contour = np.zeros_like(result)
                
                # Find contour pixels (edges of segmentation)
                from scipy import ndimage
                edges = ndimage.binary_dilation(segmentation) ^ segmentation
                
                # Highlight the contour
                contour[edges, 0] = 255  # Red channel
                contour[edges, 1] = 255  # Green channel
                contour[edges, 2] = 0    # No blue -> yellow contour
                
                # Combine with alpha blending
                mask = contour > 0
                result[mask] = contour[mask]
                
                return result
            else:
                # For grayscale, return binary mask
                return segmentation.astype(np.uint8) * 255
                
        except Exception as e:
            import traceback
            traceback.print_exc()
            raise RuntimeError(f"Error applying Morphological Snakes segmentation: {str(e)}")