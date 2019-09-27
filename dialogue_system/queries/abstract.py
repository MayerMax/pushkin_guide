import abc


class AbstractQuery(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def to_key_value_format(self):
        pass
