import numpy as np
from dataclasses import dataclass
from rich.table import Table
from rich.console import Group
from rich.panel import Panel
from typing import Iterable

ALPHABET = tuple(chr(ord('a') + i) for i in range(26))


def _letters2num(letters: Iterable[str]) -> int | list[int]:
    num = [ALPHABET.index(k) for k in letters]
    if len(num) == 1:
        num = num[0]

    return num


def _num2letter(num: int):
    return ALPHABET[num]


@dataclass(frozen=True)
class RotorSpec:
    name: str
    wiring: str
    notches: tuple[str]
    is_static: bool

    def __post_init__(self):
        if sorted(self.wiring) != sorted(ALPHABET):
            raise ValueError(r'Ungültige Rotorspezifikation, falsches Alphabet !')


class Rotor:
    def __init__(self, spec: RotorSpec):
        self.spec = spec
        self.rotation: int = 0
        self.ring_position: int = 0

        self._wiring = {k: v for k, v in zip(ALPHABET, self.spec.wiring)}

        mapping = _letters2num(self.spec.wiring)
        self._mapping_rel = tuple(m - i for i, m in enumerate(mapping))
        self._mapping_rel_inv = tuple(m - i for i, m in enumerate(np.argsort(mapping)))

    @property
    def rotation(self):
        return self.__rotation

    @rotation.setter
    def rotation(self, value):
        self.__rotation = value % len(ALPHABET)

    def route(self, character: int) -> int:
        rot = self.ring_position + self.rotation
        return (character + self._mapping_rel[(character + rot) % len(ALPHABET)]) % len(ALPHABET)

    def inv_route(self, character: int) -> int:
        rot = self.ring_position + self.rotation
        return (character + self._mapping_rel_inv[(character + rot) % len(ALPHABET)]) % len(ALPHABET)

    def doesStep(self):
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
        for letter in ALPHABET:
            table.add_column(letter.upper(), justify='center')

        highlight = "[red bold]{}[/red bold]"
        table.columns[self.rotation].header = highlight.format(table.columns[self.rotation].header)

        row = [f"{m:+03}" for m in self._mapping_rel]
        row[self.rotation] = highlight.format(row[self.rotation])
        table.add_row(*row)

        properties = (f"Name of Rotor: {self.spec.name}\n"
                      f"RingPosition: {self.ring_position}\n"
                      f"Rotation: {self.rotation}\n"
                      f"Notches: {self.spec.notches}")

        group = Group(Panel(properties, expand=False), table)
        return Panel(group, title=f"[red]Rotor: {self.spec.name}", expand=False)


class PlugBoard:
    def __init__(self, cables: tuple[str]):
        self.cables = cables

    @property
    def cables(self) -> tuple[str]:
        return self._cables

    @cables.setter
    def cables(self, cables: tuple[str]):
        self._cables = tuple(cables)
        self._mapping = list(range(1, len(ALPHABET)))

        for cable in self._cables:
            i, o = _letters2num(cable)
            self._mapping[i] = o
            self._mapping[o] = i

    def route(self, letter: int) -> int:
        return self._mapping[letter]

    def inv_route(self, character):
        return self._mapping[character]  # symmetrisches Mapping beim Plugboard: aus "c -> a" folgt "a -> c"

    def __repr__(self):
        my_str = [f"Cables: {self.cables}"]
        return "\n".join(my_str)


Scrambler: Rotor | PlugBoard


class Enigma:
    def __init__(self):
        self.scramblers: list[Scrambler] = []
        pass

    def pressKey(self, key):
        if isinstance(key, int):
            key = str(key)

        assert key in ALPHABET, 'ungültiger Schlüssel!'
        key = _letters2num(key)

        # rotate
        self.rotate()

        # calc Wiring

        routing = []  # --> names
        char = [key]  # --> [0, 1, 10, 11, 21, 22, 17, 6, 5, 5]
        for scram in self.scramblers:
            routing.append(scram.__name)
            char.append(scram.route(char[-1]))

        for scram in self.scramblers[::-1][1:]:  # reverse + exclude last element (ukw)
            routing.append(scram.__name)
            char.append(scram.inv_route(char[-1]))

        return char, routing

    def rotate(self):
        rotors = [x for x in self.scramblers if isinstance(x, Rotor) and not x.spec.is_static]

        do_rotate = [False] * len(rotors)
        do_rotate[0] = True  # first Rotor always rotates
        for i, step in enumerate([s.doesStep() for s in rotors]):
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