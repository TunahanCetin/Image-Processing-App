"""
@file image_commands.py
@brief Command implementations for image operations
"""

from abc import ABC, abstractmethod

class Command(ABC):
    """
    @class Command
    @brief Abstract base class for all commands.
    """
    
    @abstractmethod
    def execute(self):
        """
        @brief Execute the command
        """
        pass
    
    @abstractmethod
    def undo(self):
        """
        @brief Undo the command
        """
        pass


class ApplyImageCommand(Command):
    """
    @class ApplyImageCommand
    @brief Command for applying an image processor to source image
    """
    
    def __init__(self, window, processor):
        """
        @brief Initialize the command
        @param window The main window reference
        @param processor The image processor to apply
        """
        self.window = window
        self.processor = processor
        self.previous_output = None

    def execute(self):
        """
        @brief Apply the processor to the source image
        """
        # Remember the previous output (for undo)
        self.previous_output = self.window.output_image
        
        # Process the image
        try:
            if self.window.source_image is not None:
                # Apply the image processor
                result = self.processor.process(self.window.source_image)
                
                # Update the output image
                self.window.output_image = result
                
                # Display in the UI
                self.window.show_image_in_label(self.window.output_label, result)
        except Exception as e:
            self.window.statusBar().showMessage(f"Error in processing: {str(e)}", 3000)
            raise

    def undo(self):
        """
        @brief Restore the previous output image
        """
        # Restore previous output
        self.window.output_image = self.previous_output
        
        if self.previous_output is not None:
            # Show the previous output
            self.window.show_image_in_label(self.window.output_label, self.previous_output)
        else:
            # Clear the output display
            self.window.output_label.setText("Output will appear here after processing")
            self.window.output_label.setPixmap(None)


class SaveImageCommand(Command):
    """
    @class SaveImageCommand
    @brief Command for saving an image
    """
    
    def __init__(self, window, exporter, image, path):
        """
        @brief Initialize the command
        @param window The main window reference
        @param exporter The image exporter to use
        @param image The image to save
        @param path The path to save to
        """
        self.window = window
        self.exporter = exporter
        self.image = image
        self.path = path
        self.previous_path = None
    
    def execute(self):
        """
        @brief Save the image
        """
        try:
            self.previous_path = self.window.menu_actions.current_output_path
            self.exporter.save_image(self.image, self.path)
            self.window.menu_actions.current_output_path = self.path
            self.window.statusBar().showMessage(f"Image saved to {self.path}", 3000)
        except Exception as e:
            self.window.statusBar().showMessage(f"Error saving image: {str(e)}", 3000)
            raise
    
    def undo(self):
        """
        @brief Cannot truly undo a save operation, but can restore path
        """
        self.window.menu_actions.current_output_path = self.previous_path
        self.window.statusBar().showMessage("Save operation undone (path only)", 3000)