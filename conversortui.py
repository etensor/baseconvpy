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
numx = console.input("Digite un [i]número[/i] [bold red]no entero positivo [/]? :smiley: ")

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
    baseT : int
    
    def __init__(self,bT=16):
        self.baseT = bT

    def __rich__(self) -> Text:
        global numx
        return Text(convert_to_dec(numx,16),
            style = "bold green", justify="center"
        )


class Rconvertidor(Widget):

    baseT : int  = 16

    ''' 
    def __init__(self,bT):
        super().__init__()
        self.baseT = bT
    ''' 
    def on_mount(self):
        pass
    def render(self) -> Text:
        return Convertidor(self.baseT)


class ConvertidorApp(App):

    doc_size = 45

    async def on_load(self) -> None:
        await self.bind("d", "act_docs", "Ver Documentación")
        await self.bind("q", "quit", "salir : (q) ")
    
    show_docs = Reactive(False)


    def watch_show_docs(self, show_docs: bool) -> None:
        self.bar.animate("layout_offset_x", 0 if show_docs else -self.doc_size)
    
    def action_act_docs(self) -> None:
        self.show_docs = not self.show_docs
    

    async def on_mount(self) -> None:
        footer = Footer()
        self.bar = Placeholder(name="left")

        #await self.view.dock(Convertidor(), edge="top")
        await self.view.dock(footer,edge="bottom")
        await self.view.dock(self.bar, edge = "left", size=self.doc_size,z = -3)

    

ConvertidorApp.run(title="epaa")

