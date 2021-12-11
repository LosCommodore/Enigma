from enigmatic import RealEnigma
from rich.console import Console

# console
console = Console(legacy_windows=False, color_system="truecolor", style="Black on bright_white")
console.size = (200, 50)

enigma = RealEnigma(['ukw_b', 'I', 'IV', 'III'])
# enigma.plugboard.cables = ('AD', 'CN', 'ET', 'FL', 'GI', 'JV', 'KZ', 'PU', 'QY', 'WX')
enigma.wheel_rotations = "QWE"
enigma.ring_positions = [1, 1, 1]

output_text = []
for key in "r".upper():
    char = enigma.press_key(key)
    output_text.append(char)

output_text = ''.join(output_text)
print(output_text)
console.print(enigma)
console.print(enigma.memory)
