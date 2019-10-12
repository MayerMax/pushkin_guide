import typing
from elasticsearch import Elasticsearch

from dialogue_system.queries.text_based import TextQuery
from slots.recognizers.abstract import AbstractSlotRecognizer
from slots.slot import Slot


class FuzzyTextRecognizer(AbstractSlotRecognizer):
    recognized_types = [TextQuery]

    def __init__(self, search_slot: Slot, additional_slots_to_get: typing.List[Slot] = None, min_threshold: float =2,
                 elastic_params: dict = None, index_name: str = 'collection-index'):
        if elastic_params:
            self._es = Elasticsearch(elastic_params)  # for deployment
        else:
            self._es = Elasticsearch()  # only for local testing

        self._additional_slots_to_get = additional_slots_to_get if additional_slots_to_get else []
        self._search_slot = search_slot
        self._min_threshold = min_threshold
        self._index_name = index_name

    def recognize(self, query: TextQuery) -> typing.Dict[Slot, str]:
        output = self._es.search(index=f'{self._index_name}', body={
            "query": {
                "match": {
                    f"{self._search_slot.value}": {
                        "query": query.text,
                        "fuzziness": "2"
                    }
                }
            }
        })['hits']['hits']

        if output and output[0]['_score'] > self._min_threshold:
            res = {self._search_slot: output[0]['_source'][self._search_slot.value]}
            for additional_slot in self._additional_slots_to_get:
                if additional_slot.value in output[0]['_source']:
                    res[additional_slot] = output[0]['_source'][additional_slot.value]
            return res
        return {}
