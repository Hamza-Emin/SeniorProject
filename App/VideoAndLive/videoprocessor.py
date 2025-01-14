import cv2
import numpy as np

class VideoProcessor:
    def __init__(self):
        self.shift_amount = 15
        self.color_intensity = 1.2
        self.brightness_factor = 0.8

    def process_video_to_3d(self, video_path,output_path='output_3d_video.avi'):
        """Takes the video path as input and applies 3D anaglyph transformation to the video"""
        # Open the video file
        video_cap = cv2.VideoCapture(video_path)
        if not video_cap.isOpened():
            raise ValueError("Error opening video file.")

        # Get video properties
        frame_width = int(video_cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(video_cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        frame_rate = video_cap.get(cv2.CAP_PROP_FPS)

        # Set up the video writer (to save the processed video)
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        video_writer = cv2.VideoWriter(output_path, fourcc, frame_rate, (frame_width, frame_height))

        while True:
            ret, frame = video_cap.read()
            if not ret:
                break

            # Apply 3D effect
            anaglyph_frame = self.create_anaglyph(frame)
            self.update_frame(anaglyph_frame)

            # Write the processed frame to the video
            video_writer.write(anaglyph_frame)

        # Release the video reader and writer
        video_cap.release()
        video_writer.release()

        return output_path  # Return the path to the processed video

    def process_live_to_3d(self, frame):
        """Applies 3D anaglyph transformation to live feed and returns the processed frame"""
        # Apply the 3D anaglyph effect
        anaglyph_frame = self.create_anaglyph(frame)

        return anaglyph_frame  # Return the processed live frame

    def create_anaglyph(self, frame):
        """Converts a single frame to 3D anaglyph format"""
        # Fast grayscale conversion
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Apply Gaussian blur
        blur = cv2.GaussianBlur(gray, (3, 3), 0)

        # Compute gradients
        grad_x = cv2.Sobel(blur, cv2.CV_64F, 1, 0, ksize=3)
        grad_y = cv2.Sobel(blur, cv2.CV_64F, 0, 1, ksize=3)

        # Create depth map from the gradients
        depth_map = np.sqrt(grad_x * 2 + grad_y * 2)
        depth_map = cv2.normalize(depth_map, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)

        # Split the channels of the original frame
        b, g, r = cv2.split(frame)

        # Calculate the amount of shift based on the depth map
        shifts = np.int32(self.shift_amount * (1.0 - depth_map / 255.0))

        # Apply horizontal shift to create the 3D effect
        height, width = frame.shape[:2]
        y_coords, x_coords = np.mgrid[0:height, 0:width]

        left_x = np.clip(x_coords + shifts, 0, width - 1)
        right_x = np.clip(x_coords - shifts, 0, width - 1)

        # Create the anaglyph image
        anaglyph = np.zeros_like(frame)
        anaglyph[:, :, 2] = r[y_coords, left_x]  # Red channel
        anaglyph[:, :, 0] = b[y_coords, right_x]  # Blue channel
        anaglyph[:, :, 1] = g[y_coords, right_x]  # Green channel

        # Apply color intensity adjustment
        intensity_lut = np.uint8(np.clip(np.arange(256) * self.color_intensity * self.brightness_factor, 0, 255))
        anaglyph = cv2.LUT(anaglyph, intensity_lut)

        return anaglyph

    def update_frame(self, anaglyph_frame):
        pass