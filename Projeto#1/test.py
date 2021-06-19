import sys
import timeit
import numpy as np
import cv2
import random

np.set_printoptions(threshold=sys.maxsize)
INPUT_IMAGE = 'arroz.bmp'
NEGATIVO = False
THRESHOLD = 0.8

def binariza (img, threshold):
    img = np.uint8(np.where( img <= threshold, 0, 1))
    return img
    
def inunda (label, img, row, col):
    rows, cols, channels = img.shape
    if(img[row,col] == -1):
        img[row,col] = label
        if(row+1 <= rows):
            inunda (label, img, row+1, col)
        if(row-1 >= 0):
            inunda (label, img, row-1, col)
        if(col+1 <= cols):
            inunda (label, img, row, col+1)
        if(col-1 >= 0):
            inunda (label, img, row, col-1)

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

rows, cols, channels = img.shape
img_gs = img
img_gs = np.where(img == 1, -1, 1)

#coordList = np.argwhere(cv2.inRange(img_gs, -1, -1))
#for coord in coordList:
#    img_out[coord[0], coord[1]] = (0, 0, 1)

label = -2
for row in range (rows):
    for col in range (cols):
        if(img_gs[row,col] == -1):
            inunda(label, img_gs, row, col)
            label -= 1
max = []
min = []
for labels in range (label, -1):
#    R = random.uniform(0, 1)
#    G = random.uniform(0, 1)
#    B = random.uniform(0, 1)
    if (np.count_nonzero(img_gs == labels) >= 413):
        print("Label: " + str(labels) + " - " + str(np.count_nonzero(img_gs == labels)) + " pixels")
        coord = np.argwhere(cv2.inRange(img_gs, labels, labels))
#        for coordList in coord:
#            img_out[coordList[0], coordList[1]] = (B, G, R)
        #print(np.amax(coord, axis=0))
        max.append(np.amax(coord, axis=0))
        #print(np.amin(coord, axis=0))
        min.append(np.amin(coord, axis=0))

for coordMax, coordMin in zip(max, min):
    #print("(" + str(coordMax) + "," + str(coordMin) + ")")
    #alt = coordMax[1] - coordMin[1]
    #lar = coordMax[0] - coordMin[0]
    #print("Altura: " + str(alt) + " - Largura: " + str(lar))
    cv2.rectangle (img_out, (coordMin[1], coordMin[0]), (coordMax[1], coordMax[0]), (0,0,1))

cv2.imshow ('02 - out', img_out)
cv2.waitKey ()
cv2.imwrite ('02 - out.png', img_out*255)