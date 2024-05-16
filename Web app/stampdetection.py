import numpy as np
import cv2
import matplotlib.pyplot as plt
from stamp_processing import StampDetector


def run_stamp_detection(filepath):
    # Read the image from the given file path
    img = cv2.imread(filepath)
    if img is None:
        raise ValueError(f"Image at path '{filepath}' could not be read.")

    # Convert the image to an array
    image = np.array(img)

    # Initialize the StampDetector
    detector = StampDetector(model_path=None)

    # Get the predictions for stamp locations
    preds = detector([image])

    # Draw rectangles around detected stamps
    for box in preds[0]:
        cv2.rectangle(image, (int(box[0]), int(box[1])), (int(box[2]), int(box[3])), (0, 0, 255), 2)

    # Define the output path
    output_path = './output_images/stamp_detection_output.png'

    # Save the processed image
    plt.imsave(output_path, image, cmap='gray')

    # Return the output path
    return output_path