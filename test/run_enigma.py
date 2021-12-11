from enigmatic import WheelSpec, Wheel, Enigma
from rich.console import Console

# console
console = Console(legacy_windows=False, color_system="truecolor", style="Black on bright_white")
console.size = (200, 50)

# Enigma I
rot_I = WheelSpec('I', 'EKMFLGDQVZNTOWYHXUSPAIBRCJ', True, ('Q',))
rot_II = WheelSpec('II', 'AJDKSIRUXBLHWTMCQGZNPYFVOE', True, ('E',))
rot_III = WheelSpec('III', 'BDFHJLCPRTXVZNYEIWGAKMUSQO', True, ('V',))
rot_IV = WheelSpec('IV', 'ESOVPZJAYQUIRHXLNFTGKDCMWB', True, ('J',))
whl_etw = WheelSpec('etw', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', False)
whl_ukw_b = WheelSpec('ukw_b', 'YRUHQSLDPXNGOKMIEBFZCWVJAT', False)

r1 = Wheel(rot_I, 16, "Q")
r2 = Wheel(rot_IV, 26, "W")
r3 = Wheel(rot_III, 8, "E")
ukw = Wheel(whl_ukw_b)

enigma = Enigma([r1, r2, r3, ukw])
enigma.press_key("A")

console.print(enigma)
console.print(enigma.memory)
