import abc
from typing import Iterable

import rich.console

ALPHABET: tuple[str, ...] = tuple(chr(ord('A') + i) for i in range(26))  # Alphabet of the engima machine(s)


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
