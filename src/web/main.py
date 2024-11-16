from enigmatic.enigma import Enigma
from pyscript import window, document  # noqa: F401

def handle_click(event):
    sel_output = document.querySelector("#decode")
    sel_output.innerHTML = ""

    rot_names = [document.querySelector(f"#rot{i+1}").value for i in range(5)]
    window.console.log(f"{rot_names=}")

    rot_positions = [document.querySelector(f"#pos{i+1}").value for i in range(1, 5)]
    rot_positions = "*"+"".join(rot_positions)
    window.console.log(f"{rot_positions=}")

    ring_positions = [document.querySelector(f"#pos{i+1}").value for i in range(1, 5)]
    ring_positions = "*"+"".join(ring_positions)
    window.console.log(f"{ring_positions=}")

    enigma = Enigma.assemble(rotor_specs=rot_names)
    enigma.plug_board.add_cables("AE BF CM DQ HU JN LX PR SZ VW")
    enigma.rotor_positions = rot_positions
    enigma.ring_settings = ring_positions

    input_text = document.querySelector("#cyper").value
    output_text = enigma.write(input_text)

    sel_output.innerHTML = output_text
