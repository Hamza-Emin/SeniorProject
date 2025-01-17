import cv2
import numpy as np
import multiprocessing
import os
import time

def process_frames_in_chunk(frames, video_processor):
    """Applies the create_anaglyph function to each frame in the chunk."""
    processed_frames = []
    for frame in frames:
        processed_frames.append(video_processor.create_anaglyph(frame))
    return processed_frames

class VideoProcessor:
    def __init__(self):
        self.shift_amount = 15
        self.color_intensity = 1.2
        self.brightness_factor = 0.8

    def process_video_with_multiprocessing(self, video_path, output_path='output_3d_video.avi', num_processes=4):
        """Processes a video using multiprocessing to divide chunks and apply create_anaglyph."""
        try:
            video_cap = cv2.VideoCapture(video_path)
            if not video_cap.isOpened():
                raise ValueError("Error opening video file. Please check the file path and format.")

            frame_width = int(video_cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            frame_height = int(video_cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            frame_rate = video_cap.get(cv2.CAP_PROP_FPS)
            frame_count = int(video_cap.get(cv2.CAP_PROP_FRAME_COUNT))

            if frame_count == 0:
                raise ValueError("The video appears to be empty or corrupted.")

            # Read all frames into memory (for simplicity in multiprocessing)
            frames = []
            while True:
                ret, frame = video_cap.read()
                if not ret:
                    break
                frames.append(frame)

            video_cap.release()

            # Split frames into chunks
            chunk_size = len(frames) // num_processes
            frame_chunks = [frames[i * chunk_size:(i + 1) * chunk_size] for i in range(num_processes)]

            # Add remaining frames to the last chunk
            if len(frames) % num_processes != 0:
                frame_chunks[-1].extend(frames[num_processes * chunk_size:])

            # Use multiprocessing Pool to process each chunk
            with multiprocessing.Pool(processes=num_processes) as pool:
                processed_chunks = pool.starmap(process_frames_in_chunk, [(chunk, self) for chunk in frame_chunks])

            # Flatten the processed chunks back into a single list of frames
            processed_frames = [frame for chunk in processed_chunks for frame in chunk]

            # Write processed frames to output video
            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            video_writer = cv2.VideoWriter(output_path, fourcc, frame_rate, (frame_width, frame_height))

            for frame in processed_frames:
                video_writer.write(frame)

            video_writer.release()
            return output_path

        except Exception as e:
            print(f"An error occurred during video processing: {e}")

    def create_anaglyph(self, frame):
        """Converts a single frame to 3D anaglyph format."""
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (3, 3), 0)
        grad_x = cv2.Sobel(blur, cv2.CV_64F, 1, 0, ksize=3)
        grad_y = cv2.Sobel(blur, cv2.CV_64F, 0, 1, ksize=3)
        depth_map = np.sqrt(grad_x * 2 + grad_y * 2)
        depth_map = cv2.normalize(depth_map, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
        b, g, r = cv2.split(frame)
        shifts = np.int32(self.shift_amount * (1.0 - depth_map / 255.0))
        height, width = frame.shape[:2]
        y_coords, x_coords = np.mgrid[0:height, 0:width]
        left_x = np.clip(x_coords + shifts, 0, width - 1)
        right_x = np.clip(x_coords - shifts, 0, width - 1)
        anaglyph = np.zeros_like(frame)
        anaglyph[:, :, 2] = r[y_coords, left_x]
        anaglyph[:, :, 0] = b[y_coords, right_x]
        anaglyph[:, :, 1] = g[y_coords, right_x]
        intensity_lut = np.uint8(np.clip(np.arange(256) * self.color_intensity * self.brightness_factor, 0, 255))
        anaglyph = cv2.LUT(anaglyph, intensity_lut)
        return anaglyph

    def benchmark_processing(self, video_path):
        """Compares processing time for single core, two core, four core, and six core execution."""
        core_counts = [1, 2, 4, 6]
        timings = {}

        for cores in core_counts:
            try:
                start_time = time.time()
                self.process_video_with_multiprocessing(video_path, output_path=f"output_{cores}_cores.avi", num_processes=cores)
                end_time = time.time()
                timings[cores] = end_time - start_time
            except Exception as e:
                print(f"An error occurred while processing with {cores} cores: {e}")

        for cores, timing in timings.items():
            print(f"Processing with {cores} cores took {timing:.2f} seconds.")

        return timings

if __name__ == "__main__":
    video_processor = VideoProcessor()
    video_path = r"C:\Users\deniz\Downloads\Car Control Master.mp4"
    try:
        video_processor.benchmark_processing(video_path)
    except Exception as e:
        print(f"Failed to run benchmark processing: {e}")
