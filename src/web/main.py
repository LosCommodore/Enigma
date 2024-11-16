from enigmatic.enigma import Enigma
from pyscript import window, document  # noqa: F401

whl_input = document.querySelector("#whl_pos")
ring_input = document.querySelector("#ring_pos")


cables_input = document.querySelector("#cables")
cables_input.value = "AE BF CM DQ HU JN LX PR SZ VW"

whl_input.value = "*SCHL"
ring_input.value = "*AAEL"

def handle_click(event):
    input_text = document.querySelector("#cyper").value
    whl_text = document.querySelector("#whl_pos").value
    ring_text = document.querySelector("#ring_pos").value

    # window.console.log(f"{input_text=}")

    enigma = Enigma.assemble(wheel_specs=["ukw-c", "I", "V", "VI", "VIII"])
    enigma.plug_board.add_cables("AE BF CM DQ HU JN LX PR SZ VW")
    enigma.wheel_positions = whl_text
    enigma.ring_positions = ring_text

    output_text = enigma.write(input_text)

    sel_output = document.querySelector("#decode")
    sel_output.innerHTML = output_text
