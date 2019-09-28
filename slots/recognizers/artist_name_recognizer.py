import typing
from elasticsearch import Elasticsearch

from dialogue_system.queries.text_based import TextQuery
from slots.recognizers.abstract import AbstractSlotRecognizer
from slots.recognizers.slots import Slots


class ArtistNameRecognizer(AbstractSlotRecognizer):
    def __init__(self, elastic_params: dict):
        self.es = Elasticsearch(elastic_params)

    def recognize(self, query: TextQuery) -> typing.Dict[Slots, str]:
        output = self.es.search(index='collection-index', body={
            "query": {
                "match": {
                    "about_author.name": {
                        "query": query.text,
                        "fuzziness": 'AUTO',
                    }
                }
            }
        })['hits']['hits']

        if output:
            return {Slots.Name: output[0]['about_author']['name'],
                    Slots.NameProfession: output[0]['type']}