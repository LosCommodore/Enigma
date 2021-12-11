"""
This module provides the functionality for simulating enigma machines
"""

import numpy as np
import abc
from dataclasses import dataclass
import rich.console
from rich.table import Table
from typing import Iterable, Union
from collections import deque

ALPHABET = tuple(chr(ord('A') + i) for i in range(26))  # Alphabet of the engima machine(s)


def _letters2num(letters: Iterable[str]) -> list[int]:
    return [ALPHABET.index(k) for k in letters]


def _num2letter(num: int):
    return ALPHABET[num]


class Scrambler(abc.ABC):
    """ A Scramber is any part which takes part in the encryption of the signal. For an Enigma machine these are the
    Rotors and the Plugboard """

    name: str

    @abc.abstractmethod
    def route(self, letter: int) -> int:
        """ Forward routing of a letter trouth the Scrambler """

    @abc.abstractmethod
    def inv_route(self, letter: int) -> int:
        """ Backwarts routing of a letter trouth the Scrambler """

    def __rich_console__(self, console: rich.console.Console,
                         options: rich.console.ConsoleOptions) -> rich.console.RenderResult:
        yield self.__str__()


@dataclass(frozen=True)
class WheelSpec:
    name: str
    wiring: str
    is_rotor: bool  # rotor or reflector (does not move)
    notches: tuple[str, ...] = tuple()  # Übertragskerben

    def __post_init__(self):
        if sorted(self.wiring) != sorted(ALPHABET):
            raise ValueError(r'Invalid rotor specification, invalid alphabet !')


class Wheel(Scrambler):
    """A rotor or reflector for the enigma machine """

    def __init__(self, spec: WheelSpec, ring_position: int = 1, rotation: str = "A"):
        self.name: str = spec.name
        self.ring_position = ring_position

        self._spec = spec
        self._rotation = _letters2num(rotation)[0]

        mapping = _letters2num(self._spec.wiring)
        self._mapping_rel = tuple(m - i for i, m in enumerate(mapping))
        self._mapping_rel_inv = tuple(m - i for i, m in enumerate(np.argsort(mapping)))

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
        value = self.ring_position - 1 + self.rotation
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
    def __init__(self, scramblers: list[Scrambler], max_memory: int = 100):
        if len(set(scramblers)) != len(scramblers):
            raise ValueError("All Scrambles have to be unique objects")

        self.scramblers = scramblers

        # Some Enigma machines, such as the Zählwerksmaschine A28 and the Enigma G, were driven by a gear mechanism
        # with cog-wheels rather than by pawls and rachets. These machines do not suffer from the double stepping
        # anomaly and behave exactly like the odometer of a car.
        self.doube_step = True
        self.__memory: deque[list[str]] = deque([], maxlen=max_memory)

    @property
    def memory(self):
        return self.__memory

    @property
    def position(self):
        pos = [_num2letter(x.rotation) for x in self.scramblers if isinstance(x, Wheel) and not x.spec.is_rotor]
        return pos

    def _route_scramblers(self) -> Union[Scrambler.route, Scrambler.inv_route]:
        for scrambler in self.scramblers:
            yield scrambler.route

        for scrambler in reversed(self.scramblers[:-1]):
            yield scrambler.inv_route

    def press_key(self, key: str) -> str:
        if key not in ALPHABET:
            raise ValueError(f'Invalid letter: "{key}"')

        # Whenever a key is pressed, the wheels move before a lamp is turned on.
        self.rotate()

        n_key = _letters2num(key)[0]
        current_key = n_key
        routing = [current_key]
        for route in self._route_scramblers():
            # noinspection PyArgumentList
            current_key = route(current_key)
            routing.append(current_key)

        self.memory.append([_num2letter(x) for x in routing])

        return _num2letter(routing[-1])

    def rotate(self):
        if not self.doube_step:
            raise NotImplemented("Enigma currently has to be double-step")

        rotors = [x for x in self.scramblers if isinstance(x, Wheel) and x.spec.is_rotor]

        do_rotate = {rotors[0]}  # first Rotor always rotates

        for r1, r2 in zip(rotors, rotors[1:]):
            if r1.does_step():
                do_rotate.add(r1)
                do_rotate.add(r2)

        for rotor in do_rotate:
            rotor.rotation += 1

    def __str__(self):
        my_str = [f"Enigma, Pos: {self.position}"]

        return "\n".join(my_str)

    def __rich_console__(self, console: rich.console.Console,
                         options: rich.console.ConsoleOptions) -> rich.console.RenderResult:

        if not self.memory:
            table = Table()
            table.add_column('Component')
            table.add_column('Routing')
            for s in self.scramblers:
                table.add_row(s.name, s)

            yield table
        else:
            table = Table()
            table.add_column('Component')
            table.add_column('State')

            for s in self.scramblers:
                table.add_row(s.name, s)

            yield table

            table = Table()
            table.add_column('Component')
            table.add_column('Routing')

            m = self.memory[-1]
            input_nr = _letters2num(m[0])[0]
            table.add_row("Alphabet", "".join(ALPHABET))
            table.add_row("", " " * input_nr + "[green]↓")

            scr = self.scramblers.copy()

            scr += reversed(self.scramblers[:-1])
            symbol = "[green]↓"

            for s, routing, in zip(scr, _letters2num(m[1:])):
                if type(s) == PlugBoard:
                    table.add_row("Plugboard", "".join(ALPHABET))

                elif type(s) == Wheel:
                    rot = deque(ALPHABET)
                    # noinspection PyUnresolvedReferences
                    rot.rotate(-1 * s.total_rotation)
                    table.add_row(s.name, "".join(rot))
                else:
                    table.add_row(s.name, s)

                table.add_row("", " " * routing + symbol)

            table.add_row("Alphabet", "".join(ALPHABET))

            yield table


