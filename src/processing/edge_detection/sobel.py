from skimage.filters import sobel
from processing.base_processor import BaseProcessor
from skimage.color import rgb2gray

class SobelEdgeDetectionProcessor(BaseProcessor):
    """!
    @brief Class that performs Sobel edge detection.
    
    This class implements the Sobel operator which is used in image processing 
    for edge detection. It creates an image emphasizing edges by calculating 
    the gradient of image intensity at each pixel.
    */
    """

    def process(self, image):
        """!
        @brief Applies Sobel edge detection algorithm to an image.
        
        If the input image is in RGB format, it's automatically converted to grayscale
        before applying the edge detection.
        
        @param image NumPy array in RGB or grayscale format
        @return NumPy array with detected edges
        @exception ValueError In case of invalid input image
        */
        """
        if image.ndim == 3:
            image = rgb2gray(image)
        edges = sobel(image)
        return edges