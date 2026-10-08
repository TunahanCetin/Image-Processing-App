 
"""
@file __init__.py
@brief Edge detection module initialization.

This sub-package contains algorithms for detecting edges in images,
including Roberts, Sobel, Scharr, and Prewitt operators.
"""

from .roberts import RobertsEdgeDetectionProcessor
from .sobel import SobelEdgeDetectionProcessor
from .scharr import ScharrEdgeDetectionProcessor
from .prewitt import PrewittEdgeDetectionProcessor

__all__ = ['RobertsEdgeDetectionProcessor', 'SobelEdgeDetectionProcessor', 
           'ScharrEdgeDetectionProcessor', 'PrewittEdgeDetectionProcessor']