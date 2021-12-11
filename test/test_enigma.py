import pytest
import enigmatic
from enigmatic import WheelSpec, Wheel, PlugBoard, Enigma
import random
from rich.console import Console

# console
console = Console(legacy_windows=False, color_system="truecolor", style="Black on bright_white")
console.size = (200, 50)


def test_plug_board():
    cables = ('bz', 'fg')

    p = enigmatic.PlugBoard(tuple())
    assert p.route(0) == 0
    assert p.route(20) == 20

    p.cables = cables
    for cable in cables:
        i, o = enigmatic._letters2num(cable)
        assert p.route(i) == o
        assert p.route(o) == i


def test_unvalid_rotor_spec():
    with pytest.raises(Exception):
        enigmatic.WheelSpec("testRotor", "ABC", False)


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
    enigma = enigmatic.RealEnigma(['I', 'II', 'III', 'ukw_b'])

    input_text = "hallodiesisteintest".upper()
    output_text = []
    for key in input_text:
        char = enigma.press_key(key)
        output_text.append(char)

    output_text = ''.join(output_text)
    assert output_text == "MTNCZEVKHZUDSOACOEF"
    console.print(enigma)
    console.print(enigma.memory)


def test_type_message():
    message = """XYOWN LJPQH SVDWC LYXZQ FXHIU VWDJO BJNZX RCWEO TVNJC IONTF
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

    plugBoard = PlugBoard(('AD', 'CN', 'ET', 'FL', 'GI', 'JV', 'KZ', 'PU', 'QY', 'WX'))

    # Enigma I
    rot_I     = WheelSpec('I',     'EKMFLGDQVZNTOWYHXUSPAIBRCJ', True, ('Q',))
    rot_II    = WheelSpec('II',    'AJDKSIRUXBLHWTMCQGZNPYFVOE', True, ('E',))
    rot_III   = WheelSpec('III',   'BDFHJLCPRTXVZNYEIWGAKMUSQO', True, ('V',))
    rot_IV    = WheelSpec('IV',    'ESOVPZJAYQUIRHXLNFTGKDCMWB', True, ('J',))
    whl_etw   = WheelSpec('etw',   'ABCDEFGHIJKLMNOPQRSTUVWXYZ', False)
    whl_ukw_b = WheelSpec('ukw_b', 'YRUHQSLDPXNGOKMIEBFZCWVJAT', False)

    etw = Wheel(whl_etw)

    # Tagesschlüssel:
    # - Walzenlage: B I IV III
    # - Ringstellung 16 26 08

    # Benutzer denkt sich eine zufällige Grundstellung aus:
    r1 = Wheel(rot_I,  16, "Q")
    r2 = Wheel(rot_IV, 26, "W")
    r3 = Wheel(rot_III, 8, "E")
    ukw = Wheel(whl_ukw_b)

    enigma = Enigma([plugBoard, r1, r2, r3, ukw])

    output_text = []
    message_pre = 'RTZ'
    translation_pre = 'EWG'
    for key in message_pre:
        char = enigma.press_key(key)
        output_text.append(char)

    output_text = ''.join(output_text)

    console.print(enigma)
    console.print(enigma.memory)

    assert output_text == translation_pre
