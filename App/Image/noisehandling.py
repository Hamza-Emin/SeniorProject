import cv2
import numpy as np
from skimage.restoration import denoise_wavelet


def remove_noise(image, method="bilateral"):
    """
    Removes noise from an RGB image using the specified method.

    Args:
        image (numpy.ndarray): The input RGB image.
        method (str): Method to use for noise removal. Options: "bilateral", "wavelet".
        save_path (str, optional): Path to save the denoised image.
        save (bool): Whether to save the denoised image.

    Returns:
        numpy.ndarray: The denoised RGB image.
    """
    if method == "bilateral":
        # Apply bilateral filter to remove noise while preserving edges
        denoised_image = cv2.bilateralFilter(image, d=9, sigmaColor=75, sigmaSpace=75)
    elif method == "wavelet":
        # Use wavelet denoising (requires scikit-image)
        denoised_image = denoise_wavelet(image, multichannel=True, rescale_sigma=True)
        denoised_image = (denoised_image * 255).astype(np.uint8)  # Convert back to 8-bit
    else:
        raise ValueError("Invalid method specified. Choose 'bilateral' or 'wavelet'.")

    return denoised_image

def process_temp_image(temp_file_path, method="bilateral", save=False, save_path=None):
    """
    Reads an image from a temporary file, removes noise using the specified method,
    and optionally saves the denoised image.

    Args:
        temp_file_path (str): Path to the temporary image file.
        method (str): Method to use for noise removal. Options: "bilateral", "wavelet".
        save (bool): Whether to save the denoised image.
        save_path (str, optional): Path to save the denoised image if save is True.

    Returns:
        numpy.ndarray: The denoised RGB image.
    """
    # Read the image from the temporary file
    image = cv2.imread(temp_file_path)

    if image is None:
        raise FileNotFoundError(f"The file at {temp_file_path} could not be read.")

    # Convert the image to RGB (OpenCV loads images in BGR format)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Call the remove_noise function
    denoised_image = remove_noise(image_rgb, method=method)
    denoised_image = cv2.cvtColor(denoised_image, cv2.COLOR_BGR2RGB)

    if save:
        if save_path is None:
            raise ValueError("save_path must be provided if save is True.")
        # Convert the image back to BGR for saving with OpenCV
        denoised_bgr = cv2.cvtColor(denoised_image, cv2.COLOR_BGR2RGB)
        cv2.imwrite(save_path, denoised_bgr)


    return denoised_image





"""
# Example usage
image_path = "input_image.jpg"  # Path to your input image
image = cv2.imread(image_path)

if image is None:
    raise FileNotFoundError("Input image not found.")

# Apply noise removal
save_denoised_path = "denoised_image.jpg"  # Path to save the denoised image
denoised_image = remove_noise(image, method="wavelet", save_path=save_denoised_path, save=True)
"""
