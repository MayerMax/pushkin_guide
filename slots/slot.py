from enum import Enum


class Slot(Enum):
    Name = 'name'  # фио
    NameProfession = 'profession'  # фотограф, скульптор, пейзажист....
    Address = 'address'
    SomeNameDetected = 'some_name'  # произвольное имя
    Material = 'material'
    Hall = 'hall'  # номер холла
    ArtName = 'art_name'  # название произведения искусства
    ArtType = 'type'  # скульптура, фотография, ...
    Image = 'img'
    Country = 'country'
    EventName = 'event_name'
