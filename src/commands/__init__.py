"""
@file __init__.py
@brief Command module initialization.

This module implements the Command pattern for undo/redo functionality
and operation encapsulation in the image processing application.
"""

from .base_command import BaseCommand
from .command_history import CommandHistory
from .image_commands import ApplyImageCommand

__all__ = ['BaseCommand', 'CommandHistory', 'ApplyImageCommand']