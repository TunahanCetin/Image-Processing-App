from skimage.segmentation import chan_vese
from processing.base_processor import BaseProcessor
from skimage.color import rgb2gray

class ChanVeseSegmentationProcessor(BaseProcessor):
    """!
    @brief Class that applies Chan-Vese segmentation algorithm.
    
    This class implements the Chan-Vese segmentation algorithm, an active contour model
    that segments an image without relying on edges. It's particularly useful for
    segmenting objects with smooth or even noisy boundaries.
    */
    """

    def process(self, image):
        """!
        @brief Applies Chan-Vese segmentation to an image.
        
        If the input image is in RGB format, it's automatically converted to grayscale
        before applying the segmentation.
        
        @param image NumPy array in RGB or grayscale format
        @return Binary mask (NumPy array) representing the segmentation
        @exception ValueError In case of invalid input image
        */
        """
        if image.ndim == 3:
            image = rgb2gray(image)
        result = chan_vese(image, max_num_iter=200, extended_output=False)
        return result