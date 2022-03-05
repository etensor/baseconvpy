"""
**modificado desde el original : -> examples/calculator.py
https://github.com/Textualize/textual

La documentación de la libreria es muy escasa y sus alcances se ocultan
entre los ejemplos del autor.

        Conversor de Bases
       --------------------

"""
from typing import List
from decimal import Decimal
from time import sleep

from rich.align import Align
from rich.console import Console, ConsoleOptions, RenderResult, RenderableType
from rich.padding import Padding
from rich.text import Text

from textual.app import App
from textual.reactive import Reactive
from textual.views import GridView
from textual.widget import Widget
from textual.widgets import Button, ButtonPressed, Footer, ScrollView

#from convb import convertirNM
from convb3 import Conversor
from docscalculadora import codigo_fuente


try:
    from pyfiglet import Figlet
except ImportError:
    print(" Error: -> pip install pyfiglet")
    raise


class FigletText:   # para autoescalar el texto

    def __init__(self, text: str) -> None:
        self.text = text

    def __rich_console__(
        self, console: Console, options: ConsoleOptions
    ) -> RenderResult:
        """Build a Rich renderable to render the Figlet text.

                Rich render==>figlet
        """
        size = min(options.max_width / 2, options.max_height)
        if size < 4:
            yield Text(self.text, style="light")
        else:
            if size < 7:
                font_name = "mini"
            elif size < 8:
                font_name = "small"
            elif size < 10:
                font_name = "standard"
            else:
                font_name = "big"
            font = Figlet(font=font_name, width=options.max_width)
            yield Text(font.renderText(self.text).rstrip("\n"), style="bold")


class EleganTexto(Widget):

    texto = ""
    style = Reactive("")

    def __init__(self, texto, style="yellow on rgb(20,40,20)"):
        super().__init__()
        self.texto = texto
        self.style = style


    def render(self) -> RenderableType:
        
        return Padding(
            Align.center(FigletText(self.texto), vertical="middle"),
            (0,2),
            style=self.style,
        )


class Numbers(Widget):
    """The digital display of the calculator.

        Aqui tomamos 4 para las bases 2,8,10,16

    """

    value = Reactive("0.0")
    base = ""
    
    def render(self) -> RenderableType:
        """Build a Rich renderable to render the calculator display.

            este metodo retorna un renderizable compatible con textual

        """  # Padding <- [Renderizable]
        return Padding(
            Align.center(FigletText(self.value), vertical="middle"),
            (0, 1),
            style="rgb(216,229,42) on rgb(0,0,0)",
        )


