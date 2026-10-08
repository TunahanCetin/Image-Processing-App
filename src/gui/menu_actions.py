"""
@file menu_actions.py
@brief Centralized menu and toolbar action manager for the GUI.

This module manages all menu and toolbar actions in the application,
creating the menus, connecting them to handlers, and managing their states.
It serves as the central control point for user interactions through the UI.
"""

from PyQt5.QtWidgets import QAction, QFileDialog, QMessageBox, QMenu
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSettings
from processing.conversion.grayscale import GrayscaleProcessor
from processing.conversion.hsv import HSVProcessor
from processing.segmentation.otsu import OtsuSegmentationProcessor
from processing.segmentation.chan_vese import ChanVeseSegmentationProcessor
from processing.segmentation.morphological_snakes import MorphologicalSnakesProcessor
from processing.edge_detection.sobel import SobelEdgeDetectionProcessor
from processing.edge_detection.roberts import RobertsEdgeDetectionProcessor
from processing.edge_detection.scharr import ScharrEdgeDetectionProcessor
from processing.edge_detection.prewitt import PrewittEdgeDetectionProcessor
from commands.command_history import CommandHistory
from commands.image_commands import ApplyImageCommand
from fileio.image_loader import ImageLoader
from fileio.image_exporter import ImageExporter
from skimage import data

ICON_PATH = "resources/icons/"

