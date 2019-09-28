import abc
import typing

from dialogue_system.queries.abstract import AbstractQuery
from slots.slot import Slot


class AbstractSlotRecognizer(metaclass=abc.ABCMeta):
    recognized_types = []

    @abc.abstractmethod
    def recognize(self, query: AbstractQuery) -> typing.Dict[Slot, str]:
        pass