import typing

from slots.slot import Slot
from dialogue_system.queries.text_based import TextQuery
from slots.recognizers.abstract import AbstractSlotRecognizer


class AddressRecognizer(AbstractSlotRecognizer):
    recognized_types = [TextQuery]

    def recognize(self, query: TextQuery) -> typing.Dict[Slot, str]:
        return {}
