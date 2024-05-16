from word_detector import prepare_img, detect, sort_line
import cv2

def run_text_detection(image_path, scale_height=500):
    img = prepare_img(cv2.imread(image_path), scale_height)
    detections = detect(img, kernel_size=25, sigma=11, theta=7, min_area=100)
    lines = sort_line(detections)
    
    output_img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)  # Convert gray to BGR for color drawing

    for line in lines:
        for word in line:
            # Using the BBox attributes correctly
            x, y, w, h = word.bbox.x, word.bbox.y, word.bbox.w, word.bbox.h
            cv2.rectangle(output_img, (x, y), (x + w, y + h), (0, 255, 0), 2)

    output_path = './output_images/text_detection_output.png'
    cv2.imwrite(output_path, output_img)
    return output_path
