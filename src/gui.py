"""
sh0rtifier - GUI Interface (PyQt6)

Cross-platform GUI using PyQt6.
"""

import sys
from pathlib import Path
from typing import Optional

from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QApplication,
    QButtonGroup,
    QDoubleSpinBox,
    QFileDialog,
    QFrame,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QMessageBox,
    QProgressBar,
    QPushButton,
    QRadioButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from core import ConversionOptions, VideoInfo, convert_to_shorts, get_video_info


class VideoProcessorThread(QThread):
    """Background thread for video processing"""

    progress_updated = pyqtSignal(float)
    processing_finished = pyqtSignal(Path)
    processing_failed = pyqtSignal(str)

    def __init__(self, processor, input_path, output_path, options):
        super().__init__()
        self.processor = processor
        self.input_path = input_path
        self.output_path = output_path
        self.options = options

    def run(self):
        try:
            # Use convert_to_shorts function directly
            def progress_callback(progress: float):
                self.progress_updated.emit(progress)

            result_path = convert_to_shorts(
                self.input_path, self.output_path, self.options, progress_callback
            )
            self.processing_finished.emit(result_path)
        except Exception as e:
            self.processing_failed.emit(str(e))


class ShortsConverterGUI(QMainWindow):
    """Main GUI application"""

    def __init__(self):
        super().__init__()

        # State
        self.input_file: Optional[Path] = None
        self.output_folder: Optional[Path] = None
        self.video_info: Optional[VideoInfo] = None
        self.is_processing = False
        self.processor_thread: Optional[VideoProcessorThread] = None

        self.init_ui()
        self.apply_styles()

    def init_ui(self):
        """Initialize UI components"""

        self.setWindowTitle("sh0rtifier")
        self.setMinimumSize(750, 700)
        self.resize(750, 750)

        # Central widget with scroll area
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Main layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        # Scroll area for content
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)

        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_layout.setSpacing(15)

        # === Title ===
        title_label = QLabel("sh0rtifier")
        title_font = QFont("Arial", 24, QFont.Weight.Bold)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        scroll_layout.addWidget(title_label)

        subtitle_label = QLabel("Convert 16:9 videos to 9:16 Shorts (max 60s)")
        subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        scroll_layout.addWidget(subtitle_label)

        scroll_layout.addSpacing(10)

        # === File Selection ===
        file_group = QGroupBox("Step 1: Select Video")
        file_layout = QVBoxLayout()

        self.file_path_label = QLabel("No file selected")
        self.file_path_label.setWordWrap(True)
        file_layout.addWidget(self.file_path_label)

        self.video_info_label = QLabel("")
        self.video_info_label.setStyleSheet("color: gray;")
        file_layout.addWidget(self.video_info_label)

        select_file_btn = QPushButton("📁 Browse Video File")
        select_file_btn.clicked.connect(self.select_input_file)
        file_layout.addWidget(select_file_btn)

        file_group.setLayout(file_layout)
        scroll_layout.addWidget(file_group)

        # === Output Folder ===
        output_group = QGroupBox("Step 2: Select Output Folder")
        output_layout = QVBoxLayout()

        self.output_path_label = QLabel("Same as input file")
        self.output_path_label.setWordWrap(True)
        output_layout.addWidget(self.output_path_label)

        select_output_btn = QPushButton("📁 Browse Output Folder")
        select_output_btn.clicked.connect(self.select_output_folder)
        output_layout.addWidget(select_output_btn)

        output_group.setLayout(output_layout)
        scroll_layout.addWidget(output_group)

        # === Options Section (dynamic) ===
        self.options_group = QGroupBox("Step 3: Conversion Options")
        self.options_layout = QVBoxLayout()
        self.create_default_options_ui()
        self.options_group.setLayout(self.options_layout)
        scroll_layout.addWidget(self.options_group)

        # Add stretch to push content to top
        scroll_layout.addStretch()

        scroll.setWidget(scroll_content)
        main_layout.addWidget(scroll)

        # === Progress Bar (outside scroll) ===
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        main_layout.addWidget(self.progress_bar)

        self.status_label = QLabel("Ready")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setStyleSheet("color: #ffffff; font-size: 13px;")
        main_layout.addWidget(self.status_label)

        # === Convert Button ===
        self.convert_btn = QPushButton("🎬 Convert to Shorts")
        self.convert_btn.setEnabled(False)
        self.convert_btn.clicked.connect(self.start_conversion)
        self.convert_btn.setMinimumHeight(40)
        main_layout.addWidget(self.convert_btn)

        # Menu bar
        self.create_menu_bar()

    def create_menu_bar(self):
        """Create menu bar"""
        menubar = self.menuBar()

        # File menu
        file_menu = menubar.addMenu("&File")

        open_action = file_menu.addAction("&Open Video")
        open_action.triggered.connect(self.select_input_file)

        file_menu.addSeparator()

        exit_action = file_menu.addAction("E&xit")
        exit_action.triggered.connect(self.close)

        # Help menu
        help_menu = menubar.addMenu("&Help")

        about_action = help_menu.addAction("&About")
        about_action.triggered.connect(self.show_about)

    def create_default_options_ui(self):
        """Create default options UI (no video selected)"""
        # Clear existing widgets
        while self.options_layout.count():
            child = self.options_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        info_label = QLabel("Select a video file to see conversion options")
        info_label.setStyleSheet("color: gray; font-style: italic;")
        self.options_layout.addWidget(info_label)

    def create_options_ui_for_short_video(self):
        """Create options UI for videos under 60 seconds"""
        # Clear existing widgets
        while self.options_layout.count():
            child = self.options_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        info_label = QLabel(
            "✓ Video is under 60 seconds - will convert as-is with optimal settings"
        )
        info_label.setStyleSheet("color: green; font-weight: bold;")
        self.options_layout.addWidget(info_label)

    def create_options_ui_for_long_video(self):
        """Create options UI for videos over 60 seconds"""
        # Clear existing widgets
        while self.options_layout.count():
            child = self.options_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        # Warning
        warning_label = QLabel(f"⚠️  Video is {self.video_info.duration:.1f}s (over 60s limit)")
        warning_label.setStyleSheet("color: orange; font-weight: bold;")
        self.options_layout.addWidget(warning_label)

        # Mode selection
        mode_label = QLabel("Select conversion mode:")
        mode_label.setStyleSheet("font-weight: bold; margin-top: 10px;")
        self.options_layout.addWidget(mode_label)

        self.mode_group = QButtonGroup()

        speed_radio = QRadioButton("Speed Adjustment (Recommended)")
        speed_radio.setChecked(True)
        speed_radio.toggled.connect(self.update_options_visibility)
        self.mode_group.addButton(speed_radio, 1)
        self.options_layout.addWidget(speed_radio)

        segment_radio = QRadioButton("Select Specific Segment")
        segment_radio.toggled.connect(self.update_options_visibility)
        self.mode_group.addButton(segment_radio, 2)
        self.options_layout.addWidget(segment_radio)

        # === Speed Options ===
        self.speed_widget = QWidget()
        speed_layout = QVBoxLayout(self.speed_widget)
        speed_layout.setContentsMargins(20, 10, 0, 10)

        speed_label = QLabel("Speed Multiplier:")
        speed_layout.addWidget(speed_label)

        speed_control_layout = QHBoxLayout()

        suggested_speed = self.video_info.duration / 59.0
        self.speed_spinbox = QDoubleSpinBox()
        self.speed_spinbox.setRange(1.0, 4.0)
        self.speed_spinbox.setSingleStep(0.1)
        self.speed_spinbox.setValue(suggested_speed)
        self.speed_spinbox.setDecimals(2)
        self.speed_spinbox.setSuffix("x")
        self.speed_spinbox.valueChanged.connect(self.update_speed_label)
        speed_control_layout.addWidget(self.speed_spinbox)

        self.speed_result_label = QLabel()
        self.update_speed_label()
        speed_control_layout.addWidget(self.speed_result_label)
        speed_control_layout.addStretch()

        speed_layout.addLayout(speed_control_layout)

        suggested_btn = QPushButton(f"Use Suggested ({suggested_speed:.2f}x)")
        suggested_btn.clicked.connect(lambda: self.speed_spinbox.setValue(suggested_speed))
        speed_layout.addWidget(suggested_btn)

        self.options_layout.addWidget(self.speed_widget)

        # === Segment Options ===
        self.segment_widget = QWidget()
        segment_layout = QVBoxLayout(self.segment_widget)
        segment_layout.setContentsMargins(20, 10, 0, 10)

        # Start time
        start_layout = QHBoxLayout()
        start_layout.addWidget(QLabel("Start Time (seconds):"))
        self.start_spinbox = QDoubleSpinBox()
        self.start_spinbox.setRange(0, self.video_info.duration - 1)
        self.start_spinbox.setValue(0)
        self.start_spinbox.setDecimals(1)
        start_layout.addWidget(self.start_spinbox)
        start_layout.addStretch()
        segment_layout.addLayout(start_layout)

        # Duration
        duration_layout = QHBoxLayout()
        duration_layout.addWidget(QLabel("Duration (seconds):"))
        self.duration_spinbox = QDoubleSpinBox()
        self.duration_spinbox.setRange(1, 60)
        self.duration_spinbox.setValue(min(60, self.video_info.duration))
        self.duration_spinbox.setDecimals(1)
        duration_layout.addWidget(self.duration_spinbox)
        duration_layout.addStretch()
        segment_layout.addLayout(duration_layout)

        self.options_layout.addWidget(self.segment_widget)

        # Initial visibility
        self.update_options_visibility()

    def update_options_visibility(self):
        """Update which options are visible based on mode"""
        if not hasattr(self, "mode_group"):
            return

        mode = self.mode_group.checkedId()

        self.speed_widget.setVisible(mode == 1)
        self.segment_widget.setVisible(mode == 2)

    def update_speed_label(self):
        """Update speed result label"""
        if not self.video_info:
            return

        speed = self.speed_spinbox.value()
        output_duration = self.video_info.duration / speed
        self.speed_result_label.setText(f"→ {output_duration:.1f}s output")

    def select_input_file(self):
        """Open file dialog to select input video"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Video File",
            "",
            "Video Files (*.mp4 *.mov *.mkv *.avi *.webm);;All Files (*)",
        )

        if file_path:
            self.input_file = Path(file_path)
            self.file_path_label.setText(str(self.input_file))

            # Load video info
            try:
                self.video_info = get_video_info(self.input_file)
                info_text = (
                    f"Duration: {self.video_info.duration:.1f}s | "
                    f"Resolution: {self.video_info.width}x{self.video_info.height}"
                )
                self.video_info_label.setText(info_text)

                # Update options UI based on duration
                if self.video_info.is_short:
                    self.create_options_ui_for_short_video()
                else:
                    self.create_options_ui_for_long_video()

                # Enable convert button
                self.convert_btn.setEnabled(True)

                # Set default output folder
                if not self.output_folder:
                    self.output_folder = self.input_file.parent
                    self.output_path_label.setText(str(self.output_folder))

            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to load video info:\n{str(e)}")
                self.input_file = None
                self.video_info = None

    def select_output_folder(self):
        """Open dialog to select output folder"""
        folder_path = QFileDialog.getExistingDirectory(self, "Select Output Folder")

        if folder_path:
            self.output_folder = Path(folder_path)
            self.output_path_label.setText(str(self.output_folder))

    def get_conversion_options(self) -> ConversionOptions:
        """Get conversion options from UI"""
        if self.video_info.is_short:
            return ConversionOptions()

        mode = self.mode_group.checkedId()

        if mode == 1:  # Speed mode
            return ConversionOptions(speed=self.speed_spinbox.value())
        else:  # Segment mode
            return ConversionOptions(
                start_time=self.start_spinbox.value(), duration=self.duration_spinbox.value()
            )

    def start_conversion(self):
        """Start video conversion in background thread"""
        if self.is_processing:
            return

        if not self.input_file or not self.video_info:
            QMessageBox.critical(self, "Error", "Please select a video file first")
            return

        # Get options
        try:
            options = self.get_conversion_options()

            # Validate
            is_valid, error_msg = options.validate(self.video_info)
            if not is_valid:
                QMessageBox.critical(self, "Validation Error", error_msg)
                return

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Invalid options:\n{str(e)}")
            return

        # Determine output path
        output_path = self.output_folder / f"{self.input_file.stem}_shorts.mp4"

        # Confirm overwrite if exists
        if output_path.exists():
            reply = QMessageBox.question(
                self,
                "File Exists",
                f"File already exists:\n{output_path.name}\n\nOverwrite?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            )
            if reply == QMessageBox.StandardButton.No:
                return

        # Disable UI
        self.is_processing = True
        self.convert_btn.setEnabled(False)
        self.status_label.setText("Converting...")
        self.progress_bar.setValue(0)
        self.progress_bar.setVisible(True)

        # Start conversion thread
        self.processor_thread = VideoProcessorThread(None, self.input_file, output_path, options)
        self.processor_thread.progress_updated.connect(self.update_progress)
        self.processor_thread.processing_finished.connect(self.on_conversion_complete)
        self.processor_thread.processing_failed.connect(self.on_conversion_error)
        self.processor_thread.start()

    def update_progress(self, progress: float):
        """Update progress bar"""
        self.progress_bar.setValue(int(progress))

    def on_conversion_complete(self, output_path: Path):
        """Called when conversion completes successfully"""
        self.is_processing = False
        self.convert_btn.setEnabled(True)
        self.status_label.setText("✓ Conversion complete!")
        self.progress_bar.setValue(100)

        QMessageBox.information(
            self, "Success", f"Video converted successfully!\n\nSaved to:\n{output_path}"
        )

        self.progress_bar.setVisible(False)
        self.progress_bar.setValue(0)

    def on_conversion_error(self, error_msg: str):
        """Called when conversion fails"""
        self.is_processing = False
        self.convert_btn.setEnabled(True)
        self.status_label.setText("✗ Conversion failed")
        self.progress_bar.setVisible(False)

        QMessageBox.critical(self, "Conversion Error", f"Failed to convert video:\n\n{error_msg}")

    def show_about(self):
        """Show about dialog"""
        QMessageBox.about(
            self,
            "About sh0rtifier",
            "<h2>sh0rtifier</h2>"
            "<p>Version 1.0.0-dev0</p>"
            "<p>Convert 16:9 videos to 9:16 YouTube Shorts (max 60s)</p>"
            "<p>© 2025 sl0thm4n</p>"
            "<p><a href='https://github.com/sl0thm4n/sh0rtifier'>GitHub</a></p>",
        )

    def apply_styles(self):
        """Apply custom stylesheet"""
        self.setStyleSheet(
            """
            QMainWindow {
                background-color: #2b2b2b;
            }
            QWidget {
                background-color: #2b2b2b;
                color: #ffffff;
            }
            QScrollArea {
                background-color: #2b2b2b;
                border: none;
            }
            QLabel {
                color: #ffffff;
            }
            QGroupBox {
                font-weight: bold;
                color: #ffffff;
                border: 2px solid #4a4a4a;
                border-radius: 6px;
                margin-top: 12px;
                padding-top: 15px;
                background-color: #333333;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 15px;
                padding: 0 8px;
                color: #4da6ff;
            }
            QPushButton {
                background-color: #0066cc;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px 20px;
                font-weight: bold;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #0052a3;
            }
            QPushButton:pressed {
                background-color: #003d7a;
            }
            QPushButton:disabled {
                background-color: #555555;
                color: #999999;
            }
            QRadioButton {
                color: #ffffff;
                spacing: 8px;
            }
            QRadioButton::indicator {
                width: 18px;
                height: 18px;
            }
            QRadioButton::indicator:checked {
                background-color: #0066cc;
                border: 2px solid #0066cc;
                border-radius: 9px;
            }
            QRadioButton::indicator:unchecked {
                background-color: #555555;
                border: 2px solid #777777;
                border-radius: 9px;
            }
            QDoubleSpinBox {
                background-color: #3d3d3d;
                color: #ffffff;
                border: 1px solid #555555;
                border-radius: 3px;
                padding: 5px;
            }
            QDoubleSpinBox::up-button, QDoubleSpinBox::down-button {
                background-color: #555555;
                border: none;
                width: 18px;
            }
            QDoubleSpinBox::up-button:hover, QDoubleSpinBox::down-button:hover {
                background-color: #666666;
            }
            QProgressBar {
                border: 2px solid #555555;
                border-radius: 6px;
                text-align: center;
                height: 28px;
                background-color: #3d3d3d;
                color: #ffffff;
                font-weight: bold;
                font-size: 14px;
            }
            QProgressBar::chunk {
                background-color: #0066cc;
                border-radius: 4px;
            }
            QMenuBar {
                background-color: #2b2b2b;
                color: #ffffff;
            }
            QMenuBar::item:selected {
                background-color: #0066cc;
            }
            QMenu {
                background-color: #2b2b2b;
                color: #ffffff;
                border: 1px solid #555555;
            }
            QMenu::item:selected {
                background-color: #0066cc;
            }
        """
        )


def main():
    """Main entry point for GUI"""
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    window = ShortsConverterGUI()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
