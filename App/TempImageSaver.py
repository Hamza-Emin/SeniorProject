import os
import tempfile

import cv2
from PyQt5.QtGui import QImage


class TempImageSaver:
    """
    A class for saving images temporarily as .temp files.
    """

    @staticmethod
    def save_temp_image(image, suffix=".temp.png"):
        """
        Save an image temporarily with a .temp suffix.

        Args:
            image (numpy.ndarray): Image to save.
            suffix (str): File suffix for the temporary file (default: .temp).

        Returns:
            str: Path to the temporary file.
        """
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
        cv2.imwrite(temp_file.name, image)
        return temp_file.name

    def convert_cv_to_qimage(cv_img):
        """
        Convert an OpenCV image (NumPy array) to QImage.

        Parameters:
        - cv_img: OpenCV image in BGR format.

        Returns:
        - QImage object.
        """
        height, width, channel = cv_img.shape
        bytes_per_line = 3 * width  # 3 channels for RGB
        cv_img_rgb = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        q_image = QImage(cv_img_rgb.data, width, height, bytes_per_line, QImage.Format_RGB888)
        return q_image

    @staticmethod
    def cleanup():
        for file in TempImageSaver.temp_files:
            try:
                os.remove(file)
            except FileNotFoundError:
                pass
        TempImageSaver.temp_files.clear()