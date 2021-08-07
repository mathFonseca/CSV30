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

IMAGE_1 = 'Images/60.bmp'
IMAGE_2 = 'Images/82.bmp'
IMAGE_3 = 'Images/114.bmp'
IMAGE_4 = 'Images/150.bmp'
IMAGE_5 = 'Images/205.bmp'

ALL_IMAGES_TEST = True

# Good Candidates to try
# C = -50 / Sigma = 1
# C = -25 / Sigma = 1

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

def allTest(CTest,SigmaTest = 1):
    # Abre as imagens.
    image_01 = cv2.imread(IMAGE_1)
    if image_01 is None:
        print ('Erro abrindo a imagem 01.\n')
        sys.exit ()

    image_02 = cv2.imread(IMAGE_2)
    if image_02 is None:
        print ('Erro abrindo a imagem 02.\n')
        sys.exit ()

    image_03 = cv2.imread(IMAGE_3)
    if image_03 is None:
        print ('Erro abrindo a imagem 03.\n')
        sys.exit ()

    image_04 = cv2.imread(IMAGE_4)
    if image_04 is None:
        print ('Erro abrindo a imagem 04.\n')
        sys.exit ()

    image_05 = cv2.imread(IMAGE_5)
    if image_05 is None:
        print ('Erro abrindo a imagem 05.\n')
        sys.exit ()

    # Escala de Cinza
    image_01_gray = cv2.cvtColor(image_01, cv2.COLOR_BGR2GRAY)
    image_02_gray = cv2.cvtColor(image_02, cv2.COLOR_BGR2GRAY)
    image_03_gray = cv2.cvtColor(image_03, cv2.COLOR_BGR2GRAY)
    image_04_gray = cv2.cvtColor(image_04, cv2.COLOR_BGR2GRAY)
    image_05_gray = cv2.cvtColor(image_05, cv2.COLOR_BGR2GRAY)

    # Limiarização Adaptativa
    C = CTest
    adaptative_01 = cv2.adaptiveThreshold(image_01_gray,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,51,C)
    adaptative_02 = cv2.adaptiveThreshold(image_02_gray,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,51,C)
    adaptative_03 = cv2.adaptiveThreshold(image_03_gray,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,51,C)
    adaptative_04 = cv2.adaptiveThreshold(image_04_gray,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,51,C)
    adaptative_05 = cv2.adaptiveThreshold(image_05_gray,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,51,C)

    kernel = np.ones((3,3),np.uint8)

    fechamento_01 = cv2.morphologyEx(adaptative_01,cv2.MORPH_OPEN,kernel)
    fechamento_02 = cv2.morphologyEx(adaptative_02,cv2.MORPH_OPEN,kernel)
    fechamento_03 = cv2.morphologyEx(adaptative_03,cv2.MORPH_OPEN,kernel)
    fechamento_04 = cv2.morphologyEx(adaptative_04,cv2.MORPH_OPEN,kernel)
    fechamento_05 = cv2.morphologyEx(adaptative_05,cv2.MORPH_OPEN,kernel)
    
    fechamento_01 = fechamento_01.astype(np.float32)/255    
    fechamento_02 = fechamento_02.astype(np.float32)/255    
    fechamento_03 = fechamento_03.astype(np.float32)/255    
    fechamento_04 = fechamento_04.astype(np.float32)/255    
    fechamento_05 = fechamento_05.astype(np.float32)/255

    # Retorna uma lista das areas dos blobs encontrados
    areas_01 = rotula(fechamento_01)
    areas_02 = rotula(fechamento_02)
    areas_03 = rotula(fechamento_03)
    areas_04 = rotula(fechamento_04)
    areas_05 = rotula(fechamento_05)

    arr_01 = np.array(areas_01)
    arr_02 = np.array(areas_02)
    arr_03 = np.array(areas_03)
    arr_04 = np.array(areas_04)
    arr_05 = np.array(areas_05)

    # Cria um histograma das areas encontradas
    histograma_01 = np.histogram(arr_01, bins='auto')
    histograma_02 = np.histogram(arr_02, bins='auto')
    histograma_03 = np.histogram(arr_03, bins='auto')
    histograma_04 = np.histogram(arr_04, bins='auto')
    histograma_05 = np.histogram(arr_05, bins='auto')


    sigma = SigmaTest 
    min_area_01 = histograma_01[1][np.argmax(histograma_01[0]) - sigma]
    max_area_01 = histograma_01[1][np.argmax(histograma_01[0]) + sigma]

    min_area_02 = histograma_02[1][np.argmax(histograma_02[0]) - sigma]
    max_area_02 = histograma_02[1][np.argmax(histograma_02[0]) + sigma]

    min_area_03 = histograma_03[1][np.argmax(histograma_03[0]) - sigma]
    max_area_03 = histograma_03[1][np.argmax(histograma_03[0]) + sigma]

    min_area_04 = histograma_04[1][np.argmax(histograma_04[0]) - sigma]
    max_area_04 = histograma_04[1][np.argmax(histograma_04[0]) + sigma]

    min_area_05 = histograma_05[1][np.argmax(histograma_05[0]) - sigma]
    max_area_05 = histograma_05[1][np.argmax(histograma_05[0]) + sigma]

    singular_mask_01 = (min_area_01 < arr_01) & (arr_01 <= max_area_01)
    area_media_01 = np.mean(arr_01[singular_mask_01])
    n_arroz_01 = int(np.sum(np.round(arr_01/area_media_01)))
    if( np.abs(60 - n_arroz_01) <= 15  ):
        print('Numero de arroz Image 01:', n_arroz_01)

    singular_mask_02 = (min_area_02 < arr_02) & (arr_02 <= max_area_02)
    area_media_02 = np.mean(arr_02[singular_mask_02])
    n_arroz_02 = int(np.sum(np.round(arr_02/area_media_02)))
    if( np.abs(82 - n_arroz_02) <= 15  ):
        print('Numero de arroz Image 02:', n_arroz_02)
    
    singular_mask_03 = (min_area_03 < arr_03) & (arr_03 <= max_area_03)
    area_media_03 = np.mean(arr_03[singular_mask_03])
    n_arroz_03 = int(np.sum(np.round(arr_03/area_media_03)))
    if( np.abs(114 - n_arroz_03) <= 15  ):
        print('Numero de arroz Image 03:', n_arroz_03)
        
    singular_mask_04 = (min_area_04 < arr_04) & (arr_04 <= max_area_04)
    area_media_04 = np.mean(arr_04[singular_mask_04])
    n_arroz_04 = int(np.sum(np.round(arr_04/area_media_04)))
    if( np.abs(150 - n_arroz_04) <= 15  ):
        print('Numero de arroz Image 04:', n_arroz_04)    
    
    singular_mask_05 = (min_area_05 < arr_05) & (arr_05 <= max_area_05)
    area_media_05 = np.mean(arr_05[singular_mask_05])
    n_arroz_05 = int(np.sum(np.round(arr_05/area_media_05)))
    if( np.abs(205 - n_arroz_05) <= 15  ):
        print('Numero de arroz Image 05:', n_arroz_05) 
    

def main():
    
    img = cv2.imread (INPUT_IMAGE)
    if img is None:
        print ('Erro abrindo a imagem.\n')
        sys.exit ()

    if ALL_IMAGES_TEST:
        allTest(-25,1)
        sys.exit()

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

    # cv2.imshow('img',img)
    # cv2.imshow('adaptative',adaptative)
    # cv2.imshow('fechamento',fechamento)

    # Salvando pois no Windows não consigo gerar imshow() usando terminal.
    cv2.imwrite('Adaptative.png', adaptative)
    cv2.imwrite('fechamento.png', fechamento)

    cv2.waitKey ()
    cv2.destroyAllWindows ()

if __name__ == '__main__':
    main ()

#===============================================================================