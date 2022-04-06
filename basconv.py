from unicodedata import decimal
from itsdangerous import base64_decode
import streamlit as st
from derivadas import *
from plotter import plot_funcion
from falsaposicion import falsa_pos
import numpy as np
import sympy as sp
from matplotlib import pyplot as plt
from met_biseccion import biseccion
from conversor import analizar
from conversor import floatingPoint
from simpson1by3 import empezar
import numpy as np
from derivadas import transformations


st.set_page_config(
    layout="wide",
    page_icon='🛠',
    initial_sidebar_state='expanded',
    menu_items={'About': "### Github:\n www.github.com/etensor/baseconvpy"}
    )
st.title('Métodos Númericos')

def texbox(text):
    texbx = st.container()
    with texbx:
        st.write('\n')
        st.latex(text)
        st.write('\n')
        st.write('\n')
              
    return texbx

def campo_numeros(numeros):
    titulos = ["Decimal", "Binaria", "Octal", "Hexadecimal"]
    return [st.text_input(titulos[i],numeros[i]) for i in range(len(titulos))]


opt_menu = st.sidebar.selectbox(
    "Navegador del proyecto",
    ("Presentacion","Convertidor de Bases","Derivadas","Métodos","Simpson")
)
st.sidebar.caption('Bienvenido.')

if opt_menu == "Presentacion":
    st.subheader('Calculadoras')
    st.markdown(r'''
    ---
    ##### Equipo: ''')
    st.write('''
     Jean Pierre Vargas\n
     David Penilla\n
     Juan Camilo Bolaños\n
     Sergio Andres Angel\n
     Santiago Abadia
    ''')


if opt_menu == "Convertidor de Bases":
    #st.warning('ADVERTENCIA: Funcionalidad impletada otra interfaz!')
    st.write('Conversor de bases')
    #convertidor_bases = st.container()

    menu_met = st.radio('Base :',('Decimal','Binaria','Octal', 'Hexadecimal'))
    #Bases
    if menu_met == 'Decimal':
        base = 10
    
    if menu_met == 'Binaria':
        base = 2
    
    if menu_met == 'Octal':
        base = 8

    if menu_met == 'Hexadecimal':
        base = 16
        

    #Entrada del numero
    numero = st.text_input("Escribe el numero en la base que seleccionaste", key=int)
    denegado = False

    if numero != '':
        if base == 2:
            for x in numero:
                if x == '0' or x == '1' or x == '-' or x == '.':
                    pass
                else:
                    denegado = True
                    break
        
        if base == 8:
            for x in numero:
                if x == '0' or x == '1' or x == '2' or x == '3' or x == '4' or x == '5' or x == '6' or x == '7' or x == '-' or x == '.':
                    pass
                else:
                    denegado = True
                    break

        if base == 10:
            for x in numero:
                if x == '0' or x == '1' or x == '2' or x == '3' or x == '4' or x == '5' or x == '6' or x == '7' or x == '8' or x == '9' or x == '-' or x == '.':
                    pass
                else:
                    denegado = True
                    break

        if base == 16:
            for x in numero:
                if x == '0' or x == '1' or x == '2' or x == '3' or x == '4' or x == '5' or x == '6' or x == '7' or x == '8' or x == '9' or x == 'A' or x == 'B' or x == 'C' or x == 'D' or x == 'E' or x == 'F' or x == 'a' or x == 'b' or x == 'c' or x == 'd' or x == 'e' or x == 'f' or x == '-' or x == '.':
                    pass
                else:
                    denegado = True
                    break

        if denegado == False:
            negativo = False
            if numero[0] == '-':
                negativo = True
                if numero.find('.') == -1:
                    numero = str(int(numero) * -1)
                else:
                    numero = str(float(numero) * -1.0)

            binario, octal, decimal, hexadecimal = analizar(numero, base)

            if negativo == True:
                ptoflotante, expontente, mantisa = floatingPoint(float(decimal)*-1)
                st.success(f'Binario: -{binario}')
                st.success(f'Octal: -{octal}')
                st.success(f'Decimal: -{decimal}')
                st.success(f'Hexadecimal: -{hexadecimal}')
            else:
                ptoflotante, expontente, mantisa = floatingPoint(float(decimal))
                st.success(f'Binario: {binario}')
                st.success(f'Octal: {octal}')
                st.success(f'Decimal: {decimal}')
                st.success(f'Hexadecimal: {hexadecimal}')

            st.success(f'Punto flotante: {ptoflotante}')
            st.success(f'Exponente: {expontente}')
            st.success(f'Mantisa:  {mantisa}')

        else:
            st.write('Por favor ingresa numeros validos.')
            st.write('Numeros validos:')
            st.write('Binario: 0, 1')
            st.write('Octal: 0, 1, 2, 3, 4, 5, 6, 7')
            st.write('Decimal: 0, 1, 2, 3, 4, 5, 6, 7, 8, 9')
            st.write('Hexadecimal: 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, a, b, c, d, e, f, A, B, C, D, E, F')