class Calculator(GridView):
    """A working calculator app.

        Modificada calculadora para el conversor de bases
        Métodos Númericos
        -----------------


    """

    DARK = "white on rgb(51,51,51)"
    LIGHT = "red on rgb(32,32,32)"
    YELLOW = "white on rgb(255,159,7)"

    BUTTON_STYLES = {
        "AC": YELLOW,
        "C": DARK,
        "+/-": LIGHT,
    }

    display = Reactive("0")
    show_ac = Reactive(True)


    conversor = Conversor()

    vect_bases = [10,2,8,16]

    def watch_display(self, value: str) -> None:
        """Called when self.display is modified."""
        # self.numbers is a widget that displays the calculator result
        # Setting the attribute value changes the display
        # This allows us to write self.display = "100" to update the display
        # =>> watch: update valor del display [   0.0   ]
        #self.numbers[0].value = convertirNM(self.value,self.baseT,2)
    
        idx = self.getbaseT_idx()
        self.display = self.numbers[idx].value = value
        for ix in range(len(self.numbers)):
            if ix != idx:
                self.numbers[ix].value = self.conversor.convertirNM(
                    self.value,
                    self.baseT,
                    self.vect_bases[ix]
                    )
        
        num_dec = self.conversor.convertirNM(self.display,self.baseT,10)
        if self.value not in ('', '0.0'):
            self.ieee32num.value,s32 = self.conversor.dec_ieee3264(num_dec,mod=32)
            self.ieee64num.value,s64 = self.conversor.dec_ieee3264(num_dec,mod=64)

            self.exp32n.value,self.mnt32dec.value = self.conversor.ieee3264_2n(str(self.ieee32num.value),s32)
            self.exp64n.value,self.mnt64dec.value = self.conversor.ieee3264_2n(str(self.ieee64num.value),s64)
        else:
            self.ieee32num.value  = '0.0'
            self.ieee64num.value = '0.0'
            self.mnt32dec.value = '0.0'
            self.mnt64dec.value = '0.0'


    def compute_show_ac(self) -> bool:
        """Compute show_ac reactive value."""
        # Condition to show AC button over C | util para borrar y resetear los valores.
        return self.value in ("", "0", "0.0") and self.display == "0.0"

    def watch_show_ac(self, show_ac: bool) -> None:
        """When the show_ac attribute change we need to update the buttons."""
        # Show AC and hide C or vice versa

        # este metodo sirve de esquema para modificar [[X_B2],...,[X_B16]]
        self.c.visible = not show_ac
        self.ac.visible = show_ac


    def on_mount(self) -> None:
        self.value = "0"

        # The calculator display
        # button : BIN -> B_2 , ...
        self.basedict = {10: 'DEC', 2: 'BIN', 8: 'OCT', 16: 'HEX'}
        self.textos = {base: EleganTexto(base)
                       for base in self.basedict.values()}
        self.numbers = [Numbers() for i in range(4)]
        self.bases = {10: True, 2: False, 8: False, 16: False}
        self.baseT = 2
        self.sel_base(10)

        self.ieee32num = Numbers()
        self.ieee64num = Numbers()
        self.exp32n = Numbers()
        self.exp64n = Numbers()
        self.mnt32dec = Numbers()
        self.mnt64dec = Numbers()
        
        self.modos = {
            '32': EleganTexto('32 bit',"yellow on black"),
            '64': EleganTexto('64 bit','yellow on black')
            }
        

        self.emptyspc = EleganTexto("","white on rgb(0,0,0)")

        self.titulo = EleganTexto(
            "Conversor de Bases: IEEE-754", "rgb(0,150,80) on rgb(20,20,20)")

        for i in range(len(self.numbers)):
            self.numbers[i].style_border = "bold"

        def make_button(text: str, style: str) -> Button:
            """Create a button with the given Figlet label."""
            return Button(FigletText(text), style=style, name=text)

        # Make all the buttons
            # Elegante compresion para formar botones
        self.buttons = {
            name: make_button(name, self.BUTTON_STYLES.get(name, self.DARK))
            for name in "+/-,D,E,F,A,B,C,7,8,9,4,5,6,1,2,3,.".split(",")
        }

        # Buttons that have to be treated specially
        self.zero = make_button("0", self.DARK)
        self.ac = make_button("AC", self.LIGHT)
        self.c = make_button("EC", self.YELLOW)
        self.elim  = make_button("DEL",self.LIGHT)
        self.c.visible = False

        # Set basic grid settingsq
        self.grid.set_gap(1, 1)
        self.grid.set_gutter(1)
        self.grid.set_align("center", "center")  # <- ?

        # Create rows / columns / areas
        self.grid.add_column("col", max_size=30, repeat=8) 
        self.grid.add_row("row", max_size=12, repeat=8)
        self.grid.add_areas(                     # <== if defined -> grid.place<->vincular
            clear="col1,row1",
            elim="col3,row1",
            texto10="col4,row2",
            texto2="col4,row3",
            texto8="col4,row4",
            texto16="col4,row5",
            titulo="col4-start|col8-end,row1",
            modo_32="col4,row6",
            modo_64="col4,row7",
            numbers10="col5-start|col8-end,row2",
            numbers2="col5-start|col8-end,row3",
            numbers8="col5-start|col8-end,row4",
            numbers16="col5-start|col8-end,row5",
            num_32='col5-start|col8-end,row6',
            num_64='col5-start|col8-end,row7',
            exp32t='col1,row8',
            exp64t='col4,row8',
            mnt32t='col2-start|col3-end,row8',
            mnt64t='col5-start|col8-end,row8',
            
            #emptyspc="col5-start|col8-end,row6-start|row7-end",

            zero="col1-start|col2-end,row7",
        )  # Posicionamiento de areas en la grid
        # Place out widgets in to the layout
        # <- agrega el contenido a las areas definidas
        self.grid.place(clear=self.c)
        self.grid.place(
            numbers10=self.numbers[0],
            numbers2=self.numbers[1],
            numbers8=self.numbers[2],
            numbers16=self.numbers[3],
            texto10=self.textos['DEC'],
            texto2=self.textos['BIN'],
            texto8=self.textos['OCT'],
            texto16=self.textos['HEX'],
            modo_32=self.modos['32'],
            modo_64=self.modos['64'],
            #emptyspc=self.emptyspc,     # cambiar este
            titulo=self.titulo,
            elim=self.elim,
            num_32=self.ieee32num,
            num_64=self.ieee64num,
            exp32t=self.exp32n,
            exp64t=self.exp64n,
            mnt32t=self.mnt32dec,
            mnt64t=self.mnt64dec,
            *self.buttons.values(),
            clear=self.ac,
            zero=self.zero
        )
    
        '''  Para seleccionar en que base ingresar el número '''

    
    def sel_base(self, b) -> None:

        if self.baseT == b:
            return None
        act_style = "black on rgb(210,210,210)"
        dact_style = "yellow on rgb(20,40,20)"

        self.bases[self.baseT] = False
        self.textos[self.basedict[self.baseT]].style = dact_style
        
        self.bases[b] = True
        self.textos[self.basedict[b]].style = act_style
        self.baseT = b

        idx = self.getbaseT_idx()
        if idx != b:
            self.value = self.numbers[idx].value

    def getbaseT_idx(self):
        idx : int
        for i, x in enumerate(self.bases.values()):
            if x:
                idx = i
                break
        return idx
       


    def handle_button_pressed(self, message: ButtonPressed) -> None:
        """A message sent by the button widget
        Para darle funcionalidad a cada boton
        """

        assert isinstance(message.sender, Button)
        button_name = message.sender.name


        if button_name.isdigit():
            i = int(button_name)
            if (self.baseT == 8 and i > 7) \
            or (self.baseT == 2 and i > 1):
                pass
            else:
                self.display = self.value = self.value + button_name
            #self.display = self.value = self.value.lstrip("0") + button_name
        
        elif button_name == "+/-":
            self.display = self.value = str(Decimal(self.value or '0') * -1)
        elif button_name == ".":  # importante para solo agregar un .
            if "." not in self.value:
                self.display = self.value = (self.value + '.' or "0.0")
        elif button_name == "AC":       # reset
            self.value = ""
            self.display = "0.0"

        elif button_name == "EC":
            self.value = ""
            self.display = "0.0"

        elif button_name in ('A','B','C','D','E','F'):
            if self.baseT > 10:
                self.display = self.value = self.value.lstrip("0") + button_name

        elif button_name == "DEL":
            if len(self.value) > 0:
                self.display = self.value = self.value[0:len(self.value)-1]
            



