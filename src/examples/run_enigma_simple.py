from enigmatic.enigma import Enigma

enigma = Enigma.assemble(rotor_specs=["ukw-b", "beta", "V", "VI", "VIII"])
enigma.plug_board.add_cables("AE BF CM DQ HU JN LX PR SZ VW")
enigma.rotor_positions = "*SCHL"
enigma.ring_settings = "*AAEL"

output_text = enigma.write("Hello World")
print(output_text)
