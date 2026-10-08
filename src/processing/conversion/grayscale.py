from skimage.color import rgb2gray
from processing.base_processor import BaseProcessor

class GrayscaleProcessor(BaseProcessor):
    """!
    @brief Class that converts RGB image to grayscale.
    
    This class uses the rgb2gray function from the scikit-image library
    to convert a color image to a grayscale image.
    */
    """

    def process(self, image):
        """!
        @brief Converts RGB image to grayscale.
        
        @param image NumPy array in RGB format
        @return Grayscale NumPy array
        @exception ValueError In case of invalid input image
        */
        """
        return rgb2gray(image)