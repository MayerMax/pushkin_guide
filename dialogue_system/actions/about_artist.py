import random
from typing import Dict, Union

from elasticsearch import Elasticsearch

from dialogue_system.actions.abstract import AbstractAction, ActivationResponse
from dialogue_system.queries.text_based import TextQuery
from dialogue_system.responses.image_based import SingleImageResponse
from dialogue_system.responses.text_based import SingleTextResponse
from slots.slot import Slot
from utils import clean_html


class AboutArtistAction(AbstractAction):
    recognized_types = [TextQuery]
    triggering_phrases = ['расскажи', 'хочу послушать о', 'есть ли в музее картина', 'что ты знаешь о',
                          'хочу узнать про']

    def __init__(self, user_id, props: dict, slots: Dict[Slot, str], es_params: dict = None):
        super().__init__(user_id=user_id, props=props, slots=slots)
        self._es = Elasticsearch() if not es_params else Elasticsearch(es_params)# need to configure

    @classmethod
    def activation_response(cls, initial_query: TextQuery, slots: Dict[Slot, str]) -> ActivationResponse:
        if Slot.Name not in slots:
            return None

        for phrase in AboutArtistAction.triggering_phrases:
            if phrase in initial_query.text:
                return ActivationResponse(intent_detected=True)

    def reply(self, slots: Dict[Slot, str], user_id=None) -> Union[SingleTextResponse, SingleImageResponse]:

        name, profession = self._initial_slots[Slot.Name], self._initial_slots[Slot.NameProfession]
        output = self._es.search(index='collection-index', body={
            "query": {
                "match": {
                    "about_author.name": {
                        "query": name,
                        "fuzziness": "2"
                    }
                }
            }
        })['hits']['hits']
        output = random.choice(output)
        hall = output["_source"]["hall"] if output["_source"]["hall"] else random.randint(1, 25)
        picture_name = "'{}'".format(output["_source"]["name"])

        text = f'{name}, основная отрасль искусства: {profession}. Страна {output["_source"]["country"]}. ' \
               f'Одно из популярных произведений {picture_name}. Посмотреть на шедевр можно в {hall} зале'

        raw_text = clean_html(output['_source']['text']).split('.')

        summary = '.'.join(raw_text[0:2]) if len(raw_text) >= 2 else '.'.join(raw_text) + '.'

        descr = clean_html(output['_source']['annotation']) if output['_source']['annotation'] != 'empty' \
            else summary

        if output["_source"]['img']:
            yield SingleImageResponse(is_finished=True, is_successful=True, text=text,
                                      img_url=output["_source"]['img'], img_description=descr)
        else:
            yield SingleTextResponse(is_finished=True, is_successful=True, text=text)