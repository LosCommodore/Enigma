import pytest

import enigmatic
from enigmatic.enigma import Enigma
from rich.console import Console
from rich.table import Table
from pathlib import Path
import plotext as plt
import yaml
from collections import Counter

# console
console = Console(legacy_windows=False, color_system="truecolor", style="Black on bright_white")
console.size = (200, 50)


def test_double_step():
    """Test the double step feature
    „Royal Flags Wave Kings Above
    https://de.wikipedia.org/wiki/Enigma_(Maschine)#Anomalie
    """

    enigma = Enigma.assemble(["ukw_b", "I", "II", "III"])
    enigma.wheel_positions = "*ADU"

    enigma.write("x")
    assert enigma.wheel_positions == "AADV"

    enigma.write("x")
    assert enigma.wheel_positions == "AAEW"

    enigma.write("x")
    assert enigma.wheel_positions == "ABFX"


@pytest.mark.parametrize(
    "wheels,expected_period",
    [(["ukw_b", "III", "II", "I"], 26 * 25 * 26), (["ukw_b", "III", "II", "VI"], 8450)],
)
def test_enigma_period(wheels, expected_period):
    """
    https://de.wikipedia.org/wiki/Enigma_(Maschine)#Schl%C3%BCsselraum
    Period = 26*25*26 = 16.900 Walzenstellungen

    https://en.wikipedia.org/wiki/Cryptanalysis_of_the_Enigma
    The alphabet rings of rotors VI, VII and VIII contained two notches which, despite shortening the period of the substitution alphabet, made decryption more difficult.
    """
    print("\n")
    console.rule("Testing the period of the enigma", align="left")
    console.print(f"{wheels=}\n{expected_period=}")
    print("\n")

    enigma = Enigma.assemble(wheels)

    input_text = "X" * expected_period * 3

    possible_states = set(x + y + z for x in enigmatic.ALPHABET for y in enigmatic.ALPHABET for z in enigmatic.ALPHABET)

    states = []
    msg = []
    for t in input_text:
        states.append(enigma.wheel_positions[1:])
        m = enigma.write(t)
        msg.append(m)

    text = "".join(msg)

    assert "X" not in text

    missed_states = possible_states - set(states)

    count = list(Counter(states).values())
    count += [0] * len(missed_states)

    bins = len(set(count))
    if bins == 1:
        console.print(f"[bold]All used states (same rotor position) where reached {count[0]} times")
    else:
        # plt.clear_figure()
        plt.title("Number times the same rotor position was reached")
    #        plt.hist(count, bins, xside=[1, 2])
    #        plt.show()

    states_as_num = [enigmatic._letters_to_numbers(s) for s in states]

    r1, r2, r3 = list(zip(*states_as_num))
    h1 = Counter(r1)
    h2 = Counter(r2)
    h3 = Counter(r3)
    v1 = [h1[x] if x in h1 else 0 for x in range(26)]
    v2 = [h2[x] if x in h2 else 0 for x in range(26)]
    v3 = [h3[x] if x in h3 else 0 for x in range(26)]

    print("\n\n")
    table = Table(title="Num Rotor is in a certain position")
    table.add_column("Rotor_nr")
    for i in enigmatic.ALPHABET:
        table.add_column(i)

    for i, v in enumerate([v1, v2, v3]):
        table.add_row(str(i), *[str(u) for u in v])

    console.print(table)

    for period in range(1, len(text)):
        if text == (text[period:] + text[:period]):
            break
    else:
        raise Exception("No period found!")

    assert expected_period == len(possible_states) - len(missed_states)
    assert period == expected_period


def test_enigma_typing():
    enigma = Enigma.assemble(["ukw_b", "III", "II", "I"])

    assert enigma.write("hallodiesisteintest") == "MTNCZEVKHZUDSOACOEF"
    console.print(enigma)
    console.print(enigma.memory)


def load_testdata(schema):
    source = Path(r"test_messages")
    data = []
    id_ = []
    for f in source.glob(f"{schema}*.yaml"):
        with open(f, "r") as stream:
            y = yaml.safe_load(stream)
            id_.append(y["id"])
            data.append(y)

    return data, id_


def pytest_generate_tests(metafunc):
    for fixture in metafunc.fixturenames:
        if fixture.startswith("data_"):
            schema = "".removeprefix("data_")
            tests, ids = load_testdata(schema)
            metafunc.parametrize(fixture, tests, ids=ids)
            break


def test_enigma_messages(data_tests):
    enigma = Enigma.assemble(**data_tests["enigma"])
    console.print("\n")
    console.print(enigma)

    input_ = data_tests["input"].replace(" ", "").replace("\n", "")
    output = enigma.write(input_)

    expected_output = data_tests["output"].replace(" ", "").replace("\n", "").upper()

    assert output == expected_output


@pytest.mark.skip()
def test_repr_enigma():
    enigma = Enigma.assemble(["ukw_caesar", "beta", "V", "VI", "VIII"])
    enigma.plug_board.add_cables("AE BF CM DQ HU JN LX PR SZ VW")
    enigma.wheel_positions = "*NAEM"
    enigma.ring_positions = "*EPEL"

    print("\n")
    console.print(enigma)

    print(repr(enigma))
    enigma_copy = eval(repr(enigma))
    assert isinstance(enigma_copy, Enigma)
