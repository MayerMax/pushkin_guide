import abc

from collections import namedtuple


ActivationResponse = namedtuple('ActivationResponse', ['intent_detected', 'props'])
ActivationResponse.__new__.__defaults__ = (False, None)


class AbstractResponse(metaclass=abc.ABCMeta):
    def __init__(self, is_finished: bool = True, is_successful: bool = False, text: str = ''):
        self.is_finished = is_finished
        self.is_successful = is_successful
        self._text = text

    @abc.abstractmethod
    def to_key_value_format(self):
        pass
