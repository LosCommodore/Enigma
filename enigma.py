import abc
import numpy as np

from rich.console import Console
from rich.table import Table
from rich.console import Group
from rich.panel import Panel

alphabet = tuple(chr(ord('a') + i) for i in range(26))


def letter2num(key: str):
    return alphabet.index(key)


def num2letter(num: int):
    return alphabet[num]


class Scrambler:
    def __init__(self, name: str):
        self.name = name

    @abc.abstractmethod
    def route(self, character: int) -> int:
        """ relatives Routing vom character """
        return int(0)

    @abc.abstractmethod
    def inv_route(self, character) -> int:
        """ inverses relatives Routing vom character """
        return int(0)


class Rotor(Scrambler):

    def __init__(self, name: str, wiring: str, notches=tuple(), isStatic=False):
        super().__init__(name)

        # Define Properties:
        self.notches: tuple[int] = tuple(letter2num(x) for x in notches)
        self.ringPos: int = 0
        self.isStatic: boolean = isStatic
        self.__rotation: int = 0

        # Check if wiring is valid: is alphabet and unique items
        assert tuple(sorted(wiring)) == alphabet, 'Rotor falsch initialisiert, falsches Alphabet !'
        # //TODO: char is not allowed to map on itself ?

        # save wiring as Dict
        self._wiring = {k: v for k, v in zip(alphabet, wiring)}

        # Mapping - abs - rel - invRev
        absMapping = [letter2num(key) for key in wiring]
        self.relMapping = tuple(key - i for i, key in enumerate(absMapping))
        self.invRelMapping = tuple(key - i for i, key in enumerate(np.argsort(absMapping)))

    def route(self, character: int) -> int:
        rot = self.ringPos + self.rotation
        return (character + self.relMapping[(character + rot) % len(alphabet)]) % len(alphabet)

    def inv_route(self, character: int) -> int:
        rot = self.ringPos + self.rotation
        return (character + self.invRelMapping[(character + rot) % len(alphabet)]) % len(alphabet)

    def doesStep(self):
        return any([self.rotation == n for n in self.notches])

    def __repr__(self):
        myStr = [f"Name of Rotor: {self.name}",
                 f"Wiring: {self._wiring}",
                 f"RingPosition: {self.ringPos}",
                 f"Rotation: {self.rotation}",
                 f"Notches: {self.notches}"]

        return "\n".join(myStr)

    def __rich__(self):
        table = Table(padding=(0, 0))
        for letter in alphabet:
            table.add_column(letter.upper(), justify='center')

        highlight = "[red bold]{}[/red bold]"
        table.columns[self.rotation].header = highlight.format(table.columns[self.rotation].header)

        row = [f"{m:+03}" for m in self.relMapping]
        row[self.rotation] = highlight.format(row[self.rotation])
        table.add_row(*row)

        properties = (f"Name of Rotor: {self.name}\n"
                      f"RingPosition: {self.ringPos}\n"
                      f"Rotation: {self.rotation}\n"
                      f"Notches: {self.notches}")

        group = Group(Panel(properties, expand=False), table)
        return Panel(group, title=f"[red]Rotor: {self.name}", expand=False)

    @property
    def rotation(self):
        return self.__rotation

    @rotation.setter
    def rotation(self, value):
        self.__rotation = value % len(alphabet)


class PlugBoard(Scrambler):
    def __init__(self, name):
        super().__init__(name)

        self._mapping = [letter2num(letter) for letter in alphabet]
        # properties
        self.__cables = []  # List of Tuples, e.g: cables = [('a','b'), ('u','v'), ('r','x'), ('t','w')]

    @property
    def cables(self) -> list[(str,str)]:
        return self.__cables

    @cables.setter
    def cables(self, cables: list[(str, str)]):
        characters = [char for cable in cables for char in cable]
        assert len(characters) == len(set(characters)), 'Error in Plubboard! Characters are not unique'

        self.__cables = cables

        plug_mapping = list(alphabet)
        for i,o in cables:
            plug_mapping[alphabet.index(i)] = o
            plug_mapping[alphabet.index(o)] = i

        self._mapping = [letter2num(x) for x in plug_mapping]

    def route(self, character: int) -> int:
        return self._mapping[character]

    def inv_route(self, character):
        return self._mapping[character]  # symmetrisches Mapping beim Plugboard: aus "c -> a" folgt "a -> c"

    def __repr__(self):
        myStr = [f"Name of Pulgboard: {self.name}",
                 f"Cables: {self.cables}"]

        return "\n".join(myStr)


class Enigma:

    def __init__(self):
        self.scramblers: list[Scrambler] = []
        pass

    def pressKey(self, key):
        if isinstance(key, int):
            key = str(key)

        assert key in alphabet, 'ungültiger Schlüssel!'
        key = letter2num(key)

        # rotate
        self.rotate()

        # calc Wiring

        routing = []  # --> names
        char = [key]  # --> [0, 1, 10, 11, 21, 22, 17, 6, 5, 5]
        for scram in self.scramblers:
            routing.append(scram.name)
            char.append(scram.route(char[-1]))

        for scram in self.scramblers[::-1][1:]:  # reverse + exclude last element (ukw)
            routing.append(scram.name)
            char.append(scram.inv_route(char[-1]))

        return char, routing

    def rotate(self):
        rotors = [x for x in self.scramblers if isinstance(x, Rotor) and not x.isStatic]

        doRotate = [False] * len(rotors)
        doRotate[0] = True  # first Rotor always rotates
        for i, step in enumerate([s.doesStep() for s in rotors]):
            if step:
                doRotate[i] = True
                doRotate[i + 1] = True

        for rotor, step in zip(rotors, doRotate):
            rotor.rotation += step

    @property
    def position(self):
        pos = [num2letter(x.rotation) for x in self.scramblers if isinstance(x, Rotor) and not x.isStatic]
        return pos

    def __repr__(self):
        myStr = [f"Enigma, Pos: {self.position}"]

        return "\n".join(myStr)
