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

#===============================================================================

INPUT_IMAGE = 'arroz.bmp'

# TODO: ajuste estes parâmetros!
NEGATIVO = False
THRESHOLD = 0.7
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
    return np.uint8(np.where( img <= threshold, 0, 1))
    

#-------------------------------------------------------------------------------

def inunda (label, img, row, col):
    rows, cols, channels = img.shape
    if(img[row,col] == -1):
        img[row,col] = label
        if(row+1 <= rows):
            inunda (label, img, row+1, col)
        if(row-1 >= 0):
            inunda (label, img, row-1, col)
        if(col+1 <= cols):
            inunda (label, img, row, col+1)
        if(col-1 >= 0):
            inunda (label, img, row, col-1)

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
    img_gs = np.where(img == 1, -1, 1)

    label = -2
    for row in range (rows):
        for col in range (cols):
            if(img_gs[row,col] == -1):
                inunda(label, img_gs, row, col)
                label -= 1

    dictBlobs = []
    for labels in range (label, -1):
        if (np.count_nonzero(img_gs == labels) >= N_PIXELS_MIN):
            pixels = np.count_nonzero(img_gs == labels)
            print("Label: " + str(labels) + " - " + str(pixels) + " pixels")
            coord = np.argwhere(cv2.inRange(img_gs, labels, labels))
            max = np.amax(coord, axis=0)
            min = np.amin(coord, axis=0)
            alt = max[1] - min[1]
            lar = max[0] - min[0]
            if (alt >= altura_min and lar >= largura_min):
                blob = {
                    'label' : labels,
                    'n_pixels' : pixels,
                    'L' : min[1],
                    'T' : min[0],
                    'R' : max[1],
                    'B' : max[0]
                }
                dictBlobs.append(blob)

    print(len(dictBlobs))
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
    cv2.imshow ('01 - binarizada', img)
    cv2.imwrite ('01 - binarizada.png', img*255)

    start_time = timeit.default_timer ()
    componentes = rotula (img, LARGURA_MIN, ALTURA_MIN, N_PIXELS_MIN)
    n_componentes = len (componentes)
    print ('Tempo: %f' % (timeit.default_timer () - start_time))
    print ('%d componentes detectados.' % n_componentes)

    # # Mostra os objetos encontrados.
    for c in componentes:
        cv2.rectangle (img_out, (c ['L'], c ['T']), (c ['R'], c ['B']), (0,0,1))

    cv2.imshow ('02 - out', img_out)
    cv2.imwrite ('02 - out.png', img_out*255)
    cv2.waitKey ()
    cv2.destroyAllWindows ()


if __name__ == '__main__':
    main ()

#===============================================================================
