from rich.console import Console

import enigmatic
from enigmatic.plugboard import PlugBoard


def test_symmetry(cables=('BZ', 'FG')):
    p = PlugBoard(cables)
    print("")
    print(p)
    print(list(p._mapping))
    print("")

    for letter in range(len(enigmatic.ALPHABET)):
        r1 = p.route(letter)
        r2 = p.route_backward(r1)
        print(f"{letter} -> {r1} -> {r2}")
        assert letter == r2


def test_beep_trough_cables( cables = ('BZ', 'FG')):
    p = PlugBoard(cables)

    for cable in cables:
        i, o = enigmatic._letters_to_numbers(cable)
        assert p.route(i) == o
        assert p.route(o) == i
