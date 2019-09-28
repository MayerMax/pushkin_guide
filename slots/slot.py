from enum import Enum


class Slot(Enum):
    Name = 'name'  # фио
    NameProfession = 'profession'  # фотограф, скульптор, пейзажист....
    Address = 'address'
    SomeNameDetected = 'some_name'  # произвольное имя
