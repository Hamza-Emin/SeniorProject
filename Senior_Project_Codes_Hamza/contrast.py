import cv2
import numpy as np

def adjust_brightness_contrast(image, alpha=1.0, beta=0):
    """
    Adjust brightness and contrast of an image.

    Parameters:
    - image: Input image.
    - alpha (float): Contrast control (1.0 means no change).
    - beta (int): Brightness control (0 means no change).

    Returns:
    - adjusted_image: The adjusted image.
    """
    adjusted_image = cv2.convertScaleAbs(image, alpha=alpha, beta=beta)
    return adjusted_image

def apply_gamma_correction(image, gamma=1.0):
    """
    Apply gamma correction to an image.

    Parameters:
    - image: Input image.
    - gamma (float): Gamma value (>1 for brighter, <1 for darker).

    Returns:
    - gamma_corrected: The gamma-corrected image.
    """
    inv_gamma = 1.0 / gamma
    lut = np.array([((i / 255.0) ** inv_gamma) * 255 for i in range(256)], dtype='uint8')
    gamma_corrected = cv2.LUT(image, lut)
    return gamma_corrected

def equalize_histogram(image):
    """
    Enhance the contrast of an image using histogram equalization.

    Parameters:
    - image: Input image (grayscale or BGR).

    Returns:
    - equalized_image: The image with enhanced contrast.
    """
    if len(image.shape) == 2:  # Grayscale image
        equalized_image = cv2.equalizeHist(image)
    else:  # Color image (BGR)
        # Convert to YCrCb color space
        ycrcb = cv2.cvtColor(image, cv2.COLOR_BGR2YCrCb)
        y_channel, cr, cb = cv2.split(ycrcb)

        # Equalize the histogram of the Y channel
        y_channel_eq = cv2.equalizeHist(y_channel)

        # Merge the equalized Y channel back
        ycrcb_eq = cv2.merge((y_channel_eq, cr, cb))

        # Convert back to BGR color space
        equalized_image = cv2.cvtColor(ycrcb_eq, cv2.COLOR_YCrCb2BGR)

    return equalized_image

if __name__ == "__main__":
    # Load an example image
    input_image_path = "input.jpg"
    image = cv2.imread(input_image_path)

    if image is None:
        raise FileNotFoundError(f"Image at '{input_image_path}' could not be loaded. Check the file path.")

    # Adjust brightness and contrast
    alpha = 1.2  # Contrast control
    beta = 25    # Brightness control
    adjusted_image = adjust_brightness_contrast(image, alpha=alpha, beta=beta)
    cv2.imwrite("adjusted_image.jpg", adjusted_image)
    
    # Apply gamma correction
    gamma = 1.5
    gamma_corrected_image = apply_gamma_correction(image, gamma=gamma)
    cv2.imwrite("gamma_corrected_image.jpg", gamma_corrected_image)

    # Apply histogram equalization
    equalized_image = equalize_histogram(image)
    cv2.imwrite("equalized_image.jpg", equalized_image)

    # Display results
    cv2.imshow("Original Image", image)
    cv2.imshow("Brightness/Contrast Adjusted", adjusted_image)
    cv2.imshow("Gamma Corrected", gamma_corrected_image)
    cv2.imshow("Histogram Equalized", equalized_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
