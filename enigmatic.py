"""
This module provides the functionality for simulating enigma machines
"""

import numpy as np
import abc
from dataclasses import dataclass
import rich
from rich.table import Table
from rich.console import Group
from rich.panel import Panel
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
        self._rotation = _letters2num(rotation)[0] - 1  # example: "B" => rotation=1

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
        my_str = [f"Name of Rotor: {self._spec.name}",
                  f"Wiring: {self._spec.wiring}",
                  f"RingPosition: {self.ring_position}",
                  f"Rotation: {self.rotation}",
                  f"Notches: {self._spec.notches}"]

        return "\n".join(my_str)

    def __rich_console__(self, console: rich.console.Console,
                         options: rich.console.ConsoleOptions) -> rich.console.RenderResult:
        table = Table(padding=(0, 0))
        table.add_column('Absolute')
        for letter in ALPHABET:
            table.add_column(letter.upper(), justify='center')

        row = [f'Spec: wiring'] + list(self._spec.wiring)
        table.add_row(*row)

        rel = [f"{m:+03}" for m in self._mapping_rel]
        row = [f'Spec: relative'] + rel
        table.add_row(*row)

        relative_rot = deque(rel)
        relative_rot.rotate(self.total_rotation)
        row = [f'Total rotation {self.total_rotation:+03}'] + list(relative_rot)
        table.add_row(*row)

        properties = (f"Name of rotor: {self._spec.name}\n"
                      f"Ring position: {self.ring_position}\n"
                      f"Rotation: {self.rotation}\n"
                      f"Notches: {self._spec.notches}")

        group = Group(Panel(properties, expand=False), table)
        yield Panel(group, title=f"[red]Rotor: {self._spec.name}", expand=False)


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

    def __rich_console__(self, console: rich.console.Console,
                         options: rich.console.ConsoleOptions) -> rich.console.RenderResult:
        yield self.__str__()


@dataclass(frozen=True)
class EnigmaMemory:
    key: str
    routing: list[str]


class Enigma:
    def __init__(self, scramblers: list[Scrambler], max_memory: int = 100):
        if len(set(scramblers)) != len(scramblers):
            raise ValueError("All Scrambles have to be unique objects")

        self.scramblers = scramblers

        # Some Enigma machines, such as the Zählwerksmaschine A28 and the Enigma G, were driven by a gear mechanism
        # with cog-wheels rather than by pawls and rachets. These machines do not suffer from the double stepping
        # anomaly and behave exactly like the odometer of a car.
        self.doube_step = True
        self.__memory: deque[EnigmaMemory] = deque([], maxlen=max_memory)

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

        self.memory.append(EnigmaMemory(key, [_num2letter(x) for x in routing]))

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

    def __rich__(self):
        table = Table()
        if not self.memory:
            table.add_column('Component')
            table.add_column('Routing')
            for s in self.scramblers:
                table.add_row(s.name, s)
        else:
            table.add_column('Component')
            table.add_column('Routing')

            m = self.memory[-1]
            input_nr = _letters2num(m.key)[0]
            table.add_row("Alphabet", "".join(ALPHABET))
            table.add_row("", " "*input_nr + "[green]↓")

            scr = self.scramblers.copy()

            scr += reversed(self.scramblers[:-1])
            symbol = "[green]↓"

            for s, routing, in zip(scr, _letters2num(m.routing)):
                if type(s) == PlugBoard:
                    table.add_row("Plugboard","".join(ALPHABET))

                elif type(s) == Wheel:
                    rot = deque(ALPHABET)
                    # noinspection PyUnresolvedReferences
                    rot.rotate(s.total_rotation)
                    table.add_row(s.name, "".join(rot))

                else:
                    table.add_row(s.name, s)

                table.add_row("", " " * routing + symbol)

            table.add_row("Alphabet", "".join(ALPHABET))

        return table
