import numpy as np
import cv2
from matplotlib import pyplot as plt
import os
def run_check_finder(image_path, check_type, mark_thresh):
    def plt_img(img):
        '''Quick visualization of the checked fields.'''
        plt.figure(figsize=(30, 30))
        plt.imshow(img, 'gray')
        plt.show()

    def im_threshold(img):
        '''Thresholds values of light grey to white. Inverts colours to black page w/ white writing.'''
        _, thresh = cv2.threshold(img, 200, 255, cv2.THRESH_BINARY_INV)
        return thresh

    def check_find(img, threshold, mark_thresh, check_type):
        '''Returns an image labeled with all relevant checks.'''
        if cv2.getVersionMajor() in [2, 4]:
            contours, _ = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        else:
            _, contours, _ = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        font = cv2.FONT_HERSHEY_TRIPLEX
        document_height, document_width = img.shape[0], img.shape[1]
        mark_thresh = float(mark_thresh.strip('%')) / 100.0

        for cnt in contours:
            approx = cv2.approxPolyDP(cnt, 0.1*cv2.arcLength(cnt, True), True)
            coords = approx.ravel()
            if len(approx) == 4:
                x, y, x2, y2 = coords[0], coords[1], coords[4], coords[5]
                feature_height, feature_width = (y2 - y), (x2 - x)
                if feature_width > float(document_width)/100 and feature_height > float(document_width)/100:
                    if abs(feature_height - feature_width) < 5:
                        crop_img = img[y: y + feature_height, x: x + feature_width]
                        _, crop_thresh = cv2.threshold(crop_img, 127, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
                        total = crop_img.shape[0] * crop_img.shape[1]
                        count_black = total - cv2.countNonZero(crop_thresh)
                        if count_black > float(total)*mark_thresh and (check_type == "filled" or check_type == "all"):
                            cv2.drawContours(img, [approx], 0, (0), 2)
                            cv2.putText(img, "Filled", (x, y), font, 1, (0))
                        elif check_type == "empty" or check_type == "all":
                            cv2.drawContours(img, [approx], 0, (0), 2)
                            cv2.putText(img, "Empty", (x, y), font, 0.5, (0))

        return img

    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise ValueError("Error reading image from directory provided.")
    threshold = im_threshold(img)
    img = check_find(img, threshold, mark_thresh, check_type)
    output_path = os.path.join('output_images', 'edited.png')
    cv2.imwrite(output_path, img)
    return output_path
