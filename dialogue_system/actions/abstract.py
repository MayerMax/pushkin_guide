import abc
from typing import Union, Dict
from collections import namedtuple

from dialogue_system.queries.text_based import TextQuery
from dialogue_system.responses.abstract import AbstractResponse, ActivationResponse
from dialogue_system.responses.text_based import SingleTextResponse, SingleTextWithFactAttachments
from slots.slot import Slot



class AbstractAction(metaclass=abc.ABCMeta):
    recognized_types = []  # возможно, дальше нужен будет enum

    def __init__(self, user_id, initial_query: object = None, props: dict = None, slots: Dict[Slot, str] = None):
        self._user_id = user_id
        self._props = props
        self._initial_slots = slots
        self._initial_query = initial_query

    @abc.abstractclassmethod
    def activation_response(cls, initial_query: object, slots: Dict[Slot, str]) -> ActivationResponse:  # TODO rename
        pass

    @abc.abstractmethod
    def reply(self, slots: Dict[Slot, str], user_id=None) -> AbstractResponse:
        pass


class DummyHelloAction(AbstractAction):
    recognized_types = [TextQuery]

    @classmethod
    def activation_response(cls, initial_query: TextQuery, slots: Dict[Slot, str]) -> ActivationResponse:
        if initial_query.lower() in ['привет', 'здорово', 'здравствуйте', 'хай']:
            return ActivationResponse(intent_detected=True)
        # TODO

    def reply(self, slots: Dict[Slot, str], user_id=None) -> SingleTextResponse:
        yield SingleTextResponse(is_finished=True, is_successful=True, text='Привет! Я виртуальный '
                                                                            'помощник Наталья по Пушкинскому музею и готова Вам помочь в любой момент!')


class DummyYouKnowWhoIsPushkin(AbstractAction):
    recognized_types = [TextQuery]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._qa = {
            'самое известное произведение Пушкина?': 'Многие считают, что это Евгений Онегин, но Капитанская дочка не '
                                                     'менее популярна',
            'как звали жену Пушкина?': 'Наталья Николаевна Гончарова.'
        }

    @classmethod
    def activation_response(cls, initial_query: TextQuery, slots: Dict[Slot, str]) -> ActivationResponse:
        if initial_query.lower() in ['кто такой пушкин', 'расскажи про пушкина']:
            return ActivationResponse(intent_detected=True)

    def reply(self, slots: Dict[Slot, str], user_id=None) -> Union[SingleTextWithFactAttachments, SingleTextResponse]:
        query, _ = yield SingleTextWithFactAttachments(is_finished=False, is_successful=True,
                                                    text='Александ Сергеевич Пушкин - великий русский писатель',
                                                    attachments=list(self._qa.keys()))

        if query in self._qa:
            yield SingleTextResponse(is_finished=True, is_successful=True, text=self._qa[query])
        else:
            yield SingleTextResponse(is_finished=False, is_successful=False)
