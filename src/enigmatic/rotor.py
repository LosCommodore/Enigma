"""Enigma Rotors
https://www.cryptomuseum.com/crypto/enigma/wiring.htm
Secodary source: Wikipedia (less precise): https://en.wikipedia.org/wiki/Enigma_rotor_details
"""

from functools import cached_property

import numpy as np
from enigmatic import ALPHABET, ALPHABET_SET, Scrambler, _letters_to_numbers, _num2letter
from attrs import define, field
from attrs.setters import frozen


@define(frozen=True)
class RotorSpec:
    """ Specification of the enigma rotors
    According to: https://www.cryptomuseum.com/crypto/enigma/wiring.htm
    """
    name: str = field(converter=lambda x: x.upper())
    wiring: str = field(converter=lambda x: x.upper())

    turnovers: str = field(converter=lambda x: x.upper())  #
    """ Turnover shows which letter (or number) is visible in the window at the point of stepping .
    In German: Übertragskerben"""

    # noinspection PyUnresolvedReferences,PyUnusedLocal
    @wiring.validator
    def _check_wiring(self, attribute, value):
        if sorted(value) != sorted(ALPHABET):
            raise ValueError(r"Invalid wheel specification, invalid alphabet !")

    # noinspection PyUnresolvedReferences,PyUnusedLocal
    @turnovers.validator
    def _check_wiring(self, attribute, value):
        if not set(value).issubset(ALPHABET_SET):
            raise ValueError(r"Invalid wheel specification, invalid alphabet !")

    @property
    def is_dynamic(self) -> bool:
        """A dynamic rotor is actually able to rotate (not a stator)"""
        return len(self.turnovers) > 0

    @cached_property
    def notch_numbers(self) -> tuple[int, ...]:
        return tuple(_letters_to_numbers(self.turnovers))


WHEEL_SPECS: dict[str, RotorSpec] = {
    spec.name: spec

    # ENIGMA M4: Uboat-Enigma
    for spec in [
        # --- ENIGMA M3
        RotorSpec("M3: ukw-b", "YRUHQSLDPXNGOKMIEBFZCWVJAT", ""),

        # --- ENIGMA M4: Uboot-Enigma ---
        # https://www.cryptomuseum.com/crypto/enigma/wiring.htm#15

        RotorSpec("ETW", "ABCDEFGHIJKLMNOPQRSTUVWXYZ", ""),
        RotorSpec("I", "EKMFLGDQVZNTOWYHXUSPAIBRCJ", "Q"),
        RotorSpec("II", "AJDKSIRUXBLHWTMCQGZNPYFVOE", "E"),
        RotorSpec("III", "BDFHJLCPRTXVZNYEIWGAKMUSQO", "V"),
        RotorSpec("IV", "ESOVPZJAYQUIRHXLNFTGKDCMWB", "J"),
        RotorSpec("V", "VZBRGITYUPSDNHLXAWMJQOFECK", "Z"),
        RotorSpec("VI", "JPGVOUMFYQBENHZRDKASXLICTW", "ZM"),
        RotorSpec("VII", "NZJHGRCXMYSWBOUFAIVLPEKQDT", "ZM"),
        RotorSpec("VIII", "FKQHTLXOCBJSPDZRAMEWNIUYGV", "ZM"),
        RotorSpec("Beta", "LEYJVCNIXWPBQMDRTAKZGFUHOS", ""),
        RotorSpec("Gamma", "FSOKANUERHMBTIYCWLQPZXVGJD", ""),
        RotorSpec("UKW-B", "ENKQAUYWJICOPBLMDXZVFTHRGS", ""),  # UKW-BRUNO  == reflector b thin
        RotorSpec("UKW-C", "RDOBJNTKVEHMLFCWZAXGYIPSUQ", ""),  # UKW-CAESAR == reflector c thin
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
    """ Visible letter of the alphabet ring of the rotor trough the window of the enigma machine.
    The letter is represented as a 0-indexed number (A=0) 
    """

    ring_setting: int = field(default=1, converter=_ring_settings_converter)
    """ Changing the position of the ring will change 
    the position of the notch and alphabet, relative to the internal wiring. This setting is called the ring setting
    ring_setting is 1-indexed -> 1==A 
    """

    _relative_rotation: list[int] = field(init=False, repr=False)
    _relative_rotation_backward: list[int] = field(init=False, repr=False)

    def __attrs_post_init__(self):
        mapping = _letters_to_numbers(self.spec.wiring)
        sorted_mapping = np.argsort(mapping).tolist()

        self._relative_rotation = [m - i for i, m in enumerate(mapping)]
        self._relative_rotation_backward = [m - i for i, m in enumerate(sorted_mapping)]

    def route(self, letter: int) -> int:
        """
        Routing logic (example):
                 ↓
                ABCDEFG   - letter = 1
              ABCDEFG     - Rotation of wiring = 2
                 ↓        - Input rotation = 3 (D)
                 └─────┐  - relative rotation
                    output_rotation
        """
        input_rotation = (self.rotation_of_wiring + letter) % len(ALPHABET)
        output_rotation = letter + self._relative_rotation[input_rotation]

        return output_rotation % len(ALPHABET)

    def route_backward(self, letter: int) -> int:
        input_rotation = (self.rotation_of_wiring + letter) % len(ALPHABET)
        output_rotation = letter + self._relative_rotation_backward[input_rotation]

        return output_rotation % len(ALPHABET)

    @property
    def rotation_of_wiring(self) -> int:
        """The rotation of the wiring of the rotor is offset by the ring_settings"""
        rotation = self.position - (self.ring_setting - 1)
        return rotation % len(ALPHABET)

    def does_step(self) -> bool:
        return self.position in self.spec.notch_numbers

    def __str__(self):
        my_str = f"Pos: {_num2letter(self.position)} Ring: {self.ring_setting}  Wiring: {self.spec.wiring} Notch: {self.spec.turnovers}"

        return my_str
