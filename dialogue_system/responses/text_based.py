from typing import List

from dialogue_system.responses.abstarct import AbstractResponse


class SingleTextResponse(AbstractResponse):
    def __init__(self, is_finished: bool = True, is_successful: bool = False, text: str = ''):
        super().__init__(is_finished, is_successful, text)

    def to_key_value_format(self):
        return {
            'text': self._text
        }

    def __repr__(self):
        return self._text


class SingleTextWithFactAttachments(AbstractResponse):
    def __init__(self, is_finished: bool = True, is_successful: bool = False, text: str = '',
                 attachments: List[str] = None):
        super().__init__(is_finished, is_successful, text)
        self._attachments = attachments

    def to_key_value_format(self):
        return {
            'text': self._text,
            'attachments': self._attachments
        }

    def __repr__(self):
        return f'({self._text})({" ".join(x for x in self._attachments)})'

