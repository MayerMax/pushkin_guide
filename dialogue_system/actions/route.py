from typing import Dict

from dialogue_system.actions.abstract import AbstractAction, ActivationResponse
from dialogue_system.queries.text_based import TextQuery
from dialogue_system.responses.text_based import SingleTextResponse
from slots.slot import Slot


class RouteAction(AbstractAction):
    recognized_types = [TextQuery]
    triggering_phrases = ['как доехать', 'как проехать', 'маршрут до', 'способ проехать', 'способ доехать']

    @classmethod
    def activation_response(cls, initial_query: TextQuery, slots: Dict[Slot, str]) -> ActivationResponse:
        for phrase in RouteAction.triggering_phrases:
            if phrase in initial_query:
                return ActivationResponse(intent_detected=True)

    @classmethod
    def _get_routes(cls, from_address):
        return '''Для вас найдено несколько вариантов маршрута до музея:
    за 18 минут на метро: от станции "Охотный ряд" до станции "Кропоткинская, далее 350м пешком
    за 30 минут на автобусе номер 255: от остановки "Зарядье" до остановки "Большой Каменный мост, далее 470м пешком.
Ждем вас в гости!'''

    @classmethod
    def reply(cls, slots: Dict[Slot, str]):
        address = slots[Slot.Address]
        if not address:
            query = yield SingleTextResponse(is_finished=False,
                                             is_successful=True,
                                             text='Пожалуйста, уточните место отправления.')
            yield SingleTextResponse(is_finished=True,
                                     is_successful=True,
                                     text=cls._get_routes(query))
