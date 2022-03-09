# Algoritmo Posicion Falsa para raices
# busca en intervalo [a,b]
# tolera = error

import numpy as np
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr
from derivadas import transformations

# INGRESO
x = sp.Symbol('x')

def falsa_pos(f,a,b,tolera):
    f = str(parse_expr(f,transformations=transformations))
    fx = sp.lambdify(x,f,'numpy')
    #fx = lambda x: ma.exp(x-2)-ma.log(x) -2.5

    lista_c =[]
    #a = 3
    #b = 4
    #tolera = 0.0001

    # PROCEDIMIENTO
    tabla = []
    tramo = abs(b-a)
    fa = fx(a)
    fb = fx(b)
    while not(tramo<=tolera):
        c = b - fb*(a-b)/(fa-fb)
        lista_c.append(c)
        fc = fx(c)
        tabla.append([a,c,b,fa,fc,fb,tramo])
        cambio = np.sign(fa)*np.sign(fc)
        if cambio>0:
            tramo = abs(c-a)
            a = c
            fa = fc
        else:
            tramo = abs(b-c)
            b = c
            fb = fc
            
    tabla = np.array(tabla)
    ntabla = len(tabla)

    # SALIDA
    np.set_printoptions(precision=4)

    return tabla,lista_c
    #for i in range(0,ntabla,1):
        #print('------------------------------------------------------')
        #print('iteración:  ',i)
        #print('Raiz : ', lista_c[i])
        #print('[a,c,b]:    ', tabla[i,0:3])
        #print('[fa,fc,fb]: ', tabla[i,3:6])
        #print('[tramo]:    ', tabla[i,6])

    #print('------------------------------------------------------')
    #print('raiz:  ',c)
    #print('error: ',tramo)