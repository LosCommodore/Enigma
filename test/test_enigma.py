import time
import pytest
import enigmatic
import random
from rich.console import Console

# console
console = Console(legacy_windows=False, color_system="truecolor", style="Black on bright_white")
console.size = (200, 50)


def test_plug_board():
    cables = ('BZ', 'FG')
    p = enigmatic.PlugBoard(cables)

    # scheck for symmetry
    for x in enigmatic._letters2num(enigmatic.ALPHABET):
        assert x == p.inv_route(p.route(x))

    for cable in cables:
        i, o = enigmatic._letters2num(cable)
        assert p.route(i) == o
        assert p.route(o) == i


def test_wheel_spec_constructor():
    ok_spec = "EKMFLGDQVZNTOWYHXUSPAIBRCJ"

    # check ok
    enigmatic.WheelSpec("test", ok_spec)

    # check conversion to upper
    w = enigmatic.WheelSpec("test", ok_spec.lower())
    assert w.wiring.isupper()

    # check wrong letter
    err_spec = list(ok_spec)
    err_spec[4] = "^"
    err_spec = str(err_spec)
    with pytest.raises(ValueError):
        enigmatic.WheelSpec("testRotor", err_spec)

    # wrong length
    with pytest.raises(ValueError):
        enigmatic.WheelSpec("testRotor", ok_spec[:-1])


def test_rotor_symmetry():
    wiring = list(enigmatic.ALPHABET)
    random.shuffle(wiring)
    wiring = "".join(str(x) for x in wiring)
    spec = enigmatic.WheelSpec("r1", wiring)
    r = enigmatic.Wheel(spec)

    for i, _ in enumerate(enigmatic.ALPHABET):
        letter_out = r.inv_route(r.route(i))
        assert i == letter_out


def test_double_step():
    """ Test the double step feature
    „Royal Flags Wave Kings Above“
    https://de.wikipedia.org/wiki/Enigma_(Maschine)#Anomalie
    """

    enigma = enigmatic.Enigma(['ukw_b', 'I', 'II', 'III'])
    enigma.wheel_rotations = "ADU"

    enigma.write("x")
    assert enigma.wheel_rotations == "ADV"

    enigma.write("x")
    assert enigma.wheel_rotations == "AEW"

    enigma.write("x")
    assert enigma.wheel_rotations == "BFX"


def test_enigma_period():
    """
    https://de.wikipedia.org/wiki/Enigma_(Maschine)#Schl%C3%BCsselraum
    Period = 26*25*26 = 16.900 Walzenstellungen
    """

    enigma = enigmatic.Enigma(['ukw_b', 'I', 'II', 'III'])

    t = time.perf_counter()
    text = enigma.write("x" * 3 * 16900)
    dt = time.perf_counter() - t

    print(f"elapsed time: {dt}")

    assert text[:16900] == text[16900:2*16900] == text[2*16900:]


def test_enigma_typing():
    enigma = enigmatic.Enigma(['ukw_b', 'III', 'II', 'I'])

    assert enigma.write("hallodiesisteintest") == "MTNCZEVKHZUDSOACOEF"
    console.print(enigma)
    console.print(enigma.memory)


def test_type_wiki_message():
    """
    messsage described in:
    https://de.wikipedia.org/wiki/Enigma_(Maschine)
    """

    message = """LJPQH SVDWC LYXZQ FXHIU VWDJO BJNZX RCWEO TVNJC IONTF
QNSXW ISXKH JDAGD JVAKU KVMJA JHSZQ QJHZO IAVZO WMSCK ASRDN
XKKSR FHCXC MPJGX YIJCC KISYY SHETX VVOVD QLZYT NJXNU WKZRX
UJFXM BDIBR VMJKR HTCUJ QPTEE IYNYN JBEAQ JCLMU ODFWM ARQCF
OBWN""".replace(' ', '').replace('\n', '')

    translation = """dasoberkommandoderwehrmaqtgibtbekanntxaachenxaache
nxistgerettetxdurqgebuendelteneinsatzderhilfskraef
tekonntediebedrohungabgewendetunddierettungderstad
tgegenxeinsxaqtxnullxnullxuhrsiqergestelltwerdenx"""

    # Tagesschlüssel:
    # Tag UKW Walzenlage Ringstellung ---- Steckerverbindungen ----    Kenngruppen
    #  31  B  I   IV III   16 26 08   AD CN ET FL GI JV KZ PU QY WX  dmr now wxy bev
    #
    # Die Kenngruppe hat keine kryptologische Bedeutung,[49] sie dient dem Empfänger der Nachricht nur dazu, zu erkennen, dass die Nachricht wirklich für ihn bestimmt ist und auch befugt entschlüsselt werden kann.

    enigma = enigmatic.Enigma(['ukw_b', 'I', 'IV', 'III'])
    enigma.plugboard.cables = ('AD', 'CN', 'ET', 'FL', 'GI', 'JV', 'KZ', 'PU', 'QY', 'WX')
    enigma.wheel_rotations = "QWE"
    enigma.ring_positions = [16, 26, 8]

    message_key = 'RTZ'
    assert enigma.write(message_key) == 'EWG'

    # Spruchkopf wird offen übertragen
    # Uhrzeit - Anzahl zeichen - Zufällige Wahl + Ergebnis
    # Kopf: 2220 – 204 – QWE EWG -

    enigma.wheel_rotations = message_key
    assert enigma.write(translation) == message
