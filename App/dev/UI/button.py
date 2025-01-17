import sys
from PyQt5.QtWidgets import QApplication, QPushButton, QVBoxLayout, QMainWindow, QWidget
from PyQt5.QtCore import QSize


class StylishButtonApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Stylish and Responsive Button")
        self.setGeometry(200, 200, 400, 300)

        # Create a central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Create a button
        button = QPushButton("Click Me!")
        button.setMinimumSize(QSize(120, 40))

        # Style the button
        button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50; 
                color: white; 
                border: 2px solid #4CAF50; 
                border-radius: 10px;
                font-size: 16px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3e8e41;
                border: 2px solid #3e8e41;
            }
        """)

        # Connect button to an action
        button.clicked.connect(self.on_button_click)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(button)
        central_widget.setLayout(layout)

    def on_button_click(self):
        print("Button was clicked!")


# Run the application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = StylishButtonApp()
    window.show()
    sys.exit(app.exec_())
