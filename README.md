# Enigma Simulator

A simple enigma simulator written in python, just for fun :)

⚠ The code is not tested thoroughly

## Web App

Developed with pyscript:
https://los_commodore.pyscriptapps.com/enigma/latest/

## Example with python

```python
from enigmatic.enigma import Enigma

enigma = Enigma.assemble(rotor_specs=["ukw-b", "beta", "V", "VI", "VIII"])
enigma.plug_board.add_cables("AE BF CM DQ HU JN LX PR SZ VW")
enigma.rotor_positions = "*SCHL"
enigma.ring_settings = "*AAEL"

output_text = enigma.write("Hello World")
print(output_text)
# result:
# GBAKITMLDZ
```


