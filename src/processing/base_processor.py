from abc import ABC, abstractmethod

class BaseProcessor(ABC):
    """!
    @brief Abstract base class for all image processing classes.
    
    This abstract class defines the interface that all image processors
    must implement. It ensures consistency across different image processing
    implementations by requiring a standard process method.
    */
    """

    @abstractmethod
    def process(self, image):
        """!
        @brief Performs processing on the input image.
        
        This abstract method must be implemented by all derived classes to
        perform their specific image processing operations.
        
        @param image The input image as a NumPy array
        @return The processed image as a NumPy array
        @exception NotImplementedError If the method is not implemented by a derived class
        */
        """
        pass