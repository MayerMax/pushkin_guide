import typing

from slots.slot import Slot
from dialogue_system.queries.text_based import TextQuery
from slots.recognizers.abstract import AbstractSlotRecognizer
from navigation.data.main_floor_1 import HALLS
from dialogue_system.matchers.similarity import tokenize, normalize


class HallRecognizer(AbstractSlotRecognizer):
    recognized_types = [TextQuery]

    def recognize(self, query: TextQuery) -> typing.Dict[Slot, str]:
        slots = {}
        query = ' '.join(normalize(token) for token in tokenize(query))
        for hall in HALLS:
            if ' '.join(normalize(token) for token in tokenize(hall.area.title)) in query:
                slots[Slot.HallName] = hall.area.title
        return slots