class RealEnigma(Enigma):
    def __init__(self, whl_specs: list[str]):
        whls = [Wheel(WHEELS[x]) for x in whl_specs]
        self.__plugboard = PlugBoard(tuple())
        self.__wheels = whls

        if not all([x.spec.is_rotor for x in whls[:-1]]):
            raise ValueError("Real Enigma needs to have rotos for all but the last wheel")

        if whls[-1].spec.is_rotor:
            raise ValueError("Last Wheel has to be a stator for an Enigma3")

        scramblers = [self.__plugboard, *whls]
        enigma = super().__init__(scramblers)

    @property
    def plugboard(self) -> PlugBoard:
        return self.__plugboard

    @property
    def wheels(self) -> list[Wheel]:
        return self.__wheels

    @property
    def wheel_rotations(self):
        rots = [_num2letter(x.rotation) for x in self.wheels]
        return "".join(rots)

    @wheel_rotations.setter
    def wheel_rotations(self, rotations: str):

        if len(rotations) != len(self.wheels) - 1:
            raise ValueError("Wrong number of positions")

        for whl, rot in zip(self.wheels, rotations):
            whl.rotation = _letters2num(rot)[0]

    @property
    def ring_positions(self) -> list[int]:
        return [x.ring_position for x in self.wheels]

    @ring_positions.setter
    def ring_positions(self, pos: list[int]):

        if len(pos) != len(self.wheels) - 1:
            raise ValueError("Wrong number of positions")

        for whl, rot in zip(self.wheels, pos):
            whl.ring_position = rot


WHEELS = {'I': WheelSpec('I', 'EKMFLGDQVZNTOWYHXUSPAIBRCJ', True, ('Q',)),
          'II': WheelSpec('II', 'AJDKSIRUXBLHWTMCQGZNPYFVOE', True, ('E',)),
          'III': WheelSpec('III', 'BDFHJLCPRTXVZNYEIWGAKMUSQO', True, ('V',)),
          'IV': WheelSpec('IV', 'ESOVPZJAYQUIRHXLNFTGKDCMWB', True, ('J',)),
          'etw': WheelSpec('etw', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', False),
          'ukw_b': WheelSpec('ukw_b', 'YRUHQSLDPXNGOKMIEBFZCWVJAT', False)
          }
