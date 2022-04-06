from jinja2 import evalcontextfilter, evalcontextfunction
import numpy as np
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr
from derivadas import transformations
from numpy import sin, cos, tan, cosh, tanh, sinh


def lit(xn,q):#list of f(x) creating
    #x = sp.Symbol('x')
    #q = str(parse_expr(q, transformations= transformations))
    #q = sp.lambdify(x, q,'numpy')
    #print("LA Q: ", q)
    l=len(xn)
#    print(l)
    b=[]
    s=[]
    for i in range(l):
        x=y=o=xn[i]
        b.append(eval(q))
    return b

def intg(a,b):
    l=len(b)-1
    j=0
    h=(a[1]-a[0])/3
    for i in range(0,l-1,2):
        j=j+h*(b[i]+4*b[i+1]+b[i+2])
    return(j)

def empezar(fun, a, b, c):
    d=(b-a)/c
    xn=[]
    while(c+1!=0):
        xn.append(a)
        a=a+d
        c-=1

    print("FUNCION: ", fun)
    esto = lit(xn, fun)
    resultado = intg(xn, esto)

    return resultado