from dialogue_system.queries.abstract import AbstractQuery


class TextQuery(AbstractQuery, str):
    def __init__(self, text: str):
        super().__init__()
        self._text = text

    def to_key_value_format(self):
        return {
            'text': self._text
        }

    @property
    def text(self):
        return self._text

    def __repr__(self):
        return self._text

    def __str__(self):
        return self._text