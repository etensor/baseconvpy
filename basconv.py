import streamlit as st
from derivadas import *
from plotter import plot_funcion
from falsaposicion import falsa_pos
import numpy as np
import sympy as sp
from matplotlib import pyplot as plt
from met_biseccion import biseccion


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
    ("Presentacion","Convertidor de Bases","Derivadas","Métodos")
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
    st.warning('ADVERTENCIA: Funcionalidad impletada otra interfaz!')
    st.write('Ingrese un numero en cualquier casilla')
    convertidor_bases = st.container()

    with convertidor_bases:
        with st.expander(' Convertidor de Bases ',True):
            col_text, col_nums = st.columns(2)

            with col_text:
                texbox(r'''B_{10} \; : ''')
                texbox(r'''B_{2} \; : ''')
                texbox(r'''B_{8} \; : ''')
                texbox(r'''B_{16} \; : ''')

            
            with col_nums:
                campo_numeros([0,0,0,0])



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

    menu_met = st.radio('Qué método usar? :',('Falsa Posición','Bisección','Raices de un polinomio'))
    
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
            col_expr.write(f'Iteración #{i+1}: ')
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

    if menu_met == 'Raices de un polinomio':
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

            
