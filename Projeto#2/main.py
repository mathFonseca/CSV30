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
                    # TODO: Tratar casos que a janela cai pra fora da imagem.
                    # De acordo com PDF Trabalho 02 -  ignorar posições cujas janelas ficariam fora da imagem.
                    if(x_janela < WIDTH_IMAGE and y_janela < HEIGHT_IMAGE):
                        sum += img[y_janela][x_janela]
                        print(sum)
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
                # TODO: Tratar casos que a janela cai pra fora da imagem.
                # De acordo com PDF Trabalho 02 -  ignorar posições cujas janelas ficariam fora da imagem.
                if(x_janela < WIDTH_IMAGE):
                    sum += img[y][x_janela]
            imgHorizontal[y][x] = sum/WIDTH_WINDOW
    
    # Filtro Vertical (HEIGHT_WINDOW,1)
    for y in range(HEIGHT_IMAGE):
        for x in range(WIDTH_IMAGE):
            sum = np.zeros(3)
            for y_janela in range(y-(int(HEIGHT_WINDOW/2)),y+(int(HEIGHT_WINDOW/2)+1)):
                # TODO: Tratar casos que a janela cai pra fora da imagem.
                # De acordo com PDF Trabalho 02 -  ignorar posições cujas janelas ficariam fora da imagem.
                if(y_janela < HEIGHT_IMAGE):
                    sum += imgHorizontal[y_janela][x]
            imgSeparavel[y][x] = sum/HEIGHT_WINDOW
        
    return imgSeparavel

def filtroIntegral(img, HEIGHT_WINDOW, WIDTH_WINDOW):
    HEIGHT_IMAGE = img.shape[0]
    WIDTH_IMAGE = img.shape[1]

    print(HEIGHT_IMAGE)
    print(WIDTH_IMAGE)

    TOTAL = HEIGHT_WINDOW * WIDTH_WINDOW
    # Ajusta largura pro ímpar mais próximo (Sempre maior pra não gerar larguras menores
    # que a janela requisita pelo usuário).
    if(WIDTH_WINDOW%2 == 0): # Largura
        WIDTH_WINDOW += 1
    if(HEIGHT_WINDOW%2 == 0): # Altura
        HEIGHT_WINDOW += 1

    # Cria a imagem integral
    img_integral = img
    for y in range(0,HEIGHT_IMAGE):
        img_integral[y][0] = img[y][0]
        for x in range(1,WIDTH_IMAGE):
            img_integral[y][x] = img[y][x] + img_integral[y][x-1]
            
    for y in range(1,HEIGHT_IMAGE):
        for x in range(WIDTH_IMAGE):
            img_integral[y][x] = img_integral[y][x] + img_integral[y-1][x]

    # Salva uma cópia
    print(img_integral)
    img_filtrada = img_integral

    for pixel_y in range(0,HEIGHT_IMAGE):
        for pixel_x in range(0,WIDTH_IMAGE):
        # Identify 4 edges of rectangle
            # Checa se o retangulo da janela não ultrapassa a imagem

            maximum_x_value = (pixel_x + (WIDTH_WINDOW-1)/2)
            minimum_x_value = (pixel_x - (WIDTH_WINDOW-1)/2)

            minimum_y_value = (pixel_y - (HEIGHT_WINDOW-1)/2)
            maximum_y_value = (pixel_y + (HEIGHT_WINDOW-1)/2)

            if( minimum_y_value < 0 or maximum_y_value >= (HEIGHT_IMAGE)):
                # Ultrapasou as bordas.
                img_filtrada[pixel_y][pixel_x] = img_integral[pixel_y][pixel_x]  
            elif( minimum_x_value < 0 or maximum_x_value >= (WIDTH_IMAGE)):
                # Ultrapasou as bordas.
                img_filtrada[pixel_y][pixel_x] = img_integral[pixel_y][pixel_x] 
            elif( (minimum_y_value -1) < 0 or (minimum_x_value -1) < 0): 
                # # Janela cabe perfeitamente mas não dá para fazer o cálculo corretamente
                # print("Janela cabe mas não dá pra extender." + "(" + str(pixel_y) + "," + str(pixel_x) + ")")
                img_filtrada[pixel_y][pixel_x] = np.floor(img_integral[int(pixel_y + (HEIGHT_WINDOW-1)/2)][int(pixel_x + (WIDTH_WINDOW-1)/2)] /TOTAL)
            else:
                # print("# Está dentro as bordas." + "(" + str(pixel_y) + "," + str(pixel_x) + ")")

                bottomLeft = img_integral[int(maximum_y_value)][int(minimum_x_value -1)]
                bottomRight = img_integral[int(maximum_y_value)][int(maximum_x_value)]
                topLeft = img_integral[int(minimum_y_value)][int(minimum_x_value)]
                topRight = img_integral[int(minimum_y_value -1)][int(maximum_x_value)]
                img_filtrada[pixel_y][pixel_x] = np.floor((bottomRight - bottomLeft - topRight + topLeft)/TOTAL)
    # TODO: Recortar linhas e colunas cuja janela ficou pra fora.       
                    
    return img_filtrada


def main():
    # Abre a imagem em escala de cinza.
    img = cv2.imread (INPUT_IMAGE)
    if img is None:
        print ('Erro abrindo a imagem.\n')
        sys.exit ()

    # É uma boa prática manter o shape com 3 valores, independente da imagem ser
    # colorida ou não. Também já convertemos para float32.
    #img = img.reshape ((img.shape [0], img.shape [1], 1))
    img = img.astype (np.float32) / 255

    # Filtra a imagem.
    # TODO: Preencher lista de filtragens da imagem

    img_out_integral = filtroMediaIngenuo(img, HEIGHT_WINDOW, WIDTH_WINDOW)

    # Salva imagens filtradas
    cv2.imwrite ('02 - integral.png', img_out_integral*255)

    cv2.waitKey ()
    cv2.destroyAllWindows ()


if __name__ == '__main__':
    main ()

#===============================================================================