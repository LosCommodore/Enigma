from enigmatic import Enigma
from rich.console import Console
import rich.traceback

rich.traceback.install(show_locals=True)

# console
console = Console(legacy_windows=False, color_system="truecolor", style="Black on bright_white")
console.size = (200, 50)

enigma = Enigma(['ukw_b', 'III', 'II', 'I'])
# enigma.plugboard.cables = ('AD', 'CN', 'ET', 'FL', 'GI', 'JV', 'KZ', 'PU', 'QY', 'WX')
enigma.wheel_rotations = "AAA"
enigma.ring_positions = [1, 1, 5]

output_text = enigma.write("hallodiesisteinTest")

print(output_text)
console.print(enigma)
console.print(enigma.memory)
