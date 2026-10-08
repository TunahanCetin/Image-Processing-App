import numpy as np
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt

def numpy_to_qpixmap(image, target_width=None, target_height=None):
    """!
    @brief Converts a NumPy array image to a QPixmap for display in Qt widgets.
    
    This utility function handles the conversion of images from NumPy array format 
    (as used in image processing libraries like scikit-image) to QPixmap objects 
    that can be displayed in PyQt interfaces.
    
    The function handles various data types:
    - Boolean arrays are converted to binary images (0 and 255)
    - Floating-point arrays are clipped to [0,1] range and scaled to [0,255]
    - Integer arrays are converted to uint8
    
    It also distinguishes between grayscale (2D) and color (3D) images and
    converts them to the appropriate QImage format.
    
    @param image NumPy array containing the image data
    @param target_width Optional width to scale the output pixmap to
    @param target_height Optional height to scale the output pixmap to
    @return QPixmap object ready for display in Qt widgets, or None if input is None
    @exception ValueError May occur if the input array has invalid dimensions or format
    */
    """
    if image is None:
        return None

    if image.dtype == bool:
        image = (image.astype(np.uint8)) * 255

    elif np.issubdtype(image.dtype, np.floating):
        image = np.clip(image, 0, 1)
        image = (image * 255).astype(np.uint8)

    elif np.issubdtype(image.dtype, np.integer):
        image = image.astype(np.uint8)

    if image.ndim == 2:
        q_image = QImage(image, image.shape[1], image.shape[0], image.strides[0], QImage.Format_Grayscale8)
    else:
        q_image = QImage(image, image.shape[1], image.shape[0], image.strides[0], QImage.Format_RGB888)

    pixmap = QPixmap.fromImage(q_image)

    if target_width and target_height:
        pixmap = pixmap.scaled(target_width, target_height, Qt.KeepAspectRatio)
    return pixmap