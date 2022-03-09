from tkinter import Y
from dash import Dash,html,dcc
from matplotlib.pyplot import plot
import plotly.express as px
import pandas as pd
import numpy as np
import sympy as sp

x = sp.Symbol('x')

colors = {
    'background': '#000000',
    'text': '#917010'
}

app = Dash(__name__)
## Data : missing -> from function gen point lists

'''
xs = np.linspace(-4,4,200)
ys = np.sin(xs)*np.cos(xs)


df = pd.DataFrame(
    dict(
        x = xs,
        y = ys
    )
)

fig = px.line(
    df,
    x= df.loc[:,'x'],
    y= df.loc[:,'y'],
    title= 'plotsito'
)
'''


def plot_funcion(f , var = 'x', limxs : tuple = (0,10,100)):
    #f = sp.sympify(f,evaluate=False)
    #exec(f'{f}')

    #xi = sp.symbols(var)
    xs = np.linspace(*limxs)
    ys = sp.lambdify(x,f,'numpy')

    df = pd.DataFrame(
        dict(
            x = xs,
            y = ys(xs) #
        )
    )

    fig = px.line(
        df,
        x=df.loc[:, 'x'],
        y=df.loc[:, 'y'],
        title='plotsito'
    )

    return fig


fig = plot_funcion(sp.cos(5*x)*sp.exp(x/5),'x',(-10,5,500))


app.layout = html.Div(style={'backgroundColor': colors['background']},
    children = [
        html.H1(
            children='Dash plotsito',
            style={
                'textAlign': 'center',
                'color': colors['text']
            }
        ),

        html.Div(children='Dash: web app pa los datos.',
            style={
                'textAlign': 'center',
                'color': colors['text']
            }
        ),

        # markdown
        html.Div(
            dcc.Markdown(children=r'''
            #### Dash pa los plots
            ---
            $\oint \frac{1}{z}dz \;=\; ?$

            Epa
            ''')
        ),

        dcc.Graph(
            id='plot1e',
            figure=fig
        ),
        #dcc.     
    ]
)

#var = sp.Symbol('x')
#plot_funcion(sp.cos,'x',(-1,1,10))



if __name__ == '__main__':
    app.run_server(debug=True)


