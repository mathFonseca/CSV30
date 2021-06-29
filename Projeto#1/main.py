#===============================================================================
# Exemplo: segmentação de uma imagem em escala de cinza.
#-------------------------------------------------------------------------------
# Autor: Bogdan T. Nassu
# Universidade Tecnológica Federal do Paraná
#===============================================================================

import sys
import timeit
import numpy as np
import cv2

# TODO: Descomentar img.show() na entrega final. Posso testar pelo Windows depois

#===============================================================================

INPUT_IMAGE = 'arroz.bmp'

# TODO: ajuste estes parâmetros!
NEGATIVO = False
THRESHOLD = 0.8
ALTURA_MIN = 18
LARGURA_MIN = 18
N_PIXELS_MIN = 413

#===============================================================================

def binariza (img, threshold):
    ''' Binarização simples por limiarização.

Parâmetros: img: imagem de entrada. Se tiver mais que 1 canal, binariza cada
              canal independentemente.
            threshold: limiar.
            
Valor de retorno: versão binarizada da img_in.'''

    # TODO: escreva o código desta função.
    # Dica/desafio: usando a função np.where, dá para fazer a binarização muito
    # rapidamente, e com apenas uma linha de código!

    # np.where(condition, if Yes, if No)
    # Nesse caso, se o valor do pixel menor que threshold, põe como 0; Se maior,
    # põe -1 Esses valores são pra o algoritmo, e não faz muito sentido
    # tentar printar a imagem assim.

    # TODO: modificar para funcionar com mais de um canal. Acredito eu que seria
    # algo como img[x] ? Mas não sei como testar.
    return np.uint8(np.where( img <= threshold, 0, 1))
    

#-------------------------------------------------------------------------------

def inunda (label, img, row, col):
    rows, cols, channels = img.shape
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

def rotula (img, largura_min, altura_min, n_pixels_min):
    '''Rotulagem usando flood fill. Marca os objetos da imagem com os valores
[0.1,0.2,etc].

Parâmetros: img: imagem de entrada E saída.
            largura_min: descarta componentes com largura menor que esta.
            altura_min: descarta componentes com altura menor que esta.
            n_pixels_min: descarta componentes com menos pixels que isso.

Valor de retorno: uma lista, onde cada item é um vetor associativo (dictionary)
com os seguintes campos:

'label': rótulo do componente.
'n_pixels': número de pixels do componente.
'T', 'L', 'B', 'R': coordenadas do retângulo envolvente de um componente conexo,
respectivamente: topo, esquerda, baixo e direita.'''

    # TODO: escreva esta função.
    # Use a abordagem com flood fill recursivo.
    rows, cols, channels = img.shape
    img_gs = img
    img_gs = np.where(img == 1, -1, 1) #coloca label -1 em todos os pixels brancos

    label = -2 #inicia o contador de labels em -2
    coords = np.argwhere(cv2.inRange(img_gs, -1, -1)) #retorna uma lista de tuplas com as coordenadas de todos os pixels classificados com label atual
    for coord in coords: #para cada coordenada da lista
        if(img_gs[coord[0],coord[1]] == -1): #se o pixel selecionado tem o label -1
            inunda(label, img_gs, coord[0], coord[1]) #chamamos inunda para esse blob
            label -= 1 #inunda so retorna quando o blob for completamente percorrido, desta forma podemos incrementar o label

    dictBlobs = [] #lista de dicionarios para cada um dos blobs
    for labels in range (label, -1): #percorre todos os valores de labels encontrados iniciando em -2
        pixels = np.count_nonzero(img_gs == labels) #conta o numero de pixels que estao classificado com label atual
        if (pixels >= N_PIXELS_MIN): #verifica se a quantidade de pixels e valida para um blob
            coords = np.argwhere(cv2.inRange(img_gs, labels, labels)) #retorna uma lista de tuplas com as coordenadas de todos os pixels classificados com label atual
            max = np.amax(coords, axis=0) #pega a tupla de maior valor levando em considereção suas duas componentes
            min = np.amin(coords, axis=0) #pega a tupla de menor valor levando em considereção suas duas componentes
            alt = max[1] - min[1] #calcaula a altora do blob em pixels
            lar = max[0] - min[0] #calcaula a lergura do blob em pixels
            print("Label: " + str(labels) + " | n_pixels: " + str(pixels) + " pixels | altura: " + str(alt) + " pixels | largura: " + str(lar) + " pixels")
            if (alt >= altura_min and lar >= largura_min): #verifica se a altura e a largura sao validas para um blob
                blob = { #cria um dicionario com as informacoes do blob
                    'label' : labels,
                    'n_pixels' : pixels,
                    'L' : min[1],
                    'T' : min[0],
                    'R' : max[1],
                    'B' : max[0]
                }
                dictBlobs.append(blob)

    return(dictBlobs)
#===============================================================================

def main ():

    # Abre a imagem em escala de cinza.
    img = cv2.imread (INPUT_IMAGE, cv2.IMREAD_GRAYSCALE)
    if img is None:
        print ('Erro abrindo a imagem.\n')
        sys.exit ()

    # É uma boa prática manter o shape com 3 valores, independente da imagem ser
    # colorida ou não. Também já convertemos para float32.
    img = img.reshape ((img.shape [0], img.shape [1], 1))
    img = img.astype (np.float32) / 255

    # Mantém uma cópia colorida para desenhar a saída.
    img_out = cv2.cvtColor (img, cv2.COLOR_GRAY2BGR)

    # Segmenta a imagem.
    if NEGATIVO:
        img = 1 - img
    img = binariza (img, THRESHOLD)
    # cv2.imshow ('01 - binarizada', img)
    cv2.imwrite ('01 - binarizada.png', img*255)

    start_time = timeit.default_timer ()
    componentes = rotula (img, LARGURA_MIN, ALTURA_MIN, N_PIXELS_MIN)
    n_componentes = len (componentes)
    print ('Tempo: %f' % (timeit.default_timer () - start_time))
    print ('%d componentes detectados.' % n_componentes)

    # # Mostra os objetos encontrados.
    for c in componentes:
        cv2.rectangle (img_out, (c ['L'], c ['T']), (c ['R'], c ['B']), (0,0,1))

    # cv2.imshow ('02 - out', img_out)
    cv2.imwrite ('02 - out.png', img_out*255)
    cv2.waitKey ()
    cv2.destroyAllWindows ()


if __name__ == '__main__':
    main ()

#===============================================================================
