""" Plugboard
https://en.wikipedia.org/wiki/Enigma_machine#Plugboard
https://www.cryptomuseum.com/crypto/enigma/i/sb.htm

A cable placed onto the plugboard connected letters in pairs; for example, E and Q might be a steckered pair.
The effect was to swap those letters before and after the main rotor scrambling unit.
For example, when an operator pressed E, the signal was diverted to Q before entering the rotors.
Up to 13 steckered pairs might be used at one time, although only 10 were normally used.
"""

from collections import Counter
from typing import Iterable
from enigmatic import Scrambler, ALPHABET, _letters_to_numbers


class PlugBoard(Scrambler):
    """ PlugBoard (Mark 3)

    Create Plugboard
    >>> pb = PlugBoard("AB CD HP")
    """

    _cables: set[str]  # e.g. {"AB", "FK"}
    _mapping: bytearray

    def __init__(self, cables: Iterable[str] | str = ""):
        super().__init__(name="PlugBoard")
        self._mapping = bytearray(len(ALPHABET))
        self._cables = set()
        self.add_cables(cables)

    def route(self, letter: int) -> int:
        return self._mapping[letter]

    def route_backward(self, letter):
        return self._mapping[letter]

    @property
    def cables(self) -> tuple[str, ...]:
        return tuple(self._cables)

    def add_cables(self, cables: Iterable[str] | str):
        cables = _validate_cables(cables)

        # Add set of existing Cables
        cables |= self._cables

        # Check no letter is reoccuring
        counter = Counter("".join(cables))
        reoccuring_letters = set(letter for letter, count in counter.items() if count > 1)
        if reoccuring_letters:
            raise ValueError(
                f'Letters must not be used multiple times. All cables: {cables}. Error caused by letters: {reoccuring_letters}')

        self._use_cables(cables)

    def remove_cables(self, cables: Iterable[str] | str = ""):
        if not cables:
            new_cables = set()
        else:
            cables = _validate_cables(cables)
            new_cables = self._cables - cables

        self._use_cables(new_cables)

    def _use_cables(self, cables: set[str]):
        self._cables = cables
        self._mapping = bytearray(len(ALPHABET))
        for cable in self._cables:
            i, o = _letters_to_numbers(cable)
            self._mapping[i] = o
            self._mapping[o] = i

    def __repr__(self):
        return f"{self.__class__.__name__}({self.cables})"


def _validate_cables(cables: Iterable[str] | str) -> set[str]:
    """ Validate new cables from user

    :return uppercase set of cables, e.g. {"GH", "FA"}
    """
    if isinstance(cables, str):
        cables = cables.split()
    cables = set(cable.upper() for cable in cables)

    # Check for invalid letters
    letters = "".join(cables)
    if invalid_letters := set(letters) - set(ALPHABET):
        raise ValueError(f'Invalid letters used for cable: {invalid_letters}')

    # Check cables are pairs of letters
    if invalid_cables := set(cable for cable in cables if len(cable) != 2):
        raise ValueError(f'Cables must be pairs of letters. Invalid cables: {invalid_cables}')

    return cables


if __name__ == "__main__":
    import doctest
    doctest.testmod()

    """ Demo usage: """
    p = PlugBoard("AB CD HP")
    p.add_cables("KT")
    p.remove_cables("AB")
    print(p)
    print(p.route(2))