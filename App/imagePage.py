import cv2
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QGraphicsView, QGraphicsScene, \
    QFileDialog, QDialog, QCheckBox, QGroupBox, QRadioButton, QMessageBox
from Image.contrast import adjust_brightness_contrast, apply_gamma_correction, equalize_histogram, process_image
from Image.depthandanaglyp import generate_depth_map, generate_anaglyph
from Image.noisehandling import process_temp_image
from Image.upscale import upscale_image
from TempImageSaver import TempImageSaver


class ImagePage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        # Upper part with buttons and file location
        upper_layout = QHBoxLayout()

        self.choose_button = QPushButton("Choose")
        self.choose_button.setFixedSize(80, 40)
        self.choose_button.setStyleSheet(self.get_button_stylesheet())
        self.choose_button.clicked.connect(self.open_file_dialog)
        upper_layout.addWidget(self.choose_button, alignment=Qt.AlignLeft)

        self.file_label = QLabel("Image Location")
        self.file_label.setAlignment(Qt.AlignRight)
        self.file_label.setStyleSheet("color: black; font-size: 14px;")
        upper_layout.addWidget(self.file_label, alignment=Qt.AlignBaseline)

        layout.addLayout(upper_layout)

        # Middle part with image viewers
        middle_layout = QHBoxLayout()

        # Input image viewer
        self.input_graphics_view = QGraphicsView()
        self.input_graphics_scene = QGraphicsScene()
        self.input_graphics_view.setScene(self.input_graphics_scene)

        # Apply transparency to input view
        self.input_graphics_view.setStyleSheet("""
                    background: transparent;
                    border: 4px dashed qlineargradient(
                        spread:pad,
                        x1:0, y1:0, x2:1, y2:1,
                        stop:0 rgba(1, 26, 47, 0.6), /* Slightly more opaque dark base */
                        stop:0.5 rgba(1, 26, 47, 0.3), /* Mid-tone with your color grade */
                        stop:1 rgba(20, 50, 80, 0.4) /* Complementary metallic highlight */
                    );
                """)
        self.input_graphics_scene.setBackgroundBrush(Qt.transparent)

        middle_layout.addWidget(self.input_graphics_view)

        # Output image viewer
        self.output_graphics_view = QGraphicsView()
        self.output_graphics_scene = QGraphicsScene()
        self.output_graphics_view.setScene(self.output_graphics_scene)

        # Apply transparency to output view
        self.output_graphics_view.setStyleSheet("""
                    background: transparent;
                    border: 4px dashed qlineargradient(
                        spread:pad,
                        x1:0, y1:0, x2:1, y2:1,
                        stop:0 rgba(1, 26, 47, 0.6), /* Slightly more opaque dark base */
                        stop:0.5 rgba(1, 26, 47, 0.3), /* Mid-tone with your color grade */
                        stop:1 rgba(20, 50, 80, 0.4) /* Complementary metallic highlight */
                    );
                """)
        self.output_graphics_scene.setBackgroundBrush(Qt.transparent)

        middle_layout.addWidget(self.output_graphics_view)

        layout.addLayout(middle_layout)

        # Bottom part with buttons
        bottom_layout = QHBoxLayout()

        choose_window_button = QPushButton("Choose Process")
        choose_window_button.setFixedSize(150, 40)
        choose_window_button.clicked.connect(self.open_new_window)
        choose_window_button.setStyleSheet(self.get_button_stylesheet())
        bottom_layout.addWidget(choose_window_button)

        start_button = QPushButton("Start")
        start_button.setFixedSize(100, 40)
        start_button.clicked.connect(self.start_processing)
        start_button.setStyleSheet(self.get_button_stylesheet())
        bottom_layout.addWidget(start_button)

        save_button = QPushButton("Save")
        save_button.setFixedSize(100, 40)
        save_button.clicked.connect(self.save_output_image)
        save_button.setStyleSheet(self.get_button_stylesheet())
        bottom_layout.addWidget(save_button)

        layout.addLayout(bottom_layout)
        self.setLayout(layout)

    def open_file_dialog(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Choose Image", "", "Images (*.png *.jpg *.jpeg *.bmp)",
                                                   options=options)

        if file_path:
            # Use OpenCV to read the image
            image = cv2.imread(file_path)
            if image is None:
                print("Failed to load image using OpenCV.")
                return

            # Store the OpenCV image and file path as instance variables
            self.selected_image = image
            self.selected_image_path = file_path

            # Convert the OpenCV image (BGR) to a format suitable for PyQt (RGB)
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            height, width, channels = image_rgb.shape
            bytes_per_line = channels * width
            q_image = QImage(image_rgb.data, width, height, bytes_per_line, QImage.Format_RGB888)

            # Display the image in a QLabel
            self.file_label.setText(self.selected_image_path)
            self.display_input_image(q_image)

    def display_input_image(self, file_path):
        pixmap = QPixmap(file_path)
        self.input_graphics_scene.clear()
        self.input_graphics_scene.addPixmap(pixmap)
        self.input_graphics_view.fitInView(self.input_graphics_scene.sceneRect(), Qt.KeepAspectRatio)

    def open_new_window(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Choose Processing Options")
        dialog.setFixedSize(300, 400)

        # Set semi-transparent background
        dialog.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)
        dialog.setStyleSheet("""
                QDialog {
                    background-color: rgba(0, 129, 255, 140);  /* Semi-transparent blue */
                    border-radius: 0px;  /* No rounded corners */
                }
                QCheckBox {
                    color: white;  /* White text for checkboxes */
                    font-size: 14px;
                }
                QPushButton {
                    background-color: #0078D7;  /* Blue button */
                    color: white;
                    font-size: 14px;
                    border: none;
                    border-radius: 10px;
                    padding: 5px;
                }
                QPushButton:hover {
                    background-color: #005BB5;  /* Darker blue on hover */
                }
            """)

        layout = QVBoxLayout()

        # Create checkboxes for techniques
        contrast_option = QCheckBox("Adjust Contrast")
        layout.addWidget(contrast_option)

        noise_option = QCheckBox("Noise Removal")
        layout.addWidget(noise_option)

        upscale_group = QGroupBox("Upscale Options")
        upscale_layout = QHBoxLayout()
        upscale_group.setMaximumHeight(100)

        upscale_x2 = QRadioButton("Upscale x2")
        upscale_layout.addWidget(upscale_x2)

        upscale_x4 = QRadioButton("Upscale x4")
        upscale_layout.addWidget(upscale_x4)

        upscale_x8 = QRadioButton("Upscale x8")
        upscale_layout.addWidget(upscale_x8)

        upscale_group.setLayout(upscale_layout)
        layout.addWidget(upscale_group)

        depth_option = QCheckBox("Depth Map and Anaglyph")
        layout.addWidget(depth_option)

        apply_button = QPushButton("Apply")
        apply_button.clicked.connect(lambda: self.set_processing(dialog, {
            "contrast": contrast_option.isChecked(),
            "noise": noise_option.isChecked(),
            "upscale": 2 if upscale_x2.isChecked() else 4 if upscale_x4.isChecked() else 8 if upscale_x8.isChecked() else None,
            "depth": depth_option.isChecked()
        }))
        layout.addWidget(apply_button)

        dialog.setLayout(layout)
        dialog.exec_()

    def set_processing(self, dialog, form_data):
        self.selected_process = {}

        # Map selected techniques to values
        selected_techniques = []

        if form_data["contrast"]:
            selected_techniques.append("Adjust Contrast")

        if form_data["noise"]:
            selected_techniques.append("Noise Removal")

        if form_data["upscale"]:
            selected_techniques.append(f"Upscale x{form_data['upscale']}")

        if form_data["depth"]:
            selected_techniques.append("Depth Map and Anaglyph")

        self.selected_process["techniques"] = selected_techniques

        dialog.accept()

    # Start processing selected techniques
    def start_processing(self):
        """if not hasattr(self, 'selected_process') or not self.selected_process:
            return  # No process selected"""

        self.temp_path = TempImageSaver.save_temp_image(self.selected_image)
        # Retrieve selected process data
        selected_techniques = self.selected_process.get("techniques", [])

        # Check and process each technique individually
        if "Adjust Contrast" in selected_techniques:
            print("Processing: Adjust Contrast")
            self.adjust_contrast()

        if "Noise Removal" in selected_techniques:
            print("Processing: Noise Removal")
            self.remove_noise()

        upscale_technique = next((technique for technique in selected_techniques if technique.startswith("Upscale x")),
                                 None)
        if upscale_technique:
            upscale_factor = int(upscale_technique.split("x")[1])
            print(f"Processing: Upscale x{upscale_factor}")
            self.upscale_image(upscale_factor)

        if "Depth Map and Anaglyph" in selected_techniques:
            print("Processing: Depth Map and Anaglyph")
            self.generate_depth_map_and_anaglyph()

        generated_image = cv2.imread(self.temp_path)
        self.display_output_image(QPixmap.fromImage(TempImageSaver.convert_cv_to_qimage(generated_image)))


    def adjust_contrast(self):
        """
        Adjust Contrast
        """
        if not hasattr(self, 'temp_path') or self.temp_path is None:
            print("No valid temporary path found.")
            return
        try:
            adjusted_image = process_image(self.temp_path)
            self.temp_path = TempImageSaver.save_temp_image(adjusted_image)
            print(f"Depth map and anaglyph image generated and saved temporarily at {self.temp_path}.")
            self.display_output_image(QPixmap.fromImage(TempImageSaver.convert_cv_to_qimage(adjusted_image)))
        except Exception as e:
            # Display the error using a message box
            error_message = QMessageBox()
            error_message.setIcon(QMessageBox.Critical)
            error_message.setWindowTitle("Error")
            error_message.setText("An error occurred during depth map and anaglyph generation.")
            error_message.setInformativeText(str(e))
            error_message.exec_()



    def generate_depth_map_and_anaglyph(self):
        """
        Generate a depth map and an anaglyph image from the selected image.
        """
        if not hasattr(self, 'temp_path') or self.temp_path is None:
            print("No valid temporary path found.")
            return
        try:
            depth_map = generate_depth_map(self.temp_path)
            anaglyph_image = generate_anaglyph(self.temp_path, depth_map)
            self.temp_path = TempImageSaver.save_temp_image(anaglyph_image)
            print(f"Depth map and anaglyph image generated and saved temporarily at {self.temp_path}.")
            self.display_output_image(QPixmap.fromImage(TempImageSaver.convert_cv_to_qimage(anaglyph_image)))
            #self.display_output_image(QPixmap.fromImage(QImage(anaglyph_image)))
        except Exception as e:
            # Display the error using a message box
            error_message = QMessageBox()
            error_message.setIcon(QMessageBox.Critical)
            error_message.setWindowTitle("Error")
            error_message.setText("An error occurred during depth map and anaglyph generation.")
            error_message.setInformativeText(str(e))
            error_message.exec_()

    def remove_noise(self):
        """
        Remove noise from the selected image path and save the result temporarily.
        """
        if not hasattr(self, 'temp_path') or self.temp_path is None:
            print("No valid image loaded or temp path not found.")
            return

        try:
            denoised_image = process_temp_image(self.temp_path)
            # Save the denoised image temporarily
            self.temp_path = TempImageSaver.save_temp_image(denoised_image)
            print(f"Noise removal applied and saved temporarily at {self.temp_path}.")
            self.display_output_image(QPixmap.fromImage(TempImageSaver.convert_cv_to_qimage(denoised_image)))
        except Exception as e:
            # Display the error using a message box
            error_message = QMessageBox()
            error_message.setIcon(QMessageBox.Critical)
            error_message.setWindowTitle("Error")
            error_message.setText("An error occurred during noise removal.")
            error_message.setInformativeText(str(e))
            error_message.exec_()

    def upscale_image(self, factor):
        """
        Upscale an image using a specified factor and save the result temporarily.

        Args:
            factor (int): The upscale factor (2, 4, or 8).
        """
        model_map = {
            2: "LapSRN_x2.pb",
            4: "LapSRN_x4.pb",
            8: "LapSRN_x8.pb"
        }

        model_path = "Image/" + model_map.get(factor)
        if not model_path:
            print("Error: Invalid upscale factor.")
            return

        try:
            upscaled_image = upscale_image(self.selected_image_path, model_path)
            # Save the upscaled image temporarily
            self.temp_path = TempImageSaver.save_temp_image(upscaled_image)
            self.display_output_image(QPixmap.fromImage(TempImageSaver.convert_cv_to_qimage(upscaled_image)))
            print(f"Upscaled image (x{factor}) applied and saved temporarily at {self.temp_path}.")
        except Exception as e:
            # Display the error using a message box
            error_message = QMessageBox()
            error_message.setIcon(QMessageBox.Critical)
            error_message.setWindowTitle("Error")
            error_message.setText("An error occurred during upscaling.")
            error_message.setInformativeText(str(e))
            error_message.exec_()

    def display_output_image(self, pixmap):
        self.output_graphics_scene.clear()
        self.output_graphics_scene.addPixmap(pixmap)
        self.output_graphics_view.fitInView(self.output_graphics_scene.sceneRect(), Qt.KeepAspectRatio)

    def save_output_image(self):
        options = QFileDialog.Options()
        save_path, _ = QFileDialog.getSaveFileName(self, "Save Image", "", "Images (*.png *.jpg *.jpeg *.bmp)", options=options)
        if save_path:
            items = self.output_graphics_scene.items()
            if items:
                pixmap_item = items[0]  # Assuming one item in the scene
                pixmap = pixmap_item.pixmap()
                pixmap.save(save_path)

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