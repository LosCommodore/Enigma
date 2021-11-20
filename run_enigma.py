from enigmatic import Enigma, RotorSpec, Rotor, PlugBoard
from rich.console import Console

# console
console = Console(legacy_windows=False, color_system="truecolor")
console.size = (200, 50)
console.record = True

# Assemble Enimga
plugBoard = PlugBoard(('ab', 'uv'))

rot_I = RotorSpec('I', 'EKMFLGDQVZNTOWYHXUSPAIBRCJ'.lower(), ('q',), False)
rot_II = RotorSpec('II', 'AJDKSIRUXBLHWTMCQGZNPYFVOE'.lower(), ('e',), False)
rot_III = RotorSpec('III', 'BDFHJLCPRTXVZNYEIWGAKMUSQO'.lower(), ('v',), False)
rot_ukw_b = RotorSpec('ukw_b', 'YRUHQSLDPXNGOKMIEBFZCWVJAT'.lower(), tuple(), True)

r1 = Rotor(rot_I)
r2 = Rotor(rot_II)
r3 = Rotor(rot_III)
r4 = Rotor(rot_ukw_b)

enigma = Enigma()
enigma.scramblers = [plugBoard, r3, r2, r1, r4]

# Use Engima:
console.rule("[bold red]START")

input_text = 'hallodiesisteintestumzusehenobmeinpythonscriptdasgleicheergebnislieferthallodiesisteintestumzus' \
             'ehenobmeinpythonscriptdasgleicheergebnisliefert'
print("Output Text: ", input_text)

output_text = []
for key in input_text:
    char, routing = enigma.pressKey(key)
    output_text.append(chr(char[-1] + ord('a')))

output_text = ''.join(output_text)
print("Output Text: ", output_text)

console.rule("[bold red]ENDE")
console.print(enigma.scramblers[1])