class CalculatorApp(App):
    """The Calculator Pro V2.0 Application"""

    doc_size = 65
    calc = Calculator()
    bar : RenderableType

    async def on_load(self) -> None:
        await self.bind("g", "selectbase(10)", " DEC ")
        await self.bind("h", "selectbase(2)", " BIN ")
        await self.bind("j", "selectbase(8)", " OCT ")
        await self.bind("k", "selectbase(16)", "HEX ")
        await self.bind("l", "act_docs", "Documentacion")
        await self.bind("q", "quit", " Salir ")

    def action_act_docs(self) -> None:
        self.bar.visible = not self.bar.visible
        self.calc.visible = not self.bar.visible

    def action_selectbase(self, b) -> None:
        self.calc.sel_base(b)
        
    def on_key(self, event):
        idx = self.calc.getbaseT_idx()

        if event.key.isdigit():
            i = int(event.key)
            if (self.calc.baseT == 8 and i > 7) \
                or (self.calc.baseT == 2 and i > 1):
                pass
            else:
                self.calc.display = self.calc.value = self.calc.value + event.key
                self.calc.numbers[idx].value = self.calc.display

        if event.key in ('a', 'b', 'c', 'd', 'e', 'f') or event.key in ('A','B','C','D','E','F'):
            if self.calc.baseT > 10:
                self.calc.display = self.calc.value = self.calc.value + event.key.upper()
                self.calc.numbers[idx].value = self.calc.display
        
        if event.key == '.':
            if "." not in self.calc.display or self.display == '':
                self.calc.display = self.calc.value = (self.calc.value + '.' or "0.0")
        
        if event.key == '-':
            self.calc.display = self.calc.value = str(Decimal(self.calc.value or '0') * -1)
        
        if event.key == "ctrl+h": # === borrar (backspace)
            if self.calc.value != '0.0':
                self.calc.display = self.calc.value = self.calc.value[0:len(self.calc.value)-1]


    async def on_mount(self) -> None:
        """Mount the calculator widget."""
        footer = Footer()
        self.bar = ScrollView(codigo_fuente,auto_width=True)
        self.bar.visible = False

        await self.view.dock(self.calc, edge='top')
        await self.view.dock(self.bar, edge='left', z=1)
        await self.view.dock(footer, edge='bottom', size=1, z=2)
        ###


CalculatorApp.run(title="Calculator Test", log="textual.log")
