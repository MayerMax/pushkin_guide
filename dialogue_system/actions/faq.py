import json
import textdistance

from dialogue_system.actions.abstract import AbstractAction, ActivationResponse
from dialogue_system.queries.text_based import TextQuery
from dialogue_system.responses.text_based import SingleTextResponse
from dialogue_system.matchers.similarity import is_matching


FAQ_DATASET_PATH = ''


class FAQDataset():
    def __init__(self):
        self._responses = {}
        with open(FAQ_DATASET_PATH) as f:
            responses_json = json.load(f)

        for index, questions in responses_json['question_variations'].items():
            self._responses[index] = {'question_variations': questions, 'response': responses_json['response'][index]}

    @property
    def responses(self):
        return self._responses


class GeneralFAQAction(AbstractAction):
    recognized_types = [TextQuery]
    _faq_dataset = FAQDataset()

    @classmethod
    def _is_matching_question_category(cls, question_category: str, query: str) -> bool:
        for question in cls._faq_dataset.responses[question_category]['question_variations']:
            if is_matching(question, query, textdistance.levenshtein.normalized_similarity, threshold=0.6):
                return True
        return False

    @classmethod
    def activation_response(cls, initial_query: TextQuery) -> ActivationResponse:
        for question_category in cls._faq_dataset.responses:
            if cls._is_matching_question_category(question_category, initial_query.text):
                return ActivationResponse(intent_detected=True,
                                          props={'question_category': question_category})

    def reply(self, query: TextQuery = None) -> SingleTextResponse:
        yield SingleTextResponse(is_finished=True,
                                 is_successful=True,
                                 text=self._faq_dataset.responses[self._props['question_category']]['response'])
