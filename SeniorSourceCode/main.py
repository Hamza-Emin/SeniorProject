import sys
import cv2
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QTimer
from stacked_widget_ui import Ui_MainWindow  # Adjust the import based on the generated file name
import webbrowser

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # Connect the main page buttons to switch to respective pages
        self.pushButton_toPage1.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(1))
        self.pushButton_toPage2.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(2))
        self.pushButton_toPage3.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(3))

        # Connect the back buttons on each page to return to the main page
        self.pushButton_backFromPage1.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(0))
        self.pushButton_backFromPage2.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(0))
        self.pushButton_backFromPage3.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(0))

        self.pushButton_3.clicked.connect(self.open_web_page)

        # Set up the camera feeds on Page 1
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.cap = cv2.VideoCapture(0)
        self.timer.start(30)

        # Apply background image to each page
        image_path = r"C:\Users\HAMZA\Desktop\d\bc.jpeg".replace("\\", "/")
        self.apply_background_image(self.stackedWidget.widget(0), image_path)
        self.apply_background_image(self.stackedWidget.widget(1), image_path)
        self.apply_background_image(self.stackedWidget.widget(2), image_path)
        self.apply_background_image(self.stackedWidget.widget(3), image_path)

    def apply_background_image(self, widget, image_path):
        widget.setStyleSheet(f"""
            background-image: url({image_path});
            background-repeat: no-repeat;
            background-position: center;
        """)
    def open_web_page(self):
        webbrowser.open("https://hamza-emin.github.io/SeniorProject/", new=2)

    def update_frame(self):
        ret, frame = self.cap.read()
        if ret:
            # Display original frame
            original_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            height, width, channel = original_image.shape
            step = channel * width
            q_original_image = QImage(original_image.data, width, height, step, QImage.Format_RGB888)
            self.label_camera1.setPixmap(QPixmap.fromImage(q_original_image))

            # Create 3D effect
            left_image = frame.copy()
            right_image = np.roll(frame, shift=5, axis=1)  # Slightly shift the image for stereo effect

            # Apply red-cyan filters
            left_image[:, :, 1] = 0  # Remove green
            left_image[:, :, 2] = 0  # Remove blue

            right_image[:, :, 0] = 0  # Remove red
            right_image[:, :, 1] = right_image[:, :, 1]  # Keep green
            right_image[:, :, 2] = right_image[:, :, 2]  # Keep blue

            # Combine images
            combined_image = cv2.addWeighted(left_image, 0.5, right_image, 0.5, 0)

            # Convert to QImage
            filtered_image = cv2.cvtColor(combined_image, cv2.COLOR_BGR2RGB)
            height, width, channel = filtered_image.shape
            step = channel * width
            q_filtered_image = QImage(filtered_image.data, width, height, step, QImage.Format_RGB888)
            self.label_camera2.setPixmap(QPixmap.fromImage(q_filtered_image))

    def closeEvent(self, event):
        self.cap.release()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
