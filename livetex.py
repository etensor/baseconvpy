from rich.console import Console
from rich.layout import Layout
from rich.live import Live
from rich.text import Text
from rich.align import Align
from time import sleep
from textual.app import App
from textual.reactive import Reactive
from textual.widgets import Footer, Placeholder
from textual.widget import Widget
from convb import convert_to_dec

console = Console()
#tui = Layout()

''' 👺 '''
numx = console.input(
    "Digite un [i]número[/i] [bold red]no entero positivo [/]? :smiley: ")

'''
tui = Layout()
    
    tui.split(Layout(name="main"), Layout(name="header", size=1))

    tui["main"].update(
        Convertidor()
    )ls

    with Live(tui, screen=True, redirect_stderr=False) as live:
        try:
            while True:
                sleep(5)
        except KeyboardInterrupt:
            pass

'''

# layout["upper"].visible = True


class Convertidor:
    baseT: int

    def __init__(self, bT):
        self.baseT = bT

    def __rich__(self) -> Text:
        return Text(convert_to_dec(numx, 16),
                    style="bold green", justify="center"
                    )


tui = Layout()

tui.split(Layout(name="main"), Layout(name="header", size=1))

tui["main"].update(
    Convertidor(8)
)

with Live(tui, screen=True, redirect_stderr=False) as live:
    try:
        while True:
            sleep(1)
    except KeyboardInterrupt:
        pass
