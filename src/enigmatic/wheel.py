from typing import Union
import numpy as np
from enigmatic import ALPHABET, Scrambler, _letters_to_numbers, _num2letter
from attrs import define, field
from attrs.setters import frozen


@define(frozen=True)
class WheelSpec:
    name: str
    wiring: str = field(converter=lambda x: x.upper())
    notches: str = field(converter=lambda x: x.upper())  # Übertragskerben

    # noinspection PyUnresolvedReferences,PyUnusedLocal
    @wiring.validator
    def _check_wiring(self, attribute, value):
        if sorted(value) != sorted(ALPHABET):
            raise ValueError(r'Invalid wheel specification, invalid alphabet !')

    @property
    def is_rotor(self) -> bool:
        return len(self.notches) > 0


WHEEL_SPECS: dict[str, WheelSpec] = \
    {spec.name: spec for spec in [
        WheelSpec('I', 'EKMFLGDQVZNTOWYHXUSPAIBRCJ', 'Q'),
        WheelSpec('II', 'AJDKSIRUXBLHWTMCQGZNPYFVOE', 'E'),
        WheelSpec('III', 'BDFHJLCPRTXVZNYEIWGAKMUSQO', 'V'),
        WheelSpec('IV', 'ESOVPZJAYQUIRHXLNFTGKDCMWB', 'J'),
        WheelSpec('V', 'VZBRGITYUPSDNHLXAWMJQOFECK', 'Z'),
        WheelSpec('VI', 'JPGVOUMFYQBENHZRDKASXLICTW', 'ZM'),
        WheelSpec('VII', 'NZJHGRCXMYSWBOUFAIVLPEKQDT', 'ZM'),
        WheelSpec('VIII', 'FKQHTLXOCBJSPDZRAMEWNIUYGV', 'ZM'),
        WheelSpec('etw', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', ''),
        WheelSpec('ukw_b', 'YRUHQSLDPXNGOKMIEBFZCWVJAT', ''),
        WheelSpec('ukw_bruno', 'ENKQAUYWJICOPBLMDXZVFTHRGS', ''),  # == reflector b thin
        WheelSpec('ukw_caesar', 'RDOBJNTKVEHMLFCWZAXGYIPSUQ', ''),  # == reflector c thin
        WheelSpec('beta', 'LEYJVCNIXWPBQMDRTAKZGFUHOS', ''),
        WheelSpec('gamma', 'FSOKANUERHMBTIYCWLQPZXVGJD', ''),
    ]}


def _ring_position_converter(position: int | str):
    if isinstance(position, str):
        position = _letters_to_numbers(position)[0] + 1

    if not 1 <= position <= len(ALPHABET):
        raise ValueError("Invalid ring position")

    return position


@define
class Wheel(Scrambler):
    """A rotor or reflector for the enigma machine """
    spec: WheelSpec = field(on_setattr=frozen)
    rotation: int = field(default=0, converter=lambda x: x % len(ALPHABET))
    ring_position: int = field(default=1, converter=_ring_position_converter)

    _relative_mapping: list[int] = field(init=False, repr=False)
    _relative_mapping_backwards: list[int] = field(init=False, repr=False)

    def __attrs_post_init__(self):
        mapping = _letters_to_numbers(self.spec.wiring)
        sorted_mapping = np.argsort(mapping).tolist()

        self._relative_mapping = [m - i for i, m in enumerate(mapping)]
        self._relative_mapping_backwards = [m - i for i, m in enumerate(sorted_mapping)]

    @property
    def total_rotation(self):
        #  Wird der Ring um eine Position weiter gestellt, wird statt Position B im Sichtfenster der Walze ein A angezeigt.
        value = self.rotation - (self.ring_position - 1)
        return value % len(ALPHABET)

    def route(self, character: int) -> int:
        rot = self.total_rotation
        return (character + self._relative_mapping[(character + rot) % len(ALPHABET)]) % len(ALPHABET)

    def route_backward(self, letter: int) -> int:
        rot = self.total_rotation
        return (letter + self._relative_mapping_backwards[(letter + rot) % len(ALPHABET)]) % len(ALPHABET)

    def does_step(self):
        return self.rotation in set(_letters_to_numbers(self.spec.notches))

    def __str__(self):
        my_str = f"Pos: {_num2letter(self.rotation)} Ring: {self.ring_position}  Wiring: {self.spec.wiring} Notch: {self.spec.notches}"

        return my_str
