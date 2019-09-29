from dialogue_system.queries.abstract import AbstractQuery


class ImageQuery(AbstractQuery, str):
    def __init__(self, url: str, local_path: str):
        super().__init__()
        self._url = url
        self._local_path = local_path

    def to_key_value_format(self):
        return {
            'url': self._url,
            'local_patht': self._local_path
        }

    @property
    def url(self):
        return self._url

    @property
    def local_path(self):
        return self._local_path

    def __repr__(self):
        return self._url

    def __str__(self):
        return self._url
