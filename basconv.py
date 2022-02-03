import streamlit as st
import numpy as np

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
    ("Presentacion","Convertidor de Bases")
)
if opt_menu == "Presentacion":
    st.title('Codigo Fuente del Proyecto')

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
                campo_numeros([1,2,3,4])
