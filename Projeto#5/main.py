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
INPUT_FOREGROUND = 'img/5.bmp'
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

    max_b = 0 #maior valor da diferenca entre o canal verde e o azul
    max_r = 0 #maior valor da diferenca entre o canal verde e o vermelho
    for y in range(F.shape[0]):
        for x in range(F.shape[1]):
            if (Fg[y][x] > Fb[y][x]):
                if (Fg[y][x] - Fb[y][x] > max_b):
                    max_b = Fg[y][x] - Fb[y][x]
            if (Fg[y][x] > Fr[y][x]):
                if (Fg[y][x] - Fr[y][x] > max_r):
                    max_r = Fg[y][x] - Fr[y][x]
    print(max_b)
    print(max_r)

    thresh_b = 0.2*max_b #mantem os valores de threshold entre 0 e 0.2 (valores totalmente empiricos)
    thresh_r = 0.2*max_r #mantem os valores de threshold entre 0 e 0.2 (valores totalmente empiricos)

    print(thresh_b)
    print(thresh_r)

    for y in range(F.shape[0]):
        for x in range(F.shape[1]):
            if (Fg[y][x] - Fb[y][x] > thresh_b and Fg[y][x] - Fr[y][x] > thresh_r): #threshold aplicado apenas se verde eh maior que azul e vermelho porem eh diferente de ambos
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