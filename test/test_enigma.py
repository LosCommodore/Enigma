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


def test_rotor_spec():
    ok_spec = "EKMFLGDQVZNTOWYHXUSPAIBRCJ"

    # check ok
    enigmatic.WheelSpec("test", ok_spec, False)

    # check conversion to upper
    w = enigmatic.WheelSpec("test", ok_spec.lower(), False)
    assert w.wiring.isupper()

    # check wrong letter
    err_spec = list(ok_spec)
    err_spec[4] = "^"
    err_spec = str(err_spec)
    with pytest.raises(ValueError):
        enigmatic.WheelSpec("testRotor", err_spec, False)

    # wrong length
    with pytest.raises(ValueError):
        enigmatic.WheelSpec("testRotor", ok_spec[:-1], False)


def test_create_rotor_spec():
    spec = enigmatic.WheelSpec('I', 'EKMFLGDQVZNTOWYHXUSPAIBRCJ'.lower(), True, ('q',))
    print(spec)


def test_rotor_move():
    print("")

    routing = 'EKMFLGDQVZNTOWYHXUSPAIBRCJ'.lower()
    spec = enigmatic.WheelSpec('I', routing, True, ('q',))
    rotor = enigmatic.Wheel(spec)
    len_alphabet = len(enigmatic.ALPHABET)

    for rot in range(len_alphabet * 2):
        rotor.rotation = rot
        console.print(rotor)

        for i in range(len_alphabet):
            o = rotor.route(i)
            expected_letter = routing[(i + rot) % len_alphabet]
            assert o == enigmatic._letters2num(expected_letter)[0] + rot


def test_rotor_symmetry():
    wiring = list(enigmatic.ALPHABET)
    random.shuffle(wiring)
    wiring = "".join(str(x) for x in wiring)
    spec = enigmatic.WheelSpec("r1", wiring, False)
    r = enigmatic.Wheel(spec)

    for i, _ in enumerate(enigmatic.ALPHABET):
        letter_out = r.inv_route(r.route(i))
        assert i == letter_out


def test_real_enigma():
    enigma = enigmatic.RealEnigma(['ukw_b', 'III', 'II', 'I'])

    assert enigma.type("hallodiesisteintest") == "MTNCZEVKHZUDSOACOEF"
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
OBWN"""

    message = message.replace(' ', '').replace('\n', '')

    translation = """dasoberkommandoderwehrmaqtgibtbekanntxaachenxaache
nxistgerettetxdurqgebuendelteneinsatzderhilfskraef
tekonntediebedrohungabgewendetunddierettungderstad
tgegenxeinsxaqtxnullxnullxuhrsiqergestelltwerdenx"""

    translation = translation.replace('\n', '').upper()

    # Tagesschlüssel:
    # Tag UKW Walzenlage Ringstellung ---- Steckerverbindungen ----    Kenngruppen
    #  31  B  I   IV III   16 26 08   AD CN ET FL GI JV KZ PU QY WX  dmr now wxy bev
    #
    # Die Kenngruppe hat keine kryptologische Bedeutung,[49] sie dient dem Empfänger der Nachricht nur dazu, zu erkennen, dass die Nachricht wirklich für ihn bestimmt ist und auch befugt entschlüsselt werden kann.

    enigma = enigmatic.RealEnigma(['ukw_b', 'I', 'IV', 'III'])
    enigma.plugboard.cables = ('AD', 'CN', 'ET', 'FL', 'GI', 'JV', 'KZ', 'PU', 'QY', 'WX')
    enigma.wheel_rotations = "QWE"
    enigma.ring_positions = [16, 26, 8]

    message_key = 'RTZ'
    translation_pre = 'EWG'
    output_text = enigma.type(message_key)

    assert output_text == translation_pre

    # Spruchkopf wird offen übertragen
    # Uhrzeit - Anzahl zeichen - Zufällige Wahl + Ergebnis
    # Kopf: 2220 – 204 – QWE EWG -

    enigma.wheel_rotations = message_key
    output_text = enigma.type(translation)
    assert output_text == message

