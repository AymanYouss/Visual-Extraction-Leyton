import numpy as np
import cv2 as cv
import requests
from matplotlib import pyplot as plt

img_link = 'https://i.ibb.co/pwTwWfg/13581.jpg'
resp = requests.get(img_link)
arr = np.asarray(bytearray(resp.content), dtype=np.uint8)
img = cv.imdecode(arr, -1)
img = cv.GaussianBlur(img, (15, 15), 0)
assert img is not None, "file could not be read, check with os.path.exists()"
edges = cv.Canny(img,100,120, apertureSize=3)
plt.subplot(121),plt.imshow(img,cmap = 'gray')
plt.title('Original Image'), plt.xticks([]), plt.yticks([])
plt.subplot(122),plt.imshow(edges,cmap = 'gray')
plt.title('After Canny'), plt.xticks([]), plt.yticks([])
plt.show()