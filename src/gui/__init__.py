"""
@file __init__.py
@brief GUI module initialization and exports.

This module provides the graphical user interface components for the
Image Processing Application, including the main window, menu actions,
and related UI utilities.
"""

from .main_window import MainWindow
from .menu_actions import MenuActions

# Define public API
__all__ = ['MainWindow', 'MenuActions']