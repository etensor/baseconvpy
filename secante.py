import sympy as sp
##Calculadora de secante
x, y = sp.symbols('x y')
str_ecuacion = input("Ingrese la funcion:\n")
funcion = sp.sympify(str_ecuacion)
sp.plot(funcion, (x, -10, 10), title='mira las raices', aspect_ratio='auto')
a = float(input('Digite el extremo inferior del intervalo: '))
b = float(input('Digite el extremo superior del intervalo: '))
tolerancia = float(input('Digite el error de tolerancia'))


def fnc(x):
    b = funcion.free_symbols
    var = b.pop
    valor = funcion.evalf(subs={var: x})
    return valor


fa = fnc(a)
fb = fnc(b)
c = ((a * fb) - (b * fa)) / (fb - fa)
iteraciones = 0
print('')
print('{0}\t{1}\t{2}\t{3}\t{4}'.format(
    '#', 'raíz', 'error', 'valorInf', 'valorSup'))
while(abs(fnc(c)) > tolerancia and iteraciones <= 50):
    fa = fnc(a)
    fb = fnc(b)
    c = ((a * fb) - (b * fa)) / (fb - fa)
    a = b
    b = c
    error = abs(fnc(c))
    print(iteraciones, "\t{:.6f}\t{:.6f}\t{:.6f}\t{:.6f}".format(
        c, error, a, b))
    iteraciones = iteraciones + 1
if(iteraciones == 50):
    print("\nSe ha alcanzado el numero máximo de iteraciones")
    print("Es posible que no hayan raices en el intervalo")
    print("\nLa raíz es: ", c)
    print("El error relativo es: ", error)
else:
    print("\nLa raíz es: ", c)
    print("El error relativo es: ", error)