if opt_menu == 'Derivadas':
    st.subheader('Calculadora de Derivadas')
    calc_derivadas = st.container()
    

    with calc_derivadas:
        col_eq,col_diff = st.columns([4,1])
        diff_var = ''

        with col_eq:
            st.write('\n')
            st.write('\n')
            eq_funcion = st.text_input(
                'Ingrese función: ', value='cos(xy) + 3x**3*y**-3 z**2 - sin(xz)')
            

        with col_diff:
            tipo_diff = st.radio(
                '',
                ('simple','libre'))
            
            if tipo_diff == 'simple':
                diff_var = st.selectbox(
                    'Diferenciar sobre:',
                    ('x','y','z','t','r','v','w'),
                )
            else:
                diff_var = st.text_input('Respecto a qué variable derivar, y cuantas veces:',
                    value='x,2 ; y ; z ; z',
                    help='Utilice ; para separar argumentos, \n puede diferenciar n veces x y luego z asi: x,n;z')
                diff_var = diff_var.split(';')

        with st.expander(' ',True):
            st.subheader('Derivadas ')
            derivadas = derivadasFuncion(eq_funcion, *diff_var)
            col_spc,col_expr,col_spc2 = st.columns(3)
            
            
            for dfdx in derivadas:
                col_expr.latex(f"{dfdx[0]} \quad = \quad {dfdx[1]}")

            st.subheader('Gráficas')
            lim_inf = int(st.slider('x min:',min_value=-100,max_value=100,value=-8))
            lim_sup = int(st.slider('y max:', min_value=-100,max_value=100, value=8))
            plots = [plot_funcion(derivadas[i][2],diff_var,lim_inf,lim_sup) for i in range(len(derivadas))]
            idx = 0
            for plot in plots:
                st.latex(f'f({diff_var})\;=\;'+derivadas[idx][1])
                st.plotly_chart(plot, use_container_width=True)
                idx+=1
        
        #plot = plot_funcion('exp(x/3)*sin(x)')
        #st.plotly_chart(plot,use_container_width=True)
        
