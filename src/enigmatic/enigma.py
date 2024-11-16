from __future__ import annotations

import numpy as np
from typing import Union, Callable, Iterable
from collections import deque

from enigmatic import ALPHABET, _letters_to_numbers, _num2letter
from enigmatic.plugboard import PlugBoard
from enigmatic.rotor import RotorSpec, Rotor, WHEEL_SPECS
from attrs import define, field


@define
class Enigma:
    plug_board: PlugBoard
    _rotors: list[Rotor] = field()
    """ List of rotors, slow rotor first """

    memory: deque[list[str]] = field(factory=deque)

    @classmethod
    def assemble(
        cls,
        rotor_specs: list[str | RotorSpec] = "",
        max_memory: int = 100,
        plugs: str = "",
        rotor_positions: str = "",
        ring_positions=(),
    ) -> Enigma:
        """Assemlbes a new enigma machine

        :param rotor_specs: list of wheel specs, slow rotor first.
        :param max_memory:
        :param plugs:
        :param rotor_positions:
        :param ring_positions:
        :return:
        """

        rotors = [Rotor(spec if isinstance(spec, RotorSpec) else WHEEL_SPECS[spec.upper()]) for spec in rotor_specs]

        enigma = Enigma(
            plug_board=PlugBoard(plugs),
            rotors=rotors,
            memory=deque([], maxlen=max_memory),
        )

        if rotor_positions:
            enigma.rotor_positions = rotor_positions

        if ring_positions:
            enigma.ring_positions = ring_positions

        return enigma

    # noinspection PyUnresolvedReferences
    @_rotors.validator
    def _check_rotors(self, _, rotors):
        if rotors[0].spec.is_dynamic:
            raise ValueError("Die first wheel has to be a stator for an enigma machine")

        idx_is_rotor = np.where(np.array([x.spec.is_dynamic for x in rotors]))
        rotors_in_block = np.all(np.diff(idx_is_rotor) == 1)

        if not rotors_in_block:
            raise ValueError("No stators are allowed in between rotors")

    @property
    def rotors(self) -> list[Rotor]:
        """All wheels, slow rotor first"""
        return self._rotors.copy()

    @property
    def dynamic_rotors(self) -> list[Rotor]:
        """All rotors which are actually rotating, slow rotor first"""
        return [x for x in self.rotors if x.spec.is_dynamic]

    @property
    def rotor_positions(self):
        """All wheel_rotations, slow rotor first"""

        rots = [_num2letter(x.position) for x in self.rotors]
        return "".join(rots)

    @rotor_positions.setter
    def rotor_positions(self, rotations: str):
        """Set the rotations for all rotors.
        Use "*" to skip a rotor"""

        if len(rotations) != len(self.rotors):
            raise ValueError("Wrong number of roations!")

        for whl, rot in zip(self.rotors, rotations):
            if rot != "*":
                whl.position = _letters_to_numbers(rot)[0]

    @property
    def ring_positions(self) -> list[int]:
        return [x.ring_setting for x in self.rotors]

    @ring_positions.setter
    def ring_positions(self, pos: Union[list[int], str]):
        if len(pos) != len(self.rotors):
            raise ValueError("Wrong number of ring_positions")

        for whl, rot in zip(self.rotors, pos):
            if rot != "*":
                whl.ring_setting = rot

    def _route_scramblers(self) -> Iterable[Callable]:
        yield self.plug_board.route

        for wheel in reversed(self.rotors):
            yield wheel.route

        for wheel in self.rotors[1:]:
            yield wheel.route_backward

        yield self.plug_board.route_backward

    def _press_key(self, key: str) -> str:
        if key not in ALPHABET:
            raise ValueError(f'Invalid letter: "{key}"')

        # Whenever a key is pressed, the toros move before a lamp is turned on.
        self._rotate()

        current_key = _letters_to_numbers(key)[0]
        routing = [current_key]
        for route in self._route_scramblers():
            # noinspection PyArgumentList
            current_key = route(current_key)
            routing.append(current_key)

        self.memory.append([_num2letter(x) for x in routing])

        return _num2letter(routing[-1])

    def _rotate(self):
        rotors = list(reversed(self.dynamic_rotors))
        do_rotate = {0}  # first Rotor always rotates

        for i, (r1, r2) in enumerate(zip(rotors, rotors[1:])):
            if r1.does_step():
                do_rotate.add(i)
                do_rotate.add(i + 1)

        for i in do_rotate:
            rotors[i].position += 1

    def write(self, text: str) -> str:
        input_text = text.upper().replace(" ", "").replace("\n", "")

        output_text = [self._press_key(key) for key in input_text]

        return "".join(output_text)

    def __str__(self):
        my_str = f"Enigma -> Pos: {self.rotor_positions}, Wheels: {[x.spec.name for x in self.rotors]} Ring: {self.ring_positions}, Plugboard: {self.plug_board.cables}"

        return my_str
