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
import numpy as np
import cv2

# Variaveis globais. 
INPUT_IMAGE = 'Exemplos/b01 - Original.bmp'
ALFA = 1
BETA = 1

# Funções 

def identifyLightingSource(img):
    # TODO: Identificar pixeis de intensidade ou brilho mais alto
    # TODO: Criar máscara com a posição destes pixeis
    # TODO: Gerar máscara com as informações da imagem original

    # Retorne a máscara
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

    # TODO: Identificar Fontes de Luz
    # TODO: Criar uma máscara com as fontes de luz
    lightingMask = identifyLightingSource(img)

    # TODO: Borrar máscara várias vezes

    # TODO: Somar máscara sobre a imagem original com pesos
    imgBloom = ALFA*img + BETA*lightingMask


    cv2.waitKey ()
    cv2.destroyAllWindows ()

if __name__ == '__main__':
    main ()

#===============================================================================