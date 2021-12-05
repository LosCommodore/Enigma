from enigmatic import Enigma, WheelSpec, Wheel, PlugBoard
from rich.console import Console

# console
console = Console(legacy_windows=False, color_system="truecolor")
console.size = (200, 50)
console.record = True

# Assemble Enimga
plugBoard = PlugBoard(('ab', 'uv'))

rot_I = WheelSpec('I', 'EKMFLGDQVZNTOWYHXUSPAIBRCJ'.lower(), ('q',), True)
rot_II = WheelSpec('II', 'AJDKSIRUXBLHWTMCQGZNPYFVOE'.lower(), ('e',), True)
rot_III = WheelSpec('III', 'BDFHJLCPRTXVZNYEIWGAKMUSQO'.lower(), ('v',), True)
rot_ukw_b = WheelSpec('ukw_b', 'YRUHQSLDPXNGOKMIEBFZCWVJAT'.lower(), tuple(), False)

r1 = Wheel(rot_I)
r2 = Wheel(rot_II)
r3 = Wheel(rot_III)
r4 = Wheel(rot_ukw_b)

enigma = Enigma([plugBoard, r3, r2, r1, r4])

# Use Engima:
console.rule("[bold red]START")

input_text = 'hallodiesisteintestumzusehenobmeinpythonscriptdasgleicheergebnislieferthallodiesisteintestumzus' \
             'ehenobmeinpythonscriptdasgleicheergebnisliefert'

print("Input Text: ", input_text)

output_text = []
for key in input_text:
    char = enigma.press_key(key)
    output_text.append(char)

output_text = ''.join(output_text)
print("Output Text: ", output_text)