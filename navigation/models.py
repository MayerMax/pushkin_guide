from typing import Union, Optional, Tuple
from dataclasses import dataclass


@dataclass
class ImagePointCoordinates:
    x: int
    y: int

    def to_tuple(self) -> Tuple[int, int]:
        return self.x, self.y


@dataclass
class Hall:
    number: int
    title: str

    def __hash__(self):
        return hash(self.number) + hash(self.title) + hash(type(self))

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __str__(self):
        return f'Зал {self.number}. {self.title}'


@dataclass
class Place:
    museum: str
    floor: int
    area: Union[str, Hall]
    object: Optional[str]
    image_point_coordinates: ImagePointCoordinates

    def __hash__(self):
        return hash(self.museum) + hash(self.floor) + hash(self.area) + hash(self.object) + hash(type(self))

    def __eq__(self, other):
        return hash(self) == hash(other)
