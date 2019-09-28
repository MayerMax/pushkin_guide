from typing import Union, Optional
from dataclasses import dataclass


@dataclass
class ImagePointCoordinates:
    x: int
    y: int


@dataclass
class Hall:
    number: int
    title: str


@dataclass
class Place:
    museum: str
    floor: int
    area: Union[str, Hall]
    object: Optional[str]
    image_point_coordinates: ImagePointCoordinates


@dataclass
class Movement:
    start_place: Place
    end_place: Place
