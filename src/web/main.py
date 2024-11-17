from enigmatic.enigma import Enigma
from pyscript import window, document  # noqa: F401


def handle_click(event):
    sel_output = document.querySelector("#decode")
    sel_output.innerHTML = ""

    rot_names = [document.querySelector(f"#rot{i+1}").value for i in range(4)]
    rot_positions = [document.querySelector(f"#pos{i+1}").value for i in range(4)]
    ring_positions = [document.querySelector(f"#ring{i+1}").value for i in range(4)]

    cables = document.querySelector("#cables").value

    # -- insert beta for ukb-b and gamma for ukw-c
    if rot_names[0] == "UKW-B":
        rot_names.insert(1, "beta")
    elif rot_names[0] == "UKW-C":
        rot_names.insert(1, "gamma")
    else:
        raise Exception("wrong Input for ukw! ")

    rot_positions.insert(0, "*")
    ring_positions.insert(0, "*")

    window.console.log(f"{rot_names=}")
    window.console.log(f"{rot_positions=}")
    window.console.log(f"{ring_positions=}")
    window.console.log(f"{cables=}")

    enigma = Enigma.assemble(rotor_specs=rot_names)
    enigma.plug_board.add_cables(cables)
    enigma.rotor_positions = rot_positions
    enigma.ring_settings = ring_positions

    input_text = document.querySelector("#cyper").value
    output_text = enigma.write(input_text)

    sel_output.innerHTML = output_text
