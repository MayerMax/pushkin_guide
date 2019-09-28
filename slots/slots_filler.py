from dialogue_system.queries.abstract import AbstractQuery
from slots.recognizers.fuzzy_text_recognizer import FuzzyTextRecognizer
from slots.recognizers.address_recognizer import AddressRecognizer
from slots.recognizers.artist_name_recognizer import ArtistFuzzyNameRecognizer
from slots.slot import Slot


class SlotsFiller:
    def __init__(self):
        self._available_recognizers = [
            ArtistFuzzyNameRecognizer(use_natasha=True), # when deploy need to configure
            AddressRecognizer(),
            FuzzyTextRecognizer(search_slot=Slot.ArtName,
                                additional_slots_to_get=[Slot.ArtType, Slot.Hall, Slot.Image, Slot.Material],
                                min_threshold=7),
            FuzzyTextRecognizer(search_slot=Slot.Material, min_threshold=4.20),
        ]

    def enrich(self, query: AbstractQuery, previous_slots = None):
        extracted_slots = previous_slots if previous_slots else {}
        for recognizer in self._available_recognizers:
            if type(query) in recognizer.recognized_types:
                extracted_slots.update(recognizer.recognize(query))

        return extracted_slots
