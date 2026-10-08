"""
@file base_command.py
@brief Abstract base class implementation for the Command pattern.
"""

from abc import ABC, abstractmethod

class BaseCommand(ABC):
    """
    @class BaseCommand
    @brief Abstract base class for all commands in the application.
    
    This class implements the Command design pattern which encapsulates
    all information needed to perform an action or trigger an event.
    All concrete command implementations must inherit from this class.
    """
    
    @abstractmethod
    def execute(self):
        """
        @brief Execute the command.
        
        This method performs the primary operation of the command.
        Must be implemented by all concrete command classes.
        """
        pass

    @abstractmethod
    def undo(self):
        """
        @brief Undo the command.
        
        This method reverses the effects of the execute method.
        Must be implemented by all concrete command classes.
        """
        pass