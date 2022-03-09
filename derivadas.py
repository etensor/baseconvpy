import sympy as sp
from sympy.parsing.sympy_parser import parse_expr,standard_transformations, implicit_multiplication_application

x, y, z = sp.symbols('x y z')
transformations = (standard_transformations + (implicit_multiplication_application,))

def derivarFuncion(f, *args):
    f = str(parse_expr(f,transformations= transformations))
    dfdxn = sp.Derivative(f, *args)
    return sp.latex(dfdxn), sp.latex(dfdxn.doit())


def derivadasFuncion(f,*args):
    return [derivarFuncion(f, f'{args[0]},{i}') for i in range(1, 4)] \
        if len(args) == 1 else \
        [derivarFuncion(f, *args[0:i+1]) for i in range(len(args))]

def integrarFuncion(f, *args):
    F = sp.Integral(f, *args)
    return sp.latex(F), sp.latex(F.doit())


def integrarFDef(f, lims: tuple):   # *lims -> (x,x0,xf) <- inf === oo
    res = sp.integrate(f, lims)
    return res


def limF(f, xo, dir='+'):             # predet: lim x->xo+
    return sp.limit(f, xo, dir) if f.subs(x, xo) == sp.nan else f.subs(x, xo)


### sympy --> numpy:
#sp.lambdify(x ( sp.sym ), f(x) , 'numpy')


#print(integrarFuncion(sp.sin(x)*sp.exp(2*x),x))
#print(derivarFuncion(sp.exp(x)*5*y**2*x**3*z,x,y,z))
#print(derivarFuncion('cos(ty)t**2','t')) # parser OK
#args = [x,x,(z,2)]
#print(derivadasFuncion('x**5yz**2+2x**5y*z**2',*args))
#print(derivadasFuncion(sp.exp(x)*5*x**3,x))
#print(derivarFuncion(parse_expr('2*sin(x) + 2',evaluate=False),x))