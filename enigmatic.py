"""
This module provides the functionality for simulating enigma machines
"""

import numpy as np
from dataclasses import dataclass
from rich.table import Table
from rich.console import Group
from rich.panel import Panel
from typing import Iterable, Protocol, Generator, Union
from collections import deque

ALPHABET = tuple(chr(ord('a') + i) for i in range(26))  # Alphabet of the engima machine(s)


def _letters2num(letters: Iterable[str]) -> list[int]:
    return [ALPHABET.index(k) for k in letters]


def _num2letter(num: int):
    return ALPHABET[num]


class Scrambler(Protocol):
    """ A Scramber is any part which takes part in the encryption of the signal. For an Enigma machine these are the
    Rotors and the Plugboard """

    name: str

    def route(self, letter: int) -> int:
        """ Forward routing of a letter trouth the Scrambler """

    def inv_route(self, letter: int) -> int:
        """ Backwarts routing of a letter trouth the Scrambler """


@dataclass(frozen=True)
class RotorSpec:
    name: str
    wiring: str
    notches: tuple[str, ...]
    is_static: bool

    def __post_init__(self):
        if sorted(self.wiring) != sorted(ALPHABET):
            raise ValueError(r'Invalid rotor specification, invalid alphabet !')


class Rotor(Scrambler):
    """A rotor or reflector for the enigma machine """

    def __init__(self, spec: RotorSpec):
        self.spec = spec
        self.name: str = spec.name
        self.ring_position: int = 1

        self._wiring = {k: v for k, v in zip(ALPHABET, self.spec.wiring)}

        self.__rotation: int = 0  # property

        mapping = _letters2num(self.spec.wiring)
        self._mapping_rel = tuple(m - i for i, m in enumerate(mapping))
        self._mapping_rel_inv = tuple(m - i for i, m in enumerate(np.argsort(mapping)))

    @property
    def rotation(self):
        return self.__rotation

    @property
    def total_rotation(self):
        value = self.ring_position - 1 + self.rotation
        return value % len(ALPHABET)

    @rotation.setter
    def rotation(self, value):
        self.__rotation = value % len(ALPHABET)

    def route(self, character: int) -> int:
        rot = self.ring_position - 1 + self.rotation
        return (character + self._mapping_rel[(character + rot) % len(ALPHABET)]) % len(ALPHABET)

    def inv_route(self, letter: int) -> int:
        rot = self.ring_position - 1 + self.rotation
        return (letter + self._mapping_rel_inv[(letter + rot) % len(ALPHABET)]) % len(ALPHABET)

    def does_step(self):
        return self.rotation in set(_letters2num(self.spec.notches))

    def __repr__(self):
        my_str = [f"Name of Rotor: {self.spec.name}",
                  f"Wiring: {self._wiring}",
                  f"RingPosition: {self.ring_position}",
                  f"Rotation: {self.rotation}",
                  f"Notches: {self.spec.notches}"]

        return "\n".join(my_str)

    def __rich__(self):
        table = Table(padding=(0, 0))
        table.add_column('Absolute')
        for letter in ALPHABET:
            table.add_column(letter.upper(), justify='center')

        row = [f'Spec: wiring'] + list(self.spec.wiring)
        table.add_row(*row)

        rel = [f"{m:+03}" for m in self._mapping_rel]
        row = [f'Spec: relative'] + rel
        table.add_row(*row)

        relative_rot = deque(rel)
        relative_rot.rotate(self.total_rotation)
        row = [f'Total rotation {self.total_rotation:+03}'] + list(relative_rot)
        table.add_row(*row)

        properties = (f"Name of rotor: {self.spec.name}\n"
                      f"Ring position: {self.ring_position}\n"
                      f"Rotation: {self.rotation}\n"
                      f"Notches: {self.spec.notches}")

        group = Group(Panel(properties, expand=False), table)
        return Panel(group, title=f"[red]Rotor: {self.spec.name}", expand=False)


class PlugBoard(Scrambler):
    def __init__(self, cables: tuple[str, ...]):
        self.cables = cables
        self.name = "Plugboard"

    @property
    def cables(self) -> tuple[str, ...]:
        return self._cables

    @cables.setter
    def cables(self, cables: tuple[str, ...]):
        self._cables = tuple(cables)
        self._mapping = list(range(len(ALPHABET)))

        for cable in self._cables:
            i, o = _letters2num(cable)
            self._mapping[i] = o
            self._mapping[o] = i

    def route(self, letter: int) -> int:
        return self._mapping[letter]

    def inv_route(self, letter):
        return self._mapping[letter]  # symmetrisches Mapping beim Plugboard: aus "c -> a" folgt "a -> c"

    def __repr__(self):
        my_str = [f"Cables: {self.cables}"]
        return "\n".join(my_str)


class Enigma:
    def __init__(self, scramblers: list[Scrambler]):
        self.scramblers = scramblers

        # Some Enigma machines, such as the Zählwerksmaschine A28 and the Enigma G, were driven by a gear mechanism
        # with cog-wheels rather than by pawls and rachets. These machines do not suffer from the double stepping
        # anomaly and behave exactly like the odometer of a car.
        self.doube_step = True


    def _route_scramblers(self) -> Generator[Union[Scrambler.route, Scrambler.inv_route]]:
        for scrambler in self.scramblers:
            yield scrambler.route

        for scrambler in reversed(self.scramblers[:-1]):
            yield scrambler.inv_route

    def pressKey(self, key: str) -> list[int]:
        if key not in ALPHABET:
            raise ValueError('Invalid letter')

        key = _letters2num(key)[0]

        # Whenever a key is pressed, the rightmost wheel makes a single step before the switch is activated and a
        # lamp is turned on.
        self.rotate()

        current_key = key
        routing = [current_key]
        for route in self._route_scramblers():
            current_key = route(current_key)
            routing.append(current_key)

        return routing

    def rotate(self):
        if not self.doube_step:
            raise NotImplemented("Enigma currently has to be double-step")

        rotors = [x for x in self.scramblers if isinstance(x, Rotor) and not x.spec.is_static]

        do_rotate = [False] * len(rotors)
        do_rotate[0] = True  # first Rotor always rotates
        for i, step in enumerate([s.does_step() for s in rotors]):
            if step:
                do_rotate[i] = True
                do_rotate[i + 1] = True

        for rotor, step in zip(rotors, do_rotate):
            rotor.rotation += step

    @property
    def position(self):
        pos = [_num2letter(x.rotation) for x in self.scramblers if isinstance(x, Rotor) and not x.spec.is_static]
        return pos

    def __repr__(self):
        my_str = [f"Enigma, Pos: {self.position}"]

        return "\n".join(my_str)
