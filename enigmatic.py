"""
This module provides the functionality for simulating enigma machines
"""
import enum
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

    def __init__(self, name):
        self.name = ""

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
    notches: tuple[str, ...] = tuple()  # Übertragskerben

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

    def __init__(self, spec: WheelSpec, ring_position: int = 1, rotation: str = "A"):
        super().__init__(spec.name)
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


class PlugBoard(Scrambler):
    def __init__(self, cables: tuple[str, ...]):
        super().__init__("Plugboard")
        self.cables = cables

    @property
    def cables(self) -> tuple[str, ...]:
        return self._cables

    @cables.setter
    def cables(self, cables: tuple[str, ...]):
        cables = tuple(c.upper() for c in cables)
        used_letters = "".join(cables)
        if not all(x in ALPHABET for x in used_letters):
            raise ValueError("Invalid letters for cables")

        self._cables = cables
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


class GeneralEnigma:
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
        pos = [_num2letter(x.rotation) for x in self.scramblers if isinstance(x, Wheel) and x.spec.is_rotor]
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

    def write(self, text: str) -> str:
        input_text = text.upper().replace(' ', '').replace('\n', '')

        output_text = [self.press_key(key) for key in input_text]

        return "".join(output_text)

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


@enum.unique
class EnigmaVersion(enum.Enum):
    CUSTOM = enum.auto()
    M3 = enum.auto()
    M4 = enum.auto()


class Enigma(GeneralEnigma):
    def __init__(self, version: EnigmaVersion, whl_specs: list[str]):
        whls = [Wheel(WHEELS[x]) for x in reversed(whl_specs)]
        self.__version = version
        self.__plugboard = PlugBoard(tuple())
        self.__wheels = whls

        if whls[-1].spec.is_rotor:
            raise ValueError("Last Wheel has to be a stator for an enigma machine")

        idx_is_rotor = np.where(np.array([x.spec.is_rotor for x in whls]))
        rotors_in_block = np.all(np.diff(idx_is_rotor) == 1)

        if not rotors_in_block:
            raise ValueError("No stators are allowed in between rotors")

        scramblers = [self.__plugboard, *whls]
        enigma = super().__init__(scramblers)

    @property
    def version(self):
        return self.__version

    @property
    def plugboard(self) -> PlugBoard:
        return self.__plugboard

    @property
    def wheels(self) -> list[Wheel]:
        return self.__wheels

    @property
    def rotors(self) -> list[Wheel]:
        return self.__wheels[:-1]

    @property
    def wheel_rotations(self):
        rots = [_num2letter(x.rotation) for x in reversed(self.rotors)]
        return "".join(rots)

    @wheel_rotations.setter
    def wheel_rotations(self, rotations: str):

        if len(rotations) > len(self.wheels):
            raise ValueError("Too many rotations")

        for whl, rot in zip(self.wheels, reversed(rotations)):
            whl.rotation = _letters2num(rot)[0]

    @property
    def ring_positions(self) -> list[int]:
        return [x.ring_position for x in reversed(self.wheels)]

    @ring_positions.setter
    def ring_positions(self, pos: list[int]):

        if len(pos) > len(self.wheels):
            raise ValueError("Too many ring_positions")

        for whl, rot in zip(self.rotors, reversed(pos)):
            whl.ring_position = rot


WHEELS = {'I': WheelSpec('I', 'EKMFLGDQVZNTOWYHXUSPAIBRCJ', ('Q',)),
          'II': WheelSpec('II', 'AJDKSIRUXBLHWTMCQGZNPYFVOE', ('E',)),
          'III': WheelSpec('III', 'BDFHJLCPRTXVZNYEIWGAKMUSQO', ('V',)),
          'IV': WheelSpec('IV', 'ESOVPZJAYQUIRHXLNFTGKDCMWB', ('J',)),
          'etw': WheelSpec('etw', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'),
          'ukw_b': WheelSpec('ukw_b', 'YRUHQSLDPXNGOKMIEBFZCWVJAT')
          }
