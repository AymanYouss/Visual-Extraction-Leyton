from stamp_processing import StampRemover
#%%
image = np.array(images[0])
#%%
import pathlib
temp = pathlib.PosixPath
pathlib.PosixPath = pathlib.WindowsPath
#Set weight path to None to downlaod weight
remover = StampRemover(detection_weight=None, removal_weight=None)
#%%
preds = remover([image])
#%%
imshow(preds[0])