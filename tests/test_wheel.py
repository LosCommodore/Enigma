import random
import enigmatic
from enigmatic.rotor import RotorSpec, Rotor
import pytest


def test_wheel_spec_create(spec="EKMFLGDQVZNTOWYHXUSPAIBRCJ"):
    w = RotorSpec("test", spec.lower(), "")
    print("\n{w}")
    assert w.wiring.isupper()


@pytest.mark.parametrize(
    "spec",
    [
        "ABC",  # too short
        "EKMFLGDQVZNTOWYHXUSPAIBRCJABC",  # " too long"
        "EKMFLGDQVZN?OWYHXUSPAIBRCJ",  # "?" in spec
        "EEMFLGDQVZNTOWYHXUSPAIBRCJ",  # "E" twice
    ],
)
def test_error_on_wrong_wheel_spec(spec):
    with pytest.raises(ValueError):
        RotorSpec("testRotor", spec, "")


def test_rotor_symmetry():
    """Go through the rotor and the same path back -> back to staring letter"""
    w = Rotor(_get_random_wheel_spec())

    for i, _ in enumerate(enigmatic.ALPHABET):
        letter_out = w.route_backward(w.route(i))
        assert i == letter_out


def _get_random_wheel_spec() -> RotorSpec:
    wiring = list(enigmatic.ALPHABET)
    random.shuffle(wiring)
    wiring = "".join(str(x) for x in wiring)
    spec = RotorSpec("random", wiring, "")
    return spec
