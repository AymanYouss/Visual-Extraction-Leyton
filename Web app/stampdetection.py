import pdf2image
import numpy as np
import cv2
import matplotlib.pyplot as plt
#%%
def imshow(img, figsize=(10, 10), **kwargs):
    fig, ax = plt.subplots(1, 1, figsize=figsize)
    ax.axis('off')
    ax.imshow(img, **kwargs)
#%%
img = cv2.imread('./images/image.webp')
images = []
images.append(img)
#%%
image = np.array(images[0])

from stamp_processing import StampDetector
#%%
# Set path to None to download weight
detector = StampDetector(model_path=None)
#%%
preds = detector([image])
#%%
for box in preds[0]:
    cv2.rectangle(image, (int(box[0]), int(box[1])), (int(box[2]), int(box[3])), (0, 0, 255), 2)
#%%
fig, ax = plt.subplots(1, 1, figsize=(20, 20))
ax.axis('off')
ax.imshow(image)