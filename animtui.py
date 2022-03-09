from textual.app import App
from textual.reactive import Reactive
from textual.widgets import Footer, Placeholder
from textual.widget import Widget
from rich.console import Console
from rich.text import Text
from rich.align import Align

# terminal version <- ∄!x | streamlit => textual
class RichText(Widget):
    texto = "Convertidor Bases"

    def on_mount(self):
        pass

    def render(self):
        return Align.center(
            Text(self.texto, style="bold", justify="center"),
            vertical="top"
            )

        #Text(str(self.cons.rule('[bold yellow] Convertidor Bases')),style="bold",justify="center")


class Convertidor(App):
    
    async def on_load(self) -> None:
        await self.bind("d","act_sidebar"," Ver Documentacion")
        await self.bind("q", "quit","salir (q)")

    show_docs = Reactive(False)

    def watch_show_docs(self, show_docs: bool) -> None:
        self.bar.animate("layout_offset_x",0 if show_docs else -40)
    
    def action_act_sidebar(self) -> None:
        self.show_docs = not self.show_docs
    
    async def on_mount(self) -> None:
        footer = Footer()
        self.bar = Placeholder(name="left")

        await self.view.dock(footer,edge="bottom")
        await self.view.dock(RichText(), Placeholder(), edge="top")
        await self.view.dock(self.bar,edge="left",size=40,z=1)

        self.bar.layout_offset_x = -40
    

cons = Console()
cons.rule('[bold yellow] Resultados ')
Convertidor.run(title="Conv. Bases | Métodos Númericos",log='textual.log')
    
