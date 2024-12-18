import cv2
import numpy as np
from skimage.restoration import denoise_wavelet


def remove_noise(image, method="bilateral", save_path=None, save=False):
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

    # Display the denoised image
    cv2.imshow("Denoised Image", denoised_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # Save if required
    if save and save_path:
        cv2.imwrite(save_path, denoised_image)
        print(f"Denoised image saved to {save_path}")

    return denoised_image

# Example usage
image_path = "input_image.jpg"  # Path to your input image
image = cv2.imread(image_path)

if image is None:
    raise FileNotFoundError("Input image not found.")

# Apply noise removal
save_denoised_path = "denoised_image.jpg"  # Path to save the denoised image
denoised_image = remove_noise(image, method="wavelet", save_path=save_denoised_path, save=True)
