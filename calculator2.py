"""
A Textual app to create a fully working calculator, modelled after MacOS Calculator.
**modificado desde el original examples/calculator.py @Textualize/textual
La documentación de la libreria es muy escasa y sus alcances se ocultan
entre los ejemplos del autor 

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
from textual.widgets import Button, ButtonPressed, Footer, Placeholder


try:
    from pyfiglet import Figlet
except ImportError:
    print(" Error: -> pip install pyfiglet")
    raise




class FigletText:
    """auto fit figlet texto  """

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
            yield Text(self.text, style="bold")
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

    texto = style = ""

    def __init__(self, texto, style="yellow on rgb(20,40,20)"):
        super().__init__()
        self.texto = texto
        self.style = style

    def render(self) -> RenderableType:
        return Padding(
            Align.center(FigletText(self.texto), vertical="middle"),
            (0, 0),
            style=self.style,
        )


class Numbers(Widget):
    """The digital display of the calculator.
    
        Aqui tomamos 4 para las bases 2,8,10,16
    
    """

    value = Reactive("0.0")
    base = "" #

    def render(self) -> RenderableType:
        """Build a Rich renderable to render the calculator display.
        
            este metodo retorna un renderizable compatible con textual
        
        """ # Padding <- [Renderizable]
        return Padding(
            Align.center(FigletText(self.value), vertical="middle"),
            (0, 1),
            style="green on rgb(36,35,35)",
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

    display = Reactive("0.0")
    show_ac = Reactive(True)

    def watch_display(self, value: str) -> None:
        """Called when self.display is modified."""
        # self.numbers is a widget that displays the calculator result
        # Setting the attribute value changes the display
        # This allows us to write self.display = "100" to update the display   
        ####  =>> watch: update valor del display [   0.0   ]
        self.numbers[0].value = value
        self.numbers[1].value = value
        self.numbers[2].value = value
        self.numbers[3].value = value

    def compute_show_ac(self) -> bool:
        """Compute show_ac reactive value."""
        # Condition to show AC button over C | util para borrar y resetear los valores.
        return self.value in ("", "0","0.0") and self.display == "0.0"

    def watch_show_ac(self, show_ac: bool) -> None:
        """When the show_ac attribute change we need to update the buttons."""
        # Show AC and hide C or vice versa

        ### este metodo sirve de esquema para modificar [[X_B2],...,[X_B16]]
        self.c.visible = not show_ac
        self.ac.visible = show_ac


    def on_mount(self) -> None:
            # solo al comienzo
        #self.left = Decimal("0.0")
        #self.right = Decimal("0.0")
        self.value = ""
        #self.operator = "+"

        # The calculator display
        self.textos = [EleganTexto(st) for st in ["BIN","OCT","DEC","HEX"]]  # button : BIN -> B_2 , ...
        self.numbers = [Numbers() for i in range(4)]

        self.emptyspc = EleganTexto("")

        self.titulo = EleganTexto(
            "Conversor de Bases", "green on rgb(20,20,20)")

        for i in range(len(self.numbers)):
            self.numbers[i].style_border = "bold"

        def make_button(text: str, style: str) -> Button:
            """Create a button with the given Figlet label."""
            return Button(FigletText(text), style=style, name=text)

        # Make all the buttons
                # Elegante compresion para formar botones 
        self.buttons = {
            name: make_button(name, self.BUTTON_STYLES.get(name, self.DARK))
            for name in "+/-,=,D,E,F,A,B,C,7,8,9,4,5,6,1,2,3,.".split(",")
        }

        # Buttons that have to be treated specially
        self.zero = make_button("0", self.DARK)
        self.ac = make_button("AC", self.LIGHT)
        self.c = make_button("EC", self.YELLOW)
        self.c.visible = False

        # Set basic grid settings
        self.grid.set_gap(1, 1)
        self.grid.set_gutter(1)
        self.grid.set_align("center", "center") # <- ? 

        # Create rows / columns / areas
        self.grid.add_column("col", max_size=30, repeat=7) #5
        self.grid.add_row("row", max_size=12, repeat=7)
        self.grid.add_areas(                     # <== if defined -> grid.place<->vincular
            clear="col1,row1",
            texto10="col4,row2",
            texto2="col4,row3",
            texto8="col4,row4",
            texto16="col4,row5",
            titulo="col4-start|col7-end,row1",
            numbers10="col5-start|col7-end,row2",
            numbers2="col5-start|col7-end,row3",
            numbers8="col5-start|col7-end,row4",
            numbers16="col5-start|col7-end,row5",
            emptyspc="col4-start|col7-end,row6-start|row7-end",
            zero="col1-start|col2-end,row7",
        )                                          ### Posicionamiento botones en la grid
        # Place out widgets in to the layout
        self.grid.place(clear=self.c)        ## <- los agrega a la grid una vez definidos
        self.grid.place(
            numbers2=self.numbers[0],
            numbers8=self.numbers[1],
            numbers10=self.numbers[2],
            numbers16=self.numbers[3],
            texto2=self.textos[0],
            texto8=self.textos[1],
            texto10=self.textos[2],
            texto16=self.textos[3],  
            emptyspc=self.emptyspc,     # cambiar este
            titulo=self.titulo,
            *self.buttons.values(),
            clear=self.ac,                   # pos <- on_mount diff update
            zero=self.zero
        )

    def handle_button_pressed(self, message: ButtonPressed) -> None:
        """A message sent by the button widget
        Para darle funcionalidad a cada boton
        """

        assert isinstance(message.sender, Button)
        button_name = message.sender.name

#        def do_math() -> None:
#            """Does the math: LEFT OPERATOR RIGHT"""
#            self.log(self.left, self.operator, self.right)
#            try:
#                if self.operator == "+":
#                    self.left += self.right
#                elif self.operator == "-":
#                    self.left -= self.right
#                elif self.operator == "/":
#                    self.left /= self.right
#                elif self.operator == "X":
#                    self.left *= self.right
#                self.display = str(self.left)
#                self.value = ""
#                self.log("=", self.left)
#            except Exception:
#                self.display = "Error"

        if button_name.isdigit():
            self.display = self.value = self.value.lstrip("0") + button_name        # falta A -> E if B==16     # aqui es para update 
            #self.buttons[button_name].style = self.YELLOW
    
        elif button_name == "+/-":
            self.display = self.value = str(Decimal(self.value or "0") * -1)
        elif button_name == ".":        ## importante para solo agregar un .
            if "." not in self.value:
                self.display = self.value = (self.value or "0") + "."
        elif button_name == "AC":       # reset 
            self.value = ""
            self.display = "0.0"
        elif button_name == "EC":
            self.value = ""
            self.display = "0.0"
        
        elif button_name == "=":
            pass
            #do_math()

        ''' 
        elif button_name in ("+", "-", "/", "X"):
            self.right = Decimal(self.value or "0")
            do_math()
            self.operator = button_name
        '''




class CalculatorApp(App):
    """The Calculator Pro V2.0 Application"""

    doc_size = 50
    show_docs = Reactive(False)
    calc = Calculator()

    async def on_load(self) -> None:
        await self.bind("g", "toBin"," BINARIO ")
        await self.bind("h", "toBin"," OCTAL ")
        await self.bind("j", "quit"," DECIMAL ")
        await self.bind("k", "quit", " HEXADECIMAL ")
        await self.bind("l", "act_docs", "Documentacion")
        await self.bind("q", "quit", " Salir ")

    def watch_show_docs(self, show_docs: bool) -> None:
        self.bar.animate("layout_offset_x", 0 if show_docs else -self.doc_size)

    def action_act_docs(self) -> None:
        self.show_docs = not self.show_docs


    def on_key(self, event):
        if event.key.isdigit():
            #self.display = self.value = self.value.lstrip("0") + event.key.upper()
            #self.calc.display = self.calc.value = self.calc.value.lstrip("0") + event.key
            self.calc.numbers[0].value = self.calc.numbers[0].value.lstrip("0") + event.key
        
        if event.key in ('a','b','c','d','e','f'):
            pass
        

    async def on_mount(self) -> None:
        """Mount the calculator widget."""
        footer = Footer()
        self.bar = Placeholder(name="left")
        self.show_docs = False

        await self.view.dock(self.calc,edge='top')
        await self.view.dock(self.bar,edge='left',size=self.doc_size,z = 1)
        await self.view.dock(footer,edge='bottom',size=1, z = 2)
        ###

CalculatorApp.run(title="Calculator Test", log="textual.log")
