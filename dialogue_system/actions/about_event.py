from typing import Dict, Union

from elasticsearch import Elasticsearch

from dialogue_system.actions.abstract import AbstractAction, ActivationResponse
from dialogue_system.queries.text_based import TextQuery
from dialogue_system.responses.image_based import SingleImageResponse
from dialogue_system.responses.text_based import SingleTextResponse
from slots.slot import Slot
from utils import clean_html


class AboutEventAction(AbstractAction):
    recognized_types = [TextQuery]
    triggering_phrases = ['когда приедет выставка', 'когда будет', 'когда начнется', 'когда начнутся', 'программа',
                          'программа выставки', 'как купить', 'как попасть на выставку']

    def __init__(self, props: dict, slots: Dict[Slot, str], es_params: dict = None, user_id=None):
        super().__init__(props=props, slots=slots, user_id=user_id)
        self._es = Elasticsearch() if not es_params else Elasticsearch(es_params)

    @classmethod
    def activation_response(cls, initial_query: TextQuery, slots: Dict[Slot, str]) -> ActivationResponse:
        if Slot.EventName not in slots:
            return None

        for phrase in AboutEventAction.triggering_phrases:
            if phrase in initial_query.text:
                return ActivationResponse(intent_detected=True)

    def reply(self, slots: Dict[Slot, str], user_id=None) -> Union[SingleTextResponse, SingleImageResponse]:
        event_name = self._initial_slots[Slot.EventName]

        output = self._es.search(index='event-index', body={
            "query": {
                "match": {
                    "event_name": {
                        "query": event_name,
                        "fuzziness": "2"
                    }
                }
            }
        })['hits']['hits'][0]['_source']


        data_begin, data_end = output['dateBegin'], output['dateEnd']
        name = output['event_name']
        halls = output['halls'] if output['halls'] else 'уточняется'
        event_type = output['type']
        price = clean_html(output['price']) if output['price'] else 'уточняется'
        raw_text = clean_html(output['text']).split('.')
        summary = '.'.join(raw_text[0:5]) if len(raw_text) >= 5 else '.'.join(raw_text) + '.'

        text = f"{name}. Тип мероприятия: {event_type}. Будет проходить с {data_begin} по {data_end}. " \
               f"Место проведения: {halls}. Стоимость билетов: {price}.\nКоротко о событии: {summary}.".replace('\n'
                                                                                                                '<br '
                                                                                                                '/>',
                                                                                                                '').replace(' 00:00:00', '')
        img = output['img'] if output['img'] else output['extra_img']

        if img:
            yield SingleImageResponse(is_finished=True, is_successful=True, text=text,
                                      img_url=f'https://pushkinmuseum.art/{img}', img_description='')
        else:
            yield SingleTextResponse(is_finished=True, is_successful=True, text=text)
