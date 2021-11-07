import pytest
import enigmatic

import random


def test_unvalid_rotor_spec():
    with pytest.raises(Exception):
        spec = enigmatic.RotorSpec("testRotor","ABC",(),False)


def test_create_rotor_spec():
    spec = enigmatic.RotorSpec('I', 'EKMFLGDQVZNTOWYHXUSPAIBRCJ'.lower(), ('q',),False)
    print(spec)

#
# def test_rotor_symmetry():
#     wiring = list(enigma.ALPHABET)
#     random.shuffle(wiring)
#     wiring = "".join(str(x) for x in wiring)
#     r = enigma.Rotor("r1", wiring, (), False)
#
#     key_in = 5
#     key_out = r.inv_route(r.route(key_in))

#    assert key_in == key_out