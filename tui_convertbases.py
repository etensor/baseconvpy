from rich.align import Align
from rich.console import Console
from rich.layout import Layout
from rich.live import Live
from rich.text import Text
from time import sleep
from datetime import datetime

console = Console()
tui = Layout()


class Clock:
    def __rich__(self) -> Text:
        return Text(datetime.now().ctime(),
                    style="bold green",
                    justify="right"
                    )


tui.split(
    Layout(name="header",size=1),
    Layout(ratio=1,name="main"),
    Layout(size=10,name="footer"),
)

tui["main"].split_row(Layout(name="side"),Layout(name="body", ratio=2))

tui["side"].split(Layout(name="sisas"),Clock(),Layout())

tui["body"].update(
    Align.center(
        Text(
            """ Métodos Númericos | Walter M. """,
            justify="center",
        ),
        vertical="middle"
    ),
)

tui["body"].update(
    Align.center(
        Text(
            
        )
    )
)


tui["header"].update(Clock())
tui["sisas"].update(Clock())




with Live(tui,screen=True,redirect_stderr=False) as live:
    try:
        while True:
            sleep(1)
    except KeyboardInterrupt:
        pass