from typing import Optional
from collections import namedtuple
from dialogue_system.actions.abstract import AbstractAction, DummyHelloAction, DummyYouKnowWhoIsPushkin
from dialogue_system.actions.faq import FAQAction
from dialogue_system.actions.about_artist import AboutArtistAction
from dialogue_system.queries.abstract import AbstractQuery
from dialogue_system.queries.text_based import TextQuery
from dialogue_system.responses.abstract import AbstractResponse
from typing import Dict

from slots.slot import Slot
from slots.slots_filler import SlotsFiller

DynamicResponse = namedtuple('DynamicResponse', ['action', 'replier'])


class ActiveUsersManager:
    max_retry_counts = {
        DummyHelloAction: 0,
        DummyYouKnowWhoIsPushkin: 0,
        FAQAction: 1,
        AboutArtistAction: 0
    }

    def __init__(self):
        self._user_action_dict = {}
        self._num_negative_counts_to_call = {}

    def add(self, user: int, action: AbstractAction, slots: Dict[Slot, str]) -> AbstractResponse:
        dr = DynamicResponse(action, action.reply(slots))
        response: AbstractResponse = next(dr.replier)
        if not response.is_finished:
            self._user_action_dict[user] = dr
            self._num_negative_counts_to_call[user] = 0
        return response

    def get_response(self, user: int, query: AbstractQuery, slots: Dict[Slot, str]) -> Optional[AbstractResponse]:
        response: AbstractResponse = self._user_action_dict[user].replier.send((query, slots))

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
        self._slot_filler = SlotsFiller()

        self._actions_call_order = {DummyHelloAction: self.__dummy_hello_action,
                                    DummyYouKnowWhoIsPushkin: self.__dummy_you_know_who_is_pushkin,
                                    FAQAction: self.__general_faq_action,
                                    AboutArtistAction: self._get_about_artist_action}

    def reply(self, user_id: int, query: AbstractQuery) -> AbstractResponse:
        if user_id not in self._active_users:
            return self._active_users.add(user_id,
                                          self.__find_suitable_action(query),
                                          self._slot_filler.enrich(query))
        else:
            new_slots = self._slot_filler.enrich(query)
            response = self._active_users.get_response(user_id, query, new_slots)
            if not response:
                return self.reply(user_id, query)
            return response

    def __find_suitable_action(self, query: AbstractQuery) -> AbstractAction:
        slots = self._slot_filler.enrich(query)
        for action_class in self._actions_call_order:
            if type(query) in action_class.recognized_types:
                activation_response = action_class.activation_response(query, slots)
                if activation_response:  # TODO always return activation
                    # разные action-ы имеют разные конструкторы
                    return self._actions_call_order[action_class](props=activation_response.props, slots=slots)

                    # TODO видимо, самым последним вариантов будет болталка, которая всегда сработает
        raise ValueError('Сейчас нет болталки, пришло незнакомое сообщение')

    @staticmethod
    def __general_faq_action(props: dict, slots: Dict[Slot, str]):
        return  FAQAction(props=props)

    @staticmethod
    def __dummy_hello_action(props: dict, slots: Dict[Slot, str]):
        return DummyHelloAction()

    @staticmethod
    def __dummy_you_know_who_is_pushkin(props: dict, slots: Dict[Slot, str]):
        return DummyYouKnowWhoIsPushkin()

    @staticmethod
    def _get_about_artist_action(props: dict, slots: Dict[Slot, str]):
        return AboutArtistAction(props=props, slots=slots)


dm = DialogueManager()
user_one, user_two = 1, 2

print(dm.reply(user_one, TextQuery('расскажи про альфреда де дре')))
print(dm.reply(user_one, TextQuery('расскажи про пушкина')))

# print(dm.reply(user_one, TextQuery('как звали жену Пушкина?')))
# print(dm.reply(user_two, TextQuery('расскажи про пушкина')))
# print(dm.reply(user_two, TextQuery('ну и все')))
