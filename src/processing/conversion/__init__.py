"""
@file __init__.py
@brief Image conversion module initialization.

This sub-package contains algorithms for converting images between different
color spaces and formats, such as RGB to grayscale and RGB to HSV.
"""

from .grayscale import GrayscaleProcessor
from .hsv import HSVProcessor

__all__ = ['GrayscaleProcessor', 'HSVProcessor']