import numpy as np
import sympy as sp

x = sp.Symbol('x')

def biseccion(f, a, b, N):

    if f(a)*f(b) >= 0:
        return None
    a_n = a
    b_n = b
    for n in range(1, N+1):
        m_n = (a_n + b_n)/2
        f_m_n = f(m_n)
        if f(a_n)*f_m_n < 0:
            a_n = a_n
            b_n = m_n
        elif f(b_n)*f_m_n < 0:
            a_n = m_n
            b_n = b_n
        elif f_m_n == 0:
            print("Hallada solución exacta.")
            return m_n
        else:
            return None
    return (a_n + b_n)/2

print(biseccion(lambda x: np.cos(x) - np.exp(-x**2)+ 0.5,7,10,20))
