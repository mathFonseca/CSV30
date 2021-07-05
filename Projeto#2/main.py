#===============================================================================
# Trabalho 02: Filtros de Média# 
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

INPUT_IMAGE = 'arroz.bmp'

def filtroMediaIngenuo():
    ''' Filtro média 

Parâmetros: img: imagem de entrada. Se tiver mais que 1 canal, filtra cada
              canal independentemente.
            largura: Tamanho da Janela (ajustada pra ímpar).
            
Valor de retorno: versão filtro da média da img_in.'''
    # TODO
    # Margem: ignorar posições fora da janela.


def filtroMedia():
    ''' Filtro média 

Parâmetros: img: imagem de entrada. Se tiver mais que 1 canal, filtra cada
              canal independentemente.
            largura: Tamanho da Janela (ajustada pra ímpar).
            
Valor de retorno: versão filtro da média da img_in.'''
    # TODO
    # Margem: ignorar posições fora da janela.


def filtroIntegral(img, largura):
    ''' Filtro média 

Parâmetros: img: imagem de entrada. Se tiver mais que 1 canal, filtra cada
              canal independentemente.
            largura: Tamanho da Janela (ajustada pra ímpar).
            
Valor de retorno: versão filtro da média usando conceito de Imagens Integrais, da img_in.'''
    # Ajusta largura pro ímpar mais próximo (Sempre maior pra não gerar larguras menores
    # que a janela requisita pelo usuário).

    if(largura%2 == 0):
        largura += 1

    # Cria a imagem integral
    img_integral = img
    for y in range(0,len(img)):
        img_integral[0][y] = img[0,y]
        for x in range(1,len(img)):
            img_integral[x][y] = img[x][y] + img_integral[x-1][y]
    
    for y in range(1,len(img)):
        for x in range(len(img)):
            img_integral[x][y] = img_integral[x][y] + img_integral[x][y-1]

    # TODO: Comparar com a função do opencv2
    # Margem: saída menor que a janela de entrada.


def main():
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

    # Filtra a imagem.
    # TODO: Preencher lista de filtragens da imagem

    # Salva imagens filtradas
    cv2.imwrite ('02 - out.png', img_out*255)

    
    cv2.waitKey ()
    cv2.destroyAllWindows ()


if __name__ == '__main__':
    main ()

#===============================================================================