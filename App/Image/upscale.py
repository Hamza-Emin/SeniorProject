import cv2
import os

def upscale_image(input_image_path, model_path):
    """
    Upscales an image using the specified DNN super-resolution model.
    
    Args:
        input_image_path (str): Path to the input image.
        model_path (str): Path to the pre-trained model file.

    Returns:
        numpy.ndarray: The upscaled image.
    """
    # Initialize the DNN super-resolution model
    sr = cv2.dnn_superres.DnnSuperResImpl_create()

    # Extract scale factor from the model file name (e.g., "LapSRN_x2.pb" -> 2)
    if "x2" in model_path.lower():
        scale_factor = 2
    elif "x4" in model_path.lower():
        scale_factor = 4
    elif "x8" in model_path.lower():
        scale_factor = 8
    else:
        raise ValueError("Unsupported model scale. Use 'x2', 'x4', or 'x8' in the model file name.")

    # Load the model and set the scale factor
    sr.readModel(model_path)
    sr.setModel("lapsrn", scale_factor)

    # Load the input image
    image = cv2.imread(input_image_path)
    if image is None:
        raise ValueError("Input image not found. Check the file path.")
    
    # Ensure the image is in RGB format
    if len(image.shape) == 2 or image.shape[2] != 3:
        image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)

    # Apply super-resolution
    upscaled_image = sr.upsample(image)

    return upscaled_image
