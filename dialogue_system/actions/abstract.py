import abc
from typing import Union
from collections import namedtuple

from dialogue_system.queries.abstract import AbstractQuery
from dialogue_system.queries.text_based import TextQuery
from dialogue_system.responses.abstarct import AbstractResponse
from dialogue_system.responses.text_based import SingleTextResponse, SingleTextWithFactAttachments

ActivationResponse = namedtuple('ActivationResponse', ['intent_detected', 'props'])
ActivationResponse.__new__.__defaults__ = (False, None)


class AbstractAction(metaclass=abc.ABCMeta):
    recognized_types = []  # возможно, дальше нужен будет enum

    def __init__(self, initial_query: object = None, props: dict = None):
        self._props = props
        self._initial_query = initial_query

    @abc.abstractclassmethod
    def activation_response(self, initial_query: object) -> ActivationResponse:  # TODO rename
        pass

    @abc.abstractmethod
    def reply(self, query: AbstractQuery = None) -> AbstractResponse:
        pass


class DummyHelloAction(AbstractAction):
    recognized_types = [TextQuery]

    @classmethod
    def activation_response(cls, initial_query: TextQuery) -> ActivationResponse:
        if initial_query.lower() in ['привет', 'здорово']:
            return ActivationResponse(intent_detected=True)
        # TODO

    def reply(self, query: TextQuery = None) -> SingleTextResponse:
        yield SingleTextResponse(is_finished=True, is_successful=True, text='Привет! Хорошего дня!')


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
    def activation_response(cls, initial_query: TextQuery) -> ActivationResponse:
        if initial_query.lower() in ['кто такой пушкин', 'расскажи про пушкина']:
            return ActivationResponse(intent_detected=True)

    def reply(self, query: TextQuery = None) -> Union[SingleTextWithFactAttachments, SingleTextResponse]:
        query = yield SingleTextWithFactAttachments(is_finished=False, is_successful=True,
                                                    text='Александ Сергеевич Пушкин - великий русский писатель',
                                                    attachments=list(self._qa.keys()))

        if query in self._qa:
            yield SingleTextResponse(is_finished=True, is_successful=True, text=self._qa[query])
        else:
            yield SingleTextResponse(is_finished=False, is_successful=False)
