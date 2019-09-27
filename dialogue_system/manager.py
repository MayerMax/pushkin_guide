from typing import Optional
from collections import namedtuple
from dialogue_system.actions.abstract import DummyYouKnowWhoIsPushkin, DummyHelloAction, AbstractAction
from dialogue_system.queries.abstract import AbstractQuery
from dialogue_system.queries.text_based import TextQuery
from dialogue_system.responses.abstarct import AbstractResponse

DynamicResponse = namedtuple('DynamicResponse', ['action', 'replier'])


class ActiveUsersManager:
    max_retry_counts = {
        DummyHelloAction: 0,
        DummyYouKnowWhoIsPushkin: 0
    }

    def __init__(self):
        self._user_action_dict = {}
        self._num_negative_counts_to_call = {}

    def add(self, user: int, action: AbstractAction) -> AbstractResponse:
        dr = DynamicResponse(action, action.reply())
        response: AbstractResponse = next(dr.replier)
        if not response.is_finished:
            self._user_action_dict[user] = dr
            self._num_negative_counts_to_call[user] = 0
        return response

    def get_response(self, user: int, query: AbstractQuery) -> Optional[AbstractResponse]:
        response: AbstractResponse = self._user_action_dict[user].replier.send(query)
        if response.is_finished:
            self.remove(user)
            return response

        if not response.is_successful:
            self._num_negative_counts_to_call[user] += 1

        if self._num_negative_counts_to_call[user] > self.max_retry_counts[type(self._user_action_dict[user].action)]:
            self.remove(user)
            return None

        return response

    def remove(self, user):
        if user in self._user_action_dict:
            self._user_action_dict.pop(user)
            self._num_negative_counts_to_call.pop(user)

    def __contains__(self, user: int):
        return user in self._user_action_dict


class DialogueManager:
    def __init__(self):
        self._active_users = ActiveUsersManager()
        self._actions_call_order = {DummyHelloAction: self.__dummy_hello_action,
                                    DummyYouKnowWhoIsPushkin: self.__dummy_you_know_who_is_pushkin}

    def reply(self, user_id: int, query: AbstractQuery) -> AbstractResponse:
        if user_id not in self._active_users:
            return self._active_users.add(user_id, self.__find_suitable_action(query))
        else:
            response = self._active_users.get_response(user_id, query)
            if not response:
                return self.reply(user_id, query)
            return response

    def __find_suitable_action(self, query: AbstractQuery) -> AbstractAction:
        for action_class in self._actions_call_order:
            if type(query) in action_class.recognized_types:
                activation_response = action_class.activation_response(query)
                if activation_response: # TODO always return activation
                    # разные action-ы имеют разные конструкторы
                    return self._actions_call_order[action_class](activation_response.props)

                    # TODO видимо, самым последним вариантов будет болталка, которая всегда сработает
        raise ValueError('Сейчас нет болталки, пришло незнакомое сообщение')

    @staticmethod
    def __dummy_hello_action(props: dict):
        return DummyHelloAction()

    @staticmethod
    def __dummy_you_know_who_is_pushkin(props: dict):
        return DummyYouKnowWhoIsPushkin()


dm = DialogueManager()
user_one, user_two = 1, 2
print(dm.reply(user_one, TextQuery('привет')))
print(dm.reply(user_one, TextQuery('расскажи про пушкина')))
print(dm.reply(user_one, TextQuery('как звали жену Пушкина?')))
print(dm.reply(user_two, TextQuery('расскажи про пушкина')))
print(dm.reply(user_two, TextQuery('ну и все')))