if opt_menu == 'Métodos':

    menu_met = st.radio('Qué método usar? :',('Falsa Posición','Bisección','Derivada de un polinomio','Trapecios','Rectangulo'))
    
    if menu_met == 'Falsa Posición':
        st.subheader('Falsa Posición')
        funcion = st.text_input('Ingrese la función',
                                value='exp(x-2)-log(x) -2.5')
        a = int(st.text_input('Ingrese rango inferior: ',value='3'))
        b = int(st.text_input('Ingrese rango superior: ',value='4'))
        tol = float(st.text_input('Ingrese tolerancia:', value='0.0005'))

        tabla,raices = falsa_pos(funcion,a,b,tol)
        st.write('Acerca:')
        col_expr, col_vals = st.columns(2)
        
        col_expr.latex(r'x_{a}')
        col_vals.write('\n')
        col_vals.write(' limite inferior')
        col_expr.latex(r'x_{b}')
        col_vals.write('\n')
        col_vals.write(' limite superior')
        col_expr.latex(r'x_{r}')
        col_vals.write('\n')
        col_vals.write(' raiz encontrada')
        

        for i in range(0, len(tabla)):
            st.write('------------------------------------------------------')
            col_expr.write(f'Iteración #: {i+1} ')
            col_expr.latex(r'x_{a},x_{r},x_{b}')
            col_expr.write('\n')
            col_expr.write('\n')
            col_expr.write('\n')
            col_vals.write(tabla[i, 0:3])
            col_expr.write('\n')
            col_expr.latex(r'f(x_{a}),f(x_{c}), f(x_{b}): ')
            col_expr.write('\n')
            col_vals.write(tabla[i, 3:6])
            col_expr.write('\n')
            col_expr.write('\n')
            col_expr.markdown(
                "<h6 style='text-align: center; color: Green;'>Error</h6>", unsafe_allow_html=True)
            col_expr.markdown(
                "<h6 style='text-align: center; color: Green;'>Raiz</h6>", unsafe_allow_html=True)
            col_vals.write(raices[i])
            col_vals.write(tabla[i,6])

    if menu_met == 'Derivada de un polinomio':
        coefs = st.text_input('Ingrese los coeficientes de la función',
                                value='1.25,-7.4,-10.43,25.86,-3.15')

    
        coefs = coefs.split(',')
        coeficientes = [float(i) for i in coefs]

        fx = np.poly1d(np.array(coefs))
        xs = np.linspace(-10, 10, 200)

        raices = np.roots(coefs)
        idx = 0
        textos,vals = st.columns(2)
        for raiz in raices:
            textos.latex(f'x_{{{idx}}}')
            vals.write('\n')
            vals.write(raiz)
            idx+=1
        
        polinomio = np.poly1d(coeficientes)

        fig, ax = plt.subplots()
        ax.plot(xs, polinomio(xs))
        st.subheader('Gráfica')
        st.pyplot(fig)


    if menu_met == 'Bisección':
        funcion = st.text_input('Ingrese la función f(x) :', 
        value='np.cos(x)-np.exp(-x**2) + 0.5')
        
        lim_inf = int(st.slider('Rango inferior', min_value=-
                      50, max_value=50, value=-2))
        lim_sup = int(st.slider('Rango superior', min_value=-
                      50, max_value=50, value=3))
        iter_max = int(st.number_input('Cuantas iteraciones? : ',min_value=0,max_value=50))

        raiz_biseccion = biseccion(eval('lambda x: '+funcion),lim_inf,lim_sup,20)
        
        st.write(raiz_biseccion)
        st.subheader('Gráfica')
        plot = plot_funcion(eval('lambda x: '+funcion),
                            'x', lim_inf, lim_sup, modo=False)
        st.plotly_chart(plot)

    if menu_met == 'Trapecios':
        # Integración: Regla de los trapecios
        # Usando una función fx()
        
        # INGRESO
        fx = st.text_input('Ingrese la función',
                                value='x**2-2*x+3')
        #fx = lambda x: x**2-2*x+3

         
        # intervalo de integración
        a = int(st.text_input('Ingrese extremo izquierdo: ',value='-5'))
        #a = -5
        b = int(st.text_input('Ingrese extremo derecho: ',value='10'))
        #b = 10
        particiones = int(st.text_input('Ingrese numero de particiones:', value='15'))
        #tramos = 15
        fx = str(parse_expr(fx,transformations=transformations))
        funcion = sp.lambdify(x,fx,'numpy')

        #ya tengo la de rectangulo con grafica tambien
        #https://replit.com/join/qalniwjdxi-sergioangel
        #ahi esta
        #jaajaja
        # suave ya se puede ver hasta el mouse en replit xD
        # ya me pongo a meter esta mierda en streamlit 
        # poder pasarle datos a lo que seria una funcion
        # dinamica


        # PROCEDIMIENTO
        # Regla del Trapecio
        # Usando tramos equidistantes en intervalo
        h = (b-a)/particiones
        xi = a
        suma = funcion(xi)
        for i in range(0,particiones-1,1):
            xi = xi + h
            suma = suma + 2*funcion(xi)
        suma = suma + funcion(b)
        area = h*(suma/2)

        # SALIDA
        col_expr, col_vals = st.columns(2)
        col_vals.write(' Particion:')
        st.write(particiones)
        col_vals.write(' Integral:')
        st.write(area)
        #print('Integral: ', area)


        # GRAFICA
        # Puntos de muestra
        muestras = particiones + 1
        xi = np.linspace(a,b,muestras)
        fi = funcion(xi)
        # Linea suave
        muestraslinea = particiones*10 + 1
        xk = np.linspace(a,b,muestraslinea)
        fk = funcion(xk)

        # Graficando
        #plt.plot(xk,fk, label ='f(x)')
        #plt.plot(xi,fi, marker='o',
               # color='orange', label ='muestras')
        plt.plot(xk,fk, label ='f(x)')
        plt.plot(xi,fi, marker='o',
                color='orange', label ='muestras')
        plt.xlabel('x')
        plt.ylabel('f(x)')
        plt.title('Integral: Regla de Trapecios')
        plt.legend()

        # Trapecios
        plt.fill_between(xi,0,fi, color='g')
        for i in range(0,muestras,1):
            plt.axvline(xi[i], color='w')
        
        st.pyplot(plt,figsize=(2, 2))
    
    if menu_met == 'Rectangulo':
    
        def rectint(f,a,b,rectangles):
            cumulative_area=0

            a=float(a)
            b=float(b)
            rectangles=float(rectangles)

            i=(b-a)/rectangles

            trailing_x=a
            leading_x=a+i

            while (a<=leading_x<=b) or (a>=leading_x>=b):
                area=f((trailing_x+leading_x)/2)*i
                cumulative_area+=area

                leading_x+=i
                trailing_x+=i

            return cumulative_area
    
    funct = st.text_input('Ingrese la función',
                                value='x**2-2*x+3')
    a = int(st.text_input('Ingrese extremo izquierdo: ',value='-5'))
    #a = -5
    b = int(st.text_input('Ingrese extremo derecho: ',value='10'))
    #b = 10
    rectangles = int(st.text_input('Ingrese numero de particiones:', value='15'))
    #tramos = 15
    funct = str(parse_expr(funct,transformations=transformations))
    funcion = sp.lambdify(x,funct,'numpy')

    col_expr, col_vals = st.columns(2)
    col_vals.write(' Integral:')
    print("FUNCIONN ", funcion)
    st.write(rectint(funcion, a, b,rectangles))

    muestras = rectangles + 1
    xi = np.linspace(a,b,muestras)
    fi = funcion(xi)
    # Linea suave
    muestraslinea = rectangles*10 + 1
    xk = np.linspace(a,b,muestraslinea)
    fk = funcion(xk)

    # Graficando
    plt.plot(xk,fk, label ='f(x)')
    plt.plot(xi,fi, marker='o',
            color='orange', label ='muestras')

    plt.xlabel('x')
    plt.ylabel('f(x)')
    plt.title('Integral: Regla de Rectangulos')
    plt.legend()


    plt.fill_between(xi,0,fi, color='g')
    for i in range(0,muestras,1):
        plt.axvline(xi[i], color='w')

    #plt.show()
    st.pyplot(plt,figsize=(2, 2)) 

