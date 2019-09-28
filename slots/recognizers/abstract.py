import abc

import typing

from dialogue_system.queries.abstract import AbstractQuery
from slots.recognizers.slots import Slots


class AbstractSlotRecognizer(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def recognize(self, query: AbstractQuery) -> typing.Dict[Slots, str]:
        pass