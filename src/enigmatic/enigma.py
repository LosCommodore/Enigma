from __future__ import annotations

import numpy as np
import rich.console
from rich.table import Table
from typing import Union
from collections import deque

from enigmatic import ALPHABET, _letters_to_numbers, _num2letter, Scrambler
from enigmatic.plugboard import PlugBoard
from enigmatic.wheel import WheelSpec, Wheel, WHEEL_SPECS
import msgspec
from msgspec import field


class Enigma(msgspec.Struct):
    _wheels: list[Wheel]
    plugboard: PlugBoard = field(default_factory=lambda: PlugBoard(""))
    _memory: deque[list[str]] = field(default_factory=deque)

    @classmethod
    def assemble(
            cls,
            wheel_specs: list[str | WheelSpec] = "",
            max_memory: int = 100,
            plugs: str = "",
            wheel_positions: str = "",
            ring_positions=()
    ) -> Enigma:

        wheels = []
        for spec in wheel_specs:
            if isinstance(spec, WheelSpec):
                wheels.append(Wheel(spec))
            elif isinstance(spec, str):
                wheels.append(Wheel(WHEEL_SPECS[spec]))

        if wheels[0].spec.is_rotor:
            raise ValueError("Die first wheel has to be a stator for an enigma machine")

        idx_is_rotor = np.where(np.array([x.spec.is_rotor for x in wheels]))
        rotors_in_block = np.all(np.diff(idx_is_rotor) == 1)

        if not rotors_in_block:
            raise ValueError("No stators are allowed in between rotors")

        enigma = Enigma(
            _wheels=wheels,
            plugboard=PlugBoard(plugs),
            _memory=deque([], maxlen=max_memory),
        )
        if wheel_positions:
            enigma.wheel_positions = wheel_positions

        if ring_positions:
            enigma.ring_positions = ring_positions

        return enigma

    @property
    def memory(self):
        return self._memory

    @property
    def wheels(self) -> list[Wheel]:
        """ All wheels, slow rotor first """
        return self._wheels.copy()

    @property
    def rotors(self) -> list[Wheel]:
        """ All rotors, slow rotor first """
        return [x for x in self.wheels if x.spec.is_rotor]

    @property
    def wheel_positions(self):
        """ All wheel_rotations, slow rotor first """

        rots = [_num2letter(x.rotation) for x in self.wheels]
        return "".join(rots)

    @wheel_positions.setter
    def wheel_positions(self, rotations: str):
        """ Set the rotations for all wheels.
        Use "*" to skip a wheel """

        if len(rotations) != len(self.wheels):
            raise ValueError("Wrong number of roations!")

        for whl, rot in zip(self.wheels, rotations):
            if rot != "*":
                whl.rotation = _letters_to_numbers(rot)[0]

    @property
    def ring_positions(self) -> list[int]:
        return [x.ring_position for x in self.wheels]

    @ring_positions.setter
    def ring_positions(self, pos: Union[list[int], str]):

        if len(pos) != len(self.wheels):
            raise ValueError("Wrong number of ring_positions")

        for whl, rot in zip(self.wheels, pos):
            whl.ring_position = rot

    def _route_scramblers(self) -> Union[Scrambler.route, Scrambler.route_backward]:
        yield self.plugboard.route

        for wheel in reversed(self.wheels):
            yield wheel.route

        for wheel in self.wheels[1:]:
            yield wheel.route_backward

        yield self.plugboard.route_backward

    def _press_key(self, key: str) -> str:
        if key not in ALPHABET:
            raise ValueError(f'Invalid letter: "{key}"')

        # Whenever a key is pressed, the wheels move before a lamp is turned on.
        self.rotate()

        n_key = _letters_to_numbers(key)[0]
        current_key = n_key
        routing = [current_key]
        for route in self._route_scramblers():
            # noinspection PyArgumentList
            current_key = route(current_key)
            routing.append(current_key)

        self.memory.append([_num2letter(x) for x in routing])

        return _num2letter(routing[-1])

    def rotate(self):
        rotors = list(reversed(self.rotors))

        do_rotate = {rotors[0]}  # first Rotor always rotates

        for r1, r2 in zip(rotors, rotors[1:]):
            if r1.does_step():
                do_rotate.add(r1)
                do_rotate.add(r2)

        for rotor in do_rotate:
            rotor.rotation += 1

    def write(self, text: str) -> str:
        input_text = text.upper().replace(' ', '').replace('\n', '')

        output_text = [self._press_key(key) for key in input_text]

        return "".join(output_text)

    def __repr__(self):
        params = dict(wheel_specs=[w.spec.name for w in self.wheels],
                      plugs=self.plugboard.cables,
                      wheel_positions=self.wheel_positions,
                      ring_positions=self.ring_positions,
                      )

        return f"Enigma(**{repr(params)})"

    def __str__(self):
        my_str = f"Enigma -> Pos: {self.wheel_positions}, Wheels: {[x.spec.name for x in self.wheels]} Ring: {self.ring_positions}, Plugboard: {self.plugboard.cables}"

        return my_str

    def print_full(self) -> rich.console.RenderResult:

        if not self.memory:
            table = Table()
            table.add_column('Component')
            table.add_column('Routing')
            for s in self.wheels:
                table.add_row(s.name, s)

            yield table
        else:
            table = Table()
            table.add_column('Component')
            table.add_column('State')

            for s in self.wheels:
                table.add_row(s.name, s)

            yield table

            table = Table()
            table.add_column('Component')
            table.add_column('Routing')

            m = self.memory[-1]
            input_nr = _letters_to_numbers(m[0])[0]
            table.add_row("Alphabet", "".join(ALPHABET))
            table.add_row("", " " * input_nr + "[green]↓")

            scr = self.wheels.copy()

            scr += reversed(self.wheels[:-1])
            symbol = "[green]↓"

            for s, routing, in zip(scr, _letters_to_numbers(m[1:])):
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
