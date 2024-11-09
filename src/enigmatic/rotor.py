"""Enigma Rotors
https://en.wikipedia.org/wiki/Enigma_rotor_details
https://www.cryptomuseum.com/crypto/enigma/wiring.htm
"""

import numpy as np
from enigmatic import ALPHABET, ALPHABET_SET, Scrambler, _letters_to_numbers, _num2letter
from attrs import define, field
from attrs.setters import frozen


@define(frozen=True)
class RotorSpec:
    name: str
    wiring: str = field(converter=lambda x: x.upper())
    notches: str = field(converter=lambda x: x.upper())  # Übertragskerben

    # noinspection PyUnresolvedReferences,PyUnusedLocal
    @wiring.validator
    def _check_wiring(self, attribute, value):
        if sorted(value) != sorted(ALPHABET):
            raise ValueError(r"Invalid wheel specification, invalid alphabet !")

    # noinspection PyUnresolvedReferences,PyUnusedLocal
    @notches.validator
    def _check_wiring(self, attribute, value):
        if not set(value).issubset(ALPHABET_SET):
            raise ValueError(r"Invalid wheel specification, invalid alphabet !")

    @property
    def is_rotor(self) -> bool:
        return len(self.notches) > 0


WHEEL_SPECS: dict[str, RotorSpec] = {
    spec.name: spec
    for spec in [
        RotorSpec("I", "EKMFLGDQVZNTOWYHXUSPAIBRCJ", "Q"),
        RotorSpec("II", "AJDKSIRUXBLHWTMCQGZNPYFVOE", "E"),
        RotorSpec("III", "BDFHJLCPRTXVZNYEIWGAKMUSQO", "V"),
        RotorSpec("IV", "ESOVPZJAYQUIRHXLNFTGKDCMWB", "J"),
        RotorSpec("V", "VZBRGITYUPSDNHLXAWMJQOFECK", "Z"),
        RotorSpec("VI", "JPGVOUMFYQBENHZRDKASXLICTW", "ZM"),
        RotorSpec("VII", "NZJHGRCXMYSWBOUFAIVLPEKQDT", "ZM"),
        RotorSpec("VIII", "FKQHTLXOCBJSPDZRAMEWNIUYGV", "ZM"),
        RotorSpec("etw", "ABCDEFGHIJKLMNOPQRSTUVWXYZ", ""),
        RotorSpec("ukw_b", "YRUHQSLDPXNGOKMIEBFZCWVJAT", ""),
        RotorSpec("ukw_bruno", "ENKQAUYWJICOPBLMDXZVFTHRGS", ""),  # == reflector b thin
        RotorSpec("ukw_caesar", "RDOBJNTKVEHMLFCWZAXGYIPSUQ", ""),  # == reflector c thin
        RotorSpec("beta", "LEYJVCNIXWPBQMDRTAKZGFUHOS", ""),
        RotorSpec("gamma", "FSOKANUERHMBTIYCWLQPZXVGJD", ""),
    ]
}


def _ring_settings_converter(position: int | str):
    if isinstance(position, str):
        position = _letters_to_numbers(position)[0] + 1

    if not 1 <= position <= len(ALPHABET):
        raise ValueError("Invalid ring position")

    return position


@define
class Rotor(Scrambler):
    """A rotor or reflector for the enigma machine"""

    spec: RotorSpec = field(on_setattr=frozen)

    position: int = field(default=0, converter=lambda x: x % len(ALPHABET))
    """ Visible position in the enigma machine as number (A=0) """

    ring_settings: int = field(default=1, converter=_ring_settings_converter)
    """ Changing the position of the ring will change 
    the position of the notch and alphabet, relative to the internal wiring. This setting is called the ring setting

    ring_setings is 1-indexed -> 1==A 
    """

    _relative_mapping: list[int] = field(init=False, repr=False)
    _relative_mapping_backwards: list[int] = field(init=False, repr=False)

    def __attrs_post_init__(self):
        mapping = _letters_to_numbers(self.spec.wiring)
        sorted_mapping = np.argsort(mapping).tolist()

        self._relative_mapping = [m - i for i, m in enumerate(mapping)]
        self._relative_mapping_backwards = [m - i for i, m in enumerate(sorted_mapping)]

    def route(self, character: int) -> int:
        rot = self.total_rotation
        return (character + self._relative_mapping[(character + rot) % len(ALPHABET)]) % len(ALPHABET)

    def route_backward(self, letter: int) -> int:
        rot = self.total_rotation
        return (letter + self._relative_mapping_backwards[(letter + rot) % len(ALPHABET)]) % len(ALPHABET)

    @property
    def total_rotation(self):
        value = self.position - (self.ring_settings - 1)
        return value % len(ALPHABET)

    def does_step(self):
        return self.position in set(_letters_to_numbers(self.spec.notches))

    def __str__(self):
        my_str = f"Pos: {_num2letter(self.position)} Ring: {self.ring_settings}  Wiring: {self.spec.wiring} Notch: {self.spec.notches}"

        return my_str
