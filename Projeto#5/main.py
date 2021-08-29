#===============================================================================
# Trabalho 05: Chroma Key 
# Autores: Alexandre Herrero Matias
#        : Matheus Fonseca Alexandre
#-------------------------------------------------------------------------------
# Professor: Bogdan T. Nassu
# Processamento Digital de Imagens
# Universidade Tecnológica Federal do Paraná
#===============================================================================

import sys
import numpy as np
import matplotlib.pyplot as plt
import cv2

# Variaveis globais. 
INPUT_FOREGROUND = 'img/4.bmp'
INPUT_BACKGROUND = 'backgrounds/Rem.jpg'

def main():
    
    F = cv2.imread (INPUT_FOREGROUND)
    if F is None:
        print ('Erro abrindo a imagem.\n')
        sys.exit ()

    B = cv2.imread (INPUT_BACKGROUND)
    if F is None:
        print ('Erro abrindo a imagem.\n')
        sys.exit ()

    B = cv2.resize(B, (F.shape[1], F.shape[0]))

    # É uma boa prática manter o shape com 3 valores, independente da imagem ser
    # colorida ou não. Também já convertemos para float32.
    F = F.astype (np.float32) / 255
    B = B.astype (np.float32) / 255

    Fb,Fg,Fr = cv2.split(F)
    Bb,Bg,Br = cv2.split(B)

    alpha = Fg.copy() #mascara

    for y in range(F.shape[0]):
        for x in range(F.shape[1]):
            if (Fg[y][x] - Fb[y][x] > 0.1 and Fg[y][x] - Fr[y][x] > 0.1): #verde maior que ambos azul e vermelho mas tambem eh diferente de ambos
                alpha[y][x] = 1 - Fg[y][x] #fator de luminosidade do background
            else:
                alpha[y][x] = 1 #mantem o foreground

    IMGr = alpha*Fr + (1-alpha)*Br
    IMGg = alpha*Fg + (1-alpha)*Bg
    IMGb = alpha*Fb + (1-alpha)*Bb

    IMG = cv2.merge((IMGb,IMGg,IMGr))

    cv2.imshow("F", F)
    cv2.imshow("B", B)
    cv2.imshow("alpha", alpha)
    cv2.imshow("IMG",IMG)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main ()

#===============================================================================