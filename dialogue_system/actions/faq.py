import json
import textdistance

from typing import Dict

from dialogue_system.actions.abstract import AbstractAction, ActivationResponse
from dialogue_system.queries.text_based import TextQuery
from dialogue_system.responses.text_based import SingleTextResponse, SingleTextWithFactAttachments
from dialogue_system.matchers.similarity import is_matching
from slots.slot import Slot


FAQ_DATASET_PATH = 'data/json/faq.json'


class FAQDataset():
    def __init__(self):
        self._responses = {}
        with open(FAQ_DATASET_PATH) as f:
            responses_json = json.load(f)

        for question_category in responses_json['question_category']:
            self._responses[question_category] = {}
            for column in responses_json:
                if column != 'question_category':
                    self._responses[question_category][column] = responses_json[column][question_category]

    @property
    def responses(self):
        return self._responses


class FAQAction(AbstractAction):
    MUSEUM_BUILDINGS = {'Главное здание': 'main_building',
                        'Галерея': 'gallery',
                        'Мемориальная квартира С.Т. Рихтера': 'memorial_apartment',
                        'Учебный художественный музей им. И.В. Цветаева': 'educational_museum'}

    recognized_types = [TextQuery]
    _faq_dataset = FAQDataset()

    @classmethod
    def _is_matching_question_category(cls, question_category: str, query: str) -> bool:
        for question in cls._faq_dataset.responses[question_category]['question_variations']:
            if is_matching(question, query, textdistance.levenshtein.normalized_similarity):
                return True
        return False

    @classmethod
    def activation_response(cls, initial_query: TextQuery, slots: Dict[Slot, str]) -> ActivationResponse:
        for question_category in cls._faq_dataset.responses:
            if cls._is_matching_question_category(question_category, initial_query):
                is_museum_specific = cls._faq_dataset.responses[question_category]['is_museum_specific']
                return ActivationResponse(intent_detected=True,
                                          props={'question_category': question_category,
                                                 'is_museum_specific': is_museum_specific})

    def reply(self, query: TextQuery = None) -> SingleTextResponse:
        if self._props['is_museum_specific']:
            are_correct_details = False
            while not are_correct_details:
                query = yield SingleTextWithFactAttachments(is_finished=False,
                                     is_successful=False,
                                     text='Пожалуйста, уточните, для какого здания музея вам нужна эта информация',
                                     attachments=list(self.MUSEUM_BUILDINGS))
                for building_name in self.MUSEUM_BUILDINGS:
                    if is_matching(building_name, query, textdistance.levenshtein.normalized_similarity):
                        question_responses = self._faq_dataset.responses[self._props['question_category']]
                        selected_building = self.MUSEUM_BUILDINGS[building_name]
                        yield SingleTextResponse(is_finished=True,
                                                 is_successful=True,
                                                 text=question_responses['{}_response'.format(selected_building)])
                        are_correct_details = True
        else:
            yield SingleTextResponse(is_finished=True,
                                     is_successful=True,
                                     text=self._faq_dataset.responses[self._props['question_category']]['response'])
