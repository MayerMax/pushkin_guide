from typing import Dict

from dialogue_system.actions.abstract import AbstractAction, ActivationResponse
from dialogue_system.queries.text_based import TextQuery
from dialogue_system.responses.text_based import SingleTextResponse
from slots.slot import Slot


class AboutArtistAction(AbstractAction):
    recognized_types = [TextQuery]
    triggering_phrases = ['расскажи', 'хочу послушать о', 'есть ли в музее картина', 'что ты знаешь о',
                          'хочу узнать про']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @classmethod
    def activation_response(cls, initial_query: TextQuery, slots: Dict[Slot, str]) -> ActivationResponse:
        if Slot.Name not in slots:
            return None

        for phrase in AboutArtistAction.triggering_phrases:
            if phrase in initial_query.text:
                return ActivationResponse(intent_detected=True)

    def reply(self, slots: Dict[Slot, str]) -> SingleTextResponse:

        name, profession = self._initial_slots[Slot.Name], self._initial_slots[Slot.NameProfession]

        yield SingleTextResponse(is_finished=True, is_successful=True, text=f'{name}, {profession}')
