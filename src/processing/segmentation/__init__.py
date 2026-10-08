"""
@file __init__.py
@brief Image segmentation module initialization.

This sub-package contains algorithms for segmenting images into regions
or segments, including Otsu thresholding, Chan-Vese, and morphological snakes.
"""

from .otsu import OtsuSegmentationProcessor
from .chan_vese import ChanVeseSegmentationProcessor
from .morphological_snakes import MorphologicalSnakesProcessor

__all__ = ['OtsuSegmentationProcessor', 'ChanVeseSegmentationProcessor', 'MorphologicalSnakesProcessor']