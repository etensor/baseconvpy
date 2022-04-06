import numpy as np
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.axes3d as axes3d
from sympy import integrate, Symbol
from sympy.plotting import plot
import math
import sympy as sp

def comenzarX(fun, desde, hasta):
    sp.init_printing(use_unicode=False, wrap_line=False, no_global=True)
    x = Symbol('x')
    fun = eval(fun)
    sol=integrate((fun)**2, (x,desde,hasta))
    sol*=math.pi

    return sol