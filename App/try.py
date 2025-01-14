import sys

import cv2
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QStackedWidget,
    QWidget,
    QPushButton,
    QFileDialog,
    QGraphicsView,
    QGraphicsScene,
    QGraphicsPixmapItem,
    QDialog,
    QRadioButton,
    QButtonGroup,
    QSizePolicy, QCheckBox, QGroupBox,
)
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QPixmap, QImage, QDesktopServices
from imagePage import ImagePage
from livePage import LivePage
from videoPage import VideoPage


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("3DifyMe")
        self.setGeometry(100, 100, 1200, 800)

        # Create the main widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout()

        # Create and add the PageManager
        self.page_manager = PageManager()
        main_layout.addWidget(self.page_manager.left_bar)
        main_layout.addWidget(self.page_manager.page_stack)

        central_widget.setLayout(main_layout)

class PageManager:
    def __init__(self):
        # Create the stacked widget and left bar
        self.page_stack = QStackedWidget()
        self.left_bar = self.create_left_bar()

        # Add pages to the stacked widget
        self.image_page = ImagePage()
        self.page_stack.addWidget(self.image_page)

        self.video_page = VideoPage()
        self.page_stack.addWidget(self.video_page)

        self.live_page = LivePage()
        self.page_stack.addWidget(self.live_page)

        self.help_page = HelpPage()
        self.page_stack.addWidget(self.help_page)

        # Start with the first page
        self.page_stack.setCurrentIndex(0)

    def create_left_bar(self):
        layout = QVBoxLayout()

        # Add navigation buttons
        buttons = [
            ("Image", 0, "#B9E5E8"),
            ("Video", 1, "#A8D5BA"),
            ("Live", 2, "#F3C5C5"),
            ("Help", 3, "#FDE68A"),
        ]
        bSizeX,bSizeY = 80, 110

        for text, index, color in buttons:
            button = QPushButton(text)
            button.setFixedSize(bSizeX, bSizeY)
            button.setStyleSheet(self.get_button_stylesheet(color))
            button.clicked.connect(lambda _, idx=index: self.page_stack.setCurrentIndex(idx))
            layout.addWidget(button)

        # Website Button and Action
        website_button = QPushButton("Website")
        website_button.setFixedSize(bSizeX, bSizeY)
        website_button.setStyleSheet(self.get_button_stylesheet("#FFA69E"))
        website_button.clicked.connect(self.open_website)
        layout.addWidget(website_button)

        container = QWidget()
        container.setLayout(layout)
        return container

    @staticmethod
    def get_button_stylesheet(color):
        return f"""
            QPushButton {{
                background: qlineargradient(
                    spread:pad,
                    x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(1, 26, 47, 0.6), /* Slightly more opaque dark base */
                    stop:0.5 rgba(1, 26, 47, 0.3), /* Mid-tone with your color grade */
                    stop:1 rgba(20, 50, 80, 0.4) /* Complementary metallic highlight */
                );
                color: white; /* Bright text for contrast */
                font-weight: bold;
                font-size: 14px;
                border: 1px solid rgba(1, 26, 47, 0.6); /* Metallic matching border */
                border-radius: 8px; /* Slightly rounded corners */
                box-shadow: inset 1px 1px 2px rgba(255, 255, 255, 0.3), 
                            2px 2px 4px rgba(0, 0, 0, 0.6); /* Highlights and depth */
                padding: 5px;
            }}
            QPushButton:hover {{
                background: qlineargradient(
                    spread:pad,
                    x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(1, 26, 47, 0.4), /* Lighter hover effect */
                    stop:0.5 rgba(20, 50, 80, 0.5),
                    stop:1 rgba(30, 70, 100, 0.6) /* Slightly brighter highlight */
                );
                border: 1px solid rgba(20, 50, 80, 0.6); /* Brighter border */
            }}
            QPushButton:pressed {{
                background: qlineargradient(
                    spread:pad,
                    x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(1, 26, 47, 0.5), /* Darker pressed effect */
                    stop:0.5 rgba(10, 30, 50, 0.4),
                    stop:1 rgba(1, 26, 47, 0.6)
                );
                border: 1px solid rgba(1, 26, 47, 0.8); /* Stronger border */
                box-shadow: inset 2px 2px 4px rgba(0, 0, 0, 0.8); /* Deeper shadow */
            }}
        """

    def open_website(self):
        """Open a website in the default browser."""
        QDesktopServices.openUrl(QUrl("https://hamza-emin.github.io/SeniorProject/"))



class HelpPage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Help Page"))
        self.setLayout(layout)



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
