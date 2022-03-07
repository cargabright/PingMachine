from datetime import datetime

from rich import box
from rich.align import Align
from rich.layout import Layout

from rich.panel import Panel
from rich.table import Table


def generate_table(data: dict) -> Table:
    """Make a new table."""
    table = Table()

    if len(data) > 0:
        table.add_column("IP Address")
        table.add_column("RTT")
        table.add_column("Status")

        for ip, data in data.items():
            table.add_row(
                f'{ip}', f'{data.get("RTT", "N/A")}',
                '[green]Online' if data.get("Status") == "Online" else '[red]Offline'
            )
    return table


class Header:
    """Display header with clock."""
    def __rich__(self) -> Panel:
        grid = Table.grid(expand=True)
        grid.add_column(justify="center", ratio=1)
        grid.add_column(justify="right")
        grid.add_row(
            "RPP Auto Configure application",
            datetime.now().ctime().replace(":", "[blink]:[/]"),
        )
        return Panel(grid, style="black on red")


def make_data_table(data) -> Panel:
    """Some example content."""
    table = Table(min_width=100)
    table.add_column("IP Address")
    table.add_column("RTT")
    table.add_column("Status")
    if len(data):
        for ip, data in data.items():
            table.add_row(
                f'{ip}',
                f'{data.get("RTT", "N/A")}',
                '[green]Online' if data.get("Status") == "Online" else '[red]Offline'
            )
    data_panel = Panel(
        Align.left(table),
        box=box.ROUNDED,
        padding=(1, 2),
        title="[b red]Configuring RPPs",
        border_style="red",
        expand=True
    )
    return data_panel


def make_layout() -> Layout:
    """Define the layout."""
    layout = Layout(name="root")
    layout.split(
        Layout(name="header", size=3),
        Layout(name="main", ratio=1),
    )
    layout["main"].split_row(
        Layout(name="body", ratio=1, minimum_size=60),
    )
    layout["header"].update(Header())
    return layout