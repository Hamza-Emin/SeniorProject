import cv2
import numpy as np
from transformers import DPTForDepthEstimation, DPTFeatureExtractor
from PIL import Image
import torch

from transformers import DPTForDepthEstimation, DPTFeatureExtractor
from PIL import Image
import numpy as np
import cv2
import torch

def generate_depth_map(image_path):
    """
    Generate a depth map using the DPT model and optionally save it.

    Args:
        image_path (str): Path to the input image.
        save_path (str, optional): Path to save the generated depth map.
        save (bool): Whether to save the depth map.

    Returns:
        numpy.ndarray: The generated depth map.
    """
    # Load model and feature extractor
    model = DPTForDepthEstimation.from_pretrained("Intel/dpt-large")
    feature_extractor = DPTFeatureExtractor.from_pretrained("Intel/dpt-large")

    # Load and preprocess the image
    image = Image.open(image_path).convert("RGB")
    inputs = feature_extractor(images=image, return_tensors="pt")

    # Predict depth
    with torch.no_grad():
        outputs = model(**inputs)
        predicted_depth = outputs.predicted_depth[0].numpy()

    # Normalize the depth map
    normalized_depth = cv2.normalize(predicted_depth, None, 0, 255, cv2.NORM_MINMAX)
    depth_map = normalized_depth.astype(np.uint8)

    return depth_map


def create_anaglyph(image, depth_map, shift=15):
    """
    Creates an anaglyph (red-cyan) 3D image.

    Args:
        image (numpy.ndarray): Input image.
        depth_map (numpy.ndarray): Depth map corresponding to the input image.
        shift (int): Maximum pixel shift for the anaglyph effect.

    Returns:
        numpy.ndarray: Anaglyph image.
    """
    rows, cols, _ = image.shape

    # Resize depth map to match the original image dimensions
    depth_map = cv2.resize(depth_map, (cols, rows))

    # Smooth and enhance the depth map
    depth_map = cv2.bilateralFilter(depth_map, d=9, sigmaColor=75, sigmaSpace=75)
    depth_map = cv2.normalize(depth_map, None, 0, 255, cv2.NORM_MINMAX)
    depth_map = np.power(depth_map / 255.0, 0.5) * 255
    depth_map = depth_map.astype(np.uint8)

    # Create left and right shifted images
    left_image = np.zeros_like(image)
    right_image = np.zeros_like(image)

    for row in range(rows):
        for col in range(cols):
            shift_value = int(shift * depth_map[row, col] / 255)
            if col + shift_value < cols:
                left_image[row, col] = image[row, col + shift_value]
            if col - shift_value >= 0:
                right_image[row, col] = image[row, col - shift_value]

    # Combine left and right images into an anaglyph
    anaglyph = np.zeros_like(image)
    weight = depth_map / 255.0
    anaglyph[:, :, 0] = (1 - weight) * left_image[:, :, 0] + weight * right_image[:, :, 0]  # Red
    anaglyph[:, :, 1] = right_image[:, :, 1] * (1 - weight)  # Cyan (green & blue components)
    anaglyph[:, :, 2] = right_image[:, :, 2] * (1 - weight)

    # Apply gamma correction for better lighting
    gamma = 1.2
    anaglyph = np.power(anaglyph / 255.0, gamma) * 255
    anaglyph = anaglyph.astype(np.uint8)

    return anaglyph


def generate_anaglyph(image_path, depth_map):
    """
    Generate a red-cyan anaglyph image using the input image and its depth map and optionally save it.

    Args:
        image_path (str): Path to the input image.
        depth_map (numpy.ndarray): Depth map of the input image.
        save_path (str, optional): Path to save the output anaglyph image.
        save (bool): Whether to save the anaglyph image.
    """
    # Load the input image
    image = cv2.imread(image_path)

    if image is None:
        raise FileNotFoundError("Input image not found.")

    # Create the anaglyph image
    anaglyph = create_anaglyph(image, depth_map)

    return anaglyph


"""
# Example usage
image_path = "input.jpg"  # Path to your input image
save_depth_map_path = "depth_map.jpg"  # Path to save the depth map
save_anaglyph_path = "output_anaglyph.jpg"  # Path to save the anaglyph

# Step 1: Generate the depth map
depth_map = generate_depth_map(image_path, save_path=save_depth_map_path, save=True)

# Step 2: Generate the anaglyph image
generate_anaglyph(image_path, depth_map, save_path=save_anaglyph_path, save=True)
"""