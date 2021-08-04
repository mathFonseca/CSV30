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
import numpy as np
import cv2

# Variaveis globais. 
INPUT_IMAGE = 'Images/60.bmp'

def main():
    # Abre a imagem.
    img = cv2.imread (INPUT_IMAGE)
    if img is None:
        print ('Erro abrindo a imagem.\n')
        sys.exit ()

    # É uma boa prática manter o shape com 3 valores, independente da imagem ser
    # colorida ou não. Também já convertemos para float32.
    # img = img.astype (np.float32) / 255

    # Step 1 - Escala de Cinza
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Step 2 - Normalização (Necessário?)
    normalized = np.zeros((800,800))
    normalized = cv2.normalize(gray,normalized,0,255,cv2.NORM_MINMAX)

    # Step 3 - Gaussian Blur com janela fixa 7x7.
    gaussianBlur = cv2.GaussianBlur(normalized,(7,7),0)

    # Salvamos imagem antes do processamento.
    cv2.imwrite('imgBloom.png', gaussianBlur)

    # ----------
    # Daqui pra baixo, brainstorm.

    # Step 1 - Contar arroz com o que tem.
    # Step 1.1 - Contornar
    # Unico que funciona em todas as imagens, mas so temos os contornos
    edges = cv2.Canny(gaussianBlur,100,200)
    contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    print("Quantidade de contornos: " + str(len(contours)))
    num = 0
    prevx = 0
    prevy = 0
    prevw = 0
    prevh = 0
    for i, contour in enumerate(contours):
        x, y, w, h = cv2.boundingRect(contour)
        area = cv2.contourArea(contour)
        if((x != prevx) and (y != prevy) and (w != prevw) and (h != prevh)):
            print("Coordenadas do contorno: Left = " + str(x) + ", Top = " + str(y) + ", Right = " + str(x+w) + ", Botton = " + str(y+h))
            print("Area do contorno #" + str(i) + ": " + str(area))
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 1)
            num += 1
        else:
            print("ELSE Coordenadas do contorno: Left = " + str(x) + ", Top = " + str(y) + ", Right = " + str(x+w) + ", Botton = " + str(y+h))
        prevx = x
        prevy = y
        prevw = w
        prevh = h
    print(num)
    # Bom para a maioria, mas morre com 60.bmp e 205.bmp (melhor binarizacao para a 150.bmp)
    # Talvez seja possivel utilizar em todas se utilizarmos normalizacao local, mas teriamos que criar na mao
    otsu = cv2.threshold(gaussianBlur,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)

    # Binariza mas tira um pouco do interior dos graos. Morre com a 150.bmp
    adaptative = cv2.adaptiveThreshold(gaussianBlur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV,9,4)

    # Limpar ruídos da imagem Adaptative.
    rectKernel = cv2.getStructuringElement(cv2.MORPH_RECT,(2,2))
    openAdaptative = cv2.morphologyEx(adaptative, cv2.MORPH_OPEN, rectKernel)
    openCanny = cv2.morphologyEx(edges, cv2.MORPH_OPEN, rectKernel)

    cv2.imshow('img',img)
    # cv2.imshow('gray',gray)
    # cv2.imshow('normalized',normalized)
    # cv2.imshow('gaussian',gaussianBlur)

    # Salvando pois no Windows não consigo gerar imshow() usando terminal.
    # cv2.imwrite('Edges.png', edges)
    # cv2.imwrite('Adaptative.png', adaptative)
    # cv2.imwrite('openCanny.png', openCanny)
    # cv2.imwrite('Otsu.png', otsu[1])
    
    # cv2.imshow('edges',edges)
    # cv2.imshow('adaptative',adaptative)
    # cv2.imshow('Otsu',otsu[1])

    cv2.waitKey ()
    cv2.destroyAllWindows ()

if __name__ == '__main__':
    main ()

#===============================================================================