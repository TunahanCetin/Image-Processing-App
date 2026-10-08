from skimage.filters import prewitt
from processing.base_processor import BaseProcessor
from skimage.color import rgb2gray

class PrewittEdgeDetectionProcessor(BaseProcessor):
    """!
    @brief Class that performs Prewitt edge detection.
    
    This class uses the Prewitt operator from scikit-image to detect edges in images.
    The Prewitt operator calculates the gradient of the image intensity at each pixel,
    giving the direction of the largest possible increase from light to dark and the
    rate of change in that direction.
    */
    """

    def process(self, image):
        """!
        @brief Applies Prewitt edge detection algorithm to an image.
        
        If the input image is in RGB format, it's automatically converted to grayscale
        before applying the edge detection.
        
        @param image NumPy array in RGB or grayscale format
        @return NumPy array with detected edges
        @exception ValueError In case of invalid input image
        */
        """
        if image.ndim == 3:
            image = rgb2gray(image)
        edges = prewitt(image)
        return edges