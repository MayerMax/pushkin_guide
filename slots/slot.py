from enum import Enum


class Slot(Enum):
    Name = 'name'  # фио
    NameProfession = 'profession'  # фотограф, скульптор, пейзажист....
    Address = 'address'
    SomeNameDetected = 'some_name'  # произвольное имя
    Materials = 'materials'
    Hall = 'hall'  # номер холла
    ArtName = 'art_name'  # название произведения искусства
    ArtType = 'art_type'  # скульптура, фотография, ...