class MenuActions:
    """
    @class MenuActions
    @brief Manages all menu and toolbar actions in the application.
    
    This class is responsible for creating all menu entries, connecting signals to slots,
    managing action states, and providing a central interface for the application's
    command structure. It also manages the command history for undo/redo operations.
    """

    def __init__(self, window):
        """
        @brief Initializes the MenuActions object and declares necessary variables.
        
        Sets up the command history, connects signal handlers, and initializes
        file path and settings variables.
        
        @param window The main window instance that will host these actions.
        """
        self.window = window
        self.history = CommandHistory()
        self.history.command_executed.connect(self._on_command_executed)
        self.history.command_undone.connect(self._on_command_undone)
        self.history.command_redone.connect(self._on_command_redone)
        
        self.current_source_path = None
        self.current_output_path = None
        
        # Settings
        self.settings = QSettings("ImageProcessingApp", "Settings")

    def create_file_menu(self, menu_bar):
        """
        @brief Creates the File menu with all related actions.
        
        Includes open, save, export actions and sample image loading options.
        
        @param menu_bar The application's menu bar to add the menu to.
        @return The created File menu.
        """
        file_menu = menu_bar.addMenu("File")

        self.open_action = QAction(QIcon(ICON_PATH + "open.png"), "Open From File", self.window)
        self.open_action.setShortcut("Ctrl+O")
        self.open_action.setStatusTip("Open image from file")
        self.open_action.triggered.connect(self.open_from_file)
        file_menu.addAction(self.open_action)

        file_menu.addSeparator()
        file_menu.addAction(QAction(QIcon(ICON_PATH + "coffee.png"), "Load Coffee Sample", self.window, triggered=lambda: self.load_sample_image("coffee")))
        file_menu.addAction(QAction(QIcon(ICON_PATH + "camera.png"), "Load Camera Sample", self.window, triggered=lambda: self.load_sample_image("camera")))
        file_menu.addAction(QAction(QIcon(ICON_PATH + "horse.png"), "Load Horse Sample", self.window, triggered=lambda: self.load_sample_image("horse")))

        file_menu.addSeparator()

        self.save_output_action = QAction(QIcon(ICON_PATH + "save.png"), "Save Output", self.window, enabled=False)
        self.save_output_action.setShortcut("Ctrl+S")
        self.save_output_action.setStatusTip("Save current output image")
        self.save_output_action.triggered.connect(self.save_output)
        file_menu.addAction(self.save_output_action)

        self.save_as_output_action = QAction(QIcon(ICON_PATH + "save_as.png"), "Save As Output", self.window, enabled=False)
        self.save_as_output_action.setStatusTip("Save output image with new name")
        self.save_as_output_action.triggered.connect(self.save_as_output)
        file_menu.addAction(self.save_as_output_action)

        self.export_as_action = QAction(QIcon(ICON_PATH + "export.png"), "Export As", self.window, enabled=False)
        self.export_as_action.setStatusTip("Export output image to other format")
        self.export_as_action.triggered.connect(self.export_as)
        file_menu.addAction(self.export_as_action)
        
        file_menu.addSeparator()
        exit_action = QAction(QIcon(ICON_PATH + "exit.png"), "Exit", self.window)
        exit_action.setShortcut("Alt+F4")
        exit_action.setStatusTip("Exit application")
        exit_action.triggered.connect(self.window.close)
        file_menu.addAction(exit_action)
        
        return file_menu

    def create_edit_menu(self, menu_bar):
        """
        @brief Creates the Edit menu with all related actions.
        
        Includes undo/redo actions, clear operations, and command history management.
        
        @param menu_bar The application's menu bar to add the menu to.
        @return The created Edit menu.
        """
        edit_menu = menu_bar.addMenu("Edit")

        self.undo_action = QAction(QIcon(ICON_PATH + "undo.png"), "Undo Output", self.window, enabled=False)
        self.undo_action.setShortcut("Ctrl+Z")
        self.undo_action.setStatusTip("Undo last output operation")
        self.undo_action.triggered.connect(self.history.undo)

        self.redo_action = QAction(QIcon(ICON_PATH + "redo.png"), "Redo Output", self.window, enabled=False)
        self.redo_action.setShortcut("Ctrl+Y")
        self.redo_action.setStatusTip("Redo last undone operation")
        self.redo_action.triggered.connect(self.history.redo)
        
        # Clear actions
        clear_menu = QMenu("Clear", self.window)
        clear_source_action = QAction("Clear Source", self.window)
        clear_source_action.setStatusTip("Clear source image")
        clear_source_action.setShortcut("Ctrl+L")
        clear_source_action.triggered.connect(self._clear_source)
        
        clear_output_action = QAction("Clear Output", self.window)
        clear_output_action.setStatusTip("Clear output image")
        clear_output_action.setShortcut("Ctrl+Shift+L")
        clear_output_action.triggered.connect(self._clear_output)
        
        clear_all_action = QAction("Clear All", self.window)
        clear_all_action.setStatusTip("Clear all images")
        clear_all_action.triggered.connect(lambda: (self._clear_source(), self._clear_output()))
        
        clear_menu.addAction(clear_source_action)
        clear_menu.addAction(clear_output_action)
        clear_menu.addAction(clear_all_action)

        edit_menu.addAction(self.undo_action)
        edit_menu.addAction(self.redo_action)
        edit_menu.addSeparator()
        edit_menu.addMenu(clear_menu)
        edit_menu.addSeparator()
        edit_menu.addAction(QAction("Clear Command History", self.window, triggered=self._clear_command_history))
        
        return edit_menu

    def create_conversion_menu(self, menu_bar):
        """
        @brief Creates the Conversion menu with all related actions.
        
        Includes image color space conversion operations.
        
        @param menu_bar The application's menu bar to add the menu to.
        @return The created Conversion menu.
        """
        conversion_menu = menu_bar.addMenu("Conversion")

        self.gray_action = QAction(QIcon(ICON_PATH + "grayscale.png"), "RGB to Grayscale", self.window, enabled=False)
        self.gray_action.setShortcut("Ctrl+G")
        self.gray_action.setStatusTip("Convert RGB image to Grayscale")
        self.gray_action.triggered.connect(lambda: self.apply_processor(GrayscaleProcessor()))
        conversion_menu.addAction(self.gray_action)

        self.hsv_action = QAction(QIcon(ICON_PATH + "hsv.png"), "RGB to HSV", self.window, enabled=False)
        self.hsv_action.setShortcut("Ctrl+H")
        self.hsv_action.setStatusTip("Convert RGB image to HSV")
        self.hsv_action.triggered.connect(lambda: self.apply_processor(HSVProcessor()))
        conversion_menu.addAction(self.hsv_action)
        
        return conversion_menu

    def create_segmentation_menu(self, menu_bar):
        """
        @brief Creates the Segmentation menu with all related actions.
        
        Includes various image segmentation algorithms.
        
        @param menu_bar The application's menu bar to add the menu to.
        @return The created Segmentation menu.
        """
        segmentation_menu = menu_bar.addMenu("Segmentation")

        self.otsu_action = QAction(QIcon(ICON_PATH + "otsu.png"), "Multi-Otsu Thresholding", self.window, enabled=False)
        self.otsu_action.setStatusTip("Apply Multi-Otsu Thresholding segmentation")
        self.otsu_action.triggered.connect(lambda: self.apply_processor(OtsuSegmentationProcessor()))
        segmentation_menu.addAction(self.otsu_action)

        self.chan_vese_action = QAction(QIcon(ICON_PATH + "chan_vese.png"), "Chan-Vese Segmentation", self.window, enabled=False)
        self.chan_vese_action.setStatusTip("Apply Chan-Vese segmentation")
        self.chan_vese_action.triggered.connect(lambda: self.apply_processor(ChanVeseSegmentationProcessor()))
        segmentation_menu.addAction(self.chan_vese_action)

        self.snakes_action = QAction(QIcon(ICON_PATH + "snakes.png"), "Morphological Snakes", self.window, enabled=False)
        self.snakes_action.setStatusTip("Apply Morphological Snakes segmentation")
        self.snakes_action.triggered.connect(lambda: self.apply_processor(MorphologicalSnakesProcessor()))
        segmentation_menu.addAction(self.snakes_action)
        
        return segmentation_menu

    def create_edge_detection_menu(self, menu_bar):
        """
        @brief Creates the Edge Detection menu with all related actions.
        
        Includes various edge detection algorithms.
        
        @param menu_bar The application's menu bar to add the menu to.
        @return The created Edge Detection menu.
        """
        edge_menu = menu_bar.addMenu("Edge Detection")

        self.sobel_action = QAction(QIcon(ICON_PATH + "sobel.png"), "Sobel", self.window, enabled=False)
        self.sobel_action.setStatusTip("Apply Sobel edge detection")
        self.sobel_action.triggered.connect(lambda: self.apply_processor(SobelEdgeDetectionProcessor()))
        edge_menu.addAction(self.sobel_action)

        self.roberts_action = QAction(QIcon(ICON_PATH + "roberts.png"), "Roberts", self.window, enabled=False)
        self.roberts_action.setStatusTip("Apply Roberts edge detection")
        self.roberts_action.triggered.connect(lambda: self.apply_processor(RobertsEdgeDetectionProcessor()))
        edge_menu.addAction(self.roberts_action)

        self.scharr_action = QAction(QIcon(ICON_PATH + "scharr.png"), "Scharr", self.window, enabled=False)
        self.scharr_action.setStatusTip("Apply Scharr edge detection")
        self.scharr_action.triggered.connect(lambda: self.apply_processor(ScharrEdgeDetectionProcessor()))
        edge_menu.addAction(self.scharr_action)

        self.prewitt_action = QAction(QIcon(ICON_PATH + "prewitt.png"), "Prewitt", self.window, enabled=False)
        self.prewitt_action.setStatusTip("Apply Prewitt edge detection")
        self.prewitt_action.triggered.connect(lambda: self.apply_processor(PrewittEdgeDetectionProcessor()))
        edge_menu.addAction(self.prewitt_action)
        
        return edge_menu

    def create_view_menu(self, menu_bar):
        """
        @brief Creates the View menu with all related actions.
        
        Includes theme toggling and interface customization options.
        
        @param menu_bar The application's menu bar to add the menu to.
        @return The created View menu.
        """
        view_menu = menu_bar.addMenu("View")
        
        # Theme toggle action
        self.toggle_theme_action = QAction(QIcon(ICON_PATH + "dark_theme.png"), "Dark Mode", self.window)
        self.toggle_theme_action.setStatusTip("Toggle between light and dark theme")
        self.toggle_theme_action.triggered.connect(self.window.toggle_theme)
        view_menu.addAction(self.toggle_theme_action)
        
        view_menu.addSeparator()
        
        # Command history visibility
        toggle_history_action = QAction("Toggle Command History Panel", self.window)
        toggle_history_action.setStatusTip("Show or hide command history panel")
        toggle_history_action.setShortcut("Ctrl+H")
        toggle_history_action.triggered.connect(self._toggle_history_panel)
        view_menu.addAction(toggle_history_action)
        
        return view_menu

    # ------------------------ Utility Methods ------------------------

    def apply_processor(self, processor):
        """
        @brief Applies an image processor to the source image.
        
        Creates a command, executes it, and adds it to the command history.
        Updates progress indicators during processing.
        
        @param processor The image processor to apply.
        """
        if self.window.source_image is not None:
            try:
                self.window.start_progress()
                # Simulate progress (up to 70%)
                self.window.update_progress(70)
                command = ApplyImageCommand(self.window, processor)
                self.history.execute_command(command)
                self.enable_output_actions(True)
                self.window.complete_progress()
                
                # Add to command history
                self.window.add_to_command_history(processor.__class__.__name__, processor)
            except Exception as e:
                self.window.progress_bar.hide()
                QMessageBox.critical(self.window, "Processing Error", str(e))
                self.window.statusBar().showMessage(f"Processing error: {str(e)}", 3000)

    def enable_output_actions(self, status: bool):
        """
        @brief Enables or disables output-related actions.
        
        Controls the state of save, export, undo, and redo actions.
        
        @param status True to enable actions, False to disable them.
        """
        self.save_output_action.setEnabled(status)
        self.save_as_output_action.setEnabled(status)
        self.export_as_action.setEnabled(status)
        self.undo_action.setEnabled(self.history.can_undo())
        self.redo_action.setEnabled(self.history.can_redo())

    def load_sample_image(self, name):
        """
        @brief Loads a sample image from scikit-image data.
        
        @param name Name of the sample image to load ("coffee", "camera", or "horse").
        """
        images = {"coffee": data.coffee(), "camera": data.camera(), "horse": data.horse()}
        self.window.source_image = images.get(name, None)
        if self.window.source_image is not None:
            self.window.show_image_in_label(self.window.source_label, self.window.source_image)
            self.update_menu_states_based_on_image()
            
            # Add to command history
            self.window.add_to_command_history(f"Loaded sample: {name}")

    def open_from_file(self):
        """
        @brief Opens an image from a file.
        
        Displays a file dialog for the user to select an image file,
        loads it, and updates the UI accordingly.
        """
        file_name, _ = QFileDialog.getOpenFileName(self.window, "Open Image", "", "Images (*.png *.jpg)")
        if file_name:
            try:
                self.window.source_image = ImageLoader.load_image(file_name)
                self.window.show_image_in_label(self.window.source_label, self.window.source_image)
                self.current_source_path = file_name
                self.update_menu_states_based_on_image()
                
                # Add to command history
                self.window.add_to_command_history(f"Opened: {file_name}")
            except Exception as e:
                QMessageBox.critical(self.window, "File Error", str(e))

    def save_output(self):
        """
        @brief Saves the output image to the current output path.
        
        If no output path is set, prompts the user to use Save As.
        Shows progress indicators during saving.
        """
        if self.window.output_image is None:
            QMessageBox.warning(self.window, "Warning", "No output image to save.")
            return
        if self.current_output_path is None:
            QMessageBox.warning(self.window, "Warning", "No output path specified. Please use Save As.")
            return
        try:
            progress = self.window.show_progress_dialog("Saving image...")
            ImageExporter.save_image(self.window.output_image, self.current_output_path)
            self.window.statusBar().showMessage(f"Output saved to {self.current_output_path}", 3000)
            
            # Add to command history
            self.window.add_to_command_history(f"Saved output to: {self.current_output_path}")
        except Exception as e:
            QMessageBox.critical(self.window, "Save Error", f"Could not save output: {str(e)}")
        finally:
            progress.close()

        self.window.start_progress()
        self.window.complete_progress()

    def save_as_output(self):
        """
        @brief Saves the output image to a user-specified path.
        
        Displays a file dialog for the user to select a save location,
        saves the image, and updates the current output path.
        Shows progress indicators during saving.
        """
        if self.window.output_image is None:
            QMessageBox.warning(self.window, "Warning", "No output image to save.")
            return
        file_name, _ = QFileDialog.getSaveFileName(self.window, "Save Output As", "", "Images (*.png *.jpg)")
        if file_name:
            try:
                self.window.start_progress()
                ImageExporter.save_image(self.window.output_image, file_name)
                self.current_output_path = file_name
                self.window.statusBar().showMessage(f"Output saved as {file_name}", 3000)
                
                # Add to command history
                self.window.add_to_command_history(f"Saved output as: {file_name}")
                self.window.complete_progress()
            except Exception as e:
                self.window.progress_bar.hide()
                QMessageBox.critical(self.window, "Save Error", f"Could not save output: {str(e)}")

    def export_as(self):
        """
        @brief Exports the output image to a different format.
        
        Automatically switches between PNG and JPG formats.
        Shows progress indicators during export.
        
        @throws Warning If no output image or path is available.
        """
        if self.window.output_image is None or self.current_output_path is None:
            QMessageBox.warning(self.window, "Warning", "No output image or output path to export.")
            return
        export_format = '.png' if self.current_output_path.lower().endswith('.jpg') else '.jpg'
        try:
            self.window.start_progress()
            export_path = ImageExporter.export_as(self.window.output_image, self.current_output_path, export_format)
            self.window.statusBar().showMessage(f"Output exported as {export_path}", 3000)
            
            # Add to command history
            self.window.add_to_command_history(f"Exported output as: {export_path}")
            self.window.complete_progress()
        except Exception as e:
            self.window.progress_bar.hide()
            QMessageBox.critical(self.window, "Export Error", f"Could not export output: {str(e)}")

    def update_menu_states_based_on_image(self):
        """
        @brief Updates the enabled/disabled state of menu actions based on the current image.
        
        Enables/disables actions based on whether an image is loaded and its properties
        (e.g., whether it's RGB for HSV conversion).
        """
        if self.window.source_image is None:
            self.gray_action.setEnabled(False)
            self.hsv_action.setEnabled(False)
            self.otsu_action.setEnabled(False)
            self.chan_vese_action.setEnabled(False)
            self.snakes_action.setEnabled(False)
            self.sobel_action.setEnabled(False)
            self.roberts_action.setEnabled(False)
            self.scharr_action.setEnabled(False)
            self.prewitt_action.setEnabled(False)
            return
            
        # Check if image is RGB (3 channels)
        is_rgb = self.window.source_image.ndim == 3 and self.window.source_image.shape[2] == 3
        
        # Enable actions based on image properties
        self.gray_action.setEnabled(True)
        self.hsv_action.setEnabled(is_rgb)  # HSV conversion requires RGB input
        self.otsu_action.setEnabled(True)
        self.chan_vese_action.setEnabled(True)
        self.snakes_action.setEnabled(True)
        self.sobel_action.setEnabled(True)
        self.roberts_action.setEnabled(True)
        self.scharr_action.setEnabled(True)
        self.prewitt_action.setEnabled(True)
        
        # Reset undo/redo state for new image
        self.undo_action.setEnabled(False)
        self.redo_action.setEnabled(False)

    def _on_command_executed(self, command):
        """
        @brief Handler for command execution events.
        
        Updates UI elements based on command execution.
        
        @param command The executed command object.
        """
        self.undo_action.setEnabled(self.history.can_undo())
        self.redo_action.setEnabled(self.history.can_redo())

    def _on_command_undone(self, command):
        """
        @brief Handler for command undo events.
        
        Updates UI elements and command history after an undo operation.
        
        @param command The undone command object.
        """
        self.undo_action.setEnabled(self.history.can_undo())
        self.redo_action.setEnabled(self.history.can_redo())
        
        # Add to command history
        if hasattr(command, 'processor'):
            self.window.add_to_command_history(f"Undone: {command.processor.__class__.__name__}")

    def _on_command_redone(self, command):
        """
        @brief Handler for command redo events.
        
        Updates UI elements and command history after a redo operation.
        
        @param command The redone command object.
        """
        self.undo_action.setEnabled(self.history.can_undo())
        self.redo_action.setEnabled(self.history.can_redo())
        
        # Add to command history
        if hasattr(command, 'processor'):
            self.window.add_to_command_history(f"Redone: {command.processor.__class__.__name__}")

    def _clear_source(self):
        """
        @brief Clears the source image.
        
        Resets the source image display and updates menu states accordingly.
        Adds an entry to the command history.
        """
        if self.window.source_image is not None:
            self.window.source_image = None
            self.window.source_label.setText("Drag and drop an image here or use Open menu")
            self.window.source_label.setPixmap(None)
            self.update_menu_states_based_on_image()
            self.window.add_to_command_history("Cleared source image")

    def _clear_output(self):
        """
        @brief Clears the output image.
        
        Resets the output image display and disables output-related actions.
        Adds an entry to the command history.
        """
        if self.window.output_image is not None:
            self.window.output_image = None
            self.window.output_label.setText("Output will appear here after processing")
            self.window.output_label.setPixmap(None)
            self.current_output_path = None
            self.enable_output_actions(False)
            self.window.add_to_command_history("Cleared output image")

    def _clear_command_history(self):
        """
        @brief Clears the command history list in the UI.
        
        Removes all entries from the command history panel.
        Does not affect the actual command stack for undo/redo.
        """
        self.window.history_list.clear()
        self.window.statusBar().showMessage("Command history cleared", 3000)

    def _toggle_history_panel(self):
        """
        @brief Toggles the visibility of the command history panel.
        
        Shows the panel if it's hidden, hides it if it's visible.
        """
        if self.window.history_dock.isVisible():
            self.window.history_dock.hide()
        else:
            self.window.history_dock.show()