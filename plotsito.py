from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd


app = Dash(__name__)

df = pd.DataFrame({
    "Frutilla": ["Fresilla", "Uvilla","Morilla","Tomatillo"],
    "Cantidad": [6,1,2,3],
    "Ciudad" : ["Cali", "Jamundi","Palmira","Buga"]
})


fig = px.bar(df,x="Frutilla",y = "Cantidad", color="Ciudad", barmode="group")


app.layout = html.Div(children=[
    html.H1(children='Sisas dash'),

    html.Div(children='''
        Dash: La propia pa las graficas chimba.
        '''),

    #doc.Graph(
    #   id='exampl'
    #)
])