import typing
from elasticsearch import Elasticsearch

from dialogue_system.queries.text_based import TextQuery
from slots.recognizers.abstract import AbstractSlotRecognizer
from slots.slot import Slot


MIN_THRESHOLD = 2

class MaterialFuzzyRecognizer(AbstractSlotRecognizer):
    recognized_types = [TextQuery]

    def __init__(self, elastic_params: dict = None, use_natasha=False):
        if elastic_params:
            self._es = Elasticsearch(elastic_params)  # for deployment
        else:
            self._es = Elasticsearch()  # only for local testing

    def recognize(self, query: TextQuery) -> typing.Dict[Slot, str]:


        output = self._es.search(index='collection-index', body={
            "query": {
                "match": {
                    "material": {
                        "query": query.text,
                        "fuzziness": "AUTO"
                    }
                }
            }
        })['hits']['hits']

        if output and output[0]['_score'] < MIN_THRESHOLD:
                return {Slot.Materials: output[0]['_score']['material']}
        return {}