from skimage.color import rgb2hsv
from processing.base_processor import BaseProcessor

class HSVProcessor(BaseProcessor):
    """!
    @brief Class that converts RGB image to HSV color space.
    
    This class uses the rgb2hsv function from the scikit-image library
    to convert an image from RGB color space to HSV (Hue, Saturation, Value)
    color space.
    */
    """

    def process(self, image):
        """!
        @brief Converts RGB image to HSV format.
        
        @param image NumPy array in RGB format
        @return NumPy array in HSV format
        @exception ValueError In case of invalid input image
        */
        """
        return rgb2hsv(image)