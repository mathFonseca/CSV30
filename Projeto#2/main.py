#===============================================================================
# Trabalho 02: Filtros de Média 
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

# Variaveis globais. 

INPUT_IMAGE = 'Exemplos/a01 - Original.bmp'
HEIGHT_WINDOW = 7   # Altura
WIDTH_WINDOW = 7     # Largura

def filtroMediaIngenuo(img, HEIGHT_WINDOW, WIDTH_WINDOW):

    HEIGHT_IMAGE = img.shape[0]
    WIDTH_IMAGE = img.shape[1]
    WINDOW_SIZE = HEIGHT_WINDOW * WIDTH_WINDOW

    # Cria imagem de saída de mesmas proporções.
    imgMediaIngenuo = img

    for y in range(HEIGHT_IMAGE):
        for x in range(WIDTH_IMAGE):
            sum = 0
            for y_janela in range(y-(HEIGHT_WINDOW/2),y+(HEIGHT_WINDOW/2)+1):
                for x_janela in range(x-(WIDTH_WINDOW/2),x+(WIDTH_WINDOW/2)+1):

                    # TODO: Tratar casos que a janela cai pra fora da imagem.
                    # De acordo com PDF Trabalho 02 -  ignorar posições cujas janelas ficariam fora da imagem.
                    sum += img[y_janela][x_janela]
            imgMediaIngenuo[y][x] = sum/WINDOW_SIZE
    
    return imgMediaIngenuo


def filtroSeparavel(img, HEIGHT_WINDOW, WIDTH_WINDOW):

    HEIGHT_IMAGE = img.shape[0]
    WIDTH_IMAGE = img.shape[1]

    # Cria imagem de saída e uma imagem intermediária de mesmas proporções.
    imgHorizontal = img
    imgSeparavel = img

    # Filtro Horizontal (1,WIDTH_WINDOW)
    for y in range(HEIGHT_IMAGE):
        for x in range(WIDTH_IMAGE):
            sum = 0
            for x_janela in range(x-(WIDTH_WINDOW/2),x+(WIDTH_WINDOW/2)+1):

                # TODO: Tratar casos que a janela cai pra fora da imagem.
                # De acordo com PDF Trabalho 02 -  ignorar posições cujas janelas ficariam fora da imagem.
                sum += img[y][x_janela]
            imgHorizontal[y][x] = sum/WIDTH_WINDOW
    
    # Filtro Vertical (HEIGHT_WINDOW,1)
    for y in range(HEIGHT_IMAGE):
        for x in range(WIDTH_IMAGE):
            sum = 0
            for y_janela in range(y-(HEIGHT_WINDOW/2),y+(HEIGHT_WINDOW/2)+1):

                # TODO: Tratar casos que a janela cai pra fora da imagem.
                # De acordo com PDF Trabalho 02 -  ignorar posições cujas janelas ficariam fora da imagem.
                sum += imgHorizontal[y_janela][x]
            imgSeparavel[y][x] = sum/HEIGHT_WINDOW
        
    return imgSeparavel

def somaImagem(img):
    
    imgSum = img

    for y in range(imgSum.shape[0]):
        imgSum[y][0] = img[y][0]
        for x in range(1,imgSum.shape[1]):
            imgSum[y][x] = img[y][x] + imgSum[y][x-1]

    for y in range(1,imgSum.shape[0]):
        for x in range(imgSum.shape[1]):
            imgSum[y][x] = imgSum[y][x] + imgSum[y-1][x]

    return imgSum

def filtroIntegral(img, HEIGHT_WINDOW, WIDTH_WINDOW):
    
    imgSum = somaImagem(img)
    imgIntegral = img

    for y in range(imgSum.shape[0]):
        for x in range(imgSum.shape[1]):
        
            # TODO: Calcular pontos da janela.
            min_row, max_row = int(y -HEIGHT_WINDOW/2), int(y+HEIGHT_WINDOW/2)
            min_col, max_col = int(x -WIDTH_WINDOW/2), int(x+WIDTH_WINDOW/2)

            if( max_row < imgSum.shape[0] and max_col < imgSum.shape[1]):

                # Calcula o Bottom Right da janela                
                imgIntegral[y][x] = imgSum[max_row][max_col]

                if((min_row -1) > 0):
                    imgIntegral[y][x] -= imgSum[(min_row -1)][max_col]
                
                if((min_col -1 ) > 0):
                    imgIntegral[y][x] -= imgSum[(min_row)][(min_col -1)]

                if( ((min_row -1) > 0) and ((min_col -1 ) > 0) ):
                    imgIntegral[y][x] += imgSum[(min_row -1)][(min_col -1)]

            else:
                # Para tratar casos que a janela ultrapassa as bordas Direita e Inferior
                # Deixamos o valor que tá no pixel originalmente
                # E eliminamos depois.
                imgIntegral[y][x] = -1
    
    # TODO: Cortar colunas e linhas não tratadas fora.
    return imgIntegral

def main():
    # Abre a imagem em escala de cinza.
    img = cv2.imread (INPUT_IMAGE)
    if img is None:
        print ('Erro abrindo a imagem.\n')
        sys.exit ()

    # É uma boa prática manter o shape com 3 valores, independente da imagem ser
    # colorida ou não. Também já convertemos para float32.
    # img = img.reshape ((img.shape [0], img.shape [1], 1))
    # img = img.astype (np.float32) / 255

    # Filtra a imagem.
    # TODO: Preencher lista de filtragens da imagem

    img_out_integral = filtroIntegral(img, HEIGHT_WINDOW, WIDTH_WINDOW)

    # Salva imagens filtradas
    cv2.imwrite ('02 - integral.png', img_out_integral)

    cv2.waitKey ()
    cv2.destroyAllWindows ()


if __name__ == '__main__':
    main ()

#===============================================================================