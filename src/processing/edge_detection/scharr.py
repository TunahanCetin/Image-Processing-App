from skimage.filters import scharr
from processing.base_processor import BaseProcessor
from skimage.color import rgb2gray

class ScharrEdgeDetectionProcessor(BaseProcessor):
    """!
    @brief Class that performs Scharr edge detection.
    
    This class uses the Scharr operator which is a more accurate version of the 
    Sobel operator. It improves rotational symmetry and provides more accuracy 
    when detecting edges at different angles.
    */
    """

    def process(self, image):
        """!
        @brief Applies Scharr edge detection algorithm to an image.
        
        If the input image is in RGB format, it's automatically converted to grayscale
        before applying the edge detection.
        
        @param image NumPy array in RGB or grayscale format
        @return NumPy array with detected edges
        @exception ValueError In case of invalid input image
        */
        """
        if image.ndim == 3:
            image = rgb2gray(image)
        edges = scharr(image)
        return edges