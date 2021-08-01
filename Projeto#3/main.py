#===============================================================================
# Trabalho 03: Bloom Lighting 
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
INPUT_IMAGE = 'Images/GT2.BMP'
BRIGHT_PASS = 0.8
ALFA = 0.775
BETA = 0.215
MODE = 1 # 0 - Gaussian; 1 - Box

# Funções 

def identifyLightingSource(img):
    # TODO: Identificar pixeis de intensidade ou brilho mais alto
    # TODO: Criar máscara com a posição destes pixeis
    # TODO: Gerar máscara com as informações da imagem original
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    hsv[:,:,2] = np.where(hsv[:,:,2] <= BRIGHT_PASS, 0, hsv[:,:,2])
    bgr = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
    # Retorne a máscara
    return bgr   

def maskGaussianBlur(img, sigma):
    blur = cv2.GaussianBlur(img,(0,0),sigma)
    return blur

def maskBoxBlur(img, sigma, n):
    r = math.floor(math.sqrt((((12/n)*sigma**2))+1))
    for j in range(0,n):
        img = cv2.blur(img,(r,r))
    return img

def main():
    # Abre a imagem.
    img = cv2.imread (INPUT_IMAGE)
    if img is None:
        print ('Erro abrindo a imagem.\n')
        sys.exit ()

    # É uma boa prática manter o shape com 3 valores, independente da imagem ser
    # colorida ou não. Também já convertemos para float32.
    img = img.astype (np.float32) / 255

    start_time = timeit.default_timer ()

    # TODO: Identificar Fontes de Luz
    # TODO: Criar uma máscara com as fontes de luz
    lightingMask = identifyLightingSource(img)

    # TODO: Borrar máscara várias vezes
    if(MODE == 0):
        lightingMask = maskGaussianBlur(lightingMask, 10)
        lightingMask += maskGaussianBlur(lightingMask, 20)
        lightingMask += maskGaussianBlur(lightingMask, 40)
        lightingMask += maskGaussianBlur(lightingMask, 80)
    elif(MODE == 1):
        lightingMask = maskBoxBlur(lightingMask, 10, 5)
        lightingMask += maskBoxBlur(lightingMask, 20, 5)
        lightingMask += maskBoxBlur(lightingMask, 40, 5)
        lightingMask += maskBoxBlur(lightingMask, 80, 5)

    # TODO: Somar máscara sobre a imagem original com pesos
    imgBloom = ALFA*img + BETA*lightingMask

    print ('Tempo: %f' % (timeit.default_timer () - start_time))

    cv2.imwrite('imgBloom.png', imgBloom*255)

    cv2.waitKey ()
    cv2.destroyAllWindows ()

if __name__ == '__main__':
    main ()

#===============================================================================