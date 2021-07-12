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

INPUT_IMAGE = 'Exemplos/b01 - Original.bmp'
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
            sum = np.zeros(3)
            for y_janela in range(y-(int(HEIGHT_WINDOW/2)),y+(int(HEIGHT_WINDOW/2))+1):
                for x_janela in range(x-int((WIDTH_WINDOW/2)),x+int((WIDTH_WINDOW/2))+1):
                    if(x_janela < WIDTH_IMAGE and y_janela < HEIGHT_IMAGE):
                        sum += img[y_janela][x_janela]
                        # print(sum)
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
            sum = np.zeros(3)
            for x_janela in range(x-(int(WIDTH_WINDOW/2)),x+(int(WIDTH_WINDOW/2)+1)):
                if(x_janela < WIDTH_IMAGE):
                    sum += img[y][x_janela]
            imgHorizontal[y][x] = sum/WIDTH_WINDOW
    
    # Filtro Vertical (HEIGHT_WINDOW,1)
    for y in range(HEIGHT_IMAGE):
        for x in range(WIDTH_IMAGE):
            sum = np.zeros(3)
            for y_janela in range(y-(int(HEIGHT_WINDOW/2)),y+(int(HEIGHT_WINDOW/2)+1)):
                if(y_janela < HEIGHT_IMAGE):
                    sum += imgHorizontal[y_janela][x]
            imgSeparavel[y][x] = sum/HEIGHT_WINDOW
        
    return imgSeparavel

def filtroIntegral(img, HEIGHT_WINDOW, WIDTH_WINDOW):
    HEIGHT_IMAGE = img.shape[0]
    WIDTH_IMAGE = img.shape[1]

    TOTAL = HEIGHT_WINDOW * WIDTH_WINDOW
    # Ajusta largura pro ímpar mais próximo (Sempre maior pra não gerar larguras menores
    # que a janela requisita pelo usuário).
    if(WIDTH_WINDOW%2 == 0): # Largura
        WIDTH_WINDOW += 1
    if(HEIGHT_WINDOW%2 == 0): # Altura
        HEIGHT_WINDOW += 1

    # Cria a imagem integral
    img_somada = img.copy()

    for y in range(0,HEIGHT_IMAGE):
        img_somada[y][0] = img[y][0]
        for x in range(1,WIDTH_IMAGE):
            img_somada[y][x] = img[y][x] + img_somada[y][x-1]
            
    for y in range(1,HEIGHT_IMAGE):
        for x in range(WIDTH_IMAGE):
            img_somada[y][x] = img_somada[y][x] + img_somada[y-1][x]

    print(img_somada[y][x])
    # Salva uma cópia
    img_integral = img_somada.copy()

    for pixel_y in range(0,HEIGHT_IMAGE):
        for pixel_x in range(0,WIDTH_IMAGE):
        # Identify 4 edges of rectangle
            # Checa se o retangulo da janela não ultrapassa a imagem

            # Valor máximo: menor possível desde que seja abaixo dos limites da imagem
            maximum_x_value = int(min(WIDTH_IMAGE -1, pixel_x + (WIDTH_WINDOW-1)/2))
            maximum_y_value = int(min(HEIGHT_IMAGE -1,pixel_y + (HEIGHT_WINDOW-1)/2))

            # Valor minimo: mais alto possivel desde que seja acima de zero.
            minimum_x_value = int(max(0, pixel_x - (WIDTH_WINDOW-1)/2))
            minimum_y_value = int(max(0,pixel_y - (HEIGHT_WINDOW-1)/2))
            
            img_integral[pixel_y][pixel_x] = img_somada[maximum_y_value][maximum_x_value]

            # Case 1 - Janela ultrapassou 
            if(minimum_y_value > 0):
                img_integral[pixel_y][pixel_x] -= img_somada[minimum_y_value - 1][maximum_x_value]
            
            if(minimum_x_value > 0):
                img_integral[pixel_y][pixel_x] -= img_somada[maximum_y_value][minimum_x_value -1]

            if(minimum_x_value > 0 and minimum_y_value > 0):
                img_integral[pixel_y][pixel_x] += img_somada[minimum_y_value-1][minimum_x_value-1]

            # TODO: Ajustar divisão pro número correto
            img_integral[pixel_y][pixel_x] = img_integral[pixel_y][pixel_x]/TOTAL  
                    
    return img_integral

def main():
    # Abre a imagem.
    img = cv2.imread (INPUT_IMAGE)
    if img is None:
        print ('Erro abrindo a imagem.\n')
        sys.exit ()

    # É uma boa prática manter o shape com 3 valores, independente da imagem ser
    # colorida ou não. Também já convertemos para float32.
    #img = img.reshape ((img.shape [0], img.shape [1], 1))
    img = img.astype (np.float32) / 255


    # img_out_ingenuo = filtroMediaIngenuo(img, HEIGHT_WINDOW, WIDTH_WINDOW)
    # cv2.imwrite ('01 - ingenuo.png', img_out_ingenuo*255)

    # img_out_separavel = filtroSeparavel(img, HEIGHT_WINDOW, WIDTH_WINDOW)
    # cv2.imwrite ('02 - separavel.png', img_out_separavel*255)

    img_out_integral = filtroIntegral(img, HEIGHT_WINDOW, WIDTH_WINDOW)
    cv2.imwrite ('03 - integral.png', img_out_integral*255)

    cv2.waitKey ()
    cv2.destroyAllWindows ()


if __name__ == '__main__':
    main ()

#===============================================================================