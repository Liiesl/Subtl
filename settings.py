from PyQt5.QtWidgets import QFileDialog

class Settings(QWidget):
    settings_saved = pyqtSignal()  # Define a signal for settings saved

    def __init__(self, parent=None, back_callback=None):
        super().__init__(parent)
        self.back_callback = back_callback
        self.config = Config()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Back to Home button
        back_button = QPushButton("Back to Home")
        back_button.clicked.connect(self.back_callback)
        layout.addWidget(back_button)

        # Safe Area Slider
        safe_area_layout = QHBoxLayout()
        safe_area_label = QLabel("Safe Area Size (px):")
        safe_area_label.setStyleSheet("color: white; font-size: 26px;")
        safe_area_layout.addWidget(safe_area_label)

        self.safe_area_slider = QSlider(Qt.Horizontal)
        self.safe_area_slider.setMinimum(0)
        self.safe_area_slider.setMaximum(100)
        self.safe_area_slider.setValue(self.config.get_safe_area_size())
        self.safe_area_slider.setTickInterval(10)
        self.safe_area_slider.setTickPosition(QSlider.TicksBelow)
        self.safe_area_slider.valueChanged.connect(self.update_safe_area)
        safe_area_layout.addWidget(self.safe_area_slider)

        self.safe_area_value_label = QLabel(f"{self.config.get_safe_area_size()} px")
        self.safe_area_value_label.setStyleSheet("color: white;")
        safe_area_layout.addWidget(self.safe_area_value_label)

        layout.addLayout(safe_area_layout)

        # Text Size Dropdown
        text_size_layout = QHBoxLayout()
        text_size_label = QLabel("Text Size:")
        text_size_label.setStyleSheet("color: white; font-size: 26px;")
        text_size_layout.addWidget(text_size_label)

        self.text_size_dropdown = QComboBox()
        self.text_size_dropdown.addItems(["small", "default", "large", "huge"])
        self.text_size_dropdown.setCurrentText(self.config.get_text_size())
        self.text_size_dropdown.currentTextChanged.connect(self.update_text_size)
        text_size_layout.addWidget(self.text_size_dropdown)

        layout.addLayout(text_size_layout)

        # Default Save Directory
        save_dir_layout = QHBoxLayout()
        save_dir_label = QLabel("Default Save Directory:")
        save_dir_label.setStyleSheet("color: white; font-size: 26px;")
        save_dir_layout.addWidget(save_dir_label)

        self.save_dir_button = QPushButton("Choose Directory")
        self.save_dir_button.clicked.connect(self.choose_save_directory)
        save_dir_layout.addWidget(self.save_dir_button)

        self.save_dir_value_label = QLabel(self.config.get_default_save_directory())
        self.save_dir_value_label.setStyleSheet("color: white;")
        save_dir_layout.addWidget(self.save_dir_value_label)

        layout.addLayout(save_dir_layout)

        # Save button
        save_button = QPushButton("Save")
        save_button.clicked.connect(self.save_settings)
        layout.addWidget(save_button)

        self.setLayout(layout)
        self.setStyleSheet("background-color: #2c2f38;")

        # Apply button styles
        self.apply_button_styles([back_button, save_button, self.save_dir_button])

    def apply_button_styles(self, buttons):
        for button in buttons:
            button.setStyleSheet("""
                QPushButton {
                    border: 2px solid #4f86f7; /* Thicker edge line */
                    color: white;
                    border-radius: 10px;
                    padding: 10px;
                    min-height: 40px;
                    background-color: #4f86f7; /* Accented blue color */
                    text-align: center; /* Center align text */
                }
                QPushButton:hover {
                    border-color: #3a6dbf;
                    background-color: #3a6dbf; /* Darker blue on hover */
                }
            """)

    def update_safe_area(self, value):
        self.safe_area_value_label.setText(f"{value} px")

    def update_text_size(self, size):
        self.config.set_text_size(size)
        self.apply_text_size_to_all_pages()

    def apply_text_size_to_all_pages(self):
        # Trigger the text size update in the main window
        self.settings_saved.emit()

    def choose_save_directory(self):
        directory = QFileDialog.getExistingDirectory(self, "Choose Directory", self.config.get_default_save_directory())
        if directory:
            self.config.set_default_save_directory(directory)
            self.save_dir_value_label.setText(directory)

    def save_settings(self):
        self.config.set_safe_area_size(self.safe_area_slider.value())
        self.config.set_text_size(self.text_size_dropdown.currentText())
        self.settings_saved.emit()  # Emit the settings_saved signal
        QMessageBox.information(self, "Success", "Settings saved successfully!")
        self.back_callback()
