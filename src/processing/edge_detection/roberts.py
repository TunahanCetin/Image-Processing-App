from skimage.filters import roberts
from processing.base_processor import BaseProcessor
from skimage.color import rgb2gray

class RobertsEdgeDetectionProcessor(BaseProcessor):
    """!
    @brief Class that performs Roberts edge detection.
    
    This class implements the Roberts cross operator, one of the earliest edge 
    detection algorithms. It highlights regions of high spatial frequency which 
    often correspond to edges by calculating the sum of the squares of the 
    differences between diagonally adjacent pixels.
    */
    """

    def process(self, image):
        """!
        @brief Applies Roberts cross edge detection algorithm to an image.
        
        If the input image is in RGB format, it's automatically converted to grayscale
        before applying the edge detection.
        
        @param image NumPy array in RGB or grayscale format
        @return NumPy array with detected edges
        @exception ValueError In case of invalid input image
        */
        """
        if image.ndim == 3:
            image = rgb2gray(image)
        edges = roberts(image)
        return edges