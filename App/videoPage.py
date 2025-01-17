import cv2
import numpy as np
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QGraphicsView, QGraphicsScene, QFileDialog, QMessageBox
from VideoAndLive.videoprocessor import VideoProcessor


class VideoPage(QWidget):
    def __init__(self):
        super().__init__()
        self.video_processor = VideoProcessor()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.capture = None
        self.video_writer = None

        self.selected_video_path = None
        self.output_video_path = 'processed_output.avi'
        self.total_frames = 0
        self.current_frame = 0

        layout = QVBoxLayout()

        # Upper part with buttons and file location
        upper_layout = QHBoxLayout()

        self.choose_button = QPushButton("Choose Video")
        self.choose_button.setFixedSize(150, 40)
        self.choose_button.clicked.connect(self.open_file_dialog)
        self.choose_button.setStyleSheet(self.get_button_stylesheet())
        upper_layout.addWidget(self.choose_button, alignment=Qt.AlignLeft)

        self.save_button = QPushButton("Save Processed Video")
        self.save_button.setFixedSize(200, 40)
        self.save_button.clicked.connect(self.open_save_dialog)
        self.save_button.setStyleSheet(self.get_button_stylesheet())
        upper_layout.addWidget(self.save_button, alignment=Qt.AlignBaseline)

        self.file_label = QLabel("Video Location")
        self.file_label.setAlignment(Qt.AlignRight)
        self.file_label.setStyleSheet("color: black; font-size: 14px;")
        upper_layout.addWidget(self.file_label, alignment=Qt.AlignBaseline)

        layout.addLayout(upper_layout)

        # Middle part with video viewers
        middle_layout = QHBoxLayout()

        # Unprocessed video viewer
        self.input_graphics_view = QGraphicsView()
        self.input_graphics_scene = QGraphicsScene()
        self.input_graphics_view.setScene(self.input_graphics_scene)
        self.input_graphics_view.setStyleSheet("""
                        background: transparent; 
                        border: 4px dashed qlineargradient(
                            spread:pad,
                            x1:0, y1:0, x2:1, y2:1,
                            stop:0 rgba(1, 26, 47, 0.6), /* Slightly more opaque dark base */
                            stop:0.5 rgba(1, 26, 47, 0.3), /* Mid-tone with your color grade */
                            stop:1 rgba(20, 50, 80, 0.4) /* Complementary metallic highlight */
                    );""")
        self.input_graphics_scene.setBackgroundBrush(Qt.transparent)
        middle_layout.addWidget(self.input_graphics_view)

        # Processed video viewer
        self.output_graphics_view = QGraphicsView()
        self.output_graphics_scene = QGraphicsScene()
        self.output_graphics_view.setScene(self.output_graphics_scene)
        self.output_graphics_view.setStyleSheet("""
                        background: transparent; 
                        border: 4px dashed qlineargradient(
                            spread:pad,
                            x1:0, y1:0, x2:1, y2:1,
                            stop:0 rgba(1, 26, 47, 0.6), /* Slightly more opaque dark base */
                            stop:0.5 rgba(1, 26, 47, 0.3), /* Mid-tone with your color grade */
                            stop:1 rgba(20, 50, 80, 0.4) /* Complementary metallic highlight */
                    );""")
        self.output_graphics_scene.setBackgroundBrush(Qt.transparent)
        middle_layout.addWidget(self.output_graphics_view)

        layout.addLayout(middle_layout)

        # Frame count label
        self.frame_count_label = QLabel("Frame: 0 / 0")
        self.frame_count_label.setAlignment(Qt.AlignCenter)
        self.frame_count_label.setStyleSheet("color: black; font-size: 16px; font-weight: bold;")
        layout.addWidget(self.frame_count_label)

        # Bottom part with buttons
        bottom_layout = QHBoxLayout()

        self.start_button = QPushButton("Start Processing")
        self.start_button.setFixedSize(150, 40)
        self.start_button.clicked.connect(self.start_processing)
        self.start_button.setStyleSheet(self.get_button_stylesheet())
        bottom_layout.addWidget(self.start_button)

        self.stop_button = QPushButton("Stop Processing")
        self.stop_button.setFixedSize(150, 40)
        self.stop_button.clicked.connect(self.stop_processing)
        self.stop_button.setStyleSheet(self.get_button_stylesheet())
        bottom_layout.addWidget(self.stop_button)

        layout.addLayout(bottom_layout)

        self.setLayout(layout)

    def open_file_dialog(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Choose Video", "", "Videos (*.mp4 *.avi *.mkv *.mov)", options=options)

        if file_path:
            self.file_label.setText(file_path)
            self.selected_video_path = file_path

    def open_save_dialog(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Processed Video As",
            "",
            "Videos (*.avi *.mp4)",
            options=options
        )
        if file_path:
            self.output_video_path = file_path
            QMessageBox.information(self, "Save Location Set", f"Processed video will be saved as: {self.output_video_path}")


    def start_processing(self):
        if self.selected_video_path:
            if not self.output_video_path:
                QMessageBox.warning(self, "Save Location Not Set", "Please choose a save location for the processed video.")
                return

            self.capture = cv2.VideoCapture(self.selected_video_path)
            self.total_frames = int(self.capture.get(cv2.CAP_PROP_FRAME_COUNT))
            self.current_frame = 0

            # Initialize the video writer
            frame_width = int(self.capture.get(cv2.CAP_PROP_FRAME_WIDTH))
            frame_height = int(self.capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
            frame_rate = self.capture.get(cv2.CAP_PROP_FPS)
            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            self.video_writer = cv2.VideoWriter(self.output_video_path, fourcc, frame_rate, (frame_width, frame_height))

            self.timer.start(30)  # Update frame every 30 ms
        else:
            QMessageBox.warning(self, "No Video Selected", "Please select a video file to process.")


    def stop_processing(self):
        self.timer.stop()
        if self.capture:
            self.capture.release()
            self.capture = None
        if self.video_writer:
            self.video_writer.release()
            self.video_writer = None
            QMessageBox.information(self, "Processing Complete", f"Processed video saved as: {self.output_video_path}")

    def update_frame(self):
        if not self.capture:
            return

        ret, frame = self.capture.read()
        if not ret:
            self.stop_processing()
            return

        self.current_frame += 1

        # Update the frame count label
        self.frame_count_label.setText(f"Frame: {self.current_frame} / {self.total_frames}")

        # Display the original frame
        self.display_frame(self.input_graphics_scene, frame)

        # Process the frame using the VideoProcessor
        processed_frame = self.video_processor.process_live_to_3d(frame)

        # Write the processed frame to the output video
        if self.video_writer:
            self.video_writer.write(processed_frame)

        # Display the processed frame
        self.display_frame(self.output_graphics_scene, processed_frame)

    def display_frame(self, scene, frame):
        height, width, channels = frame.shape
        bytes_per_line = channels * width
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert BGR to RGB
        q_image = QImage(frame_rgb.data, width, height, bytes_per_line, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(q_image)
        scene.clear()
        scene.addPixmap(pixmap)

    def resizeEvent(self, event):
        # Ensure the input and output views fit the scene rect properly on resize
        if not self.input_graphics_scene.sceneRect().isNull():
            self.input_graphics_view.fitInView(self.input_graphics_scene.sceneRect(), Qt.KeepAspectRatio)

        if not self.output_graphics_scene.sceneRect().isNull():
            self.output_graphics_view.fitInView(self.output_graphics_scene.sceneRect(), Qt.KeepAspectRatio)

        # Call the parent resize event
        super().resizeEvent(event)

    @staticmethod
    def get_button_stylesheet():
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