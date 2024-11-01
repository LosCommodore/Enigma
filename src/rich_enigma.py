import random

import rich.text
from rich.console import Console
from rich.table import Table

console = Console(legacy_windows=False, color_system="truecolor", style="Black on bright_white")
console.size = (200, 50)
console.record = True

alphabet = tuple(chr(ord('a') + i) for i in range(26))
table = Table(title="[red]ENIGMA", padding=(0, 0))
table.add_column("Element")
table.add_column("Pos")

alp = list(alphabet)
alp[5] = rich.text.Text('f', style='red bold')
alp[10] = rich.text.Text('k', style='blue bold')

for letter in alp:
    table.add_column(letter, justify='right')

r1: any = ["+" + str(random.randint(0, 24)) for _ in alphabet]
r2: any = ["+" + str(random.randint(0, 24)) for _ in alphabet]
r3: any = ["+" + str(random.randint(0, 24)) for _ in alphabet]
r4: any = ["+" + str(random.randint(0, 24)) for _ in alphabet]
r1[5] = rich.text.Text(" -5", style='bright_red bold')
r2[0] = rich.text.Text(" +10", style='bright_red bold')
r3[10] = rich.text.Text(" +2", style='bright_red bold')
r4[12] = rich.text.Text(" +5", style='bright_red bold')
r3[17] = rich.text.Text("-10", style='bold bright_blue')
r2[7] = rich.text.Text(" +3", style='bold bright_blue')
r1[10] = rich.text.Text(" +1", style='bold bright_blue')

table.add_row("rot_1", "D", *r1)
table.add_row("rot_2", "D", *r2)
table.add_row("rot_3", "D", *r3)
table.add_row("Mirror", "D", *r4)

# table.padding = (0,0,0,0)

# for i, letter in enumerate(alphabet):
#    if i == 10:
#        table.add_row("",letter,letter,"<- " +letter,"")
#    else:
#        table.add_row("",letter, letter, "   " + letter,"")


console.clear()
console.clear_live()
console.print(table)
console.save_html("blub.html")

# console.print("Danger, Will Robinson!", style="blink bold red underline on rgb(255,255,255)")

# layout = Layout()
#
# layout.split_row(
#     Layout(table,name="upper"),
#     Layout("hallo Welt",name="lower")
# )
#
# with console.screen():
#     #console.print(table)
#     console.print(layout)
#
# print("ende")
