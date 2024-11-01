from typing import Union

from enigmatic import Scrambler, ALPHABET, _letters2num


class PlugBoard(Scrambler):
    def __init__(self, cables: Union[tuple[str, ...], str]):
        super().__init__("Plugboard")
        self.cables = cables

    @property
    def cables(self) -> tuple[str, ...]:
        return self._cables

    @cables.setter
    def cables(self, cables: Union[tuple[str, ...], str]):
        if type(cables) == str:
            cables = cables.upper().split(" ") if cables else ()
        else:
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
