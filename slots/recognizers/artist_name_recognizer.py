import typing

from elasticsearch import Elasticsearch

from dialogue_system.queries.text_based import TextQuery
from slots.recognizers.abstract import AbstractSlotRecognizer
from slots.slot import Slot

MIN_THRESHOLD_SCORE = 8.5


class ArtistNameRecognizer(AbstractSlotRecognizer):
    recognized_types = [TextQuery]

    def __init__(self, elastic_params: dict = None):
        if elastic_params:
            self.es = Elasticsearch(elastic_params)  # for deployment
        else:
            self.es = Elasticsearch()  # only for local testing

    def recognize(self, query: TextQuery) -> typing.Dict[Slot, str]:
        output = self.es.search(index='collection-index', body={
            "query": {
                "match": {
                    "about_author.name": {
                        "query": query.text,
                        "fuzziness": "AUTO"
                    }
                }
            }
        })['hits']['hits']

        if output:
            if output[0]['_score'] < MIN_THRESHOLD_SCORE:
                return {}

            return {Slot.Name: output[0]['about_author']['name'],
                    Slot.NameProfession: output[0]['type']}
        return {}