if opt_menu == 'Simpson':
    funcion = ''
    st.write('Metodo de simpson 1/3')
    #function = st.text_input("Ingresa la función")
    function = st.text_input('Ingrese la función',
                                value='')
    izq = int(st.slider('Limite izquierdo', min_value=0, max_value=25, value = 0))
    der = int(st.slider('Limite derecho', min_value=0, max_value=25, value = 0))
    intervalos = int(st.number_input('Numero de intervalos',min_value=2,max_value=30, value = 2))

    if function != "":
        function = str(parse_expr(function,transformations=transformations))
        funcion = sp.lambdify(x,function,'numpy')

    if intervalos % 2 != 0:
        st.write('El numero de intervalos no debe ser impar')
        confirmar = False
    else:
        confirmar = True

    if izq >= der:
        st.write('El limite izquierdo no puede ser mayor al derecho')
        pasar = False
    else:
        pasar = True
    
    if confirmar and pasar and function != '':
        resultado = empezar(function, izq, der, intervalos)

        st.success(f'Valor integral definido: {resultado}')

        muestras = intervalos + 1
        xi = np.linspace(izq,der,muestras)
        fi = funcion(xi)
        # Linea suave
        muestraslinea = intervalos*10 + 1
        xk = np.linspace(izq,der,muestraslinea)
        fk = funcion(xk)
        # Graficando
        plt.plot(xk,fk, label ='f(x)')
        plt.plot(xi,fi, marker='o',
                color='orange', label ='muestras')

        plt.xlabel('x')
        plt.ylabel('f(x)')
        plt.title('Integral: Regla de Simpson')
        plt.legend()


        plt.fill_between(xi,0,fi, color='g')
        for i in range(0,muestras,1):
            plt.axvline(xi[i], color='w')

        #plt.show()
        st.pyplot(plt, figsize=(2, 2)) 
               
#''' 
#st.latex(r'\frac{df}{dx} \;=\; f\,\'(x) \;=\quad')
#for i in range(2,4):
#    indx = '\''*i
#    st.latex(
#        f"\\frac{{{{d}}^{i}f }} {{{{dx}}^{i}}} \;=\; f\,{indx}(x) \;=\quad")
#'''
#
#
#''' documentacion++
#with st.echo():
#    st.write('epa')
#'''

            
