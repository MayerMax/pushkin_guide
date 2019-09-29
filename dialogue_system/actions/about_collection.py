import random
from typing import Dict, Union

from elasticsearch import Elasticsearch

from dialogue_system.actions.abstract import AbstractAction, ActivationResponse
from dialogue_system.queries.text_based import TextQuery
from dialogue_system.responses.image_based import SingleImageResponse
from dialogue_system.responses.text_based import SingleTextResponse
from slots.slot import Slot
from utils import clean_html


class AboutCollectionObject(AbstractAction):
    recognized_types = [TextQuery]
    triggering_phrases = ['расскажи про картину', 'где находится картина', 'откуда в музее картина', 'где картина',
                          'расскажи про', 'хочу узнать о картине', 'дай информации о картине', 'где расположена картина']

    def __init__(self, props: dict, slots: Dict[Slot, str], es_params: dict = None):
        super().__init__(props=props, slots=slots)
        self._es = Elasticsearch() if not es_params else Elasticsearch(es_params)

    @classmethod
    def activation_response(cls, initial_query: TextQuery, slots: Dict[Slot, str]) -> ActivationResponse:
        if Slot.ArtName not in slots:
            return None
        for phrase in AboutCollectionObject.triggering_phrases:
            if phrase in initial_query.text:
                return ActivationResponse(intent_detected=True)

    def reply(self, slots: Dict[Slot, str]) -> Union[SingleTextResponse, SingleImageResponse]:
        art_name = self._initial_slots[Slot.ArtName]

        output = self._es.search(index='collection-index', body={
            "query": {
                "match": {
                    "art_name": {
                        "query": art_name,
                        "fuzziness": "2"
                    }
                }
            }
        })['hits']['hits'][0]

        author = output['_source']['about_author']['name'] if 'about_author' in output['_source'] else 'неизвестен'
        hall = output["_source"]["hall"] if output["_source"]["hall"] != 'empty' else random.randint(1, 25)
        text = f'Работа {art_name}. Автор {author}. Посмотреть на шедевр можно в зале {hall}'

        raw_text = clean_html(output['_source']['text']).split('.')
        summary = '.'.join(raw_text[0:2]) if len(raw_text) >= 2 else '.'.join(raw_text) + '.'

        descr = clean_html(output['_source']['annotation']) if output['_source']['annotation'] != 'empty' \
            else summary

        if output["_source"]['img']:
            yield SingleImageResponse(is_finished=True, is_successful=True, text=text,
                                      img_url=output["_source"]['img'], img_description=descr)
        else:
            yield SingleTextResponse(is_finished=True, is_successful=True, text=f'{text}\n{descr}')
