import typing

from elasticsearch import Elasticsearch

import natasha

from dialogue_system.queries.text_based import TextQuery
from slots.recognizers.abstract import AbstractSlotRecognizer
from slots.slot import Slot

MIN_THRESHOLD_SCORE_FUZZY = 6.3
MIN_THRESHOLD_PURE = 2


class NatashaWrapper:
    def __init__(self):
        self._extractor = natasha.NamesExtractor()

    def extract(self, text: str):
        if 'да' in text:
            return ''
        matches = self._extractor(text)
        if not matches:
            return ''
        match = matches[0].fact

        if match.last:
            return '{} {}'.format(match.first if match.first else '', match.last).strip()
        return ''


class ArtistFuzzyNameRecognizer(AbstractSlotRecognizer):
    recognized_types = [TextQuery]

    def __init__(self, elastic_params: dict = None, use_natasha=False):
        if elastic_params:
            self._es = Elasticsearch(elastic_params)  # for deployment
        else:
            self._es = Elasticsearch()  # only for local testing

        self._natasha_recognizer = NatashaWrapper() if use_natasha else None

    def recognize(self, query: TextQuery) -> typing.Dict[Slot, str]:
        q = None

        if self._natasha_recognizer:
            q = self._natasha_recognizer.extract(query.text)

        if q:
            query = q
        else:
            query = query.text

        output = self._es.search(index='collection-index', body={
            "query": {
                "match": {
                    "about_author.name": {
                        "query": query,
                        "fuzziness": "2"
                    }
                }
            }
        })['hits']['hits']

        if output:
            if q:
                if output[0]['_score'] < MIN_THRESHOLD_PURE:
                    return {Slot.SomeNameDetected: q}
                else:
                    return {Slot.Name: output[0]['_source']['about_author']['name'],
                            Slot.NameProfession: output[0]['_source']['type'],
                            Slot.SomeNameDetected: q
                            }
            else:
                if output[0]['_score'] < MIN_THRESHOLD_SCORE_FUZZY:
                    return {}

                return {Slot.Name: output[0]['_source']['about_author']['name'],
                        Slot.NameProfession: output[0]['_source']['type']}
        if q:
            return {Slot.SomeNameDetected: q}
        return {}
