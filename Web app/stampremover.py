import numpy as np
import pathlib
from stamp_processing import StampRemover
import cv2

def run_stamp_removal(image_path):
    # Adjust path settings for Windows
    temp = pathlib.PosixPath
    pathlib.PosixPath = pathlib.WindowsPath

    # Load image
    img = cv2.imread(image_path)
    if img is None:
        raise FileNotFoundError(f"No file found at {image_path}")

    # Prepare the image for processing
    image = np.array(img)

    # Initialize the StampRemover
    remover = StampRemover(detection_weight=None, removal_weight=None)

    # Process the image
    preds = remover([image])

    # Restore original Path behavior
    pathlib.PosixPath = temp

    # Save the output
    output_path = './output_images/stamp_remover_output.png'
    cv2.imwrite(output_path, preds[0])

    return output_path
