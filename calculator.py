"""
A Textual app to create a fully working calculator, modelled after MacOS Calculator.
**modificado desde el original examples/calculator.py @Textualize/textual
La documentación de la libreria es muy escasa y sus alcances se ocultan
entre los ejemplos del autor 

"""
from typing import List
from decimal import Decimal

from rich.align import Align
from rich.console import Console, ConsoleOptions, RenderResult, RenderableType
from rich.padding import Padding
from rich.text import Text

from textual.app import App
from textual.reactive import Reactive
from textual.views import GridView
from textual.widget import Widget
from textual.widgets import Button, ButtonPressed

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
            style="green on rgb(38,38,38)",
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
        "AC": LIGHT,
        "C": LIGHT,
        "+/-": LIGHT,
        "%": LIGHT,
        "/": YELLOW,
        "X": YELLOW,
        "-": YELLOW,
        "+": YELLOW,
        "=": YELLOW,
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
        return self.value in ("", "0.0") and self.display == "0.0"

    def watch_show_ac(self, show_ac: bool) -> None:
        """When the show_ac attribute change we need to update the buttons."""
        # Show AC and hide C or vice versa

        ### este metodo sirve de esquema para modificar [[X_B2],...,[X_B16]]
        self.c.visible = not show_ac
        self.ac.visible = show_ac


    def on_mount(self) -> None:
        """Event when widget is first mounted (added to a parent view)."""

        # Attributes to store the current calculation
        self.left = Decimal("0.0")
        self.right = Decimal("0.0")
        self.value = ""
        self.operator = "+"

        # The calculator display
        self.numbers = [Numbers() for i in range(4)]
        for i in range(len(self.numbers)):
            self.numbers[i].style_border = "bold"

        def make_button(text: str, style: str) -> Button:
            """Create a button with the given Figlet label."""
            return Button(FigletText(text), style=style, name=text)

        # Make all the buttons
                # Elegante comprehension para formar botones 
        self.buttons = {
            name: make_button(name, self.BUTTON_STYLES.get(name, self.DARK))
            for name in "+/-,%,/,D,E,F,A,B,C,7,8,9,X,4,5,6,-,1,2,3,+,.,=".split(",")
        }

        # Buttons that have to be treated specially
        self.zero = make_button("0", self.DARK)
        self.ac = make_button("AC", self.LIGHT)
        self.c = make_button("C", self.LIGHT)
        self.c.visible = False

        # Set basic grid settings
        self.grid.set_gap(1, 1)
        self.grid.set_gutter(1)
        self.grid.set_align("center", "center") # <- ? 

        # Create rows / columns / areas
        self.grid.add_column("col", max_size=30, repeat=6) #5
        self.grid.add_row("row", max_size=15, repeat=6)
        self.grid.add_areas(                     # <== if defined -> grid.place<->vincular
            clear="col1,row1",
            numbers2="col4-start|col6-end,row1",
            numbers8="col4-start|col6-end,row2",
            numbers10="col4-start|col6-end,row3",
            numbers16="col4-start|col6-end,row4",
            zero="col1-start|col2-end,row5",
        )                                          ### Posicionamiento botones en la grid
        # Place out widgets in to the layout
        self.grid.place(clear=self.c)        ## <- los agrega a la grid una vez definidos
        self.grid.place(
            *self.buttons.values(), clear=self.ac, 
            numbers2=self.numbers[0],
            numbers8=self.numbers[1],
            numbers10=self.numbers[2],
            numbers16=self.numbers[3],
            zero=self.zero
        )

    def handle_button_pressed(self, message: ButtonPressed) -> None:
        """A message sent by the button widget
        Para darle funcionalidad a cada boton
        """

        assert isinstance(message.sender, Button)
        button_name = message.sender.name

        def do_math() -> None:
            """Does the math: LEFT OPERATOR RIGHT"""
            self.log(self.left, self.operator, self.right)
            try:
                if self.operator == "+":
                    self.left += self.right
                elif self.operator == "-":
                    self.left -= self.right
                elif self.operator == "/":
                    self.left /= self.right
                elif self.operator == "X":
                    self.left *= self.right
                self.display = str(self.left)
                self.value = ""
                self.log("=", self.left)
            except Exception:
                self.display = "Error"

        if button_name.isdigit():
            self.display = self.value = self.value.lstrip("0") + button_name
        elif button_name == "+/-":
            self.display = self.value = str(Decimal(self.value or "0") * -1)
        elif button_name == "%":
            self.display = self.value = str(
                Decimal(self.value or "0") / Decimal(100))
        elif button_name == ".":        ## importante para solo agregar un .
            if "." not in self.value:
                self.display = self.value = (self.value or "0") + "."
        elif button_name == "AC":       # reset 
            self.value = ""
            self.left = self.right = Decimal(0.0)
            self.operator = "+"
            self.display = "0.0"
        elif button_name == "C":
            self.value = ""
            self.display = "0.0"
        elif button_name in ("+", "-", "/", "X"):
            self.right = Decimal(self.value or "0")
            do_math()
            self.operator = button_name
        elif button_name == "=":
            if self.value:
                self.right = Decimal(self.value)
            do_math()


class CalculatorApp(App):
    """The Calculator Application"""

    async def on_mount(self) -> None:
        """Mount the calculator widget."""
        await self.view.dock(Calculator())


CalculatorApp.run(title="Calculator Test", log="textual.log")







def printHello():
    print('hello')