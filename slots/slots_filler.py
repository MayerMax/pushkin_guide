from dialogue_system.queries.abstract import AbstractQuery
from slots.recognizers.address_recognizer import AddressRecognizer
from slots.recognizers.artist_name_recognizer import ArtistFuzzyNameRecognizer
from slots.recognizers.museum_location import HallRecognizer


class SlotsFiller:
    def __init__(self):
        self._available_recognizers = [
            ArtistFuzzyNameRecognizer(use_natasha=True), # when deploy need to configure
            AddressRecognizer(),
            HallRecognizer()
        ]

    def enrich(self, query: AbstractQuery, previous_slots = None):
        extracted_slots = previous_slots if previous_slots else {}
        for recognizer in self._available_recognizers:
            if type(query) in recognizer.recognized_types:
                extracted_slots.update(recognizer.recognize(query))
        return extracted_slots
