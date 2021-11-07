import enigmatic
from enigmatic import Enigma,Rotor,Scrambler,PlugBoard
from rich.console import Console

# console
console = Console(legacy_windows=False, color_system="truecolor", style="Black on bright_white")
console.size = (200, 50)
console.record = True

# Create Enigma
riddle = Enigma()

# Plugboard
plugBoard = PlugBoard('Plugboard')
# plugBoard.cables =  [('a','b'), ('u','v'), ('r','x'), ('t','w')]

# Create Rotors
rot1 = Rotor('I', 'EKMFLGDQVZNTOWYHXUSPAIBRCJ'.lower(), ('q',))
rot2 = Rotor('II', 'AJDKSIRUXBLHWTMCQGZNPYFVOE'.lower(), ('e',))
rot3 = Rotor('III', 'BDFHJLCPRTXVZNYEIWGAKMUSQO'.lower(), ('v',))
ukw_b = Rotor('ukw_b', 'YRUHQSLDPXNGOKMIEBFZCWVJAT'.lower(), isStatic=True)
# Wire Enigma:
riddle.scramblers.append(plugBoard)
riddle.scramblers += [rot3, rot2, rot1, ukw_b]

# Press Key:
console.rule("[bold red]TEXT")
text = 'hallodiesisteintestumzusehenobmeinpythonscriptdasgleicheergebnislieferthallodiesisteintestumzus' \
       'ehenobmeinpythonscriptdasgleicheergebnisliefert'
encoded = []
for key in text:
    char, routing = riddle.pressKey(key)
    # print(char,routing)
    encoded.append(chr(char[-1] + ord('a')))
encoded = ''.join(encoded)  # List of Strings -> String
print("Encoded Text: ", encoded)
# charInv,routingInv = riddle.pressKey(lastChar)

console.print(rot1)


print("ende")
