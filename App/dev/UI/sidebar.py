import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QHBoxLayout, QMainWindow, QLabel
)
from PyQt5.QtGui import QIcon, QPalette, QBrush, QLinearGradient, QColor
from PyQt5.QtCore import QSize, Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Sidebar Toggle Example")
        self.setGeometry(100, 100, 800, 600)

        # Main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        self.main_layout = QHBoxLayout(main_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)  # Remove padding

        # Sidebar
        self.sidebar = QWidget()
        self.sidebar.setFixedWidth(200)
        self.sidebar_layout = QVBoxLayout(self.sidebar)
        self.sidebar_layout.setContentsMargins(0, 0, 0, 0)

        # Set sidebar background gradient
        palette = self.sidebar.palette()
        gradient = QLinearGradient(0, 0, 0, self.sidebar.height())
        gradient.setColorAt(0.0, QColor(0, 0, 139, 179))  # Dark blue with 0.7 transparency
        gradient.setColorAt(1.0, QColor(25, 25, 112, 179))  # Slightly lighter blue with 0.7 transparency
        palette.setBrush(QPalette.Background, QBrush(gradient))
        self.sidebar.setAutoFillBackground(True)
        self.sidebar.setPalette(palette)

        # Toggle button
        self.toggle_button = QPushButton()
        self.toggle_button.setIcon(QIcon("menu-icon.png"))  # Replace with your icon path
        self.toggle_button.setIconSize(QSize(24, 24))
        self.toggle_button.setFixedHeight(40)
        self.toggle_button.clicked.connect(self.toggle_sidebar)
        self.sidebar_layout.addWidget(self.toggle_button)

        # Other buttons
        self.buttons = []
        for i in range(5):
            button = QPushButton(f"Button {i + 1}")
            button.setIcon(QIcon(f"icon-{i + 1}.png"))  # Replace with your icons
            button.setIconSize(QSize(24, 24))
            button.setFixedHeight(40)
            self.sidebar_layout.addWidget(button)
            self.buttons.append(button)

        self.sidebar_layout.addStretch()
        self.main_layout.addWidget(self.sidebar)

        # Main content area
        self.content = QWidget()
        self.content_layout = QVBoxLayout(self.content)
        self.content_label = QLabel("Right-side content")
        self.content_label.setAlignment(Qt.AlignCenter)
        self.content_layout.addWidget(self.content_label)
        self.main_layout.addWidget(self.content)

        self.is_expanded = True

    def toggle_sidebar(self):
        if self.is_expanded:
            self.sidebar.setFixedWidth(80)
            self.toggle_button.setText("")
            for button in self.buttons:
                button.setText("")
        else:
            self.sidebar.setFixedWidth(200)
            self.toggle_button.setText("≡")
            for i, button in enumerate(self.buttons):
                button.setText(f"Button {i + 1}")

        self.is_expanded = not self.is_expanded

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
