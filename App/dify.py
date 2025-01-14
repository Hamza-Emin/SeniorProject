import sys
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QHBoxLayout,
    QLabel,
    QStackedWidget,
    QFileDialog,
    QDialog,
    QRadioButton,
    QButtonGroup,
    QSizePolicy,
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtCore import QUrl


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyQt5 App with Image and Buttons on Bar")
        self.setGeometry(100, 100, 1200, 800)  # Set the position and size of the window

        # Create the central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Create the main horizontal layout
        main_layout = QHBoxLayout()

        # Create the left bar layout
        left_bar_layout = QVBoxLayout()

        # Create buttons one by one
        self.page_stack = QStackedWidget()  # Stacked widget for pages

        # Image Button and Page
        image_button = QPushButton("Image")
        image_button.setFixedSize(60, 60)
        image_button.setStyleSheet(self.get_button_stylesheet("#B9E5E8"))
        image_button.clicked.connect(self.show_image_page)
        left_bar_layout.addWidget(image_button)

        image_page = self.create_image_page()
        self.page_stack.addWidget(image_page)

        # Video Button and Page
        video_button = QPushButton("Video")
        video_button.setFixedSize(60, 60)
        video_button.setStyleSheet(self.get_button_stylesheet("#A8D5BA"))
        video_button.clicked.connect(self.show_video_page)
        left_bar_layout.addWidget(video_button)

        video_page = self.create_video_page()
        self.page_stack.addWidget(video_page)

        # Live Button and Page
        live_button = QPushButton("Live")
        live_button.setFixedSize(60, 60)
        live_button.setStyleSheet(self.get_button_stylesheet("#F3C5C5"))
        live_button.clicked.connect(self.show_live_page)
        left_bar_layout.addWidget(live_button)

        live_page = self.create_live_page()
        self.page_stack.addWidget(live_page)

        # Help Button and Page
        help_button = QPushButton("Help")
        help_button.setFixedSize(60, 60)
        help_button.setStyleSheet(self.get_button_stylesheet("#FFFFFF  "))
        help_button.clicked.connect(lambda: self.switch_page(3))
        left_bar_layout.addWidget(help_button)

        help_page = self.create_page("Help", "#FDE68A")
        self.page_stack.addWidget(help_page)

        # Website Button and Action
        website_button = QPushButton("Website")
        website_button.setFixedSize(60, 60)
        website_button.setStyleSheet(self.get_button_stylesheet("#FFA69E"))
        website_button.clicked.connect(self.open_website)
        left_bar_layout.addWidget(website_button)

        website_page = self.create_page("Website", "#FFA69E")
        self.page_stack.addWidget(website_page)

        # Add left bar to the main layout
        left_bar_widget = QWidget()
        left_bar_widget.setLayout(left_bar_layout)
        #left_bar_widget.setStyleSheet("background-color: #DFF2EB;")  # Set the desired color for the bar
        main_layout.addWidget(left_bar_widget)

        # Add the stacked widget to the main layout
        main_layout.addWidget(self.page_stack)

        # Set the main layout for the central widget
        central_widget.setLayout(main_layout)

        # Start with the first page
        self.page_stack.setCurrentIndex(0)

    def switch_page(self, index):
        """Switch to the page with the given index."""
        self.page_stack.setCurrentIndex(index)

    def create_image_page(self):
        """Create the Image page."""
        page = QWidget()
        layout = QVBoxLayout()

        # Upper part with buttons and file location
        upper_widget = QWidget()
        upper_widget.setStyleSheet("""
                background-color: #F5F5F5;
                border-radius: 10px;
                padding: 10px;
            """)
        upper_layout = QHBoxLayout()

        self.choose_button = QPushButton("Choose")
        self.choose_button.setFixedSize(80, 40)
        self.choose_button.clicked.connect(self.open_file_dialog)
        upper_layout.addWidget(self.choose_button, alignment=Qt.AlignLeft)

        self.file_label = QLabel("Image Location")
        self.file_label.setAlignment(Qt.AlignRight)
        self.file_label.setStyleSheet("color: black; font-size: 14px;")
        upper_layout.addWidget(self.file_label, alignment=Qt.AlignBaseline)

        layout.addLayout(upper_layout)
        layout.addStretch(1)  # Add stretch after the upper layout

        # Middle part with images
        middle_layout = QHBoxLayout()

        self.input_image_label = QLabel()
        self.input_image_label.setMinimumSize(400, 400)
        self.input_image_label.setStyleSheet("background-color: #D3D3D3; border: 1px solid black;")
        self.input_image_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        middle_layout.addWidget(self.input_image_label)

        self.output_image_label = QLabel()
        self.output_image_label.setMinimumSize(400, 400)
        self.output_image_label.setStyleSheet("background-color: #D3D3D3; border: 1px solid black;")
        self.output_image_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        middle_layout.addWidget(self.output_image_label)

        layout.addLayout(middle_layout)
        layout.addStretch(6)  # Add larger stretch for middle layout

        # Bottom part with buttons
        bottom_layout = QHBoxLayout()

        left_bottom_layout = QHBoxLayout()
        choose_window_button = QPushButton("Choose Process")
        choose_window_button.setFixedSize(150, 40)
        choose_window_button.clicked.connect(self.open_new_window)
        left_bottom_layout.addWidget(choose_window_button, alignment=Qt.AlignLeft)

        self.processing_label = QLabel("Selected Process: None")
        self.processing_label.setAlignment(Qt.AlignRight)
        self.processing_label.setStyleSheet("color: black; font-size: 14px;")
        left_bottom_layout.addWidget(self.processing_label, alignment=Qt.AlignBaseline)

        right_bottom_layout = QHBoxLayout()
        start_button = QPushButton("Start")
        start_button.setFixedSize(100, 40)
        start_button.clicked.connect(self.start_processing)
        right_bottom_layout.addWidget(start_button)

        save_button = QPushButton("Save")
        save_button.setFixedSize(100, 40)
        save_button.clicked.connect(self.save_output_image)
        right_bottom_layout.addWidget(save_button)

        bottom_layout.addLayout(left_bottom_layout)
        bottom_layout.addLayout(right_bottom_layout)

        layout.addLayout(bottom_layout)
        layout.addStretch(1)  # Add stretch after the bottom layout

        page.setLayout(layout)
        return page

    def resizeEvent(self, event):
        """Handle window resizing and adjust QLabel sizes."""
        super().resizeEvent(event)

        # Get the current window size
        window_width = self.width()
        window_height = self.height()

        # Set sizes dynamically based on conditions
        if window_width >= 1920 and window_height >= 1080:
            label_size = 600
        elif window_width >= 1300 and window_height >= 720:
            label_size = 500
        else:
            label_size = 400

            # Adjust the size of input and output image labels
        self.input_image_label.setFixedSize(label_size, label_size)
        self.output_image_label.setFixedSize(label_size, label_size)

    def open_file_dialog(self):
        """Open a file dialog to select an image."""
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Choose Image", "", "Images (*.png *.jpg *.jpeg *.bmp)", options=options)
        if file_path:
            self.file_label.setText(file_path)
            self.display_input_image(file_path)

    def display_input_image(self, file_path):
        """Display the chosen input image."""
        self.input_image_label.setStyleSheet(f"background-image: url({file_path}); background-position: center; background-repeat: no-repeat; background-size: contain;")

    def open_new_window(self):
        """Open a new window to choose a processing type."""
        dialog = QDialog(self)
        dialog.setWindowTitle("Choose Processing Type")
        dialog.setFixedSize(300, 200)

        layout = QVBoxLayout()

        processing_group = QButtonGroup(dialog)

        blur_option = QRadioButton("Blur")
        processing_group.addButton(blur_option)
        layout.addWidget(blur_option)

        sharpen_option = QRadioButton("Sharpen")
        processing_group.addButton(sharpen_option)
        layout.addWidget(sharpen_option)

        edge_option = QRadioButton("Edge Detection")
        processing_group.addButton(edge_option)
        layout.addWidget(edge_option)

        apply_button = QPushButton("Apply")
        apply_button.clicked.connect(lambda: self.set_processing(dialog, processing_group))
        layout.addWidget(apply_button)

        dialog.setLayout(layout)
        dialog.exec_()

    def set_processing(self, dialog, processing_group):
        """Set the chosen processing type."""
        selected_button = processing_group.checkedButton()
        if selected_button:
            self.processing_label.setText(f"Selected Process: {selected_button.text()}")
        dialog.accept()

    def start_processing(self):
        """Start processing the image based on the selected option."""
        # Placeholder for processing logic
        pass

    def save_output_image(self):
        """Save the output image."""
        options = QFileDialog.Options()
        save_path, _ = QFileDialog.getSaveFileName(self, "Save Image", "", "Images (*.png *.jpg *.jpeg *.bmp)", options=options)
        if save_path:
            # Logic to save the output image to the selected path
            pass

    def create_video_page(self):
        """Create the Video page."""
        return self.create_page("Video", "#A8D5BA")

    def create_live_page(self):
        """Create the Live page."""
        return self.create_page("Live", "#F3C5C5")

    def show_image_page(self):
        """Show the Image page."""
        self.switch_page(0)

    def show_video_page(self):
        """Show the Video page."""
        self.switch_page(1)

    def show_live_page(self):
        """Show the Live page."""
        self.switch_page(2)

    def open_website(self):
        """Open a website in the default browser."""
        QDesktopServices.openUrl(QUrl("https://www.example.com"))

    def create_page(self, name, color):
        """Create a page with a given name and background color."""
        page = QWidget()
        page_layout = QVBoxLayout()
        page_label = QLabel(f"This is the {name} page")
        page_label.setAlignment(Qt.AlignCenter)
        page_label.setStyleSheet("color: black; font-size: 18px;")
        page_layout.addWidget(page_label)
        page.setLayout(page_layout)

        # Apply rounded edges to the page
        page.setStyleSheet(f"""
            background-color: {color};
            border-radius: 20px;  /* Rounded edges */
            padding: 10px;
        """)

        return page

    def get_button_stylesheet(self, color):
        """Return a stylesheet string for a button with the given color."""
        return f"""
            QPushButton {{
                background-color: {color};
                color: black;
                font-weight: bold;
                font-size: 14px;
                border: 0.5px solid #219ba4;
                border-radius: 20px;  /* Rounded for a circular effect */
            }}
            QPushButton:hover {{
                background-color: #E8E8E8;  /* Slightly different on hover */
            }}
            QPushButton:pressed {{
                background-color: #D0D0D0;  /* Darker when pressed */
                border: 2px solid #666666;
            }}
        """


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Set the global stylesheet for the app (including background color)
    app.setStyleSheet("""
        QMainWindow {
            background: qlineargradient(
                    spread:pad, x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(15, 82, 186, 255),  /* #0F52BA - Sapphire Blue */
                    stop:0.25 rgba(30, 144, 255, 255), /* #1E90FF - Dodger Blue */
                    stop:0.5 rgba(59, 153, 216, 255), /* #3B99D8 - Medium Blue */
                    stop:0.75 rgba(91, 179, 224, 255), /* #5BB3E0 - Light Blue */
                    stop:1 rgba(123, 198, 232, 255)  /* #7BC6E8 - Sky Blue */
                );


        }
        QPushButton {
        background-color: #1e92f6 ;
        border: 0.5px solid #1E90FF; /* Dodger Blue border */
        border-radius: 10px;
        padding: 5px 10px;
        }
        QPushButton:hover {
        background-color: #d3e9fd; /* Orange Red on hover */
    }
    """)

    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
