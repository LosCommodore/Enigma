import abc
from typing import Iterable
import rich.console
from attrs import define

# Global alphabet used by this package:
ALPHABET: tuple[str, ...] = tuple(chr(ord("A") + i) for i in range(26))
ALPHABET_SET: set[str] = set(ALPHABET)


def _letters_to_numbers(letters: Iterable[str]) -> list[int]:
    """Convert letters to numbers

    >>> _letters_to_numbers("AB")
    [0, 1]
    """
    return [ALPHABET.index(k) for k in letters]


def _num2letter(num: int):
    return ALPHABET[num]


@define(kw_only=True)
class Scrambler(abc.ABC):
    """A Scramber is any part which takes part in the encryption of the signal. For an Enigma machine these are the
    Rotors and the Plugboard"""

    name: str = ""

    @abc.abstractmethod
    def route(self, letter: int) -> int:
        """Forward routing of a letter through the Scrambler"""

    @abc.abstractmethod
    def route_backward(self, letter: int) -> int:
        """Backwards routing of a letter through the Scrambler"""

    # noinspection PyUnusedLocal
    def __rich_console__(
        self, console: rich.console.Console, options: rich.console.ConsoleOptions
    ) -> rich.console.RenderResult:
        yield self.__str__()
