from typing import Dict

from dialogue_system.actions.abstract import AbstractAction
from dialogue_system.queries.image import ImageQuery
from dialogue_system.queries.text_based import TextQuery
from dialogue_system.responses.abstract import ActivationResponse
from dialogue_system.responses.text_based import SingleTextResponse
from slots.slot import Slot


class DefaultAnswerAction(AbstractAction):
    recognized_types = [TextQuery, ImageQuery]

    @classmethod
    def activation_response(cls, initial_query: TextQuery, slots: Dict[Slot, str]) -> ActivationResponse:
        return ActivationResponse(intent_detected=True)

    def reply(self, slots: Dict[Slot, str], user_id=None) -> SingleTextResponse:
        yield SingleTextResponse(is_finished=True, is_successful=True, text='Авторы не научили меня отвечать '
                                                                            'на такие вопросы, но я исправлюсь!')