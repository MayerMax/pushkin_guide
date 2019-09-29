import random
from typing import Dict, Union

from elasticsearch import Elasticsearch

from dialogue_system.actions.abstract import AbstractAction, ActivationResponse
from dialogue_system.queries.text_based import TextQuery
from dialogue_system.responses.image_based import SingleImageResponse
from dialogue_system.responses.text_based import SingleTextResponse
from slots.slot import Slot


class ExpoInfoMaterialAction(AbstractAction):
    recognized_types = [TextQuery]
    triggering_phrases = ['хочу найти что-то', 'хочу посмотреть', 'что посмотреть', 'хочу найти что-нибудь', 'xочу найти что-то об',
                          'что в музее есть', 'где посомтреть', 'расскажи про', 'что есть по', 'что есть из']

    def __init__(self, props: dict, slots: Dict[Slot, str], es_params: dict = None, user_id=None):
        super().__init__(props=props, slots=slots, user_id=user_id)
        self._es = Elasticsearch() if not es_params else Elasticsearch(es_params)  # need to configure

    @classmethod
    def activation_response(cls, initial_query: TextQuery, slots: Dict[Slot, str]) -> ActivationResponse:
        if Slot.Material not in slots:
            return None
        for phrase in ExpoInfoMaterialAction.triggering_phrases:
            if phrase in initial_query.text:
                return ActivationResponse(intent_detected=True)

    def reply(self, slots: Dict[Slot, str], user_id=None) -> Union[SingleTextResponse, SingleImageResponse]:
        material = slots[Slot.Material]
        if Slot.Name in slots:
            pass
        elif Slot.Country in slots:
            pass
        else:
            yield self._filter_by_material_answer(material)

    def _generate_answer_for_given_author(self, material, name):
        output = [x for x in self._es.search(index='collection-index', body={
            "query": {
                "match": {
                    "about_author.name": {
                        "query": name,
                        "fuzziness": "2"
                    }
                }
            }
        })['hits']['hits'] if x[Slot.Material] == material]
        if not output:
            return SingleTextResponse(is_finished=True, is_successful=True, text=f'К сожалению, ничего не удалось '
                                                                                 f'найти для {name}')
        else:
            pass

    def _filter_by_material_answer(self, material):
        output = self._es.search(index='collection-index', body={
            "query": {
                "match": {
                    "material": {
                        "query": material,
                        "fuzziness": "2"
                    }
                }
            }
        })['hits']['hits']

        if len(output) > 3:
            output = output[0:3]
        authors = [x["_source"]["about_author"]["name"] if 'about_author' in x["_source"] else 'неизвестен' for x in output]
        answer = '.\n'.join([f'{idx}. {x["_source"]["art_name"]}, автор {authors[idx-1]}. Зал {random.randint(1, 25)}'
                            for idx, x in enumerate(output, start=1)])

        return SingleTextResponse(is_finished=True, is_successful=True, text=f'Предлагаю вам ознакомиться '
                                                                             f'с следюущими шедеврами именно в таком '
                                                                             f'поряке:\n{answer}')

    def _filter_by_material_and_country_slots(self, material, country):
        pass
