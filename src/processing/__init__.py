"""
@file __init__.py
@brief Image processing module initialization.

This package contains various image processing algorithms organized
into sub-packages by processing category (conversion, segmentation, 
edge detection).
"""

# Import sub-packages
from . import conversion
from . import segmentation
from . import edge_detection

# Define public API
__all__ = ['conversion', 'segmentation', 'edge_detection']