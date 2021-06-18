
import sys
import timeit
import numpy as np
import cv2

INPUT_IMAGE = 'C:/Users/mfado/Documents/GitHub/CSV30/Projeto#1/arroz.bmp'
NEGATIVO = False
THRESHOLD = 0.7

def binariza (img, threshold):
    img = np.uint8(np.where( img <= threshold, 1, 0))
    return img
    
img = cv2.imread(INPUT_IMAGE, cv2.IMREAD_GRAYSCALE)
if img is None:
    print ('Erro abrindo %s' % INPUT_IMAGE)

img = img.reshape ((img.shape [0], img.shape [1], 1))
img = img.astype (np.float32) / 255

img_out = cv2.cvtColor (img, cv2.COLOR_GRAY2BGR)

img = binariza (img, THRESHOLD)
cv2.imshow ('01 - binarizada', img)
cv2.waitKey ()
cv2.imwrite ('01 - binarizada.png', img*255)

