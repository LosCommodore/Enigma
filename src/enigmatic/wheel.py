from dataclasses import dataclass
from typing import Union
import numpy as np
from enigmatic import ALPHABET, Scrambler, _letters2num, _num2letter


@dataclass(frozen=True)
class WheelSpec:
    name: str
    wiring: str
    notches: str  # Übertragskerben

    def __post_init__(self):
        self.__dict__["wiring"] = self.wiring.upper()

        if sorted(self.wiring) != sorted(ALPHABET):
            raise ValueError(r'Invalid wheel specification, invalid alphabet !')

        if len(self.wiring) != 26:
            raise ValueError(r'Invalid length for wheel specification')

    @property
    def is_rotor(self) -> bool:
        return len(self.notches) > 0


class Wheel(Scrambler):
    """A rotor or reflector for the enigma machine """

    def __init__(self, spec: WheelSpec, ring_position: Union[int, str] = 1, rotation: str = "A"):
        super().__init__(spec.name)
        self.__ring_position = 1
        self.ring_position = ring_position

        self._spec = spec
        self._rotation = _letters2num(rotation)[0]

        mapping = _letters2num(self._spec.wiring)
        self._mapping_rel = tuple(m - i for i, m in enumerate(mapping))
        self._mapping_rel_inv = tuple(m - i for i, m in enumerate(np.argsort(mapping)))

    @property
    def ring_position(self):
        return self.__ring_position

    @ring_position.setter
    def ring_position(self, value: Union[int, str]):
        if type(value) == int:
            if not 1 <= value <= len(ALPHABET):
                raise ValueError("Invalid ring position")
            self.__ring_position = value
        elif type(value) == str:
            if value != "*":
                self.__ring_position = _letters2num(value)[0] + 1
        else:
            raise ValueError("Invalid ring position")

    @property
    def spec(self):
        return self._spec

    @property
    def rotation(self):
        return self._rotation

    @rotation.setter
    def rotation(self, value):
        self._rotation = value % len(ALPHABET)

    @property
    def total_rotation(self):
        #  Wird der Ring um eine Position weiter gestellt, wird statt Position B im Sichtfenster der Walze ein A angezeigt.
        value = self.rotation - (self.ring_position - 1)
        return value % len(ALPHABET)

    def route(self, character: int) -> int:
        rot = self.total_rotation
        return (character + self._mapping_rel[(character + rot) % len(ALPHABET)]) % len(ALPHABET)

    def inv_route(self, letter: int) -> int:
        rot = self.total_rotation
        return (letter + self._mapping_rel_inv[(letter + rot) % len(ALPHABET)]) % len(ALPHABET)

    def does_step(self):
        return self.rotation in set(_letters2num(self._spec.notches))

    def __str__(self):
        my_str = f"Pos: {_num2letter(self.rotation)} Ring: {self.ring_position}  Wiring: {self._spec.wiring} Notch: {self._spec.notches}"

        return my_str


WHEEL_SPECS = {spec.name: spec for spec in [
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
