import numpy as np
import cv2
import czifile
import pickle
import matplotlib.pyplot as plt
import scipy.misc
import os

SLICE_COUNT = 15

def extract_channel(channel_number, czi_image, file_name):
    with open(file_name, 'wb+') as f:
        pickle.dump(czi_image[0][0][channel_number], f)

def load_extracted_channel(file_name):
    with open(file_name, 'rb+') as f:
        images = pickle.load(f)
        return images

#czi_image = czifile.imread('CAAX_100X_20171024_1-Scene-06-P6-B02.czi')

#extract_channel(3, czi_image, "p6.dat")

file_name = "p3.dat"
cell_id = 2
start_slice = 25

with open(file_name, 'rb+') as f:
    images = pickle.load(f)

if not os.path.exists(f"images/{file_name}_{cell_id}"):
    os.mkdir(f"images/{file_name}_{cell_id}")
for i in range(start_slice, start_slice+SLICE_COUNT):
    image = images[i]

    # scale elements to fit whole range [0,65535], because we want to see same pictures as we see on fiji
    image = cv2.normalize(image, dst=None, alpha=0, beta=65535, norm_type=cv2.NORM_MINMAX)

    # make every pixel to have three components instead of one
    image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)

    # scale values pixel values from [0,65535] to [0,255]
    image = cv2.convertScaleAbs(image, alpha=(255.0 / 65535.0))

    # smoothen
    kernel = np.ones((5, 5), np.float32) / 25
    image = cv2.filter2D(image, -1, kernel)

    #cv2.imshow('preprocesed1' + str(i), image)
    image = cv2.Canny(image, 15, 25)
    #print(image)
    #cv2.imshow('preprocesed' + str(i), image)
    image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)

    #smoothen
    kernel = np.ones((5, 5), np.float32) / 25
    image = cv2.filter2D(image, -1, kernel)

    kernel = np.ones((5, 5), np.uint8)
    # use dilate to fill some empty space on border
    image = cv2.dilate(image, kernel, iterations=1)

    #cv2.imshow('preprocesed2' + str(i), image)
    #cv2.imwrite(f"images/Image{i}.jpg", image)
    #ax[i-25].imshow(image, cmap="gray")

    #seed = (1150, 600) #good 25 40 p3
    #seed = (900, 800) # good 29 44 p3
    seed = (520, 900) # semi-good 25 39 p3


    #seed = (1365, 966) #bad
    #seed = (320, 930) # good 35 50 p6
    cv2.floodFill(image, None, seedPoint=seed, newVal=(0, 0, 255))

    #cv2.circle(image, seed, 20, (0, 255, 0), cv2.FILLED, cv2.LINE_AA)

    kernel = np.ones((5, 5), np.uint8)
    # use dilate to fill some empty space on border
    image = cv2.dilate(image, kernel, iterations=6)

    #cv2.imshow('flood' + str(i), image)
    cv2.imwrite(f"images/{file_name}_{cell_id}/Images{i}.jpg", image)

cv2.waitKey(0)
cv2.destroyAllWindows()