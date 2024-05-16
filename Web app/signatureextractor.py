import cv2
import numpy as np
from skimage import measure, morphology
from skimage.color import label2rgb
from skimage.measure import regionprops
import matplotlib.pyplot as plt

def run_signature_extraction(image_path):
    # Read the input image
    img = cv2.imread(image_path, 0)
    if img is None:
        raise FileNotFoundError(f"No file found at {image_path}")
    img = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)[1]  # Ensure binary

    # Connected component analysis by scikit-learn framework
    blobs = img > img.mean()
    blobs_labels = measure.label(blobs, background=1)
    image_label_overlay = label2rgb(blobs_labels, image=img)

    the_biggest_component = 0
    total_area = 0
    counter = 0
    for region in regionprops(blobs_labels):
        if region.area > 10:
            total_area += region.area
            counter += 1
        if region.area >= 250 and region.area > the_biggest_component:
            the_biggest_component = region.area

    average = total_area / counter if counter else 0

    # Experimental-based ratio calculation for A4 size scanned documents
    constant_parameter_1 = 84
    constant_parameter_2 = 250
    constant_parameter_3 = 100
    constant_parameter_4 = 18

    a4_small_size_outliar_constant = ((average / constant_parameter_1) * constant_parameter_2) + constant_parameter_3
    a4_big_size_outliar_constant = a4_small_size_outliar_constant * constant_parameter_4

    # Remove small objects
    pre_version = morphology.remove_small_objects(blobs_labels, a4_small_size_outliar_constant)
    # Remove big objects
    component_sizes = np.bincount(pre_version.ravel())
    too_small = component_sizes > a4_big_size_outliar_constant
    too_small_mask = too_small[pre_version]
    pre_version[too_small_mask] = 0

    # Save the processed image
    output_path = './output_images/signature_extraction_output.png'
    plt.imsave(output_path, pre_version, cmap='gray')

    return output_path
