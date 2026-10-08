"""
@file command_history.py
@brief Command History Manager for undo/redo functionality.

This file implements a command history manager that allows for
tracking, undoing, and redoing of commands in the application.
It uses the Command pattern to provide a complete undo/redo stack.
"""

from PyQt5.QtCore import QObject, pyqtSignal
from typing import List, TypeVar, Generic

# Define a command type for type hints
CommandType = TypeVar('CommandType')

class CommandHistory(QObject, Generic[CommandType]):
    """
    @class CommandHistory
    @brief Manages command execution history for undo/redo functionality.
    
    This class maintains a history of executed commands and provides methods
    to undo and redo these commands. It uses Qt's signal/slot mechanism to
    notify listeners about command execution, undoing, and redoing.
    """
    # Define signals
    ## Signal emitted when a command is executed
    command_executed = pyqtSignal(object)
    ## Signal emitted when a command is undone
    command_undone = pyqtSignal(object)
    ## Signal emitted when a command is redone
    command_redone = pyqtSignal(object)
    
    def __init__(self):
        """
        @brief Initialize the command history.
        
        Creates an empty command history with position set to -1,
        indicating no commands have been executed yet.
        """
        super().__init__()  # Initialize QObject parent
        self._history: List[CommandType] = []
        self._position: int = -1

    def execute_command(self, command: CommandType) -> None:
        """
        @brief Execute a command and add it to history.
        
        Executes the given command, adds it to the history, and
        trims any commands that were previously undone.
        
        @param command The command object to execute (must implement execute/undo)
        """
        # Remove any redoable commands
        if self._position + 1 < len(self._history):
            self._history = self._history[:self._position + 1]
        
        # Execute the command
        command.execute()
        
        # Add to history
        self._history.append(command)
        self._position = len(self._history) - 1
        
        # Emit signal
        self.command_executed.emit(command)

    def undo(self) -> None:
        """
        @brief Undo the last executed command.
        
        Undoes the command at the current position in the history
        and decrements the position. Does nothing if can_undo() is False.
        """
        if self.can_undo():
            command = self._history[self._position]
            command.undo()
            self._position -= 1
            
            # Emit signal
            self.command_undone.emit(command)

    def redo(self) -> None:
        """
        @brief Redo the last undone command.
        
        Moves the position forward and re-executes the command
        at that position. Does nothing if can_redo() is False.
        """
        if self.can_redo():
            self._position += 1
            command = self._history[self._position]
            command.execute()
            
            # Emit signal
            self.command_redone.emit(command)

    def can_undo(self) -> bool:
        """
        @brief Check if undo is possible.
        
        @return True if there are commands in the history that can be undone,
                False otherwise.
        """
        return self._position >= 0

    def can_redo(self) -> bool:
        """
        @brief Check if redo is possible.
        
        @return True if there are undone commands that can be redone,
                False otherwise.
        """
        return self._position < len(self._history) - 1