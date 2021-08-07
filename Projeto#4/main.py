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
import matplotlib.pyplot as plt
import cv2

# Variaveis globais. 
INPUT_IMAGE = 'Images/114.bmp'

def inunda (label, img, row, col):
    rows, cols = img.shape
    if(img[row,col] == -1): #verifica se o pixel atual faz parte do blob
        img[row,col] = label #coloca um novo label para esse pixel
        if(row+1 <= rows): #verifica se o pixel a direta do atual faz parte da imagem
            inunda (label, img, row+1, col) #chama inunda para esse pixel
        if(row-1 >= 0): #verifica se o pixel a esquerda do atual faz parte da imagem
            inunda (label, img, row-1, col) #chama inunda para esse pixel
        if(col+1 <= cols): #verifica se o pixel acima do atual faz parte da imagem
            inunda (label, img, row, col+1) #chama inunda para esse pixel
        if(col-1 >= 0): #verifica se o pixel abaixo do atual faz parte da imagem
            inunda (label, img, row, col-1) #chama inunda para esse pixel

def rotula (img):
    rows, cols = img.shape
    img_gs = img
    img_gs = np.where(img == 1, -1, 1) #coloca label -1 em todos os pixels brancos

    label = -2 #inicia o contador de labels em -2
    coords = np.argwhere(cv2.inRange(img_gs, -1, -1)) #retorna uma lista de tuplas com as coordenadas de todos os pixels classificados com label atual
    for coord in coords: #para cada coordenada da lista
        if(img_gs[coord[0],coord[1]] == -1): #se o pixel selecionado tem o label -1
            inunda(label, img_gs, coord[0], coord[1]) #chamamos inunda para esse blob
            label -= 1 #inunda so retorna quando o blob for completamente percorrido, desta forma podemos incrementar o label
    areas = []
    for labels in range (label, -1): #percorre todos os valores de labels encontrados iniciando em -2
        pixels = np.count_nonzero(img_gs == labels) #conta o numero de pixels que estao classificado com label atual
        areas.append(pixels)
    return(areas)

def main():
    # Abre a imagem.
    img = cv2.imread (INPUT_IMAGE)
    if img is None:
        print ('Erro abrindo a imagem.\n')
        sys.exit ()

    # Step 1 - Escala de Cinza
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Step 2 - Limiarização adaptativa.
    # TODO Encontrar um valor bom de C que em conjunto com sigma estime bem a quanatidade de arroz para todas as imagens
    C = -50
    adaptative = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,51,C)
    kernel = np.ones((3,3),np.uint8)
    fechamento = cv2.morphologyEx(adaptative,cv2.MORPH_OPEN,kernel)
    
    # É uma boa prática manter o shape com 3 valores, independente da imagem ser
    # colorida ou não. Também já convertemos para float32.
    fechamento = fechamento.astype(np.float32)/255

    # Retorna uma lista das areas dos blobs encontrados
    areas = rotula(fechamento)
    arr = np.array(areas)

    # Cria um histograma das areas encontradas
    histograma = np.histogram(arr, bins='auto')

    # Imaginando o histograma como uma distribuicao gaussiana,
    # as areas minima e maxima serao dadas pelo valor de pico do histograma
    # deslocado por um valor sigma.
    # TODO encontrar um valor bom de sigma que juntamente com C estime bem para todas as imgens
    sigma = 1 
    min_area = histograma[1][np.argmax(histograma[0]) - sigma]
    max_area = histograma[1][np.argmax(histograma[0]) + sigma]
    print("Min_area = " + str(min_area) + " | Max_area = " + str(max_area))

    # Cria uma mascara para o vetor de areas apenas conter valores validos para arroz
    singular_mask = (min_area < arr) & (arr <= max_area)

    # Calcula a media dos valores validos do vetor 
    area_media = np.mean(arr[singular_mask])

    # Soma todos os valores validos de arroz divididos pela media calculada e truca 
    n_arroz = int(np.sum(np.round(arr/area_media)))
    print('Numero de arroz:', n_arroz)

    cv2.imshow('img',img)
    cv2.imshow('adaptative',adaptative)
    cv2.imshow('fechamento',fechamento)

    # Salvando pois no Windows não consigo gerar imshow() usando terminal.
    # cv2.imwrite('Adaptative.png', adaptative)
    # cv2.imwrite('fechamento.png', fechamento)

    cv2.waitKey ()
    cv2.destroyAllWindows ()

if __name__ == '__main__':
    main ()

#===============================================================================