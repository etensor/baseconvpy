import streamlit as st
import numpy as np
from convb import convert_decbase
from derivadas import *

st.set_page_config(
    layout="wide",
    page_icon='🛠',
    initial_sidebar_state='expanded',
    menu_items={'About': "### Github:\n www.github.com/etensor/baseconvpy"}
    )


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
    ("Presentacion","Convertidor de Bases","Derivadas")
)
if opt_menu == "Presentacion":
    st.title('Métodos Númericos')
    st.subheader('Calculadoras')
    st.markdown(r'''
    ---
    ### Equipo: 
    ##### Jean Pierre Vargas
    ##### David Penilla Cardona
    ##### Juan Camilo Bolaños
    ##### Sergio Andres Angel
    ##### Santiago Abadia
    ''')

if opt_menu == "Convertidor de Bases":
    st.title('Ingrese un numero en cualquier casilla')
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
    st.title('Calculadora de Derivadas')
    calc_derivadas = st.container()
    

    with calc_derivadas:
        col_eq,col_diff = st.columns([4,1])

        with col_eq:
            st.write('\n')
            st.write('\n')
            eq_funcion = st.text_input(
                'Ingrese función: ', value='cos(xy) + 3x**3 y**-3 z**2 - sin(xz)')
            diff_var = ''

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

        with st.expander(' Derivadas ',True):
            
            derivadas = derivadasFuncion(eq_funcion, *diff_var)
            col_expr,col_spc,col_plots = st.columns(3)


            for dfdx in derivadas:
                col_expr.latex(f"{dfdx[0]} \quad = \; {dfdx[1]}")
                #col_deriv.latex(f"{dfdx[1]}")
            #    st.latex(f"{dfdx[0]} \quad = \quad {dfdx[1]}")
        





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

            
