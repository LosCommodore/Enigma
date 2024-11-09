from attrs import define, field
from attrs.setters import frozen

from enigmatic import ALPHABET


@define
class Wheel:
    rotation: int = field(converter=lambda x: x % len(ALPHABET))
    name = field(default="hallo", on_setattr=frozen)

w = Wheel(42)
print(w)
w.rotation+=100
print(w)
w.name = "blub"
print(w)