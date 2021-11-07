import pytest
import enigmatic
import random


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
        enigmatic.RotorSpec("testRotor", "ABC", (), False)


def test_create_rotor_spec():
    spec = enigmatic.RotorSpec('I', 'EKMFLGDQVZNTOWYHXUSPAIBRCJ'.lower(), ('q',), False)
    print(spec)


def test_rotor_symmetry():
    wiring = list(enigmatic.ALPHABET)
    random.shuffle(wiring)
    wiring = "".join(str(x) for x in wiring)
    spec = enigmatic.RotorSpec("r1", wiring, (), False)
    r = enigmatic.Rotor(spec)

    for i,_ in enumerate(enigmatic.ALPHABET):
        letter_out = r.inv_route(r.route(i))
        assert i == letter_out
