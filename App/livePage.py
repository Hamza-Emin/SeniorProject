import cv2
import numpy as np
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QGraphicsView, QGraphicsScene
from numpy.core.defchararray import upper

from VideoAndLive.videoprocessor import VideoProcessor

class LivePage(QWidget):
    def __init__(self):
        super().__init__()
        self.video_processor = VideoProcessor()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.capture = cv2.VideoCapture(0)

        layout = QVBoxLayout()

        # Middle part with live feed viewers
        upper_layout = QHBoxLayout()

        # Input live feed viewer
        self.input_graphics_view = QGraphicsView()
        self.input_graphics_scene = QGraphicsScene()
        self.input_graphics_view.setScene(self.input_graphics_scene)
        # Apply transparency to input view
        self.input_graphics_view.setStyleSheet("""
                            background: transparent;
                            border: 4px dashed rgba(0, 0, 255, 70);
                        """)
        self.input_graphics_scene.setBackgroundBrush(Qt.transparent)
        upper_layout.addWidget(self.input_graphics_view)

        # Processed live feed viewer
        self.output_graphics_view = QGraphicsView()
        self.output_graphics_scene = QGraphicsScene()
        self.output_graphics_view.setScene(self.output_graphics_scene)
        # Apply transparency to output view
        self.output_graphics_view.setStyleSheet("""
                    background: transparent;
                    border: 4px dashed rgba(0, 0, 255, 70);
                """)
        self.output_graphics_scene.setBackgroundBrush(Qt.transparent)
        upper_layout.addWidget(self.output_graphics_view)

        layout.addLayout(upper_layout)

        # Bottom part with buttons
        bottom_layout = QHBoxLayout()


        start_button = QPushButton("Start Live Feed")
        start_button.setFixedSize(150, 40)
        start_button.clicked.connect(self.start_live_feed)
        bottom_layout.addWidget(start_button)

        stop_button = QPushButton("Stop Live Feed")
        stop_button.setFixedSize(150, 40)
        stop_button.clicked.connect(self.stop_live_feed)
        bottom_layout.addWidget(stop_button)

        layout.addLayout(bottom_layout)

        self.setLayout(layout)

    def start_live_feed(self):
        if not self.capture.isOpened():
            self.capture.open(0)
        self.timer.start(30)  # Update frame every 30 ms

    def stop_live_feed(self):
        self.timer.stop()
        if self.capture.isOpened():
            self.capture.release()

    def update_frame(self):
        ret, frame = self.capture.read()
        if not ret:
            return

        # Display the original frame
        self.display_frame(self.input_graphics_scene, frame)

        # Process the frame using process_live_to_3d
        processed_frame = self.video_processor.process_live_to_3d(frame)

        # Display the processed frame
        self.display_frame(self.output_graphics_scene, processed_frame)

    def display_frame(self, scene, frame):
        height, width, channels = frame.shape
        bytes_per_line = channels * width
        q_image = QImage(frame.data, width, height, bytes_per_line, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(q_image)
        scene.clear()
        scene.addPixmap(pixmap)
