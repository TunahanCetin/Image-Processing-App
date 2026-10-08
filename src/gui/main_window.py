"""
@file main_window.py
@brief Main GUI window for Image Processing Application (OOP2 Lab Final Project)
"""

from PyQt5.QtWidgets import (
    QMainWindow, QLabel, QWidget, QVBoxLayout, QToolBar, QStatusBar, QProgressDialog, 
    QProgressBar, QDockWidget, QListWidget, QSplitter, QHBoxLayout, QAction, 
    QListWidgetItem, QAbstractItemView
)
from PyQt5.QtCore import Qt, QMimeData, QUrl
from PyQt5.QtGui import QDragEnterEvent, QDropEvent, QIcon
from utils.image_utils import numpy_to_qpixmap
from gui.menu_actions import MenuActions
from skimage import io
import os
from datetime import datetime

ICON_PATH = "resources/icons/"

class MainWindow(QMainWindow):
    """
    @class MainWindow
    @brief Main application window that initializes menus, toolbars, status bar, and panels.
    """

    def __init__(self):
        """
        @brief Initializes the main window and all GUI components.
        """
        super().__init__()
        self.setWindowTitle("Image Processing App - Lab Final")
        self.resize(1200, 700)

        self.source_image = None
        self.output_image = None
        self.is_dark_theme = False

        # Enable drag and drop
        self.setAcceptDrops(True)

        # Initialize menu actions manager
        self.menu_actions = MenuActions(self)

        # Build the UI
        self._create_ui()
        
        # Initial theme
        self.apply_light_theme()

    def _create_ui(self):
        """
        @brief Create all UI components.
        """
        self._create_menus()
        self._create_toolbar()
        self._create_main_panels()
        self._create_command_history_panel()
        self._create_status_bar()

    def _create_menus(self):
        """
        @brief Create and set up menu bar.
        """
        menu_bar = self.menuBar()
        self.menu_actions.create_file_menu(menu_bar)
        self.menu_actions.create_edit_menu(menu_bar)
        self.menu_actions.create_conversion_menu(menu_bar)
        self.menu_actions.create_segmentation_menu(menu_bar)
        self.menu_actions.create_edge_detection_menu(menu_bar)
        self.menu_actions.create_view_menu(menu_bar)  # New View menu for theme switching

    def _create_toolbar(self):
        """
        @brief Create toolbar with all grouped actions from MenuActions.
        """
        toolbar = QToolBar("Main Toolbar")
        toolbar.setToolButtonStyle(Qt.ToolButtonIconOnly)
        self.addToolBar(toolbar)

        # Group: File / Source
        toolbar.addAction(self.menu_actions.open_action)
        toolbar.addAction(self.menu_actions.save_output_action)
        toolbar.addAction(self.menu_actions.save_as_output_action)
        toolbar.addAction(self.menu_actions.export_as_action)
        toolbar.addSeparator()

        # Group: Conversion
        toolbar.addAction(self.menu_actions.gray_action)
        toolbar.addAction(self.menu_actions.hsv_action)
        toolbar.addSeparator()

        # Group: Segmentation
        toolbar.addAction(self.menu_actions.otsu_action)
        toolbar.addAction(self.menu_actions.chan_vese_action)
        toolbar.addAction(self.menu_actions.snakes_action)
        toolbar.addSeparator()

        # Group: Edge Detection
        toolbar.addAction(self.menu_actions.sobel_action)
        toolbar.addAction(self.menu_actions.roberts_action)
        toolbar.addAction(self.menu_actions.scharr_action)
        toolbar.addAction(self.menu_actions.prewitt_action)
        toolbar.addSeparator()

        # Group: Edit
        toolbar.addAction(self.menu_actions.undo_action)
        toolbar.addAction(self.menu_actions.redo_action)
        toolbar.addSeparator()
        
        # Add theme toggle button
        toolbar.addAction(self.menu_actions.toggle_theme_action)

    def _create_main_panels(self):
        """
        @brief Create the Source and Output display panels.
        """
        # Main splitter to hold image panels
        main_splitter = QSplitter(Qt.Vertical)
        
        # Source panel
        source_widget = QWidget()
        source_layout = QVBoxLayout(source_widget)
        source_layout.setContentsMargins(0, 0, 0, 0)
        
        source_label = QLabel("Source Image")
        source_label.setAlignment(Qt.AlignCenter)
        source_label.setStyleSheet("font-weight: bold;")
        
        self.source_label = QLabel("Drag and drop an image here or use Open menu")
        self.source_label.setAlignment(Qt.AlignCenter)
        self.source_label.setMinimumHeight(250)
        
        source_layout.addWidget(source_label)
        source_layout.addWidget(self.source_label)
        
        # Output panel
        output_widget = QWidget()
        output_layout = QVBoxLayout(output_widget)
        output_layout.setContentsMargins(0, 0, 0, 0)
        
        output_label = QLabel("Output Image")
        output_label.setAlignment(Qt.AlignCenter)
        output_label.setStyleSheet("font-weight: bold;")
        
        self.output_label = QLabel("Output will appear here after processing")
        self.output_label.setAlignment(Qt.AlignCenter)
        self.output_label.setMinimumHeight(250)
        
        output_layout.addWidget(output_label)
        output_layout.addWidget(self.output_label)
        
        # Add panels to splitter
        main_splitter.addWidget(source_widget)
        main_splitter.addWidget(output_widget)
        
        # Set central widget
        self.setCentralWidget(main_splitter)

    def _create_command_history_panel(self):
        """
        @brief Create a dockable panel for command history.
        """
        self.history_dock = QDockWidget("Command History", self)
        self.history_dock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        
        # Create list widget to display command history
        self.history_list = QListWidget()
        self.history_list.setSelectionMode(QAbstractItemView.SingleSelection)
        self.history_list.setAlternatingRowColors(True)
        self.history_list.itemDoubleClicked.connect(self._on_history_item_double_clicked)
        
        self.history_dock.setWidget(self.history_list)
        self.addDockWidget(Qt.RightDockWidgetArea, self.history_dock)

    def _on_history_item_double_clicked(self, item):
        """
        @brief Handler for double-clicking on history item
        @param item The clicked list item
        """
        command_info = item.data(Qt.UserRole)
        if command_info:
            # Show detailed information about the command
            from PyQt5.QtWidgets import QMessageBox
            QMessageBox.information(
                self,
                "Command Details",
                f"Operation: {command_info['operation']}\n"
                f"Time: {command_info['timestamp']}\n"
                f"Parameters: {command_info.get('parameters', 'None')}"
            )

    def _create_status_bar(self):
        status_bar = QStatusBar()
        self.setStatusBar(status_bar)
        self.statusBar().showMessage("Ready")

        # Progress bar'ı status bar'a ekleyin
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setFixedWidth(200)
        self.progress_bar.hide()  # Başlangıçta gizli

        self.statusBar().addPermanentWidget(self.progress_bar)

    def open_source_image(self):
        """
        @brief Open image file and display in the Source panel.
        """
        try:
            from PyQt5.QtWidgets import QFileDialog
            file_name, _ = QFileDialog.getOpenFileName(self, "Open Image", "", "Images (*.png *.jpg)")
            if file_name:
                self.source_image = io.imread(file_name)
                self.show_image_in_label(self.source_label, self.source_image)
                self.menu_actions.update_menu_states_based_on_image()
                self.menu_actions.current_source_path = file_name
                self.statusBar().showMessage("Source image loaded successfully.", 3000)
        except Exception as e:
            self.statusBar().showMessage(f"Error loading image: {str(e)}", 3000)

    def show_image_in_label(self, label, image):
        """
        @brief Show the given image in the specified QLabel and display image metadata.
        @param label QLabel to display the image.
        @param image Numpy image array.
        """
        try:
            pixmap = numpy_to_qpixmap(image, label.width(), label.height())
            if pixmap:
                label.setPixmap(pixmap)
                label.setToolTip(f"Resolution: {image.shape[1]}x{image.shape[0]}, Channels: {image.shape[2] if image.ndim == 3 else 1}")
            else:
                label.setText("No Image")
        except Exception as e:
            label.setText("Error displaying image")
            self.statusBar().showMessage(f"Display error: {str(e)}", 3000)
    
    def show_progress_dialog(self, message="Processing..."):
        """
        Show a temporary progress dialog.
        """
        progress = QProgressDialog(message, None, 0, 0, self)
        progress.setWindowModality(Qt.ApplicationModal)
        progress.setCancelButton(None)
        progress.setMinimumDuration(0)
        progress.setWindowTitle("Please wait")
        progress.show()
        return progress
    
    def start_progress(self):
        self.progress_bar.setValue(0)
        self.progress_bar.show()
        self.statusBar().showMessage("Processing...")

    def update_progress(self, value):
        self.progress_bar.setValue(value)

    def complete_progress(self):
        self.progress_bar.setValue(100)
        self.statusBar().showMessage("Operation completed.", 3000)
        self.progress_bar.hide()
    
    def add_to_command_history(self, operation_name, processor=None):
        """
        @brief Add an entry to the command history
        @param operation_name Name of the operation performed
        @param processor Optional processor object
        """
        timestamp = datetime.now().strftime("%H:%M:%S")
        item = QListWidgetItem(f"{timestamp} - {operation_name}")
        
        # Store additional data about the command
        command_data = {
            "operation": operation_name,
            "timestamp": timestamp
        }
        
        if processor:
            # Storing processor parameters if available
            command_data["parameters"] = str(processor.__dict__)
        
        item.setData(Qt.UserRole, command_data)
        self.history_list.addItem(item)
        
        # Auto-scroll to the bottom
        self.history_list.scrollToBottom()
    
    def toggle_theme(self):
        """
        @brief Toggle between light and dark themes
        """
        if self.is_dark_theme:
            self.apply_light_theme()
        else:
            self.apply_dark_theme()
    
    def apply_dark_theme(self):
        """
        @brief Apply dark theme to application
        """
        self.setStyleSheet("""
            QMainWindow, QDialog, QDockWidget, QListWidget, QWidget {
                background-color: #2D2D30;
                color: #E6E6E6;
            }
            
            QMenuBar, QMenu {
                background-color: #2D2D30;
                color: #E6E6E6;
            }
            
            QMenuBar::item:selected, QMenu::item:selected {
                background-color: #3E3E40;
            }
            
            QToolBar {
                background-color: #2D2D30;
                border-bottom: 1px solid #3E3E40;
            }
            
            QStatusBar {
                background-color: #1E1E1E;
                color: #E6E6E6;
            }
            
            QLabel {
                color: #E6E6E6;
            }
            
            QProgressBar {
                border: 1px solid #3E3E40;
                border-radius: 2px;
                background-color: #252526;
                text-align: center;
                color: #E6E6E6;
            }
            
            QProgressBar::chunk {
                background-color: #007ACC;
            }
            
            QListWidget {
                background-color: #252526;
                alternate-background-color: #2D2D30;
            }
            
            QListWidget::item:selected {
                background-color: #3F3F46;
            }
        """)
        
        self.is_dark_theme = True
        self.menu_actions.toggle_theme_action.setText("Light Mode")
        self.menu_actions.toggle_theme_action.setIcon(QIcon(ICON_PATH + "light_theme.png"))
    
    def apply_light_theme(self):
        """
        @brief Apply light theme to application
        """
        self.setStyleSheet("""
            QMainWindow, QDialog, QDockWidget, QListWidget, QWidget {
                background-color: #F0F0F0;
                color: #000000;
            }
            
            QMenuBar, QMenu {
                background-color: #F0F0F0;
                color: #000000;
            }
            
            QMenuBar::item:selected, QMenu::item:selected {
                background-color: #E0E0E0;
            }
            
            QToolBar {
                background-color: #F0F0F0;
                border-bottom: 1px solid #D0D0D0;
            }
            
            QStatusBar {
                background-color: #E0E0E0;
                color: #000000;
            }
            
            QLabel {
                color: #000000;
            }
            
            QProgressBar {
                border: 1px solid #C0C0C0;
                border-radius: 2px;
                background-color: #FFFFFF;
                text-align: center;
                color: #000000;
            }
            
            QProgressBar::chunk {
                background-color: #0078D7;
            }
            
            QListWidget {
                background-color: #FFFFFF;
                alternate-background-color: #F5F5F5;
            }
            
            QListWidget::item:selected {
                background-color: #D0D0D0;
            }
        """)
        
        self.is_dark_theme = False
        self.menu_actions.toggle_theme_action.setText("Dark Mode")
        self.menu_actions.toggle_theme_action.setIcon(QIcon(ICON_PATH + "dark_theme.png"))
    
    # Drag and Drop event handlers
    def dragEnterEvent(self, event: QDragEnterEvent):
        """
        @brief Handle drag enter event for drag-and-drop
        @param event The drag enter event
        """
        if event.mimeData().hasUrls():
            # Check if at least one URL is an image file
            for url in event.mimeData().urls():
                if self._is_valid_image_file(url.toLocalFile()):
                    event.acceptProposedAction()
                    self.source_label.setStyleSheet("border: 2px dashed #0078D7;")
                    return
    
    def dragLeaveEvent(self, event):
        """
        @brief Handle drag leave event
        @param event The drag leave event
        """
        self.source_label.setStyleSheet("")
    
    def dropEvent(self, event: QDropEvent):
        """
        @brief Handle drop event for drag-and-drop
        @param event The drop event
        """
        self.source_label.setStyleSheet("")
        
        if event.mimeData().hasUrls():
            for url in event.mimeData().urls():
                file_path = url.toLocalFile()
                if self._is_valid_image_file(file_path):
                    self._load_dropped_image(file_path)
                    event.acceptProposedAction()
                    break
    
    def _is_valid_image_file(self, file_path):
        """
        @brief Check if file is a valid image file
        @param file_path Path to the file
        @return True if file is a valid image file
        """
        _, ext = os.path.splitext(file_path.lower())
        return ext in ['.jpg', '.jpeg', '.png']
    
    def _load_dropped_image(self, file_path):
        """
        @brief Load an image dropped onto the application
        @param file_path Path to the image file
        """
        try:
            self.source_image = io.imread(file_path)
            self.show_image_in_label(self.source_label, self.source_image)
            self.menu_actions.current_source_path = file_path
            self.menu_actions.update_menu_states_based_on_image()
            self.statusBar().showMessage(f"Image loaded from {os.path.basename(file_path)}", 3000)
            
            # Add to command history
            self.add_to_command_history(f"Loaded image: {os.path.basename(file_path)}")
        except Exception as e:
            self.statusBar().showMessage(f"Error loading dropped image: {str(e)}", 3000)