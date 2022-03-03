import streamlit as st
import numpy as np
from convb import convert_decbase
from derivadas import *

st.set_page_config(layout="wide")


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
    "Navegador",
    ("Presentacion","Convertidor de Bases","Derivadas")
)
if opt_menu == "Presentacion":
    st.title('Codigo Fuente del Proyecto')
    st.markdown(r'''
    ---
    # Equipo: 
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
        eq_funcion = st.text_input('Ingrese función: ')
        with st.expander(' Derivadas ',True):
            
            derivadas = derivadasFuncion(eq_funcion, x)
            for dfdx in derivadas:
                st.latex(f"{dfdx[0]} \;=\; {dfdx[1]}")
        
            





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

            
