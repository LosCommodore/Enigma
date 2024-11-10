import random

import rich.text
from rich.console import Console
from rich.table import Table

console = Console(legacy_windows=False, color_system="truecolor", style="Black on bright_white")
console.size = (200, 50)
console.record = True


# noinspection PyTypeChecker
def main():
    alphabet = tuple(chr(ord("a") + i) for i in range(26))
    table = Table(title="[red]ENIGMA", padding=(0, 0))
    table.add_column("Element")
    table.add_column("Pos")

    alp = list(alphabet)
    alp[5] = rich.text.Text("f", style="red bold")
    alp[10] = rich.text.Text("k", style="blue bold")

    for letter in alp:
        table.add_column(letter, justify="right")

    r1 = ["+" + str(random.randint(0, 24)) for _ in alphabet]
    r2 = ["+" + str(random.randint(0, 24)) for _ in alphabet]
    r3 = ["+" + str(random.randint(0, 24)) for _ in alphabet]
    r4 = ["+" + str(random.randint(0, 24)) for _ in alphabet]
    r1[5] = rich.text.Text(" -5", style="bright_red bold")
    r2[0] = rich.text.Text(" +10", style="bright_red bold")
    r3[10] = rich.text.Text(" +2", style="bright_red bold")
    r4[12] = rich.text.Text(" +5", style="bright_red bold")
    r3[17] = rich.text.Text("-10", style="bold bright_blue")
    r2[7] = rich.text.Text(" +3", style="bold bright_blue")
    r1[10] = rich.text.Text(" +1", style="bold bright_blue")

    table.add_row("rot_1", "D", *r1)
    table.add_row("rot_2", "D", *r2)
    table.add_row("rot_3", "D", *r3)
    table.add_row("Mirror", "D", *r4)

    console.clear()
    console.clear_live()
    console.print(table)

main()
