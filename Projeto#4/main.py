#===============================================================================
# Trabalho 04: Estimar Grãos de Arroz 
# Autores: Alexandre Herrero Matias
#        : Matheus Fonseca Alexandre
#-------------------------------------------------------------------------------
# Professor: Bogdan T. Nassu
# Processamento Digital de Imagens
# Universidade Tecnológica Federal do Paraná
#===============================================================================

import sys
import timeit
import numpy as np
import cv2
import math

# Variaveis globais. 
INPUT_IMAGE = 'Images/150.bmp'

def main():
    # Abre a imagem.
    img = cv2.imread (INPUT_IMAGE)
    if img is None:
        print ('Erro abrindo a imagem.\n')
        sys.exit ()

    # É uma boa prática manter o shape com 3 valores, independente da imagem ser
    # colorida ou não. Também já convertemos para float32.
    #img = img.astype (np.float32) / 255

    start_time = timeit.default_timer ()

    # TODO: Binarizar as imgens
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    #Normaliza a imagem (necessario?)
    normalized = np.zeros((800,800))
    normalized = cv2.normalize(gray,normalized,0,255,cv2.NORM_MINMAX)

    #Importante para todas as formas de binarizacao testadas
    gaussianBlur = cv2.GaussianBlur(normalized,(7,7),0)

    #Unico que funciona em todas as imagens, mas so temos os contornos
    edges = cv2.Canny(gaussianBlur,100,200)

    #Bom para a maioria, mas morre com 60.bmp e 205.bmp (melhor binarizacao para a 150.bmp)
    #Talvez seja possivel utilizar em todas se utilizarmos normalizacao local, mas teriamos que criar na mao
    otsu = cv2.threshold(gaussianBlur,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)

    #Binariza mas tira um pouco do interior dos graos. Morre com a 150.bmp
    adaptative = cv2.adaptiveThreshold(gaussianBlur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV,9,4)

    #cv2.imshow('img',img)
    #cv2.imshow('gray',gray)
    #cv2.imshow('normalized',normalized)
    #cv2.imshow('gaussian',gaussianBlur)
    cv2.imshow('edges',edges)
    cv2.imshow('adaptative',adaptative)
    cv2.imshow('Otsu',otsu[1])

    cv2.waitKey ()
    cv2.destroyAllWindows ()

if __name__ == '__main__':
    main ()

#===============================================================================