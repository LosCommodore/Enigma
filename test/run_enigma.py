from enigmatic import RealEnigma
from rich.console import Console

# console
console = Console(legacy_windows=False, color_system="truecolor", style="Black on bright_white")
console.size = (200, 50)

enigma = RealEnigma(['ukw_b', 'III', 'II', 'I'])
# enigma.plugboard.cables = ('AD', 'CN', 'ET', 'FL', 'GI', 'JV', 'KZ', 'PU', 'QY', 'WX')
enigma.wheel_rotations = "AAA"
enigma.ring_positions = [1, 1, 5]

output_text = enigma.type("hallodiesisteinTest")

print(output_text)
console.print(enigma)
console.print(enigma.memory)
