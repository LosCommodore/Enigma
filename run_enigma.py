from enigmatic import Enigma, RotorSpec, Rotor, PlugBoard
from rich.console import Console

# console
console = Console(legacy_windows=False, color_system="truecolor", style="Black on bright_white")
console.size = (200, 50)
console.record = True

# Create Enimga
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

# Press Key:
console.rule("[bold red]TEXT")
text = 'hallodiesisteintestumzusehenobmeinpythonscriptdasgleicheergebnislieferthallodiesisteintestumzus' \
       'ehenobmeinpythonscriptdasgleicheergebnisliefert'
encoded = []
for key in text:
    char, routing = enigma.pressKey(key)
    # print(char,routing)
    encoded.append(chr(char[-1] + ord('a')))
encoded = ''.join(encoded)  # List of Strings -> String
print("Encoded Text: ", encoded)
# charInv,routingInv = riddle.pressKey(lastChar)

console.print(r1)

print("ende")
