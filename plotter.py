import plotly.graph_objects as go
import numpy as np
import sympy as sp
import pandas as pd
import plotly.express as px

x,y,z,t,w,r = sp.symbols('x y z t w r')

def plot_funcion(f,diff_var=['x'],xa : int =-10,xb: int =10):
    fig = go.Figure()

    f = sp.lambdify(sp.symbols(*diff_var), f, 'numpy')

    xs = np.linspace(xa,xb,400)
    df = pd.DataFrame(
        dict(
            x=xs,
            y=f(xs)
        )
    )

    fig = px.line(
        df,
        x=df.loc[:, 'x'],
        y=df.loc[:, 'y'],
    )

    return fig

    #return fig


'''
    xs = np.arange(-1,3,0.01)
    # Add traces, one for each slider step
    for step in np.arange(-2, 2, 0.1):
        fig.add_trace(
            go.Scatter(
                visible=False,
                line=dict(color="#0dc40c", width=3),
                name="𝜈 = " + str(step),
                x=np.arange(-10, 10, 0.01),
                y=f(step * xs)))

    # Make 10th trace visible
    fig.data[10].visible = True

    # Create and add slider
    steps = []
    for i in range(len(fig.data)):
        step = dict(
            method="update",
            args=[{"visible": [False] * len(fig.data)}]#,
                #{"title": "Slider switched to step: " + str(i)}],  # layout attribute
        )
        step["args"][0]["visible"][i] = True  # Toggle i'th trace to "visible"
        steps.append(step)

    sliders = [dict(
        active=10,
        currentvalue={"prefix": "Rango: "},
        pad={"t": 50},
        steps=steps
    )]

    fig.update_layout(
        sliders=sliders
    )

'''